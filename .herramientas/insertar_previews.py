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
            tiene_png = pdf.with_suffix(".png").exists()
            disponibles[nombre] = {
                "pdf": f"{ASSETS_REL}/{pdf.name}",
                "png": f"{ASSETS_REL}/{pdf.stem}.png" if tiene_png else None,
            }
    return disponibles


def generar_enlace_preview(nombre: str, disponibles: dict, formato: str) -> str:
    """Genera el HTML/Markdown para mostrar el preview."""
    if nombre not in disponibles:
        return ""

    info = disponibles[nombre]

    if formato == "link":
        return f'\n<details>\n<summary>📸 Ver resultado</summary>\n\n[📄 Ver PDF]({info["pdf"]})\n\n</details>\n'

    elif formato == "imagen" and info["png"]:
        return f'\n<details>\n<summary>📸 Ver resultado</summary>\n\n![Preview]({info["png"]})\n\n</details>\n'

    elif formato == "ambos":
        img_part = f'![Preview]({info["png"]})\n\n' if info["png"] else ""
        return f'\n<details>\n<summary>📸 Ver resultado</summary>\n\n{img_part}[📄 Ver PDF]({info["pdf"]})\n\n</details>\n'

    return ""


def procesar_archivo(archivo: Path, disponibles: dict, formato: str, dry_run: bool = False) -> int:
    """Procesa un archivo Markdown insertando enlaces de preview."""

    contenido = archivo.read_text(encoding="utf-8")
    lineas = contenido.split("\n")
    nuevas_lineas = []

    patron_inicio = re.compile(r"^```latex", re.IGNORECASE)
    patron_fin = re.compile(r"^```\s*$")
    patron_preview_existente = re.compile(r"^<details>.*Ver resultado", re.IGNORECASE)

    numero = 0
    i = 0
    insertados = 0

    while i < len(lineas):
        nuevas_lineas.append(lineas[i])

        if patron_inicio.match(lineas[i]):
            numero += 1
            nombre_snippet = f"{archivo.stem}_{numero:03d}"

            # Buscar fin del bloque
            i += 1
            while i < len(lineas) and not patron_fin.match(lineas[i]):
                nuevas_lineas.append(lineas[i])
                i += 1

            if i < len(lineas):
                nuevas_lineas.append(lineas[i])  # Añadir ```

            # Verificar si ya existe un preview después
            siguiente_no_vacia = i + 1
            while siguiente_no_vacia < len(lineas) and not lineas[siguiente_no_vacia].strip():
                siguiente_no_vacia += 1

            ya_tiene_preview = (
                siguiente_no_vacia < len(lineas)
                and patron_preview_existente.match(lineas[siguiente_no_vacia])
            )

            # Insertar enlace si hay preview disponible y no existe ya
            if nombre_snippet in disponibles and not ya_tiene_preview:
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
