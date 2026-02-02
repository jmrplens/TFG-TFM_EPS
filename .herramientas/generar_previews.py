#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de previsualizaciones para snippets LaTeX en documentación Markdown.

Este script extrae bloques de código LaTeX MARCADOS de los archivos .md en docs/,
genera documentos standalone y los compila a PDF/PNG para previsualización.

IMPORTANTE: Solo se procesan snippets con marcador <!-- preview -->

Marcadores soportados:
    ```latex <!-- preview -->           - Renderizar con 1 pasada
    ```latex <!-- preview:2 -->         - Renderizar con 2 pasadas (refs cruzadas)
    ```latex <!-- preview:3 -->         - Renderizar con 3 pasadas
    ```latex <!-- preview: mi_nombre --> - Nombre personalizado
    ```latex <!-- preview:2 mi_nombre --> - 2 pasadas + nombre personalizado

Autor: Plantilla TFG/TFM EPS UA
Licencia: GPL-3.0
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path
from typing import Optional


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

# Directorio raíz del proyecto (padre de .herramientas)
PROYECTO_ROOT = Path(__file__).parent.parent.resolve()
DOCS_DIR = PROYECTO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets" / "previews"
MANIFEST_FILE = ASSETS_DIR / "manifest.json"
HERRAMIENTAS_DIR = PROYECTO_ROOT / ".herramientas"

# Configuración de compilación
LATEX_ENGINE = "lualatex"
LATEX_ARGS = ["-shell-escape", "-interaction=nonstopmode", "-halt-on-error"]

# Patrones para detectar tipo de contenido
PATRONES_TIPO = {
    "equation": [
        r"\\begin\{equation",
        r"\\begin\{align",
        r"\\begin\{gather",
        r"\\begin\{multline",
        r"\\begin\{cases",
        r"\\\[",
        r"\\frac\{",
        r"\\sum",
        r"\\int",
        r"\\lim",
    ],
    "table": [
        r"\\begin\{tabular",
        r"\\begin\{table",
        r"\\begin\{longtable",
        r"\\begin\{tabularx",
        r"\\toprule",
        r"\\midrule",
    ],
    "figure": [
        r"\\begin\{tikzpicture",
        r"\\begin\{axis",
        r"\\begin\{figure",
        r"\\begin\{pgfplot",
        r"\\draw",
        r"\\addplot",
        r"\\pie",
    ],
    "listing": [
        r"\\begin\{minted",
        r"\\begin\{listing",
        r"\\begin\{pythoncode",
        r"\\begin\{jscode",
        r"\\begin\{cppcode",
        r"\\mintinline",
    ],
    "list": [
        r"\\begin\{itemize",
        r"\\begin\{enumerate",
        r"\\begin\{description",
        r"\\item",
    ],
    "text": [
        r"\\textbf",
        r"\\textit",
        r"\\emph",
        r"\\underline",
        r"\\colorbox",
        r"\\fbox",
    ],
    "box": [
        r"\\begin\{tcolorbox",
        r"\\begin\{mdframed",
    ],
    "glossary": [
        r"\\newglossaryentry",
        r"\\newacronym",
        r"\\gls\{",
        r"\\acrshort",
        r"\\printglossary",
    ],
    "image": [
        r"\\includegraphics",
        r"\\begin\{subfigure",
        r"\\begin\{wrapfigure",
        r"example-image",
    ],
    "bibliography": [
        r"\\parencite",
        r"\\textcite",
        r"\\cite\{",
        r"\\citet\{",
        r"\\citep\{",
        r"\\printbibliography",
    ],
    "crossref": [
        r"\\ref\{",
        r"\\pageref",
        r"\\autoref",
        r"\\nameref",
        r"\\cref\{",
        r"\\hyperref",
    ],
}


# =============================================================================
# ESTRUCTURAS DE DATOS
# =============================================================================


@dataclass
class Snippet:
    """Representa un snippet de código LaTeX extraído."""

    archivo_origen: str
    numero: int
    codigo: str
    linea_inicio: int
    linea_fin: int
    tipo: str = "generic"
    nombre_custom: Optional[str] = None
    pasadas: int = 1  # Número de pasadas de compilación
    hash: str = field(default="", init=False)

    def __post_init__(self):
        self.hash = hashlib.md5(self.codigo.encode()).hexdigest()[:12]

    @property
    def nombre_base(self) -> str:
        """Genera nombre base para archivos de salida."""
        if self.nombre_custom:
            return self.nombre_custom
        archivo_sin_ext = Path(self.archivo_origen).stem
        return f"{archivo_sin_ext}_{self.numero:03d}"

    @property
    def pdf_path(self) -> Path:
        return ASSETS_DIR / f"{self.nombre_base}.pdf"

    @property
    def png_path(self) -> Path:
        return ASSETS_DIR / f"{self.nombre_base}.png"


@dataclass
class Manifest:
    """Manifiesto de snippets generados para tracking de cambios."""

    snippets: dict = field(default_factory=dict)
    ultima_actualizacion: str = ""

    def cargar(self):
        """Carga el manifiesto desde archivo JSON."""
        if MANIFEST_FILE.exists():
            try:
                with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.snippets = data.get("snippets", {})
                    self.ultima_actualizacion = data.get("ultima_actualizacion", "")
            except (json.JSONDecodeError, KeyError):
                pass

    def guardar(self):
        """Guarda el manifiesto a archivo JSON."""
        self.ultima_actualizacion = datetime.now().isoformat()
        MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "snippets": self.snippets,
                    "ultima_actualizacion": self.ultima_actualizacion,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

    def necesita_regenerar(self, snippet: Snippet) -> bool:
        """Verifica si un snippet necesita regenerarse."""
        key = snippet.nombre_base
        if key not in self.snippets:
            return True
        if self.snippets[key].get("hash") != snippet.hash:
            return True
        if not snippet.pdf_path.exists():
            return True
        return False

    def registrar(self, snippet: Snippet, exito: bool):
        """Registra un snippet en el manifiesto."""
        self.snippets[snippet.nombre_base] = {
            "hash": snippet.hash,
            "archivo_origen": snippet.archivo_origen,
            "linea": snippet.linea_inicio,
            "tipo": snippet.tipo,
            "generado": datetime.now().isoformat(),
            "exito": exito,
            "pasadas": snippet.pasadas if hasattr(snippet, 'pasadas') else 1,
        }


# =============================================================================
# PLANTILLAS LATEX
# =============================================================================


def generar_preambulo(tipo: str) -> str:
    """Genera el preámbulo LaTeX apropiado según el tipo de contenido."""

    # Preámbulo base común - usar varwidth más pequeño para evitar "dimension too large"
    base = r"""
\documentclass[preview, border=10pt, varwidth=15cm]{standalone}

% Codificación y fuentes
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{spanish}

% Matemáticas
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}

% Colores
\usepackage{xcolor}

% Hyperref (desactivado para standalone)
\usepackage[draft]{hyperref}
"""

    # Extensiones según tipo
    extensiones = {
        "equation": r"""
% Teoremas y definiciones (entornos personalizados de la plantilla)
\usepackage{amsthm}
\newtheorem{theorem}{Teorema}
\newtheorem{teorema}{Teorema}
\newtheorem{definition}{Definición}
\newtheorem{definicion}{Definición}
\newtheorem{lemma}{Lema}
\newtheorem{lema}{Lema}
\newtheorem{corollary}{Corolario}
\newtheorem{corolario}{Corolario}
\newtheorem{proposition}{Proposición}
\newtheorem{proposicion}{Proposición}
\newtheorem{example}{Ejemplo}
\newtheorem{ejemplo}{Ejemplo}
\newtheorem{remark}{Observación}
\newtheorem{observacion}{Observación}
\newtheorem{condiciones}{Condiciones}

% Para casos/condiciones
\usepackage{cases}
""",
        "table": r"""
% Tablas
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{longtable}
\usepackage{multirow}
\usepackage{array}
\usepackage{colortbl}

% Columnas personalizadas
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}
""",
        "figure": r"""
% Gráficas
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{polar, groupplots, fillbetween, statistics}
\usepackage{pgf-pie}

% Librerías TikZ
\usetikzlibrary{arrows.meta, positioning, shapes, calc, patterns, fillbetween}

% Imágenes y subfiguras
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{caption}
\usepackage{float}
\usepackage{mwe}  % Para example-image placeholders
""",
        "listing": r"""
% Código fuente
\usepackage{minted}
\usepackage{tcolorbox}
\tcbuselibrary{minted, skins, breakable, listings}

% Configuración minted
\setminted{
    fontsize=\small,
    breaklines=true,
    linenos=true,
    numbersep=5pt,
    frame=lines,
    framesep=2mm,
}

% Entornos personalizados de la plantilla (simplificados)
\newtcblisting{pythoncode}[1][]{
    listing engine=minted,
    minted language=python,
    minted style=default,
    colback=gray!5,
    colframe=gray!75!black,
    listing only,
    left=5mm,
    enhanced,
    #1
}

\newtcblisting{pythoncodeDark}[1][]{
    listing engine=minted,
    minted language=python,
    minted style=monokai,
    colback=gray!90!black,
    colframe=gray!50!black,
    listing only,
    left=5mm,
    enhanced,
    #1
}

\newtcblisting{jscode}[1][]{
    listing engine=minted,
    minted language=javascript,
    colback=yellow!5,
    colframe=yellow!75!black,
    listing only,
    left=5mm,
    enhanced,
    #1
}

\newtcblisting{jscodeNN}[1][]{
    listing engine=minted,
    minted language=javascript,
    minted options={linenos=false},
    colback=yellow!5,
    colframe=yellow!75!black,
    listing only,
    enhanced,
    #1
}

\newtcblisting{cppcode}[1][]{
    listing engine=minted,
    minted language=cpp,
    colback=blue!5,
    colframe=blue!75!black,
    listing only,
    left=5mm,
    enhanced,
    #1
}
""",
        "image": r"""
% Imágenes
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{wrapfig}
\usepackage{float}

% Imagen placeholder
\newcommand{\placeholderimage}[2][]{%
    \begin{tikzpicture}
        \draw[fill=gray!20, draw=gray!50, thick] (0,0) rectangle (#2);
        \node[gray!70] at ({#2/2}, {#2/2*0.6}) {\small Imagen};
    \end{tikzpicture}%
}

% example-image está disponible en mwe package
\usepackage{mwe}
""",
        "bibliography": r"""
% Para simular bibliografía sin biber
\newcommand{\parencite}[2][]{\textup{(#2, 2024)}}
\newcommand{\textcite}[2][]{#2 (2024)}
\newcommand{\cite}[2][]{[#2]}
\newcommand{\citet}[2][]{#2 (2024)}
\newcommand{\citep}[2][]{(#2, 2024)}
\newcommand{\citeauthor}[1]{#1}
\newcommand{\citeyear}[1]{2024}
""",
        "crossref": r"""
% Referencias cruzadas simuladas
\usepackage{hyperref}
\usepackage{booktabs}  % Para tablas con toprule, midrule, bottomrule
\usepackage{float}     % Para [H] float placement
\newcounter{myfigure}
\newcounter{mytable}
\newcounter{myequation}
\newcommand{\figref}[1]{Figura~\ref{#1}}
\newcommand{\tabref}[1]{Tabla~\ref{#1}}
""",
        "list": r"""
% Listas
\usepackage{enumitem}
""",
        "text": r"""
% Texto
\usepackage{soul}
\usepackage{ulem}
""",
        "box": r"""
% Cajas
\usepackage{tcolorbox}
\tcbuselibrary{skins, breakable}
\usepackage{mdframed}
""",
        "glossary": r"""
% Glosarios (simplificado para preview)
\newcommand{\gls}[1]{\textit{#1}}
\newcommand{\glspl}[1]{\textit{#1}}
\newcommand{\acrshort}[1]{\textsc{#1}}
\newcommand{\acrlong}[1]{\textit{#1}}
\newcommand{\acrfull}[1]{\textit{#1}}
""",
    }

    # Combinar preámbulo
    ext = extensiones.get(tipo, "")
    return base + ext


def generar_preambulo_combinado(tipos: list[str]) -> str:
    """Genera un preámbulo combinando múltiples tipos de contenido."""
    # Evitar duplicados de paquetes usando el preámbulo base + extensiones únicas
    base = r"""
\documentclass[preview, border=10pt, varwidth=15cm]{standalone}

% Codificación y fuentes
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{spanish}

% Matemáticas
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{mathtools}

% Colores
\usepackage{xcolor}

% Hyperref (desactivado para standalone)
\usepackage[draft]{hyperref}
"""
    
    # Agregar extensiones de cada tipo detectado
    extensiones_usadas = set()
    preambulo_extra = ""
    
    for tipo in tipos:
        ext = generar_preambulo(tipo).split("\\usepackage[draft]{hyperref}")[-1]
        if ext and ext not in extensiones_usadas:
            extensiones_usadas.add(ext)
            preambulo_extra += ext
    
    return base + preambulo_extra


def generar_documento(snippet: Snippet) -> str:
    """Genera el documento LaTeX completo para un snippet."""

    # Detectar todos los tipos necesarios y combinar preámbulos
    tipos_necesarios = detectar_tipos_necesarios(snippet.codigo)
    preambulo = generar_preambulo_combinado(tipos_necesarios)

    # Envolver código según tipo
    codigo = snippet.codigo.strip()

    # Si es ecuación y no tiene entorno, añadir uno
    if snippet.tipo == "equation":
        # Verificar si ya tiene un entorno de ecuación
        tiene_entorno = any(
            x in codigo
            for x in [
                "\\begin{equation",
                "\\begin{align",
                "\\[",
                "\\begin{gather",
                "\\begin{multline",
                "\\begin{cases",
                "$",
            ]
        )
        if not tiene_entorno:
            # Envolver en displaymath
            codigo = f"\\[\n{codigo}\n\\]"

    # Para multline, necesitamos estar en modo párrafo
    if "\\begin{multline" in codigo:
        codigo = f"\\noindent\n{codigo}"

    documento = f"""% Generado automáticamente - NO EDITAR
% Origen: {snippet.archivo_origen}:{snippet.linea_inicio}
% Tipo: {snippet.tipo}
% Hash: {snippet.hash}

{preambulo}

\\begin{{document}}
{codigo}
\\end{{document}}
"""
    return documento


# =============================================================================
# EXTRACCIÓN DE SNIPPETS
# =============================================================================


def detectar_tipo(codigo: str) -> str:
    """Detecta el tipo de contenido LaTeX."""
    for tipo, patrones in PATRONES_TIPO.items():
        for patron in patrones:
            if re.search(patron, codigo, re.IGNORECASE):
                return tipo
    return "generic"


def detectar_tipos_necesarios(codigo: str) -> list[str]:
    """Detecta TODOS los tipos de contenido necesarios para un snippet."""
    tipos_encontrados = []
    for tipo, patrones in PATRONES_TIPO.items():
        for patron in patrones:
            if re.search(patron, codigo, re.IGNORECASE):
                if tipo not in tipos_encontrados:
                    tipos_encontrados.append(tipo)
                break  # Solo necesitamos un match por tipo
    return tipos_encontrados if tipos_encontrados else ["generic"]


def extraer_snippets(archivo: Path) -> list[Snippet]:
    """Extrae snippets LaTeX MARCADOS con <!-- preview --> de un archivo Markdown.
    
    Solo se extraen snippets que tengan el marcador preview.
    Formato del marcador:
        ```latex <!-- preview -->           - 1 pasada
        ```latex <!-- preview:2 -->         - 2 pasadas
        ```latex <!-- preview: nombre -->   - nombre personalizado
        ```latex <!-- preview:2 nombre -->  - 2 pasadas + nombre
    """

    snippets = []
    contenido = archivo.read_text(encoding="utf-8")
    lineas = contenido.split("\n")

    # Patrón para bloques de código LaTeX con marcador preview
    # Captura: ```latex <!-- preview[:N] [nombre] -->
    patron_inicio = re.compile(
        r"^```latex\s*<!--\s*preview(?::(\d))?\s*(\S+)?\s*-->",
        re.IGNORECASE
    )
    patron_fin = re.compile(r"^```\s*$")

    numero = 0
    i = 0
    while i < len(lineas):
        match_inicio = patron_inicio.match(lineas[i])
        if match_inicio:
            # Extraer número de pasadas y nombre personalizado
            pasadas_str = match_inicio.group(1)
            nombre_custom = match_inicio.group(2)
            pasadas = int(pasadas_str) if pasadas_str else 1
            
            linea_inicio = i + 1

            # Buscar fin del bloque
            codigo_lineas = []
            i += 1
            while i < len(lineas) and not patron_fin.match(lineas[i]):
                codigo_lineas.append(lineas[i])
                i += 1

            linea_fin = i
            codigo = "\n".join(codigo_lineas)
            numero += 1

            # Detectar tipo
            tipo = detectar_tipo(codigo)

            snippet = Snippet(
                archivo_origen=archivo.name,
                numero=numero,
                codigo=codigo,
                linea_inicio=linea_inicio,
                linea_fin=linea_fin,
                tipo=tipo,
                nombre_custom=nombre_custom,
                pasadas=pasadas,
            )

            if codigo.strip():
                snippets.append(snippet)

        i += 1

    return snippets


