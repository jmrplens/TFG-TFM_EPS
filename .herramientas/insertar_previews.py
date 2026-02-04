#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insertador de enlaces de preview en documentación Markdown.

Este script actualiza los archivos .md añadiendo enlaces/imágenes
a las previsualizaciones generadas de los snippets LaTeX.

Uso:
    python3 insertar_previews.py [--formato {link|imagen|ambos}]
"""

import argparse
import re
from pathlib import Path
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Configuración
PROYECTO_ROOT = Path(__file__).parent.parent.resolve()
DOCS_DIR = PROYECTO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets" / "previews"
ASSETS_REL = "assets/previews"


def obtener_snippets_disponibles() -> dict:
    """Obtiene los snippets que tienen preview generado."""
    disponibles = {}
    if ASSETS_DIR.exists():
        for pdf in ASSETS_DIR.glob("*.pdf"):
            nombre = pdf.stem
            # Buscar WebP primero, luego PNG
            tiene_webp = pdf.with_suffix(".webp").exists()
            tiene_png = pdf.with_suffix(".png").exists()
            
            if tiene_webp:
                img_path = f"{ASSETS_REL}/{pdf.stem}.webp"
            elif tiene_png:
                img_path = f"{ASSETS_REL}/{pdf.stem}.png"
            else:
                img_path = None
                
            disponibles[nombre] = {
                "pdf": f"{ASSETS_REL}/{pdf.name}",
                "img": img_path,
            }
    return disponibles


def get_image_display_width(rel_path: str) -> int:
    """Calcula el ancho de visualización (max 600px)."""
    if not rel_path or not HAS_PIL:
        return 600
        
    try:
        # ASSETS_REL es "assets/previews", pero DOCS_DIR ya incluye "docs"
        # path en disco: DOCS_DIR / (rel_path relative to docs)
        # rel_path viene como "assets/previews/file.png"
        
        # Ojo: rel_path es relativo a DOCS_DIR
        full_path = DOCS_DIR / rel_path
        
        if not full_path.exists():
            return 600
            
        with Image.open(full_path) as img:
            w = img.width
            # Si es muy ancho (A4), limitar a 600
            # Si es pequeño (componente), usar su ancho real para no estirar
            # Nota: Si la imagen es Retina/HiDPI, esto podría quedar grande,
            # pero es mejor que forzar todo a 600.
            return min(w, 600)
    except Exception:
        return 600


def generar_enlace_preview(nombre: str, disponibles: dict, formato: str) -> str:
    """Genera el HTML/Markdown para mostrar el preview.
    
    Las imágenes se muestran manteniendo su relación de aspecto original.
    Al generarse todas en un lienzo A4, la escala relativa es correcta.
    """
    if nombre not in disponibles:
        return ""

    info = disponibles[nombre]
    
    if formato == "link":
        return f'\n**Resultado:**\n\n[📄 Ver PDF]({info["pdf"]})\n'

    if formato == "imagen" and info["img"]:
        return f'\n**Resultado:**\n\n<img src="{info["img"]}" alt="Preview">\n\n[📄 Ver PDF]({info["pdf"]})\n'

    elif formato == "ambos" and info["img"]:
        return f'\n**Resultado:**\n\n<img src="{info["img"]}" alt="Preview">\n\n[📄 Ver PDF]({info["pdf"]})\n'

    elif formato == "ambos":
        # Solo PDF si no hay imagen
        return f'\n**Resultado:**\n\n[📄 Ver PDF]({info["pdf"]})\n'

    return ""


def procesar_archivo(archivo: Path, disponibles: dict, formato: str, dry_run: bool = False) -> int:
    """Procesa un archivo Markdown insertando enlaces de preview."""

    contenido = archivo.read_text(encoding="utf-8")
    lineas = contenido.split("\n")
    nuevas_lineas = []

    # Patrón para bloques marcados con nombre personalizado o sin él
    # Captura: ```latex <!-- preview[:N] [nombre] -->
    patron_inicio_marcado = re.compile(
        r"^```latex\s*<!--\s*preview(?::\d)?\s*(\S+)?\s*-->",
        re.IGNORECASE
    )
    patron_inicio = re.compile(r"^```latex", re.IGNORECASE)
    patron_fin = re.compile(r"^```\s*$")
    patron_preview_existente = re.compile(r"^\*\*Resultado:\*\*|^<details>|^<img src=", re.IGNORECASE)

    numero_marcado = 0  # Solo cuenta los marcados
    i = 0
    insertados = 0

    while i < len(lineas):
        nuevas_lineas.append(lineas[i])

        # Detectar si es un bloque latex marcado
        match_marcado = patron_inicio_marcado.match(lineas[i])
        es_latex = patron_inicio.match(lineas[i])
        
        if es_latex:
            if match_marcado:
                numero_marcado += 1
                nombre_custom = match_marcado.group(1)
                # Usar nombre personalizado si existe, sino usar formato ARCHIVO_NNN
                if nombre_custom:
                    nombre_snippet = nombre_custom
                else:
                    nombre_snippet = f"{archivo.stem.upper()}_{numero_marcado:03d}"
            
            # Buscar fin del bloque
            i += 1
            while i < len(lineas) and not patron_fin.match(lineas[i]):
                nuevas_lineas.append(lineas[i])
                i += 1

            if i < len(lineas):
                nuevas_lineas.append(lineas[i])  # Añadir ```

            # Solo insertar preview para bloques marcados
            if match_marcado:
                # 1. Detectar y saltar preview existente (si hay)
                next_idx = i + 1
                has_existing_preview = False
                temp_skipped_lines = 0
                
                # Avanzar saltando líneas vacías iniciales
                while next_idx < len(lineas) and not lineas[next_idx].strip():
                    next_idx += 1
                
                # Si encontramos el inicio de un preview
                if next_idx < len(lineas) and patron_preview_existente.match(lineas[next_idx]):
                    has_existing_preview = True
                    # Consumir líneas que formen parte del preview
                    while next_idx < len(lineas):
                        line = lineas[next_idx].strip()
                        # Criterio para identificar líneas de preview:
                        # - Vacía
                        # - **Resultado:**
                        # - <img ...>
                        # - [📄 ...]
                        # - <details>, </details>, <summary>
                        # - ![Preview]
                        if (not line or 
                            line.startswith("**Resultado:**") or 
                            line.startswith("<img") or 
                            line.startswith("[📄") or
                            line.startswith("<details") or
                            line.startswith("</details") or
                            line.startswith("<summary") or
                            line.startswith("![Preview")
                           ):
                            next_idx += 1
                        else:
                            break
                    
                    # Actualizar cursor principal para saltar estas líneas
                    i = next_idx - 1

                # 2. Insertar/Reemplazar con el nuevo preview
                if nombre_snippet in disponibles:
                    enlace = generar_enlace_preview(nombre_snippet, disponibles, formato)
                    if enlace:
                        nuevas_lineas.append(enlace)
                        insertados += 1

        i += 1

    if not dry_run and insertados > 0:
        archivo.write_text("\n".join(nuevas_lineas), encoding="utf-8")

    return insertados


def main():
    parser = argparse.ArgumentParser(
        description="Inserta enlaces de preview en la documentación Markdown."
    )

    parser.add_argument(
        "--formato",
        "-f",
        choices=["link", "imagen", "ambos"],
        default="ambos",
        help="Formato del preview: link (solo PDF), imagen (PNG), ambos",
    )
    parser.add_argument(
        "--archivo",
        "-a",
        type=str,
        help="Procesar solo un archivo específico",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Mostrar cambios sin aplicarlos",
    )
    parser.add_argument(
        "--limpiar",
        "-c",
        action="store_true",
        help="Eliminar todos los bloques de preview existentes",
    )

    args = parser.parse_args()

    disponibles = obtener_snippets_disponibles()
    print(f"📸 Previews disponibles: {len(disponibles)}")

    if args.archivo:
        archivos = [Path(args.archivo)]
    else:
        archivos = sorted(DOCS_DIR.glob("*.md"))

    total_insertados = 0
    for archivo in archivos:
        if not archivo.exists():
            continue

        insertados = procesar_archivo(
            archivo, disponibles, args.formato, dry_run=args.dry_run
        )

        if insertados > 0:
            estado = "(dry-run)" if args.dry_run else ""
            print(f"   📄 {archivo.name}: +{insertados} previews {estado}")
            total_insertados += insertados

    print(f"\n✅ Total insertados: {total_insertados}")


if __name__ == "__main__":
    main()
