#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_portadas.py
--------------------------------------------------------------------------------
Generador automático de imágenes de portadas para el README.

Proyecto: Plantilla TFG/TFM EPS Universidad de Alicante
Autor:    José Manuel Requena Plens
Enlace:   https://github.com/jmrplens/TFG-TFM_EPS
Licencia: GNU GPL v3.0
Versión:  2.1.0
--------------------------------------------------------------------------------

Este script:
1. Lee las titulaciones disponibles del archivo .cls
2. Genera una portada en color para cada titulación
3. Genera una mini-tabla con color y B/N para la titulación de referencia (teleco)
4. Convierte a WebP y actualiza el README.md

Autor: Plantilla TFG/TFM EPS UA
Licencia: GPL-3.0
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from multiprocessing import cpu_count
from pathlib import Path
from typing import Optional


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

PROYECTO_ROOT = Path(__file__).parent.parent.resolve()
CLS_FILE = PROYECTO_ROOT / "cls" / "eps-tfg.cls"
README_FILE = PROYECTO_ROOT / "README.md"
OUTPUT_DIR = PROYECTO_ROOT / ".github" / "images" / "portadas"

# Titulación de referencia para la comparativa color/BN
TITULACION_REFERENCIA = "teleco"

# Configuración de imágenes
DPI = 300  # Más bajo para thumbnails
WEBP_QUALITY = 90


# =============================================================================
# ESTRUCTURAS DE DATOS
# =============================================================================

@dataclass
class Titulacion:
    """Representa una titulación extraída del .cls"""
    id: str
    nombre: str
    tipo: str  # tfg o tfm
    color: str
    texto: str  # blanco o negro
    logo_portada: str
    logo_normal: str


# =============================================================================
# PARSING DEL .CLS
# =============================================================================

def extraer_titulaciones(cls_path: Path) -> list[Titulacion]:
    """Extrae todas las titulaciones definidas en el archivo .cls"""
    
    contenido = cls_path.read_text(encoding="utf-8")
    
    # Patrón para capturar definiciones de titulación
    # \__eps_define_titulacion:nnnnnnn {id}
    #   {nombre}
    #   {tipo} {color} {texto} {logo-portada} {logo-normal}
    patron = re.compile(
        r'\\__eps_define_titulacion:nnnnnnn\s*\{([^}]+)\}\s*'
        r'\{([^}]+)\}\s*'
        r'\{([^}]+)\}\s*\{([^}]+)\}\s*\{([^}]+)\}\s*\{([^}]+)\}\s*\{([^}]+)\}',
        re.MULTILINE
    )
    
    titulaciones = []
    for match in patron.finditer(contenido):
        t = Titulacion(
            id=match.group(1).strip(),
            nombre=match.group(2).strip().replace("~", " "),
            tipo=match.group(3).strip(),
            color=match.group(4).strip(),
            texto=match.group(5).strip(),
            logo_portada=match.group(6).strip(),
            logo_normal=match.group(7).strip()
        )
        titulaciones.append(t)
    
    return titulaciones


# =============================================================================
# GENERACIÓN DE PORTADAS
# =============================================================================

def generar_documento_portada(titulacion: Titulacion, bn: bool = False) -> str:
    """Genera el documento LaTeX para una portada standalone."""
    
    tipo_portada = "bn" if bn else "color"
    
    return f"""% Generado automáticamente para preview de portada
\\documentclass[class=eps-tfg]{{standalone}}

% Cargar la clase real para usar sus comandos
\\usepackage{{fontspec}}
\\usepackage{{polyglossia}}
\\setmainlanguage{{spanish}}
\\usepackage{{graphicx}}
\\usepackage{{tikz}}
\\usepackage{{xcolor}}

% Configurar la titulación
\\input{{cls/eps-tfg.cls}}

\\EPSsetup{{
    titulo = {{Título del Trabajo de Ejemplo}},
    subtitulo = {{Subtítulo opcional del trabajo}},
    autor = {{Nombre Apellido1 Apellido2}},
    genero = m,
    tutor = {{Dr./Dra. Nombre del Tutor/a}},
    tutor-departamento = {{Departamento Universitario}},
    titulacion = {titulacion.id},
    fecha = {{Febrero 2026}},
}}

\\begin{{document}}
\\portada{tipo_portada}
\\end{{document}}
"""


