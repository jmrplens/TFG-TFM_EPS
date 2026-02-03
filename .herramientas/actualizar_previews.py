#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script unificado para generar e insertar previews de documentación.

Este script combina las funcionalidades de:
- generar_previews.py: Genera imágenes de los snippets LaTeX
- insertar_previews.py: Inserta los enlaces en los archivos Markdown

Uso:
    python3 actualizar_previews.py                    # Generar e insertar todo
    python3 actualizar_previews.py --solo-generar    # Solo generar previews
    python3 actualizar_previews.py --solo-insertar   # Solo insertar enlaces
    python3 actualizar_previews.py --archivo TEXTO   # Procesar solo un archivo
    python3 actualizar_previews.py --forzar          # Regenerar todos los previews
    python3 actualizar_previews.py --limpiar         # Limpiar previews huérfanos

Autor: Plantilla TFG/TFM EPS UA
Licencia: GPL-3.0
"""

import argparse
import subprocess
import sys
from pathlib import Path


# =============================================================================
# CONFIGURACIÓN
# =============================================================================

HERRAMIENTAS_DIR = Path(__file__).parent.resolve()
PROYECTO_ROOT = HERRAMIENTAS_DIR.parent

SCRIPT_GENERAR = HERRAMIENTAS_DIR / "generar_previews.py"
SCRIPT_INSERTAR = HERRAMIENTAS_DIR / "insertar_previews.py"


# =============================================================================
# FUNCIONES
# =============================================================================

def ejecutar_script(script: Path, args: list = None, descripcion: str = "") -> bool:
    """Ejecuta un script Python y retorna True si fue exitoso."""
    if args is None:
        args = []
    
    cmd = [sys.executable, str(script)] + args
    
    print(f"\n{'='*60}")
    print(f"🔄 {descripcion}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(cmd, cwd=PROYECTO_ROOT)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {script.name}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Genera e inserta previews de documentación LaTeX.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s                         Generar e insertar todos los previews
  %(prog)s --solo-generar          Solo generar imágenes
  %(prog)s --solo-insertar         Solo insertar enlaces en Markdown
  %(prog)s --archivo TEXTO         Procesar solo docs/TEXTO.md
  %(prog)s --forzar                Regenerar todos (ignorar caché)
  %(prog)s --limpiar               Eliminar previews sin snippet
        """
    )
    
    # Modos de operación
    modo = parser.add_mutually_exclusive_group()
    modo.add_argument(
        "--solo-generar", "-g",
        action="store_true",
        help="Solo generar previews (no insertar enlaces)"
    )
    modo.add_argument(
        "--solo-insertar", "-i",
        action="store_true",
        help="Solo insertar enlaces (no generar previews)"
    )
    
    # Opciones de generación
    parser.add_argument(
        "--archivo", "-a",
        type=str,
        metavar="NOMBRE",
        help="Procesar solo un archivo específico (sin extensión, ej: TEXTO)"
    )
    parser.add_argument(
        "--forzar", "-f",
        action="store_true",
        help="Forzar regeneración de todos los previews"
    )
    parser.add_argument(
        "--limpiar", "-c",
        action="store_true",
        help="Eliminar previews huérfanos (sin snippet asociado)"
    )
    
    # Opciones de inserción
    parser.add_argument(
        "--formato",
        choices=["link", "imagen", "ambos"],
        default="ambos",
        help="Formato del preview: link (solo PDF), imagen, ambos (default)"
    )
    
    # Opciones generales
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Mostrar qué se haría sin ejecutar cambios"
    )
    
    args = parser.parse_args()
    
    # Verificar que existen los scripts
    if not SCRIPT_GENERAR.exists():
        print(f"❌ No se encuentra: {SCRIPT_GENERAR}")
        sys.exit(1)
    if not SCRIPT_INSERTAR.exists():
        print(f"❌ No se encuentra: {SCRIPT_INSERTAR}")
        sys.exit(1)
    
    print("="*60)
    print("🖼️  Actualización de Previews de Documentación")
    print("="*60)
    
    exito_total = True
    
    # === PASO 1: Generar previews ===
    if not args.solo_insertar:
        args_generar = []
        
        if args.archivo:
            # generar_previews.py espera --archivo con ruta completa
            archivo_md = PROYECTO_ROOT / "docs" / f"{args.archivo}.md"
            args_generar.extend(["--archivo", str(archivo_md)])
        if args.forzar:
            args_generar.append("--forzar")
        if args.limpiar:
            args_generar.append("--limpiar")
        # Nota: generar_previews.py no soporta --verbose ni --dry-run
        
        # Siempre generar PNG/WebP para poder mostrar imágenes
        # args_generar.append("--png")
        
        if args.dry_run:
            # En dry-run, solo listar lo que se generaría
            args_generar = ["--listar"]
            print("\n(Modo dry-run: solo listando snippets marcados)")
        
        exito = ejecutar_script(
            SCRIPT_GENERAR,
            args_generar,
            "Generando previews de snippets LaTeX"
        )
        
        if not exito:
            print("\n⚠️  Hubo errores en la generación de previews")
            exito_total = False
    
    # === PASO 2: Insertar enlaces ===
    if not args.solo_generar:
        args_insertar = ["--formato", args.formato]
        
        if args.archivo:
            # Construir ruta completa del archivo
            archivo_md = PROYECTO_ROOT / "docs" / f"{args.archivo}.md"
            args_insertar.extend(["--archivo", str(archivo_md)])
        if args.dry_run:
            args_insertar.append("--dry-run")
        
        exito = ejecutar_script(
            SCRIPT_INSERTAR,
            args_insertar,
            "Insertando enlaces de preview en Markdown"
        )
        
        if not exito:
            print("\n⚠️  Hubo errores al insertar enlaces")
            exito_total = False
    
    # === Resumen final ===
    print("\n" + "="*60)
    if exito_total:
        print("✅ Proceso completado exitosamente")
    else:
        print("⚠️  Proceso completado con algunos errores")
    print("="*60)
    
    sys.exit(0 if exito_total else 1)


if __name__ == "__main__":
    main()