# =============================================================================
# COMPILACIÓN
# =============================================================================


def compilar_snippet(snippet: Snippet, verbose: bool = False) -> bool:
    """Compila un snippet a PDF."""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Crear archivo .tex
        tex_file = tmpdir / "snippet.tex"
        documento = generar_documento(snippet)
        tex_file.write_text(documento, encoding="utf-8")

        # Compilar
        cmd = [LATEX_ENGINE] + LATEX_ARGS + [tex_file.name]

        try:
            # Compilar el número de pasadas requerido
            for pasada in range(snippet.pasadas):
                result = subprocess.run(
                    cmd,
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result.returncode != 0:
                    if verbose:
                        print(f"    Error de compilación (pasada {pasada + 1}):")
                        # Mostrar últimas líneas relevantes del log
                        for line in result.stdout.split("\n")[-20:]:
                            if line.strip() and ("!" in line or "Error" in line):
                                print(f"      {line}")
                    return False

            # Copiar PDF a destino
            pdf_generado = tmpdir / "snippet.pdf"
            if pdf_generado.exists():
                ASSETS_DIR.mkdir(parents=True, exist_ok=True)
                shutil.copy(pdf_generado, snippet.pdf_path)
                return True
            else:
                if verbose:
                    print(f"    PDF no generado")
                return False

        except subprocess.TimeoutExpired:
            if verbose:
                print(f"    Timeout de compilación")
            return False
        except Exception as e:
            if verbose:
                print(f"    Error: {e}")
            return False


def _compilar_snippet_worker(args: tuple) -> dict:
    """
    Worker para compilar un snippet en paralelo.
    
    Args:
        args: Tupla con (snippet_dict, generar_imagen)
    
    Returns:
        Dict con resultado: {nombre, exito, nuevo, tipo, archivo_origen, ...}
    """
    snippet_dict, generar_imagen = args
    
    # Reconstruir objeto Snippet
    snippet = Snippet(
        archivo_origen=snippet_dict["archivo_origen"],
        numero=snippet_dict["numero"],
        codigo=snippet_dict["codigo"],
        linea_inicio=snippet_dict["linea_inicio"],
        linea_fin=snippet_dict["linea_fin"],
        tipo=snippet_dict["tipo"],
        nombre_custom=snippet_dict.get("nombre_custom"),
        pasadas=snippet_dict.get("pasadas", 1),
    )
    
    resultado = {
        "nombre": snippet.nombre_base,
        "tipo": snippet.tipo,
        "archivo_origen": snippet.archivo_origen,
        "hash": snippet.hash,
        "pasadas": snippet.pasadas,
        "exito": False,
        "imagen_ok": False,
        "error": None,
    }
    
    try:
        # Compilar
        exito = compilar_snippet(snippet, verbose=False)
        resultado["exito"] = exito
        
        if exito and generar_imagen:
            imagen_ok = convertir_a_imagen(snippet)
            resultado["imagen_ok"] = imagen_ok
            
    except Exception as e:
        resultado["error"] = str(e)
    
    return resultado


def convertir_a_imagen(snippet: Snippet, densidad: int = 300, formato: str = "webp") -> bool:
    """
    Convierte un PDF a imagen usando pdftoppm o ImageMagick.
    
    Args:
        snippet: Snippet con las rutas de archivos
        densidad: DPI para la conversión (default: 300 para alta calidad)
        formato: Formato de salida: 'webp', 'png' (default: 'webp')
    
    Returns:
        True si la conversión fue exitosa
    """
    if not snippet.pdf_path.exists():
        return False
    
    # Determinar la ruta de salida según el formato
    if formato == "webp":
        output_path = snippet.png_path.with_suffix(".webp")
    else:
        output_path = snippet.png_path
    
    # Para WebP necesitamos primero generar PNG y luego convertir
    if formato == "webp":
        # Primero generar PNG temporal de alta calidad
        png_temp = snippet.png_path
        png_ok = _convertir_pdf_a_png(snippet.pdf_path, png_temp, densidad)
        
        if png_ok and png_temp.exists():
            # Convertir PNG a WebP con cwebp o ImageMagick
            webp_ok = _convertir_png_a_webp(png_temp, output_path)
            
            # Eliminar PNG temporal si WebP se creó correctamente
            if webp_ok and output_path.exists():
                try:
                    png_temp.unlink()
                except Exception:
                    pass
                return True
            else:
                # Si falló WebP, mantener PNG
                return png_ok
        return png_ok
    else:
        # Generar PNG directamente
        return _convertir_pdf_a_png(snippet.pdf_path, output_path, densidad)


def _convertir_pdf_a_png(pdf_path: Path, png_path: Path, densidad: int) -> bool:
    """Convierte PDF a PNG usando pdftoppm o ImageMagick."""
    
    # Intentar con pdftoppm (poppler-utils) - mejor calidad
    if shutil.which("pdftoppm"):
        try:
            result = subprocess.run(
                [
                    "pdftoppm",
                    "-png",
                    "-r",
                    str(densidad),
                    "-singlefile",
                    str(pdf_path),
                    str(png_path.with_suffix("")),
                ],
                capture_output=True,
            )
            return result.returncode == 0 and png_path.exists()
        except Exception:
            pass

    # Intentar con ImageMagick (convert)
    if shutil.which("convert"):
        try:
            result = subprocess.run(
                [
                    "convert",
                    "-density",
                    str(densidad),
                    str(pdf_path),
                    "-quality",
                    "95",
                    str(png_path),
                ],
                capture_output=True,
            )
            return result.returncode == 0 and png_path.exists()
        except Exception:
            pass

    return False


def _convertir_png_a_webp(png_path: Path, webp_path: Path, calidad: int = 90) -> bool:
    """Convierte PNG a WebP usando cwebp o ImageMagick."""
    
    # Intentar con cwebp (libwebp) - mejor compresión
    if shutil.which("cwebp"):
        try:
            result = subprocess.run(
                [
                    "cwebp",
                    "-q", str(calidad),
                    "-lossless",  # Sin pérdida para texto y gráficos
                    str(png_path),
                    "-o", str(webp_path),
                ],
                capture_output=True,
            )
            return result.returncode == 0 and webp_path.exists()
        except Exception:
            pass
    
    # Intentar con ImageMagick
    if shutil.which("convert"):
        try:
            result = subprocess.run(
                [
                    "convert",
                    str(png_path),
                    "-quality", str(calidad),
                    str(webp_path),
                ],
                capture_output=True,
            )
            return result.returncode == 0 and webp_path.exists()
        except Exception:
            pass
    
    return False


# Alias para compatibilidad
def convertir_a_png(snippet: Snippet, densidad: int = 300) -> bool:
    """Alias para compatibilidad - usa el nuevo sistema con WebP."""
    return convertir_a_imagen(snippet, densidad, formato="webp")


# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================


def procesar_archivos(
    archivos: list[Path],
    forzar: bool = False,
    generar_png: bool = False,
    verbose: bool = True,
) -> dict:
    """Procesa una lista de archivos Markdown con compilación paralela."""

    manifest = Manifest()
    manifest.cargar()

    estadisticas = {
        "total": 0,
        "nuevos": 0,
        "actualizados": 0,
        "sin_cambios": 0,
        "errores": 0,
        "excluidos": 0,
    }

    # Recopilar todos los snippets que necesitan procesarse
    snippets_a_procesar = []
    snippets_sin_cambios = []
    
    for archivo in archivos:
        if not archivo.exists():
            print(f"⚠️  Archivo no encontrado: {archivo}")
            continue

        snippets = extraer_snippets(archivo)
        
        for snippet in snippets:
            estadisticas["total"] += 1
            
            # Verificar si necesita regenerarse
            necesita = forzar or manifest.necesita_regenerar(snippet)
            
            if not necesita:
                estadisticas["sin_cambios"] += 1
                snippets_sin_cambios.append(snippet.nombre_base)
            else:
                # Preparar para procesamiento paralelo
                snippet_dict = {
                    "archivo_origen": snippet.archivo_origen,
                    "numero": snippet.numero,
                    "codigo": snippet.codigo,
                    "linea_inicio": snippet.linea_inicio,
                    "linea_fin": snippet.linea_fin,
                    "tipo": snippet.tipo,
                    "nombre_custom": snippet.nombre_custom,
                    "pasadas": snippet.pasadas,
                    "hash": snippet.hash,
                    "es_nuevo": snippet.nombre_base not in manifest.snippets,
                }
                snippets_a_procesar.append(snippet_dict)
    
    # Mostrar snippets sin cambios
    if verbose and snippets_sin_cambios:
        print(f"\n⏭️  {len(snippets_sin_cambios)} snippets sin cambios (usar --forzar para regenerar)")
    
    # Procesar en paralelo si hay snippets que compilar
    if snippets_a_procesar:
        num_workers = min(cpu_count(), 8, len(snippets_a_procesar))
        
        if verbose:
            print(f"\n🔨 Compilando {len(snippets_a_procesar)} snippets con {num_workers} procesos paralelos...")
        
        # Preparar tareas
        tareas = [(s, generar_png) for s in snippets_a_procesar]
        
        completados = 0
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futuros = {executor.submit(_compilar_snippet_worker, tarea): tarea for tarea in tareas}
            
            for futuro in as_completed(futuros):
                completados += 1
                try:
                    resultado = futuro.result()
                    nombre = resultado["nombre"]
                    exito = resultado["exito"]
                    
                    # Encontrar el snippet_dict original
                    snippet_dict = futuros[futuro][0]
                    es_nuevo = snippet_dict["es_nuevo"]
                    
                    if exito:
                        if es_nuevo:
                            estadisticas["nuevos"] += 1
                        else:
                            estadisticas["actualizados"] += 1
                        
                        status = "✅"
                        img_info = " 📸" if resultado.get("imagen_ok") else ""
                    else:
                        estadisticas["errores"] += 1
                        status = "❌"
                        img_info = ""
                    
                    if verbose:
                        print(f"   [{completados}/{len(snippets_a_procesar)}] {nombre} [{resultado['tipo']}] {status}{img_info}")
                    
                    # Registrar en manifest
                    manifest.snippets[nombre] = {
                        "hash": resultado["hash"],
                        "archivo_origen": resultado["archivo_origen"],
                        "tipo": resultado["tipo"],
                        "generado": datetime.now().isoformat(),
                        "exito": exito,
                        "pasadas": resultado["pasadas"],
                    }
                    
                except Exception as e:
                    estadisticas["errores"] += 1
                    if verbose:
                        print(f"   [{completados}/{len(snippets_a_procesar)}] Error: {e}")

    manifest.guardar()
    return estadisticas


def listar_snippets(archivos: list[Path]):
    """Lista todos los snippets sin generar."""

    print("\n📋 Snippets LaTeX en documentación:\n")

    total = 0
    for archivo in archivos:
        if not archivo.exists():
            continue

        snippets = extraer_snippets(archivo)
        if not snippets:
            continue

        print(f"📄 {archivo.name}:")
        for s in snippets:
            estado = "📸" if s.pdf_path.exists() else "⬜"
            pasadas_info = f"x{s.pasadas}" if s.pasadas > 1 else ""
            nombre_info = f" → {s.nombre_custom}" if s.nombre_custom else ""
            print(f"   {estado} #{s.numero:03d} [{s.tipo:10}] L{s.linea_inicio}-{s.linea_fin} {pasadas_info}{nombre_info}")
            total += 1
        print()

    print(f"Total: {total} snippets marcados con <!-- preview -->")
    if total == 0:
        print("\n💡 Tip: Marca los snippets que quieres renderizar con:")
        print("   ```latex <!-- preview -->")
        print("   ```latex <!-- preview:2 -->  (para refs cruzadas)")
        print("   ```latex <!-- preview nombre_custom -->")


def listar_todos_snippets(archivos: list[Path]):
    """Lista TODOS los bloques latex, marcados o no, para ayudar a decidir cuáles marcar."""
    
    print("\n📋 TODOS los bloques ```latex en documentación:\n")
    
    total = 0
    marcados = 0
    
    for archivo in archivos:
        if not archivo.exists():
            continue
        
        contenido = archivo.read_text(encoding="utf-8")
        lineas = contenido.split("\n")
        
        patron_latex = re.compile(r"^```latex\s*(<!--\s*preview.*-->)?", re.IGNORECASE)
        patron_fin = re.compile(r"^```\s*$")
        
        bloques = []
        i = 0
        while i < len(lineas):
            match = patron_latex.match(lineas[i])
            if match:
                tiene_preview = bool(match.group(1))
                linea_inicio = i + 1
                
                # Buscar fin y extraer preview del código
                codigo_preview = []
                i += 1
                while i < len(lineas) and not patron_fin.match(lineas[i]):
                    codigo_preview.append(lineas[i])
                    i += 1
                
                # Mostrar las primeras líneas del código como preview
                preview = " ".join(codigo_preview[:2])[:60] + "..." if codigo_preview else ""
                
                bloques.append({
                    "linea": linea_inicio,
                    "marcado": tiene_preview,
                    "preview": preview.replace("\n", " "),
                })
                total += 1
                if tiene_preview:
                    marcados += 1
            i += 1
        
        if bloques:
            print(f"📄 {archivo.name}:")
            for b in bloques:
                estado = "✅" if b["marcado"] else "⬜"
                print(f"   {estado} L{b['linea']:4d}: {b['preview']}")
            print()
    
    print(f"Total: {total} bloques latex ({marcados} marcados, {total - marcados} sin marcar)")


def limpiar_huerfanos(verbose: bool = True):
    """Elimina archivos de preview que ya no corresponden a ningún snippet."""

    if not ASSETS_DIR.exists():
        print("No hay directorio de previews")
        return

    manifest = Manifest()
    manifest.cargar()

    archivos_validos = set(manifest.snippets.keys())
    eliminados = 0

    for archivo in ASSETS_DIR.glob("*.pdf"):
        nombre = archivo.stem
        if nombre not in archivos_validos:
            archivo.unlink()
            png = archivo.with_suffix(".png")
            if png.exists():
                png.unlink()
            eliminados += 1
            if verbose:
                print(f"   🗑️  Eliminado: {nombre}")

    if verbose:
        print(f"\nEliminados: {eliminados} archivos huérfanos")


def main():
    parser = argparse.ArgumentParser(
        description="Genera previsualizaciones PDF/PNG para snippets LaTeX en documentación."
    )

    parser.add_argument(
        "--archivo",
        "-a",
        type=str,
        help="Procesar solo un archivo específico",
    )
    parser.add_argument(
        "--forzar",
        "-f",
        action="store_true",
        help="Forzar regeneración de todos los snippets",
    )
    parser.add_argument(
        "--png",
        "-p",
        action="store_true",
        help="Generar también imágenes PNG",
    )
    parser.add_argument(
        "--listar",
        "-l",
        action="store_true",
        help="Solo listar snippets marcados para preview",
    )
    parser.add_argument(
        "--listar-todos",
        "-L",
        action="store_true",
        help="Listar TODOS los bloques latex (marcados y sin marcar)",
    )
    parser.add_argument(
        "--limpiar",
        "-c",
        action="store_true",
        help="Limpiar archivos huérfanos",
    )
    parser.add_argument(
        "--silencioso",
        "-s",
        action="store_true",
        help="Modo silencioso (menos output)",
    )

    args = parser.parse_args()

    # Verificar que estamos en el directorio correcto
    if not DOCS_DIR.exists():
        print(f"❌ Error: No se encuentra el directorio docs/")
        print(f"   Ejecutar desde la raíz del proyecto")
        sys.exit(1)

    # Verificar LuaLaTeX disponible
    if not shutil.which(LATEX_ENGINE):
        print(f"❌ Error: {LATEX_ENGINE} no encontrado")
        print(f"   Instalar TeX Live o similar")
        sys.exit(1)

    # Determinar archivos a procesar
    if args.archivo:
        archivos = [Path(args.archivo)]
    else:
        archivos = sorted(DOCS_DIR.glob("*.md"))

    verbose = not args.silencioso

    if verbose:
        print("=" * 60)
        print("🔧 Generador de Previsualizaciones LaTeX")
        print("=" * 60)

    if args.listar:
        listar_snippets(archivos)
        return

    if args.listar_todos:
        listar_todos_snippets(archivos)
        return

    if args.limpiar:
        limpiar_huerfanos(verbose)
        return

    # Procesar
    stats = procesar_archivos(
        archivos,
        forzar=args.forzar,
        generar_png=args.png,
        verbose=verbose,
    )

    # Resumen
    if verbose:
        print("\n" + "=" * 60)
        print("📊 Resumen:")
        print(f"   Total procesados: {stats['total']}")
        print(f"   ✅ Nuevos:        {stats['nuevos']}")
        print(f"   🔄 Actualizados:  {stats['actualizados']}")
        print(f"   ⏭️  Sin cambios:   {stats['sin_cambios']}")
        print(f"   ❌ Errores:       {stats['errores']}")
        print("=" * 60)

        if stats["errores"] > 0:
            print("\n⚠️  Algunos snippets no compilaron.")
            print("   Esto puede ser normal si usan comandos personalizados de la plantilla.")


if __name__ == "__main__":
    main()