def generar_documento_portada_simple(titulacion: Titulacion, bn: bool = False) -> str:
    """Genera un documento LaTeX simple que usa la clase directamente."""
    
    # El comando es \portadacolor o \portadabn (sin argumento)
    comando_portada = "\\portadabn" if bn else "\\portadacolor"
    
    return f"""% !TeX program = lualatex
% !TeX encoding = UTF-8
% Generado automáticamente por generar_portadas.py

\\documentclass{{cls/eps-tfg}}
\\usepackage{{sty/eps-portadas}}

\\EPSsetup{{
    titulo = {{Título del Trabajo de Fin de {'Máster' if titulacion.tipo == 'tfm' else 'Grado'}}},
    subtitulo = {{Subtítulo opcional}},
    autor = {{Nombre Apellido1 Apellido2}},
    genero = m,
    tutor = {{Dr. Nombre del Tutor}},
    tutor-departamento = {{Departamento Ejemplo}},
    titulacion = {titulacion.id},
    fecha = {{Febrero 2026}},
}}

\\begin{{document}}
{comando_portada}
\\end{{document}}
"""


def _compilar_portada_worker(args: tuple) -> tuple:
    """Worker para compilar una portada en paralelo.
    
    Args:
        args: Tupla con (titulacion_dict, bn, output_path_str)
    
    Returns:
        Tupla con (titulacion_id, bn, success, info_dict o None)
    """
    titulacion_dict, bn, output_path_str = args
    output_path = Path(output_path_str)
    
    # Reconstruir objeto Titulacion desde dict (necesario para multiprocessing)
    titulacion = Titulacion(**titulacion_dict)
    
    # Usar sufijo único para evitar colisiones entre procesos paralelos
    suffix = f"_{titulacion.id}{'_bn' if bn else '_color'}"
    tex_file = PROYECTO_ROOT / f"_temp_portada{suffix}.tex"
    pdf_file = PROYECTO_ROOT / f"_temp_portada{suffix}.pdf"
    
    try:
        # Crear documento
        documento = generar_documento_portada_simple(titulacion, bn)
        tex_file.write_text(documento, encoding="utf-8")
        
        # Configurar TEXINPUTS
        env = os.environ.copy()
        env["TEXINPUTS"] = f".:{PROYECTO_ROOT}/cls:{PROYECTO_ROOT}/sty:{PROYECTO_ROOT}/recursos:{env.get('TEXINPUTS', '')}"
        
        # Compilar DOS veces (necesario para TikZ overlay)
        cmd = [
            "lualatex",
            "-shell-escape",
            "-interaction=nonstopmode",
            tex_file.name
        ]
        
        for _ in range(2):
            subprocess.run(
                cmd,
                cwd=PROYECTO_ROOT,
                capture_output=True,
                text=True,
                timeout=120,
                env=env
            )
        
        if not pdf_file.exists():
            return (titulacion.id, bn, False, None)
        
        # Convertir PDF a PNG
        png_file = PROYECTO_ROOT / f"_temp_portada{suffix}.png"
        subprocess.run([
            "pdftoppm", "-png", "-r", str(DPI), "-singlefile",
            str(pdf_file), str(PROYECTO_ROOT / f"_temp_portada{suffix}")
        ], capture_output=True, timeout=60)
        
        if not png_file.exists():
            return (titulacion.id, bn, False, None)
        
        # Convertir a WebP
        output_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([
            "cwebp", "-q", str(WEBP_QUALITY), str(png_file), "-o", str(output_path)
        ], capture_output=True, timeout=60)
        
        if not output_path.exists():
            shutil.copy(png_file, output_path.with_suffix(".png"))
        
        # Construir info para resultados
        info = {
            "id": titulacion.id,
            "nombre": titulacion.nombre,
            "tipo": titulacion.tipo,
            "archivo": str(output_path.relative_to(PROYECTO_ROOT)),
        }
        
        return (titulacion.id, bn, True, info)
        
    except Exception as e:
        return (titulacion.id, bn, False, None)
        
    finally:
        # Limpiar archivos temporales
        for ext in [".tex", ".pdf", ".png", ".log", ".aux", ".out", ".bcf", ".run.xml"]:
            tmp = PROYECTO_ROOT / f"_temp_portada{suffix}{ext}"
            if tmp.exists():
                try:
                    tmp.unlink()
                except:
                    pass


