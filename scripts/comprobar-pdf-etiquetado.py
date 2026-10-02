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

Códigos de salida:
  0  PDF etiquetado (o --no-exigir)
  1  PDF sin etiquetar, o /Lang distinto de --idioma-esperado
  2  Error de uso / pypdf no disponible / PDF ilegible

Requiere: Python 3.9+, pypdf.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import Counter


def _contar_estructura(raiz, limite: int = 200_000) -> Counter:
    """Recorre el árbol de estructura y cuenta elementos por /S (tipo)."""
    from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject

    tipos: Counter = Counter()
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
        hijos = nodo.get("/K")
        if hijos is not None:
            pila.append(hijos)
    return tipos


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("pdf", help="Ruta al PDF a comprobar")
    parser.add_argument("--titulo", default="", help="Título para el resumen")
    parser.add_argument(
        "--idioma-esperado",
        default="",
        help="Prefijo esperado de /Lang (p. ej. 'es', 'ca', 'en-GB'); falla si no coincide",
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
    marcado = bool(markinfo and markinfo.get_object().get("/Marked", False))
    raiz = catalogo.get("/StructTreeRoot")
    tiene_arbol = raiz is not None

    tipos: Counter = Counter()
    if tiene_arbol:
        try:
            tipos = _contar_estructura(raiz.get_object())
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: no se pudo recorrer el árbol: {exc}", file=sys.stderr)

    # Declaración PDF/UA en los metadatos XMP (pdfuaid:part)
    declaracion_ua = "no"
    try:
        meta = catalogo.get("/Metadata")
        if meta is not None:
            xmp = meta.get_object().get_data().decode("utf-8", "replace")
            m = re.search(r"pdfuaid:part\s*(?:=\s*\"|>)\s*(\d+)", xmp)
            if m:
                declaracion_ua = f"sí (PDF/UA-{m.group(1)})"
    except Exception:  # noqa: BLE001
        declaracion_ua = "desconocida"

    etiquetado = marcado and tiene_arbol
    esperado = args.idioma_esperado.strip().lower()
    idioma_ok = not esperado or idioma.lower() == esperado or idioma.lower().startswith(esperado + "-")
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

    titulo = args.titulo or f"Información del PDF ({os.path.basename(args.pdf)})"
    md = [f"### {titulo}", "", "| Propiedad | Valor |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in filas]
    md.append("")
    md.append("✅ PDF etiquetado" if etiquetado else "❌ El PDF NO está etiquetado")
    if esperado:
        md.append(f"✅ Idioma {idioma} (esperado: {esperado})" if idioma_ok
                  else f"❌ Idioma {idioma}, se esperaba {esperado}")
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
