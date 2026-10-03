#!/usr/bin/env python3
"""
comprobar-pdf-etiquetado.py — Comprueba que un PDF compilado está etiquetado.

Uso en CI (GitHub Actions) tras compilar la plantilla:

    pip install pypdf
    python3 scripts/comprobar-pdf-etiquetado.py main.pdf

Comprueba:
  * /StructTreeRoot presente en el catálogo (árbol de estructura).
  * /MarkInfo << /Marked true >> (PDF etiquetado).

Imprime un resumen (páginas, versión PDF, etiquetado, idioma, número de
elementos de estructura, declaración PDF/UA en XMP) y, si existe la variable
GITHUB_STEP_SUMMARY, lo añade también al resumen del job.

Además muestra métricas de accesibilidad, solo informativas (no hacen fallar
la comprobación): figuras con y sin texto alternativo, elementos con idioma
propio (/Lang), celdas de cabecera de tabla, enlaces etiquetados y, con
--log main.log, los avisos de tagpdf agrupados por tipo.

Códigos de salida:
  0  PDF etiquetado (o --no-exigir)
  1  PDF sin etiquetar, o /Lang distinto de --idioma-esperado
  2  Error de uso / pypdf no disponible / PDF ilegible

Requiere: Python 3.9+, pypdf.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter


_NS_ESTANDAR = ("http://iso.org/pdf/ssn", "http://iso.org/pdf2/ssn")


def _obj(valor):
    """Resuelve una referencia indirecta de pypdf (o devuelve el valor tal cual)."""
    return valor.get_object() if hasattr(valor, "get_object") else valor


def _mapa_roles(raiz) -> dict:
    """
    Tabla de los roles propios (p. ej. 'section' en el espacio de nombres de
    LaTeX) al rol estándar al que equivalen (p. ej. 'H2'), a partir de
    /RoleMapNS de cada espacio de nombres y del /RoleMap global (PDF 1.7).
    Las claves son (espacio de nombres, rol); el /RoleMap global usa el
    espacio de nombres vacío, el de los elementos sin /NS.
    """
    directo: dict = {}
    for ns in _obj(raiz.get("/Namespaces")) or []:
        ns = _obj(ns)
        nombre_ns = str(ns.get("/NS", ""))
        for rol, destino in (_obj(ns.get("/RoleMapNS")) or {}).items():
            destino = _obj(destino)
            nombre = destino[0] if isinstance(destino, list) else destino
            ns_destino = ""
            if isinstance(destino, list) and len(destino) > 1:
                ns_destino = str(_obj(destino[1]).get("/NS", ""))
            directo[(nombre_ns, str(rol))] = (ns_destino, str(nombre))
    for rol, destino in (_obj(raiz.get("/RoleMap")) or {}).items():
        directo.setdefault(("", str(rol)), ("", str(_obj(destino))))
    return directo


def _resolver_rol(mapa: dict, ns: str, rol: str) -> str:
    """
    Sigue el mapa de roles hasta un rol estándar (como mucho 10 saltos). Un
    rol con espacio de nombres propio solo se resuelve con el /RoleMapNS de
    ese espacio; el /RoleMap global solo se aplica a los roles sin /NS.
    """
    for _ in range(10):
        if ns in _NS_ESTANDAR:
            break
        sig = mapa.get((ns, rol))
        if sig is None or sig == (ns, rol):
            break
        ns, rol = sig
    return rol.lstrip("/")


def _contar_estructura(raiz, limite: int = 200_000) -> tuple[Counter, Counter]:
    """
    Recorre el árbol de estructura. Devuelve los elementos por /S (tipo) y
    otras cuentas: figuras con y sin /Alt, elementos con /Lang y elementos
    por rol estándar (H1...H6, Reference) tras resolver el mapa de roles.
    """
    from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject

    tipos: Counter = Counter()
    extra: Counter = Counter()
    mapa = _mapa_roles(raiz)
    pila = [raiz.get("/K")]
    vistos = set()
    visitados = 0
    while pila and visitados < limite:
        nodo = pila.pop()
        if nodo is None:
            continue
        if isinstance(nodo, IndirectObject):
            clave = (nodo.idnum, nodo.generation)
            if clave in vistos:
                continue
            vistos.add(clave)
            nodo = nodo.get_object()
        if isinstance(nodo, ArrayObject):
            pila.extend(nodo)
            continue
        if not isinstance(nodo, DictionaryObject):
            continue  # MCID (entero) u otro contenido marcado
        visitados += 1
        tipo = nodo.get("/S")
        if tipo is not None:
            tipos[str(tipo).lstrip("/")] += 1
            ns = nodo.get("/NS")
            ns = str(ns.get_object().get("/NS", "")) if ns is not None else ""
            extra["rol:" + _resolver_rol(mapa, ns, str(tipo))] += 1
            if str(tipo) == "/Figure":
                extra["figuras_alt" if "/Alt" in nodo else "figuras_sin_alt"] += 1
        if "/Lang" in nodo:
            extra["con_lang"] += 1
        hijos = nodo.get("/K")
        if hijos is not None:
            pila.append(hijos)
    return tipos, extra


def _avisos_tagpdf(ruta_log: str) -> Counter:
    """Agrupa por tipo los avisos de tagpdf del registro de compilación."""
    with open(ruta_log, encoding="utf-8", errors="replace") as f:
        log = f.read()
    avisos: Counter = Counter()
    patron = r"Package tagpdf Warning: ([^\n]*(?:\n\(tagpdf\)[^\n]*)*)"
    for texto in re.findall(patron, log):
        texto = re.sub(r"\n\(tagpdf\)\s*", " ", texto)
        if "Parent-Child" in texto:
            par = re.findall(r"'([^']*)'", texto)[:2]
            clave = "Relación padre-hijo no permitida (" + " → ".join(par) + ")"
        elif "Destination" in texto:
            clave = "Destino sin estructura asociada"
        elif "Alternative text" in texto:
            clave = "Falta texto alternativo"
        elif "can not be closed" in texto:
            clave = "Estructura que no se puede cerrar"
        elif "still open" in texto:
            clave = "Estructuras abiertas al final"
        else:
            clave = re.sub(r"\d+", "N", texto)[:70]
        avisos[clave] += 1
    return avisos


def _enlaces(lector) -> tuple[int, int]:
    """Número de anotaciones de enlace y cuántas están en la estructura."""
    total = etiquetados = 0
    for pagina in lector.pages:
        for anot in pagina.get("/Annots") or []:
            anot = anot.get_object()
            if anot.get("/Subtype") == "/Link":
                total += 1
                if "/StructParent" in anot:
                    etiquetados += 1
    return total, etiquetados


def _metricas_base(tipos: Counter, extra: Counter) -> dict:
    """Métricas que compara la línea base."""
    valores = {f"H{n}": extra["rol:H" + str(n)] for n in range(1, 7)}
    valores["Reference"] = extra["rol:Reference"]
    valores["TH"] = tipos.get("TH", 0)
    valores["Figuras con texto alternativo"] = extra["figuras_alt"]
    return valores


def _comparar_linea_base(ruta: str, tipos: Counter, extra: Counter, avisos: Counter,
                         con_log: bool) -> tuple[list, list]:
    """
    Compara con la línea base (JSON): «minimos» por métrica y
    «avisos_tagpdf_max». Devuelve (empeoramientos, mejoras).
    """
    with open(ruta, encoding="utf-8") as f:
        base = json.load(f)
    peor, mejor = [], []
    valores = _metricas_base(tipos, extra)
    for nombre, minimo in base.get("minimos", {}).items():
        valor = valores.get(nombre, 0)
        if valor < minimo:
            peor.append(f"{nombre} {valor} (mínimo {minimo})")
        elif valor > minimo:
            mejor.append(f"{nombre} {valor} (línea base {minimo})")
    maximo = base.get("avisos_tagpdf_max")
    if maximo is not None and con_log:
        total = sum(avisos.values())
        if total > maximo:
            peor.append(f"avisos de tagpdf {total} (máximo {maximo})")
        elif total < maximo:
            mejor.append(f"avisos de tagpdf {total} (línea base {maximo})")
    return peor, mejor


def main() -> int:
    """Comprueba el PDF, imprime el resumen y devuelve el código de salida."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pdf", help="Ruta al PDF a comprobar")
    parser.add_argument("--titulo", default="", help="Título para el resumen")
    parser.add_argument(
        "--idioma-esperado",
        default="",
        help="Prefijo esperado de /Lang (p. ej. 'es', 'ca', 'en-GB'); falla si no coincide",
    )
    parser.add_argument(
        "--log",
        default="",
        help="Registro de compilación (main.log) para contar los avisos de tagpdf",
    )
    parser.add_argument(
        "--ua-esperada",
        default="",
        help="Parte de PDF/UA que debe declarar el XMP (p. ej. '2'); falla si no la declara",
    )
    parser.add_argument(
        "--exigir-estructura",
        action="store_true",
        help="Fallar si faltan encabezados (H1, H2), entradas de índice enlazadas o "
        "texto alternativo en alguna figura (veraPDF no lo detecta)",
    )
    parser.add_argument(
        "--linea-base",
        default="",
        help="JSON con los mínimos (encabezados, entradas de índice...) y el máximo de "
        "avisos de tagpdf; falla si el PDF empeora respecto a ellos",
    )
    parser.add_argument(
        "--no-exigir",
        action="store_true",
        help="No fallar si el PDF no está etiquetado (solo informar)",
    )
    args = parser.parse_args()

    try:
        from pypdf import PdfReader
    except ImportError:
        print("ERROR: falta pypdf (pip install pypdf)", file=sys.stderr)
        return 2

    try:
        lector = PdfReader(args.pdf)
        catalogo = lector.trailer["/Root"].get_object()
    except Exception as exc:  # noqa: BLE001 — informar cualquier fallo
        print(f"ERROR: no se pudo leer {args.pdf}: {exc}", file=sys.stderr)
        return 2

    version = lector.pdf_header.replace("%PDF-", "")
    # La versión del catálogo (/Version) prevalece sobre la cabecera
    if "/Version" in catalogo:
        version = str(catalogo["/Version"]).lstrip("/")
    paginas = len(lector.pages)
    idioma = str(catalogo.get("/Lang", "—"))

    markinfo = catalogo.get("/MarkInfo")
    # BooleanObject de pypdf no define __bool__: hay que comparar con True
    marcado = bool(markinfo) and markinfo.get_object().get("/Marked") == True  # noqa: E712
    raiz = catalogo.get("/StructTreeRoot")
    tiene_arbol = raiz is not None

    tipos: Counter = Counter()
    extra: Counter = Counter()
    if tiene_arbol:
        try:
            tipos, extra = _contar_estructura(raiz.get_object())
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: no se pudo recorrer el árbol: {exc}", file=sys.stderr)

    # Declaración PDF/UA en los metadatos XMP (pdfuaid:part)
    declaracion_ua = "no"
    parte_ua = ""
    try:
        meta = catalogo.get("/Metadata")
        if meta is not None:
            xmp = meta.get_object().get_data().decode("utf-8", "replace")
            m = re.search(r"pdfuaid:part\s*(?:=\s*\"|>)\s*(\d+)", xmp)
            if m:
                parte_ua = m.group(1)
                declaracion_ua = f"sí (PDF/UA-{parte_ua})"
    except Exception:  # noqa: BLE001
        declaracion_ua = "desconocida"

    etiquetado = marcado and tiene_arbol
    esperado = args.idioma_esperado.strip().lower()
    idioma_ok = not esperado or idioma.lower() == esperado or idioma.lower().startswith(esperado + "-")
    ua_esperada = args.ua_esperada.strip()
    ua_ok = not ua_esperada or parte_ua == ua_esperada
    principales = ", ".join(f"{t} {n}" for t, n in tipos.most_common(8)) or "—"

    filas = [
        ("Páginas", str(paginas)),
        ("Versión PDF", version),
        ("Etiquetado (MarkInfo/Marked)", "sí" if marcado else "no"),
        ("Árbol de estructura (StructTreeRoot)", "sí" if tiene_arbol else "no"),
        ("Elementos de estructura", str(sum(tipos.values()))),
        ("Tipos más frecuentes", principales),
        ("Idioma (/Lang)", idioma),
        ("Declaración PDF/UA (XMP)", declaracion_ua),
    ]

    # Métricas de accesibilidad (informativas)
    try:
        enlaces, enlaces_etiq = _enlaces(lector)
    except Exception:  # noqa: BLE001
        enlaces = enlaces_etiq = 0
    encabezados = " · ".join(
        f"H{n} {extra['rol:H' + str(n)]}" for n in range(1, 7) if extra["rol:H" + str(n)]
    ) or "ninguno"
    metricas = [
        ("Encabezados", encabezados),
        ("Entradas de índice enlazadas (Reference)", str(extra["rol:Reference"])),
        ("Figuras con texto alternativo", f"{extra['figuras_alt']} de "
         f"{extra['figuras_alt'] + extra['figuras_sin_alt']}"),
        ("Celdas de cabecera de tabla (TH)", str(tipos.get("TH", 0))),
        ("Elementos con idioma propio (/Lang)", str(extra["con_lang"])),
        ("Enlaces en la estructura", f"{enlaces_etiq} de {enlaces}"),
    ]
    avisos: Counter = Counter()
    if args.log:
        try:
            avisos = _avisos_tagpdf(args.log)
            metricas.append(("Avisos de tagpdf", str(sum(avisos.values()))))
        except OSError as exc:
            # Sin registro el número es desconocido: no se muestra un 0 engañoso
            print(f"Aviso: no se pudo leer {args.log}: {exc}", file=sys.stderr)
            metricas.append(("Avisos de tagpdf", "desconocido (no se pudo leer el registro)"))

    titulo = args.titulo or f"Información del PDF ({os.path.basename(args.pdf)})"
    md = [f"### {titulo}", "", "| Propiedad | Valor |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in filas]
    md += ["", "**Accesibilidad (informativo)**", "", "| Métrica | Valor |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in metricas]
    if avisos:
        md += ["", "<details><summary>Avisos de tagpdf por tipo</summary>", "",
               "| Avisos | Tipo |", "|---|---|"]
        md += [f"| {n} | {k} |" for k, n in avisos.most_common()]
        md += ["", "</details>"]
    md.append("")
    md.append("✅ PDF etiquetado" if etiquetado else "❌ El PDF NO está etiquetado")
    if esperado:
        md.append(f"✅ Idioma {idioma} (esperado: {esperado})" if idioma_ok
                  else f"❌ Idioma {idioma}, se esperaba {esperado}")
    problemas_estructura = []
    if args.exigir_estructura:
        for nivel in (1, 2):
            if not extra["rol:H" + str(nivel)]:
                problemas_estructura.append(f"no hay encabezados H{nivel}")
        if not extra["rol:Reference"]:
            problemas_estructura.append("el índice no tiene entradas enlazadas (Reference)")
        if extra["figuras_sin_alt"]:
            problemas_estructura.append(f"{extra['figuras_sin_alt']} figuras sin texto alternativo")
        md.append("❌ Estructura: " + "; ".join(problemas_estructura) if problemas_estructura
                  else "✅ Estructura: encabezados, índice enlazado y texto alternativo")
    problemas_base, mejoras_base = [], []
    if args.linea_base:
        problemas_base, mejoras_base = _comparar_linea_base(args.linea_base, tipos, extra, avisos, bool(args.log))
        md.append("❌ Peor que la línea base: " + "; ".join(problemas_base) if problemas_base
                  else "✅ Igual o mejor que la línea base")
    if ua_esperada:
        md.append(f"✅ Declara PDF/UA-{ua_esperada}" if ua_ok
                  else f"❌ No declara PDF/UA-{ua_esperada} (declaración: {declaracion_ua})")
    texto = "\n".join(md) + "\n"

    print(texto)
    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(texto + "\n")

    if not etiquetado and not args.no_exigir:
        print(
            "::error::El PDF no está etiquetado (falta /StructTreeRoot o "
            "/MarkInfo Marked=true). ¿Se ha desactivado \\input{eps-metadata}?"
        )
        return 1
    if not idioma_ok:
        print(f"::error::El idioma del PDF (/Lang {idioma}) no coincide con el esperado ({esperado})")
        return 1
    if problemas_estructura:
        print("::error::Estructura del PDF incompleta: " + "; ".join(problemas_estructura))
        return 1
    if mejoras_base:
        print("::notice::Mejor que la línea base (se puede actualizar "
              f"{args.linea_base}): " + "; ".join(mejoras_base))
    if problemas_base:
        print("::error::El etiquetado del PDF ha empeorado respecto a la línea base: "
              + "; ".join(problemas_base))
        return 1
    if not ua_ok:
        print(f"::error::El PDF no declara PDF/UA-{ua_esperada} en el XMP (declaración: {declaracion_ua})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
