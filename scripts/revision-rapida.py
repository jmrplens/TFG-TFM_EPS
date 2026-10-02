#!/usr/bin/env python3
"""
revision-rapida.py — Análisis estático del documento TFG/TFM EPS UA

Analiza los archivos .tex del proyecto y genera un informe de revisión
en informe-revision.md. No requiere IA ni conexión a internet.

Verificación de plagio (opcional): solo con la opción --plagio. Entonces,
y tras pedir confirmación, el texto del trabajo (sin código ni comentarios)
se envía a Copyleaks y/o Turnitin con las claves del archivo .env
(ver .env.example). Sin --plagio el script nunca contacta servicios externos,
aunque haya claves en .env.

Uso:
    python3 scripts/revision-rapida.py
    python3 scripts/revision-rapida.py --solo-errores
    python3 scripts/revision-rapida.py --capitulo contenido/capitulos/introduccion.tex
    python3 scripts/revision-rapida.py --plagio copyleaks   # envía el texto (pide confirmación)
"""

from __future__ import annotations

import os
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import ClassVar

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

RAIZ = Path(__file__).resolve().parent.parent
CONTENIDO_DIR = RAIZ / "contenido"
REFERENCIAS_BIB = RAIZ / "referencias.bib"
INFORME_SALIDA = RAIZ / "informe-revision.md"

# Comandos prohibidos por la plantilla
COMANDOS_PROHIBIDOS = [
    (r"\\hline", "Usar `\\toprule`, `\\midrule`, `\\bottomrule` (booktabs)"),
    (r"\\begin\{verbatim\}", "Usar entornos `*code` de minted"),
    (r"\\begin\{lstlisting\}", "Usar entornos `*code` de minted"),
    (r"\\usepackage\[utf8\]\{inputenc\}", "LuaLaTeX maneja UTF-8 nativamente"),
    (r"\\usepackage\{subfigure\}", "Usar `subcaption`"),
    (r"\\usepackage\{subfig\}", "Usar `subcaption`"),
    (r"\\bibliographystyle\{", "Usar BibLaTeX con `\\printbibliography`"),
    (r"\\bibliography\{", "Usar BibLaTeX con `\\printbibliography`"),
    (r"\\cite(?![a-zA-Z])", "Usar `\\parencite{}` o `\\textcite{}`"),
    (r"\\cite[pt](?![a-zA-Z])", "Con biblatex-apa, usar `\\parencite{}` en lugar de `\\citep` y `\\textcite{}` en lugar de `\\citet`"),
    (r"\\include\{", "Usar `\\input{}` para evitar saltos de página forzados"),
]

# Capítulos esperados en un TFG/TFM estándar (al menos algunos de estos)
CAPITULOS_ESPERADOS = [
    "introduccion", "objetivos", "marco", "teorico", "metodologia",
    "desarrollo", "resultados", "conclusiones"
]

# Palabras que indican registro informal
REGISTRO_INFORMAL = [
    r"\byo\b", r"\bmi\b(?!\s+trabajo|\s+tesis|\s+tfg|\s+tfm)",
    r"\bcreo\s+que\b", r"\bpienso\s+que\b", r"\bopino\s+que\b",
    r"\bbueno\b", r"\bpues\b", r"\bvale\b", r"\bgenial\b",
    r"\bchulo\b", r"\bguay\b",
]

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def cargar_env():
    """Carga variables de .env si existe."""
    env_path = RAIZ / ".env"
    env = {}
    if env_path.exists():
        for linea in env_path.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                clave, _, valor = linea.partition("=")
                env[clave.strip()] = valor.strip().strip('"').strip("'")
    return env


def ruta_relativa(ruta: Path) -> str:
    """Ruta relativa a la raíz del proyecto (o absoluta si está fuera)."""
    try:
        return str(ruta.resolve().relative_to(RAIZ))
    except ValueError:
        return str(ruta)


def version_plantilla() -> str:
    r"""Versión de la plantilla leída de \ProvidesClass en cls/eps-tfg.cls."""
    try:
        texto = (RAIZ / "cls" / "eps-tfg.cls").read_text(encoding="utf-8")
    except OSError:
        return "desconocida"
    m = re.search(r"\\ProvidesClass\{eps-tfg\}\[[^\]]*?v(\d+(?:\.\d+)+)", texto)
    return m.group(1) if m else "desconocida"


def leer_tex(ruta: Path) -> str:
    """Lee un archivo .tex (devuelve cadena vacía si no se puede leer)."""
    try:
        return ruta.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except PermissionError as e:
        print(f"Error de permisos al leer {ruta}: {e}", file=sys.stderr)
        return ""
    except UnicodeDecodeError as e:
        print(f"Error de codificación en {ruta}: {e}", file=sys.stderr)
        return ""


def _fin_grupo(texto: str, i: int, abre: str = "{", cierra: str = "}") -> int:
    """Devuelve el índice siguiente al delimitador que cierra el grupo que
    empieza en texto[i] (que debe ser `abre`), respetando llaves anidadas.
    Si el grupo no se cierra, devuelve len(texto)."""
    profundidad = 0
    j = i
    while j < len(texto):
        c = texto[j]
        if c == "\\":
            j += 2
            continue
        if c == abre:
            profundidad += 1
        elif c == cierra:
            profundidad -= 1
            if profundidad == 0:
                return j + 1
        elif abre == "[" and c == "{":
            # Dentro de un argumento opcional, saltar grupos {…} completos
            j = _fin_grupo(texto, j)
            continue
        j += 1
    return len(texto)


def _vaciar(fragmento: str) -> str:
    """Sustituye un fragmento por tantos saltos de línea como contenía."""
    return "\n" * fragmento.count("\n")