def compilar_portada(titulacion: Titulacion, bn: bool, output_path: Path, verbose: bool = False) -> bool:
    """Compila una portada y la convierte a WebP (versión secuencial)."""
    result = _compilar_portada_worker((titulacion.__dict__, bn, str(output_path)))
    return result[2]  # success


def generar_todas_portadas(titulaciones: list[Titulacion], verbose: bool = False) -> dict:
    """Genera todas las portadas y devuelve el mapeo de archivos."""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    resultados = {
        "grados": [],
        "masteres": [],
        "referencia_color": None,
        "referencia_bn": None,
    }
    
    total = len(titulaciones)
    
    # Determinar número de workers (núcleos disponibles, máximo 8 para no saturar)
    num_workers = min(cpu_count(), 8, total)
    
    # Preparar tareas para ejecución paralela
    tareas = []
    for t in titulaciones:
        output_color = OUTPUT_DIR / f"portada_{t.id}_color.webp"
        tareas.append((t.__dict__, False, str(output_color)))
        
        # Si es la titulación de referencia, añadir también B/N
        if t.id == TITULACION_REFERENCIA:
            output_bn = OUTPUT_DIR / f"portada_{t.id}_bn.webp"
            tareas.append((t.__dict__, True, str(output_bn)))
    
    total_tareas = len(tareas)
    completadas = 0
    errores = 0
    
    print(f"   Usando {num_workers} procesos paralelos para {total_tareas} portadas...")
    
    # Ejecutar en paralelo
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Enviar todas las tareas
        futuros = {executor.submit(_compilar_portada_worker, tarea): tarea for tarea in tareas}
        
        # Procesar resultados a medida que completan
        for futuro in as_completed(futuros):
            tarea = futuros[futuro]
            try:
                tid, bn, success, info = futuro.result()
                completadas += 1
                
                tipo_str = "(B/N)" if bn else ""
                status = "✅" if success else "❌"
                print(f"   [{completadas}/{total_tareas}] {tid} {tipo_str}... {status}")
                
                if success and info:
                    if bn:
                        resultados["referencia_bn"] = info["archivo"]
                        # También guardar color si existe
                        color_path = OUTPUT_DIR / f"portada_{tid}_color.webp"
                        if color_path.exists():
                            resultados["referencia_color"] = str(color_path.relative_to(PROYECTO_ROOT))
                    else:
                        if info["tipo"] == "tfg":
                            resultados["grados"].append(info)
                        else:
                            resultados["masteres"].append(info)
                else:
                    errores += 1
                    
            except Exception as e:
                errores += 1
                print(f"   [{completadas}/{total_tareas}] Error: {e}")
    
    # Ordenar resultados por ID para consistencia
    resultados["grados"].sort(key=lambda x: x["id"])
    resultados["masteres"].sort(key=lambda x: x["id"])
    
    print(f"\n   ✅ Completadas: {completadas - errores}")
    print(f"   ❌ Errores: {errores}")
    
    return resultados


# =============================================================================
# ACTUALIZACIÓN DEL README
# =============================================================================

