#!/usr/bin/env python3
"""
comprobar-ejemplos-doc.py — Compila los ejemplos LaTeX de la documentación.

Extrae los bloques ```latex de los archivos de instrucciones para asistentes
de IA (CLAUDE.md, AGENTS.md, .github/copilot-instructions.md,
.github/agents/*.md, docs/agents/*.md, llms.txt), genera un documento de
prueba por cada bloque con el mismo preámbulo que main.tex y lo compila con
LuaLaTeX (-shell-escape). Si algún ejemplo no compila, termina con código 1
e indica el archivo:línea del bloque que ha fallado.

Uso:
    python3 scripts/comprobar-ejemplos-doc.py                 # comprobar todo
    python3 scripts/comprobar-ejemplos-doc.py --listar        # solo listar
    python3 scripts/comprobar-ejemplos-doc.py --filtro CLAUDE.md:151
    python3 scripts/comprobar-ejemplos-doc.py --raiz . --salida /tmp/ejemplos
    python3 scripts/comprobar-ejemplos-doc.py --sin-metadata  # sin \\DocumentMetadata

Reglas de exclusión (el bloque no se compila):
  * Marcador explícito en las 3 líneas anteriores al bloque:
        <!-- no-compilar -->   o   <!-- no-compilar: motivo -->
  * Bloques que solo tienen sentido en el preámbulo o fuera de LaTeX:
    \\documentclass, \\usepackage, \\DocumentMetadata, \\addbibresource,
    \\makeglossaries, \\input@path.

Transformaciones automáticas:
  * \\EPSsetup{...}: se coloca en el preámbulo (tras \\input{configuracion})
    para validar las claves documentadas.
  * \\newacronym / \\newglossaryentry: se mueven al preámbulo y solo se definen
    si la entrada no existe ya en contenido/anexos/acronimos.tex.
  * Entradas BibTeX (@article{...}) dentro del bloque: se eliminan (las citas
    sin entrada solo producen avisos).
  * \\includegraphics: siempre usa la imagen de ejemplo «example-image» del
    paquete mwe, para que los ejemplos no dependan de figuras inexistentes.

Requiere: Python 3.9+ (sin dependencias externas), LuaLaTeX con -shell-escape
y latexminted (para los entornos de código).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# Archivos analizados por defecto (patrones glob relativos a la raíz)
ARCHIVOS_POR_DEFECTO = [
    "CLAUDE.md",
    "AGENTS.md",
    ".github/copilot-instructions.md",
    ".github/agents/*.md",
    "docs/agents/*.md",
    "llms.txt",
]

MARCADOR_EXCLUSION = re.compile(r"<!--\s*no-compilar\b(?::?\s*(?P<motivo>.*?))?\s*-->")
APERTURA = re.compile(r"^(?P<sangria>\s*)(?P<valla>`{3,}|~{3,})\s*(?P<lang>latex|tex)\s*$", re.I)

# Comandos que hacen que un bloque sea solo de preámbulo / no compilable aquí
SOLO_PREAMBULO = [
    (re.compile(r"\\documentclass\b"), "contiene \\documentclass"),
    (re.compile(r"\\usepackage\b"), "contiene \\usepackage (preámbulo)"),
    (re.compile(r"\\RequirePackage\b"), "contiene \\RequirePackage (preámbulo)"),
    (re.compile(r"\\DocumentMetadata\b"), "contiene \\DocumentMetadata"),
    (re.compile(r"\\addbibresource\b"), "contiene \\addbibresource (preámbulo)"),
    (re.compile(r"\\makeglossaries\b"), "contiene \\makeglossaries (preámbulo)"),
    (re.compile(r"\\input@path\b"), "contiene \\input@path"),
    (re.compile(r"\\(bibliography|bibliographystyle)\{"), "usa BibTeX clásico"),
]

ENTRADA_BIB = re.compile(r"^\s*@\w+\s*\{")
DEFINICION_GLOSARIO = re.compile(r"\\(newacronym|newglossaryentry)\b")
EPSSETUP = re.compile(r"\\EPSsetup\s*\{")

# Errores de TeX en el .log (formato -file-line-error y formato clásico)
ERROR_FLE = re.compile(r"^(?P<archivo>[^\s:][^:]*\.(?:tex|sty|cls|def|cfg|ltx|aux|toc|lof|lot|gls|acr)):(?P<linea>\d+): (?P<msg>.*)$")
ERROR_CLASICO = re.compile(r"^! (?P<msg>.*)$")


@dataclass
class Ejemplo:
    archivo: str          # ruta relativa a la raíz
    linea: int            # línea de la valla de apertura (1-based)
    cuerpo: list[str]     # líneas del bloque (sin vallas)
    omitir: str = ""      # motivo por el que no se compila ("" = se compila)
    preambulo: list[str] = field(default_factory=list)
    documento: list[str] = field(default_factory=list)
    # índice de línea (0-based) en `cuerpo` de cada línea de `documento`
    origen_doc: list[int] = field(default_factory=list)
    origen_pre: list[int] = field(default_factory=list)

    @property
    def id(self) -> str:
        return f"{self.archivo}:{self.linea}"


# ---------------------------------------------------------------------------
# Extracción
# ---------------------------------------------------------------------------

def extraer_ejemplos(raiz: Path, patrones: list[str]) -> list[Ejemplo]:
    archivos: list[str] = []
    for patron in patrones:
        coincidencias = sorted(glob.glob(str(raiz / patron)))
        for c in coincidencias:
            rel = os.path.relpath(c, raiz)
            if rel not in archivos:
                archivos.append(rel)

    ejemplos: list[Ejemplo] = []
    for rel in archivos:
        try:
            lineas = (raiz / rel).read_text(encoding="utf-8").split("\n")
        except OSError as exc:
            print(f"Aviso: no se pudo leer {rel}: {exc}", file=sys.stderr)
            continue
        i = 0
        while i < len(lineas):
            m = APERTURA.match(lineas[i])
            if not m:
                # Saltar otros bloques de código completos (```bash, etc.)
                otro = re.match(r"^\s*(`{3,}|~{3,})", lineas[i])
                if otro:
                    valla = otro.group(1)
                    i += 1
                    while i < len(lineas) and not lineas[i].strip().startswith(valla):
                        i += 1
                i += 1
                continue
            valla = m.group("valla")
            sangria = len(m.group("sangria"))
            inicio = i
            i += 1
            cuerpo = []
            while i < len(lineas) and not lineas[i].strip().startswith(valla):
                linea = lineas[i]
                # Quitar la sangría del bloque (listas Markdown)
                if sangria and linea[:sangria].strip() == "":
                    linea = linea[sangria:]
                cuerpo.append(linea)
                i += 1
            ej = Ejemplo(archivo=rel, linea=inicio + 1, cuerpo=cuerpo)
            # Marcador de exclusión en las 3 líneas no vacías anteriores
            k, vistas = inicio - 1, 0
            while k >= 0 and vistas < 3:
                if lineas[k].strip():
                    mm = MARCADOR_EXCLUSION.search(lineas[k])
                    if mm:
                        ej.omitir = "marcador no-compilar" + (
                            f" ({mm.group('motivo')})" if mm.group("motivo") else "")
                        break
                    vistas += 1
                    if lineas[k].strip().startswith(("#", "```")):
                        break  # no cruzar encabezados ni otros bloques
                k -= 1
            clasificar(ej)
            ejemplos.append(ej)
            i += 1
    return ejemplos


def _sin_comentario(linea: str) -> str:
    """Devuelve la línea sin el comentario TeX final (respeta \\%)."""
    return re.sub(r"(?<!\\)%.*$", "", linea)


def _extraer_balanceado(lineas: list[str], i: int, patron: re.Pattern) -> int:
    """Desde la línea i (que contiene `patron`), devuelve el índice de la
    última línea del comando con llaves balanceadas."""
    profundidad = 0
    empezado = False
    j = i
    while j < len(lineas):
        texto = _sin_comentario(lineas[j])
        if j == i:
            texto = texto[patron.search(texto).start():] if patron.search(texto) else texto
        for c in texto:
            if c == "{":
                profundidad += 1
                empezado = True
            elif c == "}":
                profundidad -= 1
        if empezado and profundidad <= 0:
            # \newacronym tiene 3 argumentos: seguir si la línea siguiente
            # continúa con más grupos {..}
            if j + 1 < len(lineas) and re.match(r"^\s*[\[{]", lineas[j + 1]) and profundidad == 0 \
                    and patron is not EPSSETUP:
                j += 1
                continue
            return j
        j += 1
    return len(lineas) - 1


def clasificar(ej: Ejemplo) -> None:
    if ej.omitir:
        return
    codigo = "\n".join(_sin_comentario(linea) for linea in ej.cuerpo)
    if not codigo.strip():
        ej.omitir = "bloque vacío o solo comentarios"
        return
    for patron, motivo in SOLO_PREAMBULO:
        if patron.search(codigo):
            ej.omitir = motivo
            return

    lineas = ej.cuerpo
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        sc = _sin_comentario(linea)
        if ENTRADA_BIB.match(sc):
            # Entrada BibTeX: descartar hasta cerrar llaves
            fin = _extraer_balanceado(lineas, i, re.compile(r"@"))
            i = fin + 1
            continue
        m_eps = EPSSETUP.search(sc)
        m_glo = DEFINICION_GLOSARIO.search(sc)
        if m_eps:
            fin = _extraer_balanceado(lineas, i, EPSSETUP)
            for k in range(i, fin + 1):
                ej.preambulo.append(lineas[k])
                ej.origen_pre.append(k)
            i = fin + 1
            continue
        if m_glo:
            fin = _extraer_balanceado(lineas, i, re.compile(r"\\(newacronym|newglossaryentry)\b"))
            bloque = "\n".join(lineas[i:fin + 1])
            clave = re.search(r"\\(?:newacronym|newglossaryentry)\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}", bloque)
            if clave:
                ej.preambulo.append(f"\\ifglsentryexists{{{clave.group(1)}}}{{}}{{%")
                ej.origen_pre.append(i)
            for k in range(i, fin + 1):
                ej.preambulo.append(lineas[k])
                ej.origen_pre.append(k)
            if clave:
                ej.preambulo.append("}")
                ej.origen_pre.append(fin)
            i = fin + 1
            continue
        ej.documento.append(linea)
        ej.origen_doc.append(i)
        i += 1

    if not any(_sin_comentario(linea).strip() for linea in ej.documento) and not ej.preambulo:
        ej.omitir = "sin contenido compilable"


# ---------------------------------------------------------------------------
# Generación del documento de prueba
# ---------------------------------------------------------------------------

def generar_documento(ej: Ejemplo, con_metadata: bool) -> tuple[str, dict[int, int]]:
    """Devuelve (fuente, mapa línea_tex -> línea_md)."""
    out: list[str] = []
    mapa: dict[int, int] = {}

    def add(texto: str, origen: int | None = None) -> None:
        out.append(texto)
        if origen is not None:
            # línea del .md = línea de la valla + 1 + índice en el cuerpo
            mapa[len(out)] = ej.linea + 1 + origen

    add("% Documento de prueba generado por scripts/comprobar-ejemplos-doc.py")
    add(f"% Ejemplo: {ej.id}")
    add(r"\makeatletter")
    add(r"\def\input@path{{cls/}{sty/}{sty/componentes/}{recursos/}}")
    add(r"\makeatother")
    if con_metadata:
        add(r"\input{eps-metadata}")
    add(r"\documentclass{eps-tfg}")
    add(r"\input{configuracion}")
    add(r"\usepackage[all]{eps-componentes}")
    add(r"\addbibresource{referencias.bib}")
    add(r"\makeglossaries")
    add(r"\input{contenido/anexos/acronimos}")
    if ej.preambulo:
        add(f"% --- Preámbulo extraído de {ej.id} ---")
        for texto, origen in zip(ej.preambulo, ej.origen_pre):
            add(texto, origen)
    # Todas las figuras apuntan a la imagen de ejemplo de mwe
    add(r"\AtBeginDocument{%")
    add(r"  \NewCommandCopy\EPSejemploIncludegraphics\includegraphics")
    add(r"  \RenewDocumentCommand\includegraphics{s O{} m}{%")
    add(r"    \EPSejemploIncludegraphics[#2]{example-image}}%")
    add(r"}")
    add(r"\begin{document}")
    add(r"\mainmatter")
    add(r"\chapter{Ejemplo de la documentación}")
    add(f"% --- Inicio del ejemplo {ej.id} ---")
    for texto, origen in zip(ej.documento, ej.origen_doc):
        add(texto, origen)
    add("% --- Fin del ejemplo ---")
    add(r"\end{document}")
    return "\n".join(out) + "\n", mapa


# ---------------------------------------------------------------------------
# Compilación
# ---------------------------------------------------------------------------

@dataclass
class Resultado:
    ejemplo: Ejemplo
    ok: bool
    errores: list[str]
    log: Path | None = None


def _leer_errores(log: Path, nombre_tex: str, mapa: dict[int, int], ej: Ejemplo) -> list[str]:
    if not log.exists():
        return ["no se generó el .log"]
    texto = log.read_text(encoding="utf-8", errors="replace").split("\n")
    errores: list[str] = []
    for n, linea in enumerate(texto):
        m = ERROR_FLE.match(linea)
        msg = None
        if m:
            archivo, num, msg = m.group("archivo"), int(m.group("linea")), m.group("msg")
            if os.path.basename(archivo) == nombre_tex:
                md = mapa.get(num)
                donde = f"{ej.archivo}:{md}" if md else f"(documento generado, línea {num})"
            else:
                donde = f"{archivo}:{num}"
        else:
            m2 = ERROR_CLASICO.match(linea)
            if m2:
                msg, donde = m2.group("msg"), f"{ej.id} (bloque; sin línea concreta)"
                # buscar «l.NN» en las líneas siguientes
                for sig in texto[n + 1:n + 12]:
                    ml = re.match(r"^l\.(\d+)", sig)
                    if ml:
                        md = mapa.get(int(ml.group(1)))
                        donde = f"{ej.archivo}:{md}" if md else f"(línea {ml.group(1)})"
                        break
        if msg is None or msg.strip().startswith("==> Fatal error occurred"):
            continue
        # Mensaje completo: algunas líneas de error continúan en la siguiente
        if len(msg) >= 70 and n + 1 < len(texto) and texto[n + 1].strip():
            msg += texto[n + 1].strip()
        entrada = f"{donde}: {msg.strip()}"
        if entrada not in errores:
            errores.append(entrada)
    return errores


def compilar(ej: Ejemplo, raiz: Path, salida: Path, con_metadata: bool,
             timeout: int, motor: str) -> Resultado:
    nombre = "ej-" + re.sub(r"[^A-Za-z0-9]+", "-", ej.id).strip("-")
    directorio = salida / nombre
    if directorio.exists():
        shutil.rmtree(directorio)
    directorio.mkdir(parents=True)
    fuente, mapa = generar_documento(ej, con_metadata)
    tex = directorio / f"{nombre}.tex"
    tex.write_text(fuente, encoding="utf-8")

    entorno = dict(os.environ)
    # Las rutas relativas del preámbulo (\input{configuracion}, ...) se
    # resuelven desde la raíz del proyecto (directorio de trabajo).
    entorno["TEXMF_OUTPUT_DIRECTORY"] = str(directorio)
    # Evitar que el .log corte las líneas a 79 caracteres (rutas y mensajes)
    entorno["max_print_line"] = "10000"
    entorno["error_line"] = "254"
    entorno["half_error_line"] = "238"
    cmd = [
        motor, "-shell-escape", "-interaction=nonstopmode", "-file-line-error",
        "-halt-on-error", f"-output-directory={directorio}", str(tex),
    ]
    try:
        proc = subprocess.run(cmd, cwd=raiz, env=entorno, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout)
        codigo = proc.returncode
    except subprocess.TimeoutExpired:
        return Resultado(ej, False, [f"tiempo agotado ({timeout} s)"], directorio / f"{nombre}.log")
    except FileNotFoundError:
        return Resultado(ej, False, [f"no se encontró el motor «{motor}»"], None)

    log = directorio / f"{nombre}.log"
    errores = _leer_errores(log, tex.name, mapa, ej)
    pdf_ok = (directorio / f"{nombre}.pdf").exists()
    if codigo != 0 and not errores:
        errores = [f"{motor} terminó con código {codigo}"]
    if not pdf_ok and not errores:
        errores = ["no se generó el PDF"]
    return Resultado(ej, codigo == 0 and pdf_ok and not errores, errores, log)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--raiz", default=None,
                        help="Raíz del proyecto (por defecto, la carpeta padre de scripts/)")
    parser.add_argument("--salida", default=None,
                        help="Carpeta para los documentos de prueba (por defecto, temporal)")
    parser.add_argument("--archivos", nargs="+", default=None,
                        help="Patrones glob de archivos a analizar (relativos a la raíz)")
    parser.add_argument("--listar", action="store_true",
                        help="Solo listar los ejemplos extraídos, sin compilar")
    parser.add_argument("--filtro", action="append", default=[],
                        help="Compilar solo ejemplos cuyo «archivo:línea» contenga este texto "
                             "(se puede repetir)")
    parser.add_argument("--sin-metadata", action="store_true",
                        help="No cargar \\input{eps-metadata} (sin \\DocumentMetadata ni etiquetado)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Tiempo máximo por ejemplo, en segundos (por defecto 300)")
    parser.add_argument("--jobs", "-j", type=int, default=max(1, (os.cpu_count() or 2) // 2),
                        help="Compilaciones en paralelo")
    parser.add_argument("--motor", default="lualatex", help="Motor (por defecto lualatex)")
    parser.add_argument("--mantener", action="store_true",
                        help="No borrar la carpeta temporal de salida")
    args = parser.parse_args()

    raiz = Path(args.raiz).resolve() if args.raiz else Path(__file__).resolve().parent.parent
    if not (raiz / "cls" / "eps-tfg.cls").exists():
        print(f"ERROR: {raiz} no parece la raíz de la plantilla (falta cls/eps-tfg.cls)",
              file=sys.stderr)
        return 2

    ejemplos = extraer_ejemplos(raiz, args.archivos or ARCHIVOS_POR_DEFECTO)
    if args.filtro:
        ejemplos = [e for e in ejemplos if any(f in e.id for f in args.filtro)]

    compilables = [e for e in ejemplos if not e.omitir]
    omitidos = [e for e in ejemplos if e.omitir]

    if args.listar:
        for e in ejemplos:
            estado = f"OMITIDO ({e.omitir})" if e.omitir else "compilar"
            print(f"=== {e.id} — {estado}")
            if not e.omitir:
                if e.preambulo:
                    print("  [preámbulo]")
                    for linea in e.preambulo:
                        print(f"    {linea}")
                    print("  [documento]")
                for linea in e.documento:
                    print(f"    {linea}")
            print()
        print(f"Total: {len(ejemplos)} bloques; {len(compilables)} a compilar, "
              f"{len(omitidos)} omitidos.")
        return 0

    if not compilables:
        print("No hay ejemplos que compilar.")
        return 0

    temporal = None
    if args.salida:
        salida = Path(args.salida).resolve()
        salida.mkdir(parents=True, exist_ok=True)
    else:
        temporal = tempfile.mkdtemp(prefix="ejemplos-doc-")
        salida = Path(temporal)

    modo = "sin \\DocumentMetadata" if args.sin_metadata else "con \\input{eps-metadata}"
    print(f"Compilando {len(compilables)} ejemplos ({modo}, {args.jobs} en paralelo, "
          f"salida: {salida})")
    for e in omitidos:
        print(f"  - omitido {e.id}: {e.omitir}")

    resultados: list[Resultado] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futuros = {pool.submit(compilar, e, raiz, salida, not args.sin_metadata,
                               args.timeout, args.motor): e for e in compilables}
        for fut in concurrent.futures.as_completed(futuros):
            r = fut.result()
            resultados.append(r)
            print(f"  {'OK   ' if r.ok else 'FALLO'} {r.ejemplo.id}", flush=True)

    orden = {e.id: n for n, e in enumerate(compilables)}
    resultados.sort(key=lambda r: orden[r.ejemplo.id])
    fallos = [r for r in resultados if not r.ok]

    informe = ["", "=" * 70,
               f"Ejemplos compilados: {len(resultados)}  |  correctos: "
               f"{len(resultados) - len(fallos)}  |  con errores: {len(fallos)}  |  "
               f"omitidos: {len(omitidos)}", "=" * 70]
    for r in fallos:
        informe.append(f"\n✗ {r.ejemplo.id}")
        for err in r.errores[:8]:
            informe.append(f"    {err}")
        if len(r.errores) > 8:
            informe.append(f"    … y {len(r.errores) - 8} errores más")
        if r.log:
            informe.append(f"    log: {r.log}")
    print("\n".join(informe))

    # Resumen para GitHub Actions
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        md = ["### Ejemplos LaTeX de la documentación", "",
              f"- Compilados: **{len(resultados)}** ({modo})",
              f"- Con errores: **{len(fallos)}**",
              f"- Omitidos: {len(omitidos)}", ""]
        if fallos:
            md += ["| Ejemplo | Primer error |", "|---|---|"]
            for r in fallos:
                primero = (r.errores[0] if r.errores else "").replace("|", "\\|")
                md.append(f"| `{r.ejemplo.id}` | {primero} |")
        with open(resumen, "a", encoding="utf-8") as f:
            f.write("\n".join(md) + "\n")
    if os.environ.get("GITHUB_ACTIONS") == "true":
        for r in fallos:
            primero = r.errores[0] if r.errores else "error de compilación"
            print(f"::error file={r.ejemplo.archivo},line={r.ejemplo.linea}::"
                  f"El ejemplo no compila: {primero}")

    if temporal and not args.mantener and not fallos:
        shutil.rmtree(temporal, ignore_errors=True)

    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