def _nombres_listings_plantilla() -> set:
    """Nombres de entornos tipo listing definidos en sty/ (tcblisting)."""
    nombres = set()
    patron = re.compile(
        r"\\(?:newtcblisting|renewtcblisting|DeclareTCBListing|NewTCBListing"
        r"|newtcbinputlisting)(?:\[[^\]]*\])?\{([^}]+)\}"
    )
    for sty in (RAIZ / "sty").rglob("*.sty") if (RAIZ / "sty").is_dir() else []:
        try:
            nombres.update(patron.findall(sty.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            pass
    return nombres


# Entornos cuyo contenido es código o texto literal: no es prosa del trabajo
# y puede contener \section{…}, \label{…}, \cite{…} de ejemplo.
_ENTORNOS_CODIGO_RE = (
    r"[A-Za-z]*code(?:Dark)?(?:NN)?\*?"            # pythoncode, latexcode, jscodeDarkNN…
    r"|codigo(?:simple)?(?:Dark)?(?:NN)?"          # codigo, codigosimple, codigoDarkNN…
    r"|[vV]erbatim\*?|[BL]Verbatim\*?|alltt"
    r"|lstlisting|minted\*?|tcblisting\*?|tcboutputlisting"
    r"|comment|filecontents\*?|terminal"
)
_PATRON_INICIO_CODIGO = re.compile(
    r"\\begin\{("
    + _ENTORNOS_CODIGO_RE
    + "".join("|" + re.escape(n) for n in sorted(_nombres_listings_plantilla()))
    + r")\}"
)
# Código en línea: \verb|…|, \verb*|…|, \lstinline|…|, \mintinline{lang}{…}
_PATRON_VERB = re.compile(r"\\(?:verb\*?|lstinline(?:\[[^\]]*\])?)([^a-zA-Z\s{])(.*?)\1")
_PATRON_MINTINLINE = re.compile(r"\\mintinline(?:\[[^\]]*\])?\{[^}]*\}")


# Opciones [..] justo tras \begin{entorno} (admite un nivel de [] anidados)
_PATRON_OPCIONES_ENTORNO = re.compile(r"\s*\[((?:[^\[\]]|\[[^\]]*\])*)\]")
# label=clave o label={clave} dentro de esas opciones
_PATRON_LABEL_OPCION = re.compile(r"(?<![\w-])label\s*=\s*\{?\s*([^,{}\]\s]+)")


def eliminar_bloques_codigo(texto: str) -> str:
    """Vacía el contenido de entornos de código y del código en línea.

    Conserva el número de líneas para que los diagnósticos posteriores
    apunten a la línea correcta. Aplicar después de eliminar_comentarios().
    """
    # 1. Código en línea (antes que los entornos: \verb|\begin{pythoncode}|
    #    no debe abrir un bloque).
    texto = _PATRON_VERB.sub(r"\\verb\1VERBATIM\1", texto)
    partes = []
    pos = 0
    for m in _PATRON_MINTINLINE.finditer(texto):
        if m.start() < pos:
            continue
        partes.append(texto[pos:m.end()])
        i = m.end()
        if i < len(texto) and texto[i] == "{":
            fin = _fin_grupo(texto, i)
        elif i < len(texto):
            delim = texto[i]
            fin = texto.find(delim, i + 1)
            fin = len(texto) if fin == -1 else fin + 1
        else:
            fin = i
        partes.append("{CODIGO}" + _vaciar(texto[i:fin]))
        pos = fin
    partes.append(texto[pos:])
    texto = "".join(partes)

    # 2. Entornos de código: todo lo que hay entre \begin{X} y \end{X}
    #    (incluidos sus argumentos) se vacía.
    partes = []
    pos = 0
    while True:
        m = _PATRON_INICIO_CODIGO.search(texto, pos)
        if not m:
            break
        cierre = "\\end{" + m.group(1) + "}"
        fin = texto.find(cierre, m.end())
        if fin == -1:
            fin = len(texto)
        partes.append(texto[pos:m.end()])
        # La clave label={...} de las opciones del entorno (p. ej.
        # \begin{pythoncode}[label={cod:x}]) define una etiqueta real: se
        # conserva como \label{} para que \ref{cod:x} no se marque como rota.
        opciones = _PATRON_OPCIONES_ENTORNO.match(texto, m.end())
        if opciones:
            for etiqueta in _PATRON_LABEL_OPCION.findall(opciones.group(1)):
                partes.append("\\label{" + etiqueta + "}")
        partes.append(_vaciar(texto[m.end():fin]))
        pos = fin
    partes.append(texto[pos:])
    return "".join(partes)


def eliminar_comentarios(texto: str) -> str:
    """Elimina comentarios LaTeX (desde un % no escapado hasta el final de línea)."""
    lineas = []
    for linea in texto.splitlines():
        # Eliminar comentarios inline: % precedido de número par de backslashes
        # (?<!\\)   → no precedido por un \ solitario (evita \%)
        # (?:\\\\)* → permite cero o más pares \\  (p.ej. \\ seguido de %)
        linea_limpia = re.sub(r"((?<!\\)(?:\\\\)*)%.*$", r"\1", linea)
        lineas.append(linea_limpia)
    return "\n".join(lineas)


def limpiar_texto(texto: str) -> str:
    """Comentarios y código fuera: deja solo el texto que se compone como prosa."""
    return eliminar_bloques_codigo(eliminar_comentarios(texto))


def contar_palabras(texto: str) -> int:
    """Cuenta palabras aproximadas en texto LaTeX."""
    # Reemplazar comandos preservando su contenido de forma iterativa para
    # manejar llaves anidadas (p.ej. \caption{texto \ref{fig:x}}).
    # Se usa r"\1" para conservar las palabras dentro de \textit{}, \textbf{},
    # \caption{}, etc. y obtener un conteo más preciso.
    prev = None
    while prev != texto:
        prev = texto
        texto = re.sub(r"\\[a-zA-Z]+\*?\{([^{}]*)\}", r"\1", texto)
    texto = re.sub(r"\\[a-zA-Z]+\*?", " ", texto)
    texto = re.sub(r"[{}]", " ", texto)
    texto = re.sub(r"\$[^$]*\$", " ", texto)
    return len(texto.split())


def extraer_texto_plano(archivos_tex: list) -> str:
    """Extrae texto sin markup LaTeX ni código para envío a APIs externas de plagio."""
    fragmentos = []
    for ruta in archivos_tex:
        texto = leer_tex(ruta)
        if not texto.strip():
            continue
        texto = limpiar_texto(texto)
        # Fuera: código en línea, citas, etiquetas, referencias, URLs,
        # \begin/\end y argumentos opcionales (no son texto del trabajo).
        texto = re.sub(r"\\(?:verb|lstinline)\S?VERBATIM\S?|\\mintinline\{[^}]*\}\{CODIGO\}", " ", texto)
        texto = _PATRON_CITA.sub(" ", texto)
        texto = re.sub(
            r"\\(?:label|ref|pageref|eqref|autoref|cref|Cref|nameref|url"
            r"|includegraphics|input|include)\*?(?:\[[^\]]*\])?\{[^}]*\}",
            " ", texto,
        )
        texto = re.sub(r"\\(?:begin|end)\{[^}]*\}", " ", texto)
        texto = re.sub(r"(\\[a-zA-Z]+\*?)\[[^\]]*\]", r"\1", texto)
        prev = None
        while prev != texto:
            prev = texto
            texto = re.sub(r"\\[a-zA-Z]+\*?\{([^{}]*)\}", r"\1", texto)
        texto = re.sub(r"\\[a-zA-Z]+\*?", " ", texto)
        texto = re.sub(r"[{}]", " ", texto)
        texto = re.sub(r"\$[^$]*\$", " ", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        if texto:
            fragmentos.append(texto)
    return "\n\n".join(fragmentos)


# ---------------------------------------------------------------------------
# Análisis
# ---------------------------------------------------------------------------

class Problema:
    SEVERIDAD: ClassVar[dict[str, str]] = {"error": "❌", "advertencia": "⚠️", "info": "ℹ️"}

    def __init__(self, archivo, linea, severidad, categoria, mensaje, sugerencia=""):
        self.archivo = archivo
        self.linea = linea
        self.severidad = severidad
        self.categoria = categoria
        self.mensaje = mensaje
        self.sugerencia = sugerencia

    def __str__(self):
        icono = self.SEVERIDAD.get(self.severidad, "•")
        if self.archivo:
            loc = f"`{self.archivo}`" + (f" línea {self.linea}" if self.linea else "")
            base = f"{icono} **{self.categoria}** — {loc}: {self.mensaje}"
        else:
            base = f"{icono} **{self.categoria}**: {self.mensaje}"
        if self.sugerencia:
            base += f"\n  > {self.sugerencia}"
        return base


def analizar_comandos_prohibidos(ruta: Path, texto: str) -> list:
    """Detecta uso de comandos prohibidos por la plantilla."""
    problemas = []
    texto_sin_comentarios = limpiar_texto(texto)
    for patron, sugerencia in COMANDOS_PROHIBIDOS:
        for m in re.finditer(patron, texto_sin_comentarios):
            linea = texto_sin_comentarios[:m.start()].count("\n") + 1
            problemas.append(Problema(
                archivo=ruta_relativa(ruta),
                linea=linea,
                severidad="error",
                categoria="Formato LaTeX",
                mensaje=f"Comando prohibido: `{m.group().strip()}`",
                sugerencia=sugerencia,
            ))
    return problemas


def analizar_etiquetas(ruta: Path, texto: str) -> list:
    r"""Detecta figuras, tablas y ecuaciones sin \label{}."""
    problemas = []
    texto_sin_comentarios = limpiar_texto(texto)

    # Entornos que deben tener \label
    entornos_con_label = ["figure", "table", "equation", "align", "lstlisting"]
    for entorno in entornos_con_label:
        patron = rf"\\begin\{{{entorno}\*?\}}(.*?)\\end\{{{entorno}\*?\}}"
        for m in re.finditer(patron, texto_sin_comentarios, re.DOTALL):
            bloque = m.group(0)
            if r"\label{" not in bloque:
                linea = texto_sin_comentarios[:m.start()].count("\n") + 1
                problemas.append(Problema(
                    archivo=ruta_relativa(ruta),
                    linea=linea,
                    severidad="advertencia",
                    categoria="Referencias",
                    mensaje=f"Entorno `{entorno}` sin `\\label{{}}` — no se podrá referenciar",
                    sugerencia=f"Añadir `\\label{{{entorno[:3]}:nombre}}` dentro del entorno",
                ))

    return problemas


def analizar_captions(ruta: Path, texto: str) -> list:
    r"""Detecta figuras y tablas sin \caption{}."""
    problemas = []
    texto_sin_comentarios = limpiar_texto(texto)

    for entorno in ["figure", "table"]:
        patron = rf"\\begin\{{{entorno}\*?\}}(.*?)\\end\{{{entorno}\*?\}}"
        for m in re.finditer(patron, texto_sin_comentarios, re.DOTALL):
            bloque = m.group(0)
            if r"\caption{" not in bloque:
                linea = texto_sin_comentarios[:m.start()].count("\n") + 1
                problemas.append(Problema(
                    archivo=ruta_relativa(ruta),
                    linea=linea,
                    severidad="error",
                    categoria="Figuras/Tablas",
                    mensaje=f"Entorno `{entorno}` sin `\\caption{{}}` — obligatorio",
                    sugerencia=f"Añadir `\\caption{{Descripción de la {entorno}}}` antes de `\\label`",
                ))

    return problemas


def analizar_referencias_cruzadas(archivos_tex: list) -> list:
    r"""Detecta \ref{} sin \label{} correspondiente."""
    problemas = []
    labels_definidos = set()
    refs_usadas = []  # (archivo, linea, clave)

    for ruta in archivos_tex:
        texto_raw = eliminar_comentarios(leer_tex(ruta))
        # Labels y referencias se recogen solo fuera de bloques de código,
        # para evitar que etiquetas de ejemplo (dentro de codigosimple/latexcode)
        # se registren como definiciones reales y oculten referencias rotas.
        texto = eliminar_bloques_codigo(texto_raw)
        for m in re.finditer(r"\\label\{([^}]+)\}", texto):
            labels_definidos.add(m.group(1))
        for m in re.finditer(r"\\(?:ref|pageref|cref|Cref)\{([^}]+)\}", texto):
            linea = texto[:m.start()].count("\n") + 1
            refs_usadas.append((ruta_relativa(ruta), linea, m.group(1)))

    for archivo, linea, clave in refs_usadas:
        if clave not in labels_definidos:
            problemas.append(Problema(
                archivo=archivo,
                linea=linea,
                severidad="error",
                categoria="Referencias",
                mensaje=f"Referencia `\\ref{{{clave}}}` sin `\\label{{{clave}}}` definido",
                sugerencia="Añadir `\\label{" + clave + "}` en el elemento referenciado",
            ))

    return problemas


# Comandos de cita de BibLaTeX y natbib (con variantes en mayúscula y forma con *).
# Las formas en plural (\parencites, \textcites…) admiten varias claves.
_COMANDOS_CITA = (
    r"[Cc]ite|[Pp]arencite|[Tt]extcite|[Aa]utocite|[Ff]ootcite|footcitetext"
    r"|[Ss]martcite|[Ss]upercite|[Cc]iteauthor|[Cc]itetitle|citeyear|citedate"
    r"|citeurl|fullcite|footfullcite|nocite|volcite|[Pp]volcite|[Ff]tvolcite"
    # Comandos natbib (la clase carga biblatex con natbib=true)
    r"|[Cc]itep|[Cc]itet|[Cc]iteal[pt]|[Cc]itenum|[Cc]itealias[pt]"
)
_ARG_OPCIONAL = r"(?:\s*\[[^\]]*\]){0,2}\s*"
_PATRON_CITA = re.compile(
    r"\\(" + _COMANDOS_CITA + r")(?:"
    # Forma plural (multicita): (pre)(post)[..]{claves}[..]{claves}…
    r"(s)\*?((?:\s*\([^)]*\)){0,2}(?:" + _ARG_OPCIONAL + r"\{[^}]*\})+)"
    # Forma singular: [pre][post]{claves}
    r"|\*?(" + _ARG_OPCIONAL + r"\{[^}]*\}))"
)


def _claves_de_cita(m: re.Match) -> list:
    """Extrae las claves de un comando de cita reconocido por _PATRON_CITA."""
    argumentos = m.group(3) if m.group(2) else m.group(4)
    claves = []
    for grupo in re.findall(r"\{([^}]*)\}", argumentos):
        claves += [c.strip() for c in grupo.split(",") if c.strip()]
    return claves


def analizar_bibliografia(archivos_tex: list) -> list:
    """Detecta citas sin entrada en .bib y entradas .bib no citadas."""
    problemas = []

    if not REFERENCIAS_BIB.exists():
        problemas.append(Problema(
            archivo="referencias.bib",
            linea=None,
            severidad="error",
            categoria="Bibliografía",
            mensaje="No se encontró el archivo `referencias.bib`",
        ))
        return problemas

    # Claves definidas en .bib
    texto_bib = REFERENCIAS_BIB.read_text(encoding="utf-8")
    claves_bib = set(re.findall(r"@\w+\s*[{(]\s*([^,\s]+)\s*,", texto_bib))

    # Claves citadas en los .tex
    claves_citadas = set()
    citas_por_archivo = []
    nocite_todo = False
    for ruta in archivos_tex:
        texto = limpiar_texto(leer_tex(ruta))
        for m in _PATRON_CITA.finditer(texto):
            linea = texto.count("\n", 0, m.start()) + 1
            for clave in _claves_de_cita(m):
                if clave == "*":
                    nocite_todo = True
                    continue
                claves_citadas.add(clave)
                citas_por_archivo.append((ruta_relativa(ruta), linea, clave))

    # Citas sin entrada en .bib
    for archivo, linea, clave in citas_por_archivo:
        if clave not in claves_bib:
            problemas.append(Problema(
                archivo=archivo,
                linea=linea,
                severidad="error",
                categoria="Bibliografía",
                mensaje=f"Cita `{clave}` no encontrada en `referencias.bib`",
                sugerencia=f"Añadir la entrada `@...{{{clave}, ...}}` a `referencias.bib`",
            ))

    # Entradas .bib no citadas (\nocite{*} las incluye todas)
    no_citadas = set() if nocite_todo else claves_bib - claves_citadas
    for clave in sorted(no_citadas):
        problemas.append(Problema(
            archivo="referencias.bib",
            linea=None,
            severidad="info",
            categoria="Bibliografía",
            mensaje=f"Entrada `{clave}` definida en `.bib` pero no citada en el texto",
            sugerencia="Citar con `\\parencite{" + clave + "}` o eliminar la entrada si no se usa",
        ))

    return problemas


# Niveles de sección: (nivel jerárquico, nombre, artículo, mínimo de palabras).
# Solo se revisan capítulos, secciones y subsecciones numerados; los niveles
# inferiores delimitan contenido pero su texto cuenta para el elemento que los
# contiene. Los encabezados con * (Resumen, Agradecimientos…) no se revisan.
NIVELES_SECCION = {
    "part": (-1, "parte", "Una", None),
    "chapter": (0, "capítulo", "Un", 300),
    "section": (1, "sección", "Una", 50),
    "subsection": (2, "subsección", "Una", 30),
    "subsubsection": (3, "subsubsección", "Una", None),
}
# Aunque una sección contenga figuras, tablas o código, se avisa si apenas
# tiene texto que los introduzca o comente.
MIN_PALABRAS_CON_ELEMENTOS = 5
_PATRON_SECCION = re.compile(
    r"\\(" + "|".join(NIVELES_SECCION) + r")(?![a-zA-Z])(\*?)"
)
# Elementos que aportan contenido aunque no sean prosa
_PATRON_ELEMENTOS = re.compile(
    r"\\begin\{(?:figure|table|sideways(?:figure|table)|longtable|tabular[xy]?|tblr"
    r"|equation|align|gather|multline|tikzpicture|itemize|enumerate|description"
    r"|subfigure|minipage)\*?\}"
    r"|\\includegraphics|\\\[|\\begin\{(?:" + _ENTORNOS_CODIGO_RE + r")\}"
)
# Títulos de páginas preliminares de tono personal
_TITULOS_PERSONALES = re.compile(
    r"agradecimientos|dedicatoria|acknowledg|agra[iï]ments|dedicat", re.IGNORECASE
)
# Si el contenido incluye otros archivos no se puede medir desde aquí
_PATRON_INCLUSION = re.compile(r"\\(?:input|include|subfile|import|subimport)(?![a-zA-Z])")


def _n_palabras(n: int) -> str:
    return f"{n} palabra" if n == 1 else f"{n} palabras"


def _buscar_secciones(texto: str) -> list:
    r"""Localiza \chapter, \section… (con *, título corto [..] y llaves anidadas).

    Devuelve una lista de tuplas (inicio, fin, comando, estrella, titulo).
    """
    secciones = []
    for m in _PATRON_SECCION.finditer(texto):
        i = m.end()
        while i < len(texto) and texto[i] in " \t\n":
            i += 1
        if i < len(texto) and texto[i] == "[":
            i = _fin_grupo(texto, i, "[", "]")
            while i < len(texto) and texto[i] in " \t\n":
                i += 1
        if i >= len(texto) or texto[i] != "{":
            continue  # p.ej. mención del comando sin argumento
        fin = _fin_grupo(texto, i)
        titulo = re.sub(r"\s+", " ", texto[i + 1:fin - 1]).strip()
        secciones.append((m.start(), fin, m.group(1), m.group(2), titulo))
    return secciones


def _fin_subarbol(secciones: list, idx: int, total: int) -> int:
    """Posición donde termina el contenido de secciones[idx] (siguiente
    encabezado de nivel igual o superior, o el final del texto)."""
    nivel = NIVELES_SECCION[secciones[idx][2]][0]
    for otra in secciones[idx + 1:]:
        if NIVELES_SECCION[otra[2]][0] <= nivel:
            return otra[0]
    return total


def analizar_secciones_vacias(ruta: Path, texto: str) -> list:
    """Detecta capítulos, secciones y subsecciones con muy poco contenido.

    El contenido de cada elemento incluye el de sus subsecciones: solo se
    avisa cuando el elemento COMPLETO (todo su subárbol) es demasiado breve.
    Se ignoran comentarios y bloques de código.
    """
    problemas = []
    limpio = limpiar_texto(texto)
    secciones = _buscar_secciones(limpio)

    for idx, (inicio, fin_cmd, comando, estrella, titulo) in enumerate(secciones):
        _, nombre, articulo, umbral = NIVELES_SECCION[comando]
        if umbral is None or estrella:
            continue
        fin_contenido = _fin_subarbol(secciones, idx, len(limpio))

        # Texto del subárbol sin los propios comandos de encabezado
        trozos = []
        pos = fin_cmd
        for otra in secciones[idx + 1:]:
            if otra[0] >= fin_contenido:
                break
            trozos.append(limpio[pos:otra[0]])
            pos = otra[1]
        trozos.append(limpio[pos:fin_contenido])
        contenido = "".join(trozos)

        if _PATRON_INCLUSION.search(contenido):
            continue  # el contenido real está en otro archivo
        palabras = contar_palabras(contenido)
        tiene_elementos = bool(_PATRON_ELEMENTOS.search(contenido))
        if palabras >= umbral:
            continue
        if tiene_elementos and palabras >= MIN_PALABRAS_CON_ELEMENTOS:
            continue

        linea = limpio.count("\n", 0, inicio) + 1
        titulo_corto = titulo if len(titulo) <= 60 else titulo[:57] + "..."
        encabezado = f"`\\{comando}{{{titulo_corto}}}`"
        if tiene_elementos:
            mensaje = (
                f"{nombre.capitalize()} {encabezado} sin apenas texto ({_n_palabras(palabras)}): "
                "solo contiene figuras, tablas, código o listas"
            )
            sugerencia = (
                "Añadir al menos un párrafo que introduzca y comente su contenido "
                "(y referenciarlo con `\\ref{}`)"
            )
        else:
            mensaje = (
                f"{nombre.capitalize()} {encabezado} con muy poco contenido "
                f"({_n_palabras(palabras)}, incluidas sus subsecciones)"
            )
            sugerencia = (
                f"{articulo} {nombre} debería tener al menos {umbral} palabras "
                "de texto (sin contar código ni comentarios), o integrarse en otra"
            )
        problemas.append(Problema(
            archivo=ruta_relativa(ruta),
            linea=linea,
            severidad="advertencia",
            categoria="Estructura",
            mensaje=mensaje,
            sugerencia=sugerencia,
        ))

    return problemas


def _rangos_personales(texto: str) -> list:
    """Rangos (inicio, fin) de dedicatoria y agradecimientos, donde la primera
    persona es adecuada: el subárbol de \\chapter*{Agradecimientos} y similares
    y, si el archivo empieza por ellos, el texto previo (dedicatoria)."""
    secciones = _buscar_secciones(texto)
    rangos = []
    for idx, sec in enumerate(secciones):
        if _TITULOS_PERSONALES.search(sec[4]):
            inicio = sec[0]
            if idx == 0:
                inicio = 0
            rangos.append((inicio, _fin_subarbol(secciones, idx, len(texto))))
    return rangos


def analizar_registro_informal(ruta: Path, texto: str) -> list:
    """Detecta posible registro informal."""
    problemas = []
    texto_sin_comentarios = limpiar_texto(texto)
    exentos = _rangos_personales(texto_sin_comentarios)

    for patron in REGISTRO_INFORMAL:
        for m in re.finditer(patron, texto_sin_comentarios, re.IGNORECASE):
            if any(ini <= m.start() < fin for ini, fin in exentos):
                continue
            linea = texto_sin_comentarios[:m.start()].count("\n") + 1
            problemas.append(Problema(
                archivo=ruta_relativa(ruta),
                linea=linea,
                severidad="advertencia",
                categoria="Lenguaje",
                mensaje=f"Posible registro informal: `{m.group().strip()}`",
                sugerencia="Usar voz impersonal: 'se ha desarrollado', 'en este trabajo se propone'",
            ))

    return problemas


def analizar_estructura_global(archivos_tex: list) -> list:
    """Verifica que el documento tiene los capítulos esperados."""
    problemas = []
    nombres_archivos = [p.stem.lower() for p in archivos_tex]
    texto_total = " ".join(nombres_archivos)

    capitulos_encontrados = []
    for cap in CAPITULOS_ESPERADOS:
        if any(cap in nombre for nombre in nombres_archivos):
            capitulos_encontrados.append(cap)

    if "introduccion" not in texto_total and "introduction" not in texto_total:
        problemas.append(Problema(
            archivo="main.tex",
            linea=None,
            severidad="advertencia",
            categoria="Estructura",
            mensaje="No se detecta capítulo de introducción",
            sugerencia="Crear `contenido/capitulos/introduccion.tex` e incluirlo en `main.tex`",
        ))

    if "conclusiones" not in texto_total and "conclusions" not in texto_total:
        problemas.append(Problema(
            archivo="main.tex",
            linea=None,
            severidad="advertencia",
            categoria="Estructura",
            mensaje="No se detecta capítulo de conclusiones",
            sugerencia="Crear `contenido/capitulos/conclusiones.tex` e incluirlo en `main.tex`",
        ))

    return problemas


# ---------------------------------------------------------------------------
# API de plagio (opcional, solo con --plagio)
# ---------------------------------------------------------------------------
#
# El texto del trabajo NUNCA se envía a un servicio externo de forma
# automática: hace falta pedirlo con --plagio y confirmar el envío.

SERVICIOS_PLAGIO = {
    "copyleaks": {
        "nombre": "Copyleaks",
        "destino": "id.copyleaks.com / api.copyleaks.com",
        "coste": "consume créditos de tu cuenta Copyleaks en cada envío",
        "claves": ("COPYLEAKS_API_KEY", "COPYLEAKS_WEBHOOK_URL"),
    },
    "turnitin": {
        "nombre": "Turnitin",
        "destino": None,  # TURNITIN_TENANT_URL
        "coste": "crea una NUEVA entrega en Turnitin en cada envío",
        "claves": ("TURNITIN_API_KEY", "TURNITIN_TENANT_URL"),
    },
}


def verificar_plagio_copyleaks(texto: str, api_key: str, webhook_url: str,
                               sandbox: bool = False) -> list:
    """
    Integración con Copyleaks API v3 (opt-in, solo con --plagio).

    Autentica con la cuenta Copyleaks y envía el documento para análisis.
    La API v3 es asíncrona: Copyleaks notifica el progreso a la URL de
    webhook indicada (obligatoria en la API) y los resultados se consultan
    en https://app.copyleaks.com.

    Configuración en .env:
        COPYLEAKS_API_KEY=email@dominio.com:00000000-0000-0000-0000-000000000000
        COPYLEAKS_WEBHOOK_URL=https://servidor-propio.example/copyleaks/{STATUS}
        # Opcional: modo de pruebas, sin consumir créditos
        COPYLEAKS_SANDBOX=true
    """
    import base64
    import json
    import urllib.error
    import urllib.request
    import uuid

    if ":" not in api_key:
        return [{
            "tipo": "advertencia",
            "mensaje": "COPYLEAKS_API_KEY debe tener formato "
                       "'email@dominio.com:clave-uuid'",
        }]
    if not webhook_url.startswith("https://"):
        return [{
            "tipo": "advertencia",
            "mensaje": "COPYLEAKS_WEBHOOK_URL debe ser una URL https:// de un "
                       "servidor que controles (la API de Copyleaks la exige)",
        }]

    email, _, key = api_key.partition(":")

    try:
        # 1. Autenticación
        login_body = json.dumps({"email": email, "key": key}).encode()
        req = urllib.request.Request(
            "https://id.copyleaks.com/v3/account/login/api",
            data=login_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            token = json.loads(resp.read().decode())["access_token"]

        # 2. Envío del documento
        scan_id = str(uuid.uuid4())
        text_b64 = base64.b64encode(texto.encode("utf-8")).decode()
        submit_body = json.dumps({
            "base64": text_b64,
            "filename": "tfg-tfm.txt",
            "properties": {
                "sandbox": sandbox,
                "action": 0,
                "webhooks": {"status": webhook_url},
            },
        }).encode()
        req = urllib.request.Request(
            f"https://api.copyleaks.com/v3/scans/submit/file/{scan_id}",
            data=submit_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            method="PUT",
        )
        with urllib.request.urlopen(req, timeout=30):
            pass  # 200/201 OK

        modo = " en modo sandbox" if sandbox else ""
        return [{
            "tipo": "info",
            "mensaje": (
                f"Copyleaks: documento enviado{modo} (scan ID: {scan_id}). "
                "El análisis es asíncrono — ver resultados en "
                "https://app.copyleaks.com"
            ),
        }]

    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")[:200]
        return [{"tipo": "advertencia", "mensaje": f"Copyleaks HTTP {e.code}: {detalle}"}]
    except Exception as e:
        return [{"tipo": "advertencia", "mensaje": f"Error al conectar con Copyleaks: {e}"}]


def verificar_plagio_turnitin(texto: str, api_key: str, tenant_url: str) -> list:
    """
    Integración completa con Turnitin Core API v1 (opt-in, solo con --plagio).

    Crea la entrega, sube el contenido y obtiene el porcentaje de similitud
    mediante sondeo (polling). Requiere acceso institucional a Turnitin.

    Credenciales en .env:
        TURNITIN_API_KEY=tu-clave-de-api
        TURNITIN_TENANT_URL=https://tu-institucion.turnitin.com/api/v1
    """
    import json
    import time
    import urllib.error
    import urllib.parse
    import urllib.request

    if not tenant_url:
        return [{
            "tipo": "advertencia",
            "mensaje": (
                "Falta TURNITIN_TENANT_URL en .env "
                "(ej: https://tu-institucion.turnitin.com/api/v1)"
            ),
        }]

    base_url = tenant_url.rstrip("/")
    origen = urllib.parse.urlsplit(base_url)
    if origen.scheme != "https" or not origen.hostname:
        # La clave de API viaja en la cabecera Authorization: solo por HTTPS
        return [{
            "tipo": "advertencia",
            "mensaje": (
                "TURNITIN_TENANT_URL debe ser una URL https:// "
                f"(valor actual: {tenant_url!r})"
            ),
        }]

    class _MismoOrigen(urllib.request.HTTPRedirectHandler):
        """Rechaza redirecciones a otro origen o sin HTTPS (no filtrar la clave)."""

        def redirect_request(self, req, fp, code, msg, headers, newurl):
            nueva = urllib.parse.urlsplit(newurl)
            if (nueva.scheme, nueva.hostname, nueva.port) != (
                    origen.scheme, origen.hostname, origen.port):
                raise urllib.error.HTTPError(
                    newurl, code, f"redirección a otro origen rechazada: {newurl}",
                    headers, fp)
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    opener = urllib.request.build_opener(_MismoOrigen)
    base_headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Turnitin-Integration-Name": "TFG-TFM-EPS-UA",
        "X-Turnitin-Integration-Version": version_plantilla(),
    }

    def _request(method: str, path: str, body=None, binary: bool = False) -> dict:
        url = f"{base_url}/{path.lstrip('/')}"
        headers = dict(base_headers)
        data = None
        if body is not None:
            if binary:
                headers["Content-Type"] = "binary/octet-stream"
                headers["Content-Disposition"] = 'inline; filename="tfg-tfm.txt"'
                data = body if isinstance(body, bytes) else body.encode("utf-8")
            else:
                headers["Content-Type"] = "application/json"
                data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with opener.open(req, timeout=30) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}

    def _poll(method: str, path: str, campo: str, valor_ok: str,
              valor_error: str, intentos: int = 24, espera: int = 5) -> dict | None:
        for _ in range(intentos):
            time.sleep(espera)
            data = _request(method, path)
            if data.get(campo) == valor_ok:
                return data
            if data.get(campo) == valor_error:
                return None
        return None

    try:
        # 1. Crear entrega
        submission = _request("POST", "/submissions", {
            "owner": "student",
            "title": "TFG-TFM EPS UA",
            "submitter": "student",
            "owner_default_permission_set": "LEARNER",
            "submitter_default_permission_set": "INSTRUCTOR",
        })
        sid = submission["id"]

        # 2. Subir contenido
        _request("PUT", f"/submissions/{sid}/original", body=texto, binary=True)

        # 3. Esperar procesamiento de la entrega
        estado = _poll("GET", f"/submissions/{sid}", "status", "COMPLETE", "ERROR")
        if estado is None:
            return [{
                "tipo": "advertencia",
                "mensaje": (
                    f"Turnitin: tiempo de espera agotado (entrega ID: {sid}). "
                    "Consultar el panel de Turnitin para ver el resultado."
                ),
            }]

        # 4. Solicitar informe de similitud
        _request("PUT", f"/submissions/{sid}/similarity", {
            "generation_settings": {
                "search_repositories": ["SUBMITTED_WORK", "INTERNET", "PUBLICATION"],
                "auto_exclude_self_matching_scope": "ALL",
            }
        })

        # 5. Obtener informe de similitud
        sim = _poll("GET", f"/submissions/{sid}/similarity", "status", "COMPLETE", "ERROR")
        if sim is None:
            return [{
                "tipo": "advertencia",
                "mensaje": (
                    f"Turnitin: informe de similitud en curso (entrega ID: {sid}). "
                    "Consultar el panel de Turnitin."
                ),
            }]

        pct = sim.get("overall_match_percentage", 0)
        internet = sim.get("internet_match_percentage", "?")
        publicaciones = sim.get("publication_match_percentage", "?")
        trabajos = sim.get("submitted_works_match_percentage", "?")
        nivel = "error" if pct > 20 else "advertencia" if pct > 10 else "info"
        return [{
            "tipo": nivel,
            "mensaje": (
                f"Turnitin: similitud global {pct}% "
                f"(internet {internet}%, publicaciones {publicaciones}%, "
                f"trabajos previos {trabajos}%)"
            ),
        }]

    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")[:200]
        return [{"tipo": "advertencia", "mensaje": f"Turnitin HTTP {e.code}: {detalle}"}]
    except Exception as e:
        return [{"tipo": "advertencia", "mensaje": f"Error al conectar con Turnitin: {e}"}]


def _es_verdadero(valor: str) -> bool:
    return valor.strip().lower() in ("1", "true", "si", "sí", "yes", "on")


def ejecutar_plagio(servicios: list, env: dict, archivos_tex: list,
                    confirmado: bool) -> list:
    """Envía el texto a los servicios pedidos con --plagio, previa confirmación.

    Devuelve una lista de Problema de la categoría "Plagio (API)".
    """
    resultados = []

    def _resultado(severidad: str, mensaje: str, sugerencia: str = ""):
        resultados.append(Problema("", None, severidad, "Plagio (API)", mensaje, sugerencia))

    # 1. Comprobar configuración de cada servicio
    listos = []
    for servicio in servicios:
        datos = SERVICIOS_PLAGIO[servicio]
        faltan = [c for c in datos["claves"] if not env.get(c)]
        if faltan:
            _resultado(
                "advertencia",
                f"{datos['nombre']}: falta configurar {', '.join(faltan)} en `.env`",
                "Ver `.env.example` para el formato de cada clave",
            )
        else:
            listos.append(servicio)
    if not listos:
        return resultados

    # 2. Mostrar qué se va a enviar y a quién
    texto = extraer_texto_plano(archivos_tex)
    sandbox = _es_verdadero(env.get("COPYLEAKS_SANDBOX", ""))
    print()
    print("Verificación de plagio solicitada (--plagio).")
    print(
        f"Se enviará el texto del trabajo ({len(texto.split())} palabras, "
        f"{len(texto)} caracteres; sin comentarios ni bloques de código) a:"
    )
    for servicio in listos:
        datos = SERVICIOS_PLAGIO[servicio]
        destino = datos["destino"] or env.get("TURNITIN_TENANT_URL", "")
        coste = datos["coste"]
        if servicio == "copyleaks":
            if sandbox:
                coste = "modo sandbox (COPYLEAKS_SANDBOX=true): no consume créditos"
            destino += f"; avisos de estado a {env.get('COPYLEAKS_WEBHOOK_URL')}"
        print(f"  - {datos['nombre']} ({destino}): {coste}")

    # 3. Confirmación explícita
    if not confirmado:
        if not sys.stdin.isatty():
            _resultado(
                "advertencia",
                "Envío a servicios de plagio cancelado: no hay terminal interactiva "
                "para confirmar",
                "Repetir con `--plagio … --si` para confirmar el envío sin preguntar",
            )
            print("No hay terminal interactiva: envío cancelado (usar --si para confirmar).")
            return resultados
        try:
            respuesta = input("¿Enviar el texto? [s/N] ").strip().lower()
        except EOFError:
            respuesta = ""
        if respuesta not in ("s", "si", "sí", "y", "yes"):
            _resultado("info", "Envío a servicios de plagio cancelado por el usuario")
            print("Envío cancelado.")
            return resultados

    # 4. Envío
    for servicio in listos:
        if servicio == "copyleaks":
            respuestas = verificar_plagio_copyleaks(
                texto, env["COPYLEAKS_API_KEY"], env["COPYLEAKS_WEBHOOK_URL"], sandbox
            )
        else:
            respuestas = verificar_plagio_turnitin(
                texto, env["TURNITIN_API_KEY"], env["TURNITIN_TENANT_URL"]
            )
        for r in respuestas:
            _resultado(r["tipo"], r["mensaje"])
    return resultados


# ---------------------------------------------------------------------------
# Generación del informe
# ---------------------------------------------------------------------------

def generar_informe(problemas: list, env: dict, archivos_analizados: list) -> str:
    """Genera el informe de revisión en formato Markdown."""
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    n_errores = sum(1 for p in problemas if p.severidad == "error")
    n_advertencias = sum(1 for p in problemas if p.severidad == "advertencia")
    n_info = sum(1 for p in problemas if p.severidad == "info")

    lineas = [
        "# Informe de revisión — TFG/TFM EPS UA",
        "",
        f"**Generado:** {ahora}  ",
        f"**Archivos analizados:** {len(archivos_analizados)}  ",
        f"**Problemas encontrados:** {n_errores} errores · {n_advertencias} advertencias · {n_info} informativos",
        "",
        "---",
        "",
    ]

    # Resumen ejecutivo
    if n_errores == 0 and n_advertencias == 0:
        lineas += [
            "## Resumen",
            "",
            "✅ No se encontraron errores ni advertencias en el análisis estático.",
            "",
        ]
    else:
        lineas += [
            "## Resumen",
            "",
            "| Severidad | Cantidad |",
            "|---|---|",
            f"| ❌ Errores | {n_errores} |",
            f"| ⚠️ Advertencias | {n_advertencias} |",
            f"| ℹ️ Informativos | {n_info} |",
            "",
        ]

    # Agrupar por categoría
    por_categoria = defaultdict(list)
    for p in problemas:
        por_categoria[p.categoria].append(p)

    orden_categorias = [
        "Estructura", "Formato LaTeX", "Referencias", "Figuras/Tablas",
        "Bibliografía", "Lenguaje", "Plagio (API)"
    ]
    categorias_ordenadas = orden_categorias + [
        c for c in por_categoria if c not in orden_categorias
    ]

    for categoria in categorias_ordenadas:
        if categoria not in por_categoria:
            continue
        items = por_categoria[categoria]
        n_err = sum(1 for p in items if p.severidad == "error")
        n_adv = sum(1 for p in items if p.severidad == "advertencia")
        resumen_cat = []
        if n_err:
            resumen_cat.append(f"{n_err} error{'es' if n_err > 1 else ''}")
        if n_adv:
            resumen_cat.append(f"{n_adv} advertencia{'s' if n_adv > 1 else ''}")
        sufijo = f" ({', '.join(resumen_cat)})" if resumen_cat else ""

        lineas += [
            f"## {categoria}{sufijo}",
            "",
        ]
        for p in items:
            lineas.append(str(p))
            lineas.append("")

    # Plagio por API: solo se ejecuta con --plagio
    if "Plagio (API)" not in por_categoria:
        configurados = [
            datos["nombre"] for datos in SERVICIOS_PLAGIO.values()
            if env.get(datos["claves"][0])
        ]
        lineas += ["## Plagio (API)", ""]
        if configurados:
            lineas += [
                f"ℹ️ Hay claves de {' y '.join(configurados)} en `.env`, pero no se ha "
                "enviado nada: la verificación de plagio solo se ejecuta si se pide "
                "explícitamente con `--plagio copyleaks`, `--plagio turnitin` o "
                "`--plagio todos` (se pedirá confirmación antes de enviar el texto).",
                "",
            ]
        else:
            lineas += [
                "ℹ️ No se ha solicitado la verificación de plagio por API externa.",
                "",
                "Para usarla, copiar `.env.example` como `.env`, rellenar las claves y "
                "ejecutar el script con `--plagio copyleaks|turnitin|todos`. "
                "El texto del trabajo solo se envía tras confirmarlo. Claves necesarias:",
                "```text",
                "# Copyleaks — formato email:clave-uuid",
                "COPYLEAKS_API_KEY=email@dominio.com:00000000-0000-0000-0000-000000000000",
                "# URL https de un servidor propio que recibirá los avisos de estado",
                "COPYLEAKS_WEBHOOK_URL=https://tu-servidor.example/copyleaks/{STATUS}",
                "",
                "# Turnitin — requiere acceso institucional",
                "TURNITIN_API_KEY=tu-clave-de-api",
                "TURNITIN_TENANT_URL=https://tu-institucion.turnitin.com/api/v1",
                "```",
                "",
                "El archivo `.env` ya está en `.gitignore` y no se subirá al repositorio.",
                "",
            ]

    # Archivos analizados
    lineas += [
        "---",
        "",
        "## Archivos analizados",
        "",
    ]
    for ruta in sorted(archivos_analizados):
        lineas.append(f"- `{ruta}`")
    lineas.append("")
    lineas += [
        "---",
        "",
        "*Generado por `scripts/revision-rapida.py`. "
        "Para una revisión semántica completa (coherencia, lenguaje, plagio por IA), "
        "usar el agente revisor en GitHub Copilot Chat o Claude.*",
    ]

    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Revisión estática del documento TFG/TFM EPS UA"
    )
    parser.add_argument(
        "--solo-errores",
        action="store_true",
        help="Mostrar solo errores, omitir advertencias e informativos",
    )
    parser.add_argument(
        "--capitulo",
        type=str,
        default=None,
        help="Analizar solo un archivo .tex específico",
    )
    parser.add_argument(
        "--salida",
        type=str,
        default=str(INFORME_SALIDA),
        help=f"Ruta del informe de salida (por defecto: {INFORME_SALIDA})",
    )
    parser.add_argument(
        "--plagio",
        choices=["copyleaks", "turnitin", "todos"],
        default=None,
        help=(
            "Enviar el texto del trabajo (sin código ni comentarios) a un servicio "
            "externo de detección de plagio. Requiere las claves en .env y "
            "confirmación. Sin esta opción nunca se envía nada."
        ),
    )
    parser.add_argument(
        "--si",
        action="store_true",
        help="Con --plagio: confirmar el envío sin preguntar (p.ej. sin terminal interactiva)",
    )
    args = parser.parse_args()

    # Cargar variables de entorno
    env = cargar_env()

    # Determinar archivos a analizar
    if args.capitulo:
        archivos_tex = [Path(args.capitulo).resolve()]
        if not archivos_tex[0].exists():
            print(f"Error: no se encontró el archivo {args.capitulo}", file=sys.stderr)
            sys.exit(1)
    else:
        archivos_tex = sorted(
            list(CONTENIDO_DIR.rglob("*.tex"))
        )
        # Añadir main.tex para análisis de estructura
        main_tex = RAIZ / "main.tex"
        if main_tex.exists():
            archivos_tex.insert(0, main_tex)

    if not archivos_tex:
        print("No se encontraron archivos .tex para analizar.", file=sys.stderr)
        sys.exit(1)

    print(f"Analizando {len(archivos_tex)} archivo(s)...")

    todos_los_problemas = []

    # Análisis global (requiere todos los archivos)
    if args.capitulo:
        # Con un solo capítulo, las etiquetas y citas se buscan en todo el
        # proyecto (las \ref pueden apuntar a otros capítulos), pero solo se
        # informa de lo que está en el capítulo pedido. No tiene sentido
        # revisar la estructura global ni las entradas .bib no citadas.
        proyecto = sorted(CONTENIDO_DIR.rglob("*.tex"))
        proyecto = [p for p in proyecto if p.resolve() != archivos_tex[0]] + archivos_tex
        capitulo_rel = ruta_relativa(archivos_tex[0])
        todos_los_problemas += [
            p for p in analizar_referencias_cruzadas(proyecto) + analizar_bibliografia(proyecto)
            if p.archivo == capitulo_rel
        ]
    else:
        todos_los_problemas += analizar_estructura_global(archivos_tex)
        todos_los_problemas += analizar_referencias_cruzadas(archivos_tex)
        todos_los_problemas += analizar_bibliografia(archivos_tex)

    # Análisis por archivo
    for ruta in archivos_tex:
        if not ruta.exists():
            continue
        texto = leer_tex(ruta)
        if not texto.strip():
            continue

        todos_los_problemas += analizar_comandos_prohibidos(ruta, texto)
        todos_los_problemas += analizar_etiquetas(ruta, texto)
        todos_los_problemas += analizar_captions(ruta, texto)
        todos_los_problemas += analizar_secciones_vacias(ruta, texto)
        todos_los_problemas += analizar_registro_informal(ruta, texto)

    # Filtrar si --solo-errores
    if args.solo_errores:
        todos_los_problemas = [p for p in todos_los_problemas if p.severidad == "error"]

    # Verificación de plagio por API externa: solo si se pide con --plagio
    if args.plagio:
        servicios = ["copyleaks", "turnitin"] if args.plagio == "todos" else [args.plagio]
        todos_los_problemas += ejecutar_plagio(servicios, env, archivos_tex, args.si)

    # Generar informe
    archivos_rel = [ruta_relativa(r) for r in archivos_tex if r.exists()]
    informe = generar_informe(todos_los_problemas, env, archivos_rel)

    # Guardar informe
    salida = Path(args.salida)
    salida.write_text(informe, encoding="utf-8")
    print(f"Informe guardado en: {salida}")

    # Resumen en consola
    n_err = sum(1 for p in todos_los_problemas if p.severidad == "error")
    n_adv = sum(1 for p in todos_los_problemas if p.severidad == "advertencia")
    n_inf = sum(1 for p in todos_los_problemas if p.severidad == "info")
    print(f"Resultado: {n_err} errores · {n_adv} advertencias · {n_inf} informativos")

    # En CI el informe es informativo: siempre salir con 0 para no bloquear el pipeline.
    # En local, salir con 1 si hay errores para que las herramientas del desarrollador lo detecten.
    if os.environ.get("CI"):
        sys.exit(0)
    sys.exit(1 if n_err > 0 else 0)


if __name__ == "__main__":
    main()
