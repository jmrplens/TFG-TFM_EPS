#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
actualizar_previews.py
--------------------------------------------------------------------------------
Herramienta unificada para generar e insertar previews de documentación LaTeX.

Proyecto: Plantilla TFG/TFM EPS Universidad de Alicante
Autor:    José Manuel Requena Plens
Enlace:   https://github.com/jmrplens/TFG-TFM_EPS
Licencia: GNU GPL v3.0
Versión:  2.1.0
--------------------------------------------------------------------------------

Este script:
1. Busca snippets LaTeX MARCADOS con <!-- preview --> en docs/*.md
2. Genera documentos standalone usando los paquetes EPS de la plantilla
3. Compila a PDF y convierte a WebP/PNG
4. Inserta los enlaces de preview en los archivos Markdown

Marcadores soportados:
    ```latex <!-- preview -->           - Renderizar con 1 pasada
    ```latex <!-- preview:2 -->         - Renderizar con 2 pasadas (refs cruzadas)
    ```latex <!-- preview:3 -->         - Renderizar con 3 pasadas
    ```latex <!-- preview: mi_nombre --> - Nombre personalizado

Uso:
    python3 actualizar_previews.py                 # Generar e insertar todo
    python3 actualizar_previews.py --listar        # Solo listar snippets marcados
    python3 actualizar_previews.py --forzar        # Regenerar todos
    python3 actualizar_previews.py --limpiar       # Eliminar previews huérfanos

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
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path
from typing import Optional

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

PROYECTO_ROOT = Path(__file__).parent.parent.resolve()
DOCS_DIR = PROYECTO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets" / "previews"
MANIFEST_FILE = ASSETS_DIR / "manifest.json"
ASSETS_REL = "assets/previews"

# Compilación
LATEX_ENGINE = "lualatex"
LATEX_ARGS = ["-shell-escape", "-interaction=nonstopmode", "-halt-on-error"]
MAX_WORKERS = min(cpu_count(), 8)

# Configurable: Resolución y calidad
DPI = 150
WEBP_QUALITY = 90


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
    nombre_custom: Optional[str] = None
    pasadas: int = 1
    hash: str = field(default="", init=False)

    def __post_init__(self):
        self.hash = hashlib.md5(self.codigo.encode()).hexdigest()[:12]

    @property
    def nombre_base(self) -> str:
        if self.nombre_custom:
            return self.nombre_custom
        archivo_sin_ext = Path(self.archivo_origen).stem.upper()
        return f"{archivo_sin_ext}_{self.numero:03d}"

    @property
    def pdf_path(self) -> Path:
        return ASSETS_DIR / f"{self.nombre_base}.pdf"

    @property
    def webp_path(self) -> Path:
        return ASSETS_DIR / f"{self.nombre_base}.webp"

    @property
    def png_path(self) -> Path:
        return ASSETS_DIR / f"{self.nombre_base}.png"


@dataclass
class Manifest:
    """Manifiesto de snippets generados para tracking de cambios."""
    snippets: dict = field(default_factory=dict)
    ultima_actualizacion: str = ""

    def cargar(self):
        if MANIFEST_FILE.exists():
            try:
                with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.snippets = data.get("snippets", {})
                    self.ultima_actualizacion = data.get("ultima_actualizacion", "")
            except (json.JSONDecodeError, KeyError):
                pass

    def guardar(self):
        self.ultima_actualizacion = datetime.now().isoformat()
        MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "snippets": self.snippets,
                "ultima_actualizacion": self.ultima_actualizacion,
            }, f, indent=2, ensure_ascii=False)

    def necesita_regenerar(self, snippet: Snippet) -> bool:
        key = snippet.nombre_base
        if key not in self.snippets:
            return True
        if self.snippets[key].get("hash") != snippet.hash:
            return True
        if not snippet.pdf_path.exists():
            return True
        return False

    def registrar(self, snippet: Snippet, exito: bool):
        self.snippets[snippet.nombre_base] = {
            "hash": snippet.hash,
            "archivo_origen": snippet.archivo_origen,
            "linea": snippet.linea_inicio,
            "generado": datetime.now().isoformat(),
            "exito": exito,
            "pasadas": snippet.pasadas,
        }


# =============================================================================
# PREÁMBULO LATEX - USA LOS PAQUETES EPS DE LA PLANTILLA
# =============================================================================

def generar_preambulo() -> str:
    """
    Genera el preámbulo LaTeX usando los paquetes de la plantilla EPS.
    
    Importa los paquetes del proyecto para que las previsualizaciones
    correspondan exactamente a lo que se verá en el documento final.
    """
    return r"""% =============================================================================
% PREÁMBULO GENERADO AUTOMÁTICAMENTE - USA PAQUETES EPS
% =============================================================================
\documentclass[preview, border=10pt, varwidth=21cm]{standalone}

% ============================================================================
% PAQUETES FUNDAMENTALES (de eps-tfg.cls)
% ============================================================================

% Idioma (polyglossia para LuaLaTeX)
\usepackage{polyglossia}
\setdefaultlanguage{spanish}
\setotherlanguage{english}

% Fuentes (fontspec para LuaLaTeX)
\usepackage{fontspec}

% Colores extendidos
\usepackage[dvipsnames,svgnames,x11names]{xcolor}

% ============================================================================
% COLORES (definidos en eps-tfg.cls)
% ============================================================================
% Colores básicos
\definecolor{gray97}{gray}{.97}
\definecolor{gray75}{gray}{.75}
\definecolor{gray45}{gray}{.45}
\definecolor{gray30}{gray}{.30}
\definecolor{negro}{RGB}{0,0,0}
\definecolor{blanco}{RGB}{255,255,255}

% Colores de grados
\definecolor{teleco}{RGB}{32,2,116}
\definecolor{civil}{RGB}{201,56,140}
\definecolor{quimica}{RGB}{41,199,255}
\definecolor{informatica}{RGB}{0,128,255}
\definecolor{multimedia}{RGB}{239,206,53}
\definecolor{arquitecnica}{RGB}{0,179,148}
\definecolor{arquitectura}{RGB}{181,0,0}
\definecolor{robotica}{RGB}{255,255,128}

% Colores de másteres
\definecolor{masterteleco}{RGB}{32,2,116}
\definecolor{caminos}{RGB}{201,56,140}
\definecolor{gestedif}{RGB}{50,120,50}
\definecolor{desweb}{RGB}{250,43,22}
\definecolor{mataguaterre}{RGB}{210,250,50}
\definecolor{masterinfor}{RGB}{0,128,255}
\definecolor{autorobo}{RGB}{83,145,201}
\definecolor{prevencion}{RGB}{0,100,0}
\definecolor{gestionagua}{RGB}{7,138,197}
\definecolor{moviles}{RGB}{121,11,21}
\definecolor{masterquimica}{RGB}{41,199,255}
\definecolor{ciberseguridad}{RGB}{9,111,192}
\definecolor{geologica}{RGB}{245,125,0}

% Colores para código
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{codeblue}{rgb}{0.13,0.13,1}
\definecolor{codered}{rgb}{0.6,0,0}
\definecolor{codeorange}{rgb}{0.9,0.4,0}
\definecolor{backcolour}{rgb}{0.97,0.97,0.97}

% ============================================================================
% GRÁFICOS Y FIGURAS (de eps-tfg.cls)
% ============================================================================
\usepackage{graphicx}
\usepackage{tikz}
\usetikzlibrary{
  tikzmark, calc, shapes.geometric, arrows, backgrounds, shadings,
  shapes.arrows, shapes.symbols, shadows, positioning, fit, automata,
  patterns, intersections, arrows.meta, shapes, shapes.misc, 
  shapes.multipart, patterns.meta, decorations, decorations.pathreplacing,
  decorations.pathmorphing, decorations.markings, shadows.blur,
  matrix, chains, scopes, fadings, er
}

\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\pgfplotsset{colormap/viridis}
\usepgfplotslibrary{patchplots,groupplots,fillbetween,polar,statistics}
\usepackage{pgfplotstable}
\usepackage{pgf-pie}

% ============================================================================
% TABLAS (de eps-tfg.cls)
% ============================================================================
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{multicol}
\usepackage{tabularx}
\usepackage{colortbl}
\usepackage{ragged2e}
\usepackage{threeparttable}
\usepackage{diagbox}
\usepackage{makecell}

% Tipos de columna personalizados (de eps-tfg.cls)
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{Y}{>{\centering\arraybackslash}X}
\newcolumntype{Z}{>{\raggedright\arraybackslash}X}

% ============================================================================
% FIGURAS Y CAPTIONS (de eps-tfg.cls)
% ============================================================================
\usepackage{subcaption}
\usepackage{caption}
\captionsetup{labelfont={bf,small},textfont=small,justification=centering}
\usepackage{setspace}
\usepackage{float}
\usepackage{rotating}
\usepackage{wrapfig}

% Para imágenes de ejemplo
\usepackage{mwe}

% ============================================================================
% TEXTO Y POSICIONAMIENTO (de eps-tfg.cls)
% ============================================================================
\usepackage{anyfontsize}
\usepackage{mdframed}

% ============================================================================
% MATEMÁTICAS (de eps-tfg.cls)
% ============================================================================
\usepackage{mathtools}
\usepackage{amsthm}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{bm}
\usepackage{mathrsfs}
\usepackage{nicefrac}
\usepackage{cancel}

% Entorno condiciones (de eps-tfg.cls)
\newenvironment{condiciones}[1][donde:]
  {#1\tabularx{\textwidth-\widthof{#1}}[t]{>{$}l<{$} @{}>{${}}c<{{}$}@{} >{\raggedright\arraybackslash}X}}
  {\endtabularx\\[\belowdisplayskip]}

% ============================================================================
% TEOREMAS (de eps-tfg.cls)
% ============================================================================
\newtheorem{teorema}{Teorema}
\newtheorem{theorem}{Theorem}
\newtheorem{ejemplo}{Ejemplo}
\newtheorem{definicion}{Definición}
\newtheorem{definition}{Definition}
\newtheorem{lema}{Lema}
\newtheorem{corolario}{Corolario}
\newtheorem{proposicion}{Proposición}

% ============================================================================
% CÓDIGO FUENTE (cargar eps-codigo.sty)
% ============================================================================
\usepackage{tcolorbox}
\tcbuselibrary{minted,skins,breakable,theorems,hooks,fitting,listings}
\usepackage{minted}
\usepackage{fontawesome5}
\usepackage{listings}

% Cargar estilos de código del proyecto
\usepackage{eps-codigo}

% ============================================================================
% UTILIDADES ADICIONALES
% ============================================================================
\usepackage{xparse}
\usepackage{etoolbox}
\usepackage{xstring}
\usepackage{calc}
\usepackage{ifthen}
\usepackage{enumitem}
\usepackage{siunitx}
\sisetup{output-decimal-marker={,}, group-separator={.}, group-minimum-digits=4}
\usepackage{eurosym}
\usepackage{forest}
\usepackage{varwidth}
\usepackage{pgfgantt}

% Química
\usepackage{mhchem}
\usepackage{chemfig}
\usepackage{chemmacros}
\chemsetup{modules=all}

% Circuitos
\usepackage{circuitikz}

% Hyperref desactivado para standalone
\usepackage[draft]{hyperref}

% ============================================================================
% CARGAR COMPONENTES EPS (todos)
% ============================================================================
\usepackage[all]{eps-componentes}

% ============================================================================
% STUBS PARA BIBLIOGRAFÍA (biblatex no funciona bien en standalone)
% ============================================================================
\providecommand{\parencite}[2][]{(Autor, 2024)}
\providecommand{\textcite}[2][]{Autor (2024)}
\providecommand{\cite}[2][]{[1]}
\providecommand{\autocite}[2][]{(Autor, 2024)}
\providecommand{\citeauthor}[1]{Autor}
\providecommand{\citeyear}[1]{2024}
\providecommand{\citetitle}[1]{\textit{Título}}
\providecommand{\fullcite}[1]{Autor. \textit{Título}. Editorial, 2024.}
\providecommand{\printbibliography}[1][]{\textit{[Bibliografía generada automáticamente]}}

% ============================================================================
% STUBS PARA GLOSARIO (glossaries no funciona en standalone)
% ============================================================================
\providecommand{\gls}[1]{\textit{#1}}
\providecommand{\glspl}[1]{\textit{#1}}
\providecommand{\Gls}[1]{\textit{#1}}
\providecommand{\Glspl}[1]{\textit{#1}}
\providecommand{\acrshort}[1]{\textsc{#1}}
\providecommand{\acrlong}[1]{\textit{#1}}
\providecommand{\acrfull}[1]{\textit{#1}}
\providecommand{\glsentryshort}[1]{#1}
\providecommand{\glsentrylong}[1]{#1}
"""


def generar_documento(snippet: Snippet) -> str:
    """Genera el documento LaTeX completo para un snippet."""
    preambulo = generar_preambulo()
    codigo = snippet.codigo.strip()

    return f"""% Generado automáticamente - NO EDITAR
% Origen: {snippet.archivo_origen}:{snippet.linea_inicio}
% Hash: {snippet.hash}

{preambulo}

\\begin{{document}}
\\begin{{minipage}}{{21cm}}
{codigo}
\\end{{minipage}}
\\end{{document}}
"""


# =============================================================================
# EXTRACCIÓN DE SNIPPETS
# =============================================================================

def extraer_snippets(archivo: Path) -> list[Snippet]:
    """Extrae snippets LaTeX MARCADOS con <!-- preview --> de un archivo Markdown."""
    snippets = []
    contenido = archivo.read_text(encoding="utf-8")
    lineas = contenido.split("\n")

    # Patrón: ```latex <!-- preview[:N] [nombre] -->
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

            snippet = Snippet(
                archivo_origen=str(archivo.relative_to(PROYECTO_ROOT)),
                numero=numero,
                codigo=codigo,
                linea_inicio=linea_inicio,
                linea_fin=linea_fin,
                nombre_custom=nombre_custom,
                pasadas=pasadas,
            )
            snippets.append(snippet)
        i += 1

    return snippets


def obtener_todos_snippets() -> list[Snippet]:
    """Obtiene todos los snippets marcados de todos los archivos .md en docs/."""
    todos = []
    if DOCS_DIR.exists():
        for md_file in sorted(DOCS_DIR.glob("*.md")):
            snippets = extraer_snippets(md_file)
            todos.extend(snippets)
    return todos


# =============================================================================
# COMPILACIÓN
# =============================================================================

def _limpiar_temporales(nombre: str) -> None:
    """Limpia archivos temporales de compilación."""
    for ext in [".tex", ".pdf", ".png", ".log", ".aux", ".out"]:
        tmp = PROYECTO_ROOT / f"_temp_{nombre}{ext}"
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass  # Ignorar errores al limpiar temporales


def _ejecutar_latex(tex_file: Path, pasadas: int) -> subprocess.CompletedProcess | None:
    """Ejecuta LaTeX las pasadas necesarias. Retorna None si todas exitosas."""
    env = os.environ.copy()
    env["TEXINPUTS"] = f".:{PROYECTO_ROOT}/cls:{PROYECTO_ROOT}/sty:{PROYECTO_ROOT}/sty/componentes:{env.get('TEXINPUTS', '')}"
    cmd = [LATEX_ENGINE] + LATEX_ARGS + [tex_file.name]
    
    for i in range(pasadas):
        result = subprocess.run(
            cmd, cwd=PROYECTO_ROOT, capture_output=True, text=True,
            timeout=120, env=env
        )
        if result.returncode != 0 and i == pasadas - 1:
            return result
    return None


def _convertir_imagenes(pdf_file: Path, snippet: 'Snippet', nombre: str) -> None:
    """Convierte PDF a PNG y WebP."""
    png_temp = PROYECTO_ROOT / f"_temp_{nombre}.png"
    subprocess.run([
        "pdftoppm", "-png", "-r", str(DPI), "-singlefile",
        str(pdf_file), str(PROYECTO_ROOT / f"_temp_{nombre}")
    ], capture_output=True, timeout=60)

    if not png_temp.exists():
        return
        
    final_webp = snippet.webp_path
    subprocess.run([
        "cwebp", "-q", str(WEBP_QUALITY), str(png_temp), "-o", str(final_webp)
    ], capture_output=True, timeout=60)
    
    if not final_webp.exists():
        shutil.copy(png_temp, snippet.png_path)


def _compilar_worker(args: tuple) -> tuple:
    """Worker para compilar un snippet en paralelo."""
    snippet_dict, _ = args  # segundo arg es forzar, no usado aquí
    snippet = Snippet(**{k: v for k, v in snippet_dict.items() if k != 'hash'})
    snippet.hash = snippet_dict.get('hash', '')

    nombre = snippet.nombre_base
    tex_file = PROYECTO_ROOT / f"_temp_{nombre}.tex"
    pdf_file = PROYECTO_ROOT / f"_temp_{nombre}.pdf"

    try:
        tex_file.write_text(generar_documento(snippet), encoding="utf-8")
        
        error_result = _ejecutar_latex(tex_file, snippet.pasadas)
        if error_result:
            msg = error_result.stderr[-500:] if error_result.stderr else "Error desconocido"
            return (nombre, False, msg)

        if not pdf_file.exists():
            return (nombre, False, "PDF no generado")

        ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy(pdf_file, snippet.pdf_path)
        _convertir_imagenes(pdf_file, snippet, nombre)

        return (nombre, True, None)

    except subprocess.TimeoutExpired:
        return (nombre, False, "Timeout")
    except Exception as e:
        return (nombre, False, str(e))
    finally:
        _limpiar_temporales(nombre)


def _serializar_snippet(s: Snippet) -> dict:
    """Serializa un snippet para multiprocessing."""
    return {
        'archivo_origen': s.archivo_origen,
        'numero': s.numero,
        'codigo': s.codigo,
        'linea_inicio': s.linea_inicio,
        'linea_fin': s.linea_fin,
        'nombre_custom': s.nombre_custom,
        'pasadas': s.pasadas,
        'hash': s.hash,
    }


def _procesar_resultado_compilacion(
    nombre: str, exito: bool, error: str | None,
    snippets: list[Snippet], manifest: Manifest
) -> bool:
    """Procesa el resultado de una compilación y actualiza el manifest."""
    status = "✅" if exito else "❌"
    print(f"   {status} {nombre}")
    if error:
        print(f"      Error: {error[:100]}...")

    for s in snippets:
        if s.nombre_base == nombre:
            manifest.registrar(s, exito)
            break
    return exito


def compilar_snippets(snippets: list[Snippet], manifest: Manifest, forzar: bool = False) -> tuple[int, int]:
    """Compila los snippets que necesitan regeneración."""
    a_compilar = [
        (_serializar_snippet(s), forzar)
        for s in snippets
        if forzar or manifest.necesita_regenerar(s)
    ]

    if not a_compilar:
        return (0, 0)

    total = len(a_compilar)
    print(f"   Compilando {total} snippets con {MAX_WORKERS} procesos...")

    exitos = 0
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuros = [executor.submit(_compilar_worker, args) for args in a_compilar]
        for futuro in as_completed(futuros):
            nombre, exito, error = futuro.result()
            if _procesar_resultado_compilacion(nombre, exito, error, snippets, manifest):
                exitos += 1

    return (exitos, total - exitos)


# =============================================================================
# INSERCIÓN DE PREVIEWS EN MARKDOWN
# =============================================================================

def obtener_previews_disponibles() -> dict:
    """Obtiene los previews que tienen archivos generados."""
    disponibles = {}
    if ASSETS_DIR.exists():
        for pdf in ASSETS_DIR.glob("*.pdf"):
            nombre = pdf.stem
            webp = pdf.with_suffix(".webp")
            png = pdf.with_suffix(".png")
            
            if webp.exists():
                img_path = f"{ASSETS_REL}/{nombre}.webp"
            elif png.exists():
                img_path = f"{ASSETS_REL}/{nombre}.png"
            else:
                img_path = None
            
            disponibles[nombre] = {
                "pdf": f"{ASSETS_REL}/{pdf.name}",
                "img": img_path,
            }
    return disponibles


# Patrones compilados para insertar previews
_PATRON_INICIO_MARCADO = re.compile(
    r"^```latex\s*<!--\s*preview(?::\d)?\s*(\S+)?\s*-->",
    re.IGNORECASE
)
_PATRON_FIN = re.compile(r"^```\s*$")
_PATRON_PREVIEW_EXISTENTE = re.compile(
    r"^\*\*Resultado:\*\*|^<img src=|^\[📄",
    re.IGNORECASE
)


def _generar_enlace_preview(info: dict) -> str:
    """Genera el enlace Markdown para un preview."""
    enlace = '\n**Resultado:**\n\n'
    if info["img"]:
        enlace += f'<img src="{info["img"]}" alt="Preview">\n\n'
    enlace += f'[📄 Ver PDF]({info["pdf"]})\n'
    return enlace


def _copiar_bloque_codigo(lineas: list[str], idx: int, nuevas_lineas: list[str]) -> int:
    """Copia el contenido del bloque de código hasta ```. Retorna nuevo índice."""
    idx += 1
    while idx < len(lineas) and not _PATRON_FIN.match(lineas[idx]):
        nuevas_lineas.append(lineas[idx])
        idx += 1
    if idx < len(lineas):
        nuevas_lineas.append(lineas[idx])  # Añadir ```
    return idx


def _saltar_preview_existente(lineas: list[str], idx: int) -> int:
    """Salta líneas de preview existente. Retorna nuevo índice."""
    next_idx = idx + 1
    # Saltar líneas vacías
    while next_idx < len(lineas) and not lineas[next_idx].strip():
        next_idx += 1
    
    # Si no hay preview existente, retornar índice original
    if next_idx >= len(lineas) or not _PATRON_PREVIEW_EXISTENTE.match(lineas[next_idx]):
        return idx
    
    # Consumir líneas del preview existente
    while next_idx < len(lineas):
        line = lineas[next_idx].strip()
        es_linea_preview = (
            not line or 
            line.startswith("**Resultado:**") or
            line.startswith("<img") or 
            line.startswith("[📄")
        )
        if not es_linea_preview:
            break
        next_idx += 1
    
    return next_idx - 1


def insertar_previews_en_archivo(archivo: Path, disponibles: dict) -> int:
    """Inserta enlaces de preview después de cada snippet marcado."""
    contenido = archivo.read_text(encoding="utf-8")
    lineas = contenido.split("\n")
    nuevas_lineas = []
    numero_marcado = 0
    insertados = 0
    i = 0

    while i < len(lineas):
        nuevas_lineas.append(lineas[i])
        match_marcado = _PATRON_INICIO_MARCADO.match(lineas[i])

        if match_marcado:
            numero_marcado += 1
            nombre_custom = match_marcado.group(1)
            nombre_snippet = nombre_custom or f"{archivo.stem.upper()}_{numero_marcado:03d}"

            i = _copiar_bloque_codigo(lineas, i, nuevas_lineas)
            i = _saltar_preview_existente(lineas, i)

            if nombre_snippet in disponibles:
                nuevas_lineas.append(_generar_enlace_preview(disponibles[nombre_snippet]))
                insertados += 1

        i += 1

    nuevo_contenido = "\n".join(nuevas_lineas)
    if nuevo_contenido != contenido:
        archivo.write_text(nuevo_contenido, encoding="utf-8")

    return insertados


def insertar_todos_previews() -> int:
    """Inserta previews en todos los archivos .md de docs/."""
    disponibles = obtener_previews_disponibles()
    total_insertados = 0

    if DOCS_DIR.exists():
        for md_file in sorted(DOCS_DIR.glob("*.md")):
            insertados = insertar_previews_en_archivo(md_file, disponibles)
            if insertados > 0:
                print(f"   📝 {md_file.name}: {insertados} previews")
                total_insertados += insertados

    return total_insertados


# =============================================================================
# LIMPIEZA
# =============================================================================

def limpiar_huerfanos(snippets: list[Snippet]) -> int:
    """Elimina previews que ya no tienen snippet asociado."""
    nombres_validos = {s.nombre_base for s in snippets}
    eliminados = 0

    if ASSETS_DIR.exists():
        for archivo in ASSETS_DIR.iterdir():
            if archivo.suffix in [".pdf", ".png", ".webp"]:
                nombre = archivo.stem
                if nombre not in nombres_validos:
                    archivo.unlink()
                    eliminados += 1
                    print(f"   🗑️  Eliminado: {archivo.name}")

    return eliminados


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Genera e inserta previews de snippets LaTeX en documentación.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s                    Generar e insertar todos los previews
  %(prog)s --listar           Listar snippets marcados sin generar
  %(prog)s --forzar           Regenerar todos (ignorar caché)
  %(prog)s --limpiar          Eliminar previews huérfanos
  %(prog)s --archivo TEXTO    Procesar solo docs/TEXTO.md
        """
    )

    parser.add_argument("--listar", "-l", action="store_true",
                        help="Solo listar snippets marcados")
    parser.add_argument("--forzar", "-f", action="store_true",
                        help="Forzar regeneración de todos los previews")
    parser.add_argument("--limpiar", "-c", action="store_true",
                        help="Limpiar previews huérfanos")
    parser.add_argument("--archivo", "-a", type=str, metavar="NOMBRE",
                        help="Procesar solo un archivo (sin extensión)")
    parser.add_argument("--solo-generar", "-g", action="store_true",
                        help="Solo generar previews (no insertar)")
    parser.add_argument("--solo-insertar", "-i", action="store_true",
                        help="Solo insertar enlaces (no generar)")

    args = parser.parse_args()

    print("=" * 60)
    print("🖼️  Actualización de Previews de Documentación")
    print("=" * 60)

    # Verificar dependencias
    for cmd in ["lualatex", "pdftoppm"]:
        if not shutil.which(cmd):
            print(f"❌ Error: '{cmd}' no encontrado")
            sys.exit(1)

    # Obtener snippets
    if args.archivo:
        archivo = DOCS_DIR / f"{args.archivo}.md"
        if not archivo.exists():
            print(f"❌ Archivo no encontrado: {archivo}")
            sys.exit(1)
        snippets = extraer_snippets(archivo)
        print(f"\n📄 Archivo: {args.archivo}.md")
    else:
        snippets = obtener_todos_snippets()
        print("\n📂 Escaneando docs/*.md")

    print(f"   Snippets marcados: {len(snippets)}")

    # Modo listar
    if args.listar:
        print("\n📋 Snippets marcados con <!-- preview -->:")
        for s in snippets:
            print(f"   • {s.nombre_base} ({s.archivo_origen}:{s.linea_inicio}, {s.pasadas} pasadas)")
        sys.exit(0)

    # Cargar manifest
    manifest = Manifest()
    manifest.cargar()

    # Limpiar huérfanos
    if args.limpiar:
        print("\n🧹 Limpiando previews huérfanos...")
        eliminados = limpiar_huerfanos(snippets)
        print(f"   Eliminados: {eliminados}")

    # Generar previews
    if not args.solo_insertar:
        print("\n🔨 Generando previews...")
        exitos, errores = compilar_snippets(snippets, manifest, args.forzar)
        manifest.guardar()
        print(f"   ✅ Generados: {exitos}")
        if errores:
            print(f"   ❌ Errores: {errores}")

    # Insertar enlaces
    if not args.solo_generar:
        print("\n📝 Insertando enlaces en Markdown...")
        insertados = insertar_todos_previews()
        print(f"   Total insertados: {insertados}")

    print("\n" + "=" * 60)
    print("✅ Proceso completado")
    print("=" * 60)


if __name__ == "__main__":
    main()