def generar_tabla_portadas(resultados: dict) -> str:
    """Genera el markdown de la tabla de portadas."""
    
    md = []
    
    # Galería de portadas - todas en una tabla compacta
    md.append("### Galería de Portadas\n")
    md.append("Cada titulación tiene su propio diseño con colores y logotipos oficiales:\n")
    
    # Grados
    md.append("#### Grados\n")
    md.append('<p align="center">')
    for info in resultados["grados"]:
        md.append(f'<img src="{info["archivo"]}" width="12%" title="{info["nombre"]}"></img>')
    md.append('</p>\n')
    
    # Másteres
    md.append("#### Másteres\n")
    md.append('<p align="center">')
    for info in resultados["masteres"]:
        md.append(f'<img src="{info["archivo"]}" width="12%" title="{info["nombre"]}"></img>')
    md.append('</p>\n')
    
    # Ejemplo color vs B/N
    if resultados["referencia_color"] and resultados["referencia_bn"]:
        md.append("### Ejemplo: Portada a color y B/N\n")
        md.append('<p align="center">')
        md.append(f'<img src="{resultados["referencia_color"]}" width="30%"></img>')
        md.append(f'<img src="{resultados["referencia_bn"]}" width="30%"></img>')
        md.append('</p>\n')
    
    return "\n".join(md)


def actualizar_readme(resultados: dict):
    """Actualiza la sección de portadas en el README."""
    
    readme = README_FILE.read_text(encoding="utf-8")
    
    # Buscar la sección de portadas
    # Desde "### Galería de Portadas" hasta "### Comandos de Portada"
    patron = re.compile(
        r'(### Galería de Portadas.*?)(### Comandos de Portada)',
        re.DOTALL
    )
    
    nueva_seccion = generar_tabla_portadas(resultados)
    
    if patron.search(readme):
        readme_nuevo = patron.sub(nueva_seccion + r'\2', readme)
    else:
        # Si no existe, buscar después de "## 🎨 Portadas"
        patron_portadas = re.compile(r'(## 🎨 Portadas\n+.*?\n)(### )', re.DOTALL)
        if patron_portadas.search(readme):
            nueva_seccion_completa = nueva_seccion + "### "
            readme_nuevo = patron_portadas.sub(r'\1' + nueva_seccion, readme)
        else:
            print("⚠️  No se encontró la sección de portadas en el README")
            return
    
    README_FILE.write_text(readme_nuevo, encoding="utf-8")
    print(f"✅ README actualizado")


# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Genera imágenes de portadas para el README"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostrar información detallada"
    )
    parser.add_argument(
        "--no-update-readme",
        action="store_true",
        help="No actualizar el README.md"
    )
    parser.add_argument(
        "--only",
        type=str,
        help="Generar solo una titulación específica"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎨 Generador de Portadas para README")
    print("=" * 60)
    print()
    
    # Verificar dependencias
    for cmd in ["lualatex", "pdftoppm", "cwebp"]:
        if not shutil.which(cmd):
            print(f"❌ Error: '{cmd}' no encontrado. Instálalo primero.")
            sys.exit(1)
    
    # Extraer titulaciones del .cls
    print("📖 Leyendo titulaciones del .cls...")
    titulaciones = extraer_titulaciones(CLS_FILE)
    print(f"   Encontradas: {len(titulaciones)} titulaciones")
    print(f"   - Grados: {sum(1 for t in titulaciones if t.tipo == 'tfg')}")
    print(f"   - Másteres: {sum(1 for t in titulaciones if t.tipo == 'tfm')}")
    print()
    
    # Filtrar si se especificó --only
    if args.only:
        titulaciones = [t for t in titulaciones if t.id == args.only]
        if not titulaciones:
            print(f"❌ Titulación '{args.only}' no encontrada")
            sys.exit(1)
    
    # Generar portadas
    print("🔨 Generando portadas...")
    resultados = generar_todas_portadas(titulaciones, verbose=args.verbose)
    print()
    
    # Resumen
    total_ok = len(resultados["grados"]) + len(resultados["masteres"])
    print(f"📊 Resumen:")
    print(f"   ✅ Generadas: {total_ok}")
    print(f"   ❌ Errores: {len(titulaciones) - total_ok}")
    print()
    
    # Actualizar README
    if not args.no_update_readme and total_ok > 0:
        print("📝 Actualizando README...")
        actualizar_readme(resultados)
    
    print()
    print("✅ Completado")


if __name__ == "__main__":
    main()
