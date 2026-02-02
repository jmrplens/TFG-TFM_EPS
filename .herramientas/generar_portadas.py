#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador automático de imágenes de portadas para el README.

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
from dataclasses import dataclass
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
DPI = 150  # Más bajo para thumbnails
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
    
    return f"""\\documentclass{{eps-tfg}}

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
\\portada{'bn' if bn else 'color'}
\\end{{document}}
"""


def compilar_portada(titulacion: Titulacion, bn: bool, output_path: Path, verbose: bool = False) -> bool:
    """Compila una portada y la convierte a WebP."""
    
    # Crear archivo temporal EN el directorio del proyecto
    tex_file = PROYECTO_ROOT / f"_temp_portada_{titulacion.id}.tex"
    pdf_file = PROYECTO_ROOT / f"_temp_portada_{titulacion.id}.pdf"
    
    try:
        # Crear documento
        documento = generar_documento_portada_simple(titulacion, bn)
        tex_file.write_text(documento, encoding="utf-8")
        
        # Configurar TEXINPUTS para encontrar la clase y los estilos
        env = os.environ.copy()
        env["TEXINPUTS"] = f".:{PROYECTO_ROOT}/cls:{PROYECTO_ROOT}/sty:{PROYECTO_ROOT}/recursos:{env.get('TEXINPUTS', '')}"
        
        # Compilar desde el directorio del proyecto
        cmd = [
            "lualatex",
            "-shell-escape",
            "-interaction=nonstopmode",
            "-halt-on-error",
            tex_file.name
        ]
        
        result = subprocess.run(
            cmd,
            cwd=PROYECTO_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )
        
        if not pdf_file.exists():
            if verbose:
                print(f"\n   Error de compilación:")
                # Buscar errores en el log
                log_file = PROYECTO_ROOT / f"_temp_portada_{titulacion.id}.log"
                if log_file.exists():
                    log = log_file.read_text(encoding="utf-8", errors="ignore")
                    for line in log.split("\n"):
                        if line.startswith("!") or "error" in line.lower():
                            print(f"      {line[:100]}")
            return False
        
        # Convertir PDF a imagen con alta calidad
        png_file = PROYECTO_ROOT / f"_temp_portada_{titulacion.id}.png"
        
        # Usar pdftoppm para convertir
        cmd_convert = [
            "pdftoppm",
            "-png",
            "-r", str(DPI),
            "-singlefile",
            str(pdf_file),
            str(PROYECTO_ROOT / f"_temp_portada_{titulacion.id}")
        ]
        
        subprocess.run(cmd_convert, capture_output=True, timeout=60)
        
        if not png_file.exists():
            if verbose:
                print(f"\n   Error: No se pudo convertir PDF a PNG")
            return False
        
        # Asegurar directorio de salida
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convertir a WebP
        cmd_webp = [
            "cwebp",
            "-q", str(WEBP_QUALITY),
            str(png_file),
            "-o", str(output_path)
        ]
        
        subprocess.run(cmd_webp, capture_output=True, timeout=60)
        
        if not output_path.exists():
            # Fallback: mantener PNG
            shutil.copy(png_file, output_path.with_suffix(".png"))
            if verbose:
                print(f"\n   Advertencia: WebP falló, usando PNG")
        
        return True
        
    finally:
        # Limpiar archivos temporales
        for ext in [".tex", ".pdf", ".png", ".log", ".aux", ".out"]:
            tmp = PROYECTO_ROOT / f"_temp_portada_{titulacion.id}{ext}"
            if tmp.exists():
                tmp.unlink()


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
    
    for i, t in enumerate(titulaciones, 1):
        print(f"   [{i}/{total}] {t.id}...", end=" ", flush=True)
        
        # Archivo de salida
        output_color = OUTPUT_DIR / f"portada_{t.id}_color.webp"
        
        # Compilar portada color
        if compilar_portada(t, bn=False, output_path=output_color, verbose=verbose):
            print("✅")
            
            info = {
                "id": t.id,
                "nombre": t.nombre,
                "tipo": t.tipo,
                "archivo": output_color.relative_to(PROYECTO_ROOT),
            }
            
            if t.tipo == "tfg":
                resultados["grados"].append(info)
            else:
                resultados["masteres"].append(info)
            
            # Si es la titulación de referencia, generar también B/N
            if t.id == TITULACION_REFERENCIA:
                output_bn = OUTPUT_DIR / f"portada_{t.id}_bn.webp"
                print(f"   [{i}/{total}] {t.id} (B/N)...", end=" ", flush=True)
                
                if compilar_portada(t, bn=True, output_path=output_bn, verbose=verbose):
                    print("✅")
                    resultados["referencia_color"] = str(output_color.relative_to(PROYECTO_ROOT))
                    resultados["referencia_bn"] = str(output_bn.relative_to(PROYECTO_ROOT))
                else:
                    print("❌")
        else:
            print("❌")
    
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
