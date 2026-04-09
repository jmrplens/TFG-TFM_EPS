#!/usr/bin/env python3
"""
instalar.py — Asistente de instalación para la plantilla TFG/TFM EPS UA

Comprueba que el sistema tiene todo lo necesario para compilar el documento
LaTeX y, cuando es posible, instala los componentes automáticamente.

No necesitas conocimientos técnicos: sigue las instrucciones en pantalla.

Uso:
    python3 scripts/instalar.py         (Linux / macOS)
    python  scripts/instalar.py         (Windows)
    python3 scripts/instalar.py --auto  (instala sin preguntar en Linux)
"""

from __future__ import annotations

import sys
import os
import subprocess
import shutil
import platform
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Colores en terminal (desactivados en Windows si no hay soporte ANSI)
# ---------------------------------------------------------------------------

def _soporte_color() -> bool:
    """Comprueba si el terminal soporta colores ANSI."""
    if os.environ.get("NO_COLOR"):
        return False
    if sys.platform == "win32":
        # Windows 10 v1511+ soporta ANSI en consolas modernas
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

_COLOR = _soporte_color()

def _c(texto: str, codigo: str) -> str:
    """Aplica un código de color ANSI si el terminal lo soporta."""
    if not _COLOR:
        return texto
    return f"\033[{codigo}m{texto}\033[0m"

def verde(t):  return _c(t, "32")
def rojo(t):   return _c(t, "31")
def amarillo(t): return _c(t, "33")
def negrita(t): return _c(t, "1")
def cyan(t):   return _c(t, "36")

# ---------------------------------------------------------------------------
# Detección del sistema operativo
# ---------------------------------------------------------------------------

def detectar_so() -> str:
    """
    Devuelve una cadena identificando el SO:
      'windows', 'macos', 'linux-debian', 'linux-fedora',
      'linux-arch', 'linux-suse', 'linux'
    """
    sistema = platform.system().lower()
    if sistema == "windows":
        return "windows"
    if sistema == "darwin":
        return "macos"
    if sistema == "linux":
        os_release = Path("/etc/os-release")
        if os_release.exists():
            contenido = os_release.read_text(encoding="utf-8", errors="ignore").lower()
            if any(d in contenido for d in ("ubuntu", "debian", "mint", "pop!_os", "elementary")):
                return "linux-debian"
            if any(d in contenido for d in ("fedora", "rhel", "centos", "almalinux", "rocky")):
                return "linux-fedora"
            if "arch" in contenido or "manjaro" in contenido or "endeavour" in contenido:
                return "linux-arch"
            if "opensuse" in contenido or "suse" in contenido:
                return "linux-suse"
        return "linux"
    return "desconocido"

# ---------------------------------------------------------------------------
# Comprobaciones individuales
# ---------------------------------------------------------------------------

def ejecutar(cmd: list, capture: bool = True, timeout: int | None = 60) -> tuple[bool, str]:
    """
    Ejecuta un comando y devuelve (éxito, salida).

    El parámetro `timeout` controla cuántos segundos esperar antes de
    cancelar el proceso (None = sin límite, útil para instalaciones largas).
    """
    try:
        resultado = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
        )
        salida = ((resultado.stdout or "") + (resultado.stderr or "")).strip()
        return resultado.returncode == 0, salida
    except FileNotFoundError:
        return False, ""
    except subprocess.TimeoutExpired:
        return False, "(tiempo de espera agotado)"
    except Exception as e:
        return False, str(e)


def comprobar_python() -> tuple[bool, str]:
    """Verifica que Python es 3.8 o superior."""
    v = sys.version_info
    version = f"{v.major}.{v.minor}.{v.micro}"
    if v >= (3, 8):
        return True, version
    return False, version


def comprobar_pip() -> tuple[bool, str]:
    """Verifica que pip está disponible."""
    ok, salida = ejecutar([sys.executable, "-m", "pip", "--version"])
    if ok and salida:
        # extraer versión "pip X.Y.Z"
        partes = salida.split()
        version = partes[1] if len(partes) > 1 else salida[:20]
        return True, version
    return False, ""


def comprobar_paquete_python(nombre: str) -> tuple[bool, str]:
    """Verifica si un paquete Python está instalado."""
    ok, salida = ejecutar([sys.executable, "-m", "pip", "show", nombre])
    if ok:
        for linea in salida.splitlines():
            if linea.lower().startswith("version"):
                version = linea.split(":", 1)[1].strip()
                return True, version
        return True, "instalado"
    return False, ""


def comprobar_comando(cmd: str, args: list | None = None) -> tuple[bool, str]:
    """Verifica si un comando del sistema está disponible y responde."""
    if args is None:
        args = ["--version"]
    if shutil.which(cmd) is None:
        return False, ""
    ok, salida = ejecutar([cmd, *args])
    # Algunos comandos retornan código != 0 en --version pero funcionan
    # correctamente (ej. biber). Si produce salida con texto, se considera
    # instalado. Si hay timeout o no hay salida y el código falla, se
    # reporta como problema.
    tiene_salida = bool(salida and salida != "(tiempo de espera agotado)")
    version = salida.splitlines()[0][:60] if tiene_salida else "(versión desconocida)"
    return ok or tiene_salida, version


# ---------------------------------------------------------------------------
# Instalación automática
# ---------------------------------------------------------------------------

def instalar_pip_paquete(nombre: str, modo_auto: bool = False) -> bool:
    """Instala un paquete Python con pip."""
    if not modo_auto:
        try:
            respuesta = input(f"  ¿Instalar {nombre} automáticamente? [S/n] ").strip().lower()
        except EOFError:
            respuesta = "n"  # sin terminal interactivo: no instalar sin confirmación
        if respuesta == "n":
            return False

    print(f"  Instalando {nombre}...", end=" ", flush=True)
    ok, salida = ejecutar(
        [sys.executable, "-m", "pip", "install", "--upgrade", nombre],
        timeout=300,  # 5 min: conexiones lentas o paquetes con muchas dependencias
    )
    if ok:
        print(verde("OK"))
        return True
    else:
        print(rojo("ERROR"))
        print(f"  Detalle: {salida[:200]}")
        return False


def intentar_instalar_latex_linux(so: str, modo_auto: bool = False) -> bool:
    """
    En distribuciones Debian/Ubuntu, intenta instalar TeX Live con apt-get.
    En otras distribuciones, solo muestra instrucciones.
    """
    if so != "linux-debian":
        return False

    if not modo_auto:
        print()
        print(amarillo("  Se puede instalar TeX Live automáticamente en Ubuntu/Debian."))
        print(amarillo("  Requiere contraseña de administrador (sudo) y ~4-6 GB de espacio."))
        try:
            respuesta = input("  ¿Instalar TeX Live completo con sudo apt-get? [S/n] ").strip().lower()
        except EOFError:
            respuesta = "n"  # sin terminal interactivo: no lanzar sudo automáticamente
        if respuesta == "n":
            return False

    cmd = [
        "sudo", "apt-get", "install", "-y",
        "texlive-full", "latexmk", "biber",
    ]
    print("  Instalando TeX Live (puede tardar varios minutos)...", flush=True)
    ok, _ = ejecutar(cmd, capture=False, timeout=None)  # sin límite: descarga ~4-6 GB
    return ok


# ---------------------------------------------------------------------------
# Instrucciones manuales por SO
# ---------------------------------------------------------------------------

INSTRUCCIONES_LATEX = {
    "linux-debian": """
  UBUNTU / DEBIAN / MINT
  ─────────────────────
  Abre una terminal (Ctrl+Alt+T) y ejecuta:

      sudo apt-get update
      sudo apt-get install texlive-full latexmk biber

  Nota: 'texlive-full' instala todos los paquetes (~4-6 GB).
  Si el espacio es limitado, usa 'texlive-luatex' en su lugar
  y añade paquetes sueltos con 'tlmgr' según los necesites.
""",
    "linux-fedora": """
  FEDORA / RHEL / CENTOS / ALMALINUX
  ────────────────────────────────────
  Abre una terminal y ejecuta:

      sudo dnf install texlive-scheme-full latexmk

  El paquete 'biber' está incluido en texlive-scheme-full.
""",
    "linux-arch": """
  ARCH LINUX / MANJARO / ENDEAVOUROS
  ────────────────────────────────────
  Abre una terminal y ejecuta:

      sudo pacman -S texlive-most texlive-lang biber
""",
    "linux-suse": """
  OPENSUSE
  ────────
  Abre una terminal y ejecuta:

      sudo zypper install texlive-scheme-full latexmk biber
""",
    "linux": """
  LINUX (distribución no reconocida)
  ────────────────────────────────────
  Usa el gestor de paquetes de tu distribución para instalar TeX Live.
  Busca el paquete 'texlive-full' o 'texlive-scheme-full'.

  Alternativa universal: instalar TeX Live desde la web oficial:
      https://www.tug.org/texlive/acquire-netinstall.html
""",
    "macos": """
  macOS
  ─────
  Opción 1 — MacTeX (recomendada, ~5 GB):
    Descarga e instala el paquete .pkg de:
        https://www.tug.org/mactex/

  Opción 2 — Homebrew (si ya lo tienes instalado):
      brew install --cask mactex

  Opción 3 — BasicTeX (instalación mínima, ~100 MB):
      brew install --cask basictex
    Después añade paquetes con:
      sudo tlmgr update --self
      sudo tlmgr install latexmk biber collection-luatex
""",
    "windows": """
  WINDOWS
  ───────
  Opción 1 — MiKTeX (recomendada para principiantes):
    Descarga e instala MiKTeX desde:
        https://miktex.org/download
    MiKTeX instala automáticamente los paquetes que faltan al compilar.
    Asegúrate de seleccionar "Instalar paquetes faltantes automáticamente".

  Opción 2 — TeX Live para Windows:
    Descarga el instalador de:
        https://www.tug.org/texlive/acquire-netinstall.html

  IMPORTANTE para Windows:
    - Después de instalar MiKTeX o TeX Live, abre MiKTeX Console y
      actualiza todos los paquetes.
    - Para usar 'make', instala Git for Windows (https://git-scm.com)
      que incluye una terminal Bash con make, o usa WSL (Windows
      Subsystem for Linux).
""",
    "desconocido": """
  SISTEMA NO RECONOCIDO
  ─────────────────────
  Instala TeX Live desde la web oficial:
      https://www.tug.org/texlive/
""",
}

INSTRUCCIONES_MAKE_WINDOWS = """
  MAKE EN WINDOWS
  ───────────────
  'make' no está disponible en Windows por defecto. Tienes varias opciones:

  Opción 1 — Git for Windows (más sencilla):
    Instala Git for Windows desde https://git-scm.com/download/win
    Abre "Git Bash" y ejecuta los comandos de compilación desde ahí.

  Opción 2 — WSL (Windows Subsystem for Linux):
    Abre PowerShell como administrador y ejecuta:
        wsl --install
    Reinicia y usa Ubuntu en WSL para compilar con 'make'.

  Mientras tanto, puedes compilar manualmente con:
      lualatex -shell-escape -interaction=nonstopmode main.tex
      biber main
      lualatex -shell-escape -interaction=nonstopmode main.tex
      lualatex -shell-escape -interaction=nonstopmode main.tex
"""

# ---------------------------------------------------------------------------
# Presentación de resultados
# ---------------------------------------------------------------------------

def _icono(ok: bool) -> str:
    return verde("  ✔") if ok else rojo("  ✗")


def _linea_resultado(nombre: str, ok: bool, detalle: str) -> str:
    estado = verde("OK") if ok else rojo("NO ENCONTRADO")
    return f"{_icono(ok)}  {nombre:<22} {estado}   {detalle}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Asistente de instalación — Plantilla TFG/TFM EPS UA"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Instalar dependencias automáticamente sin preguntar (solo Linux)",
    )
    args = parser.parse_args()
    modo_auto = args.auto

    so = detectar_so()

    print()
    print(negrita("━" * 60))
    print(negrita("  Asistente de instalación — Plantilla TFG/TFM EPS UA"))
    print(negrita("━" * 60))
    print()
    print(f"  Sistema detectado: {cyan(so)}")
    print()
    print("  Comprobando dependencias...\n")

    # ------------------------------------------------------------------
    # 1. Python
    # ------------------------------------------------------------------
    py_ok, py_ver = comprobar_python()
    print(_linea_resultado("Python 3.8+", py_ok, py_ver))
    if not py_ok:
        print(rojo("\n  ERROR: Python 3.8 o superior es obligatorio."))
        print("  Descarga Python desde https://www.python.org/downloads/")
        print("  (marca la opción 'Add Python to PATH' en Windows)\n")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 2. pip
    # ------------------------------------------------------------------
    pip_ok, pip_ver = comprobar_pip()
    print(_linea_resultado("pip", pip_ok, pip_ver))
    if not pip_ok:
        print(amarillo("\n  pip no encontrado. Intenta reinstalar Python o ejecuta:"))
        cmd_pip = "python" if so == "windows" else "python3"
        print(f"    {cmd_pip} -m ensurepip --upgrade\n")

    # ------------------------------------------------------------------
    # 3. latexminted (paquete Python para minted 3.x)
    # ------------------------------------------------------------------
    minted_ok, minted_ver = comprobar_paquete_python("latexminted")
    print(_linea_resultado("latexminted (Python)", minted_ok, minted_ver))

    # ------------------------------------------------------------------
    # 4. LuaLaTeX
    # ------------------------------------------------------------------
    lua_ok, lua_ver = comprobar_comando("lualatex")
    print(_linea_resultado("LuaLaTeX", lua_ok, lua_ver[:50] if lua_ver else ""))

    # ------------------------------------------------------------------
    # 5. Biber
    # ------------------------------------------------------------------
    biber_ok, biber_ver = comprobar_comando("biber")
    print(_linea_resultado("Biber (bibliografía)", biber_ok, biber_ver[:50] if biber_ver else ""))

    # ------------------------------------------------------------------
    # 6. latexmk
    # ------------------------------------------------------------------
    latexmk_ok, latexmk_ver = comprobar_comando("latexmk")
    print(_linea_resultado("latexmk (compilación)", latexmk_ok, latexmk_ver[:50] if latexmk_ver else ""))

    # ------------------------------------------------------------------
    # 7. make (opcional en Windows)
    # ------------------------------------------------------------------
    make_ok, make_ver = comprobar_comando("make")
    sufijo_make = "" if so != "windows" else " (opcional en Windows)"
    print(_linea_resultado(f"make{sufijo_make}", make_ok, make_ver[:50] if make_ver else ""))

    # ------------------------------------------------------------------
    # Diagnóstico y acciones
    # ------------------------------------------------------------------
    print()
    print(negrita("━" * 60))

    todo_ok = py_ok and pip_ok and minted_ok and lua_ok and biber_ok and latexmk_ok
    if so != "windows":
        todo_ok = todo_ok and make_ok

    if todo_ok:
        print()
        print(verde("  ✔ Todo correcto. El entorno está listo para compilar."))
        print()
        if so == "windows":
            print("  Compila el documento (con Git Bash o WSL):")
            print(cyan("      make            ") + " → compilación completa")
            print(cyan("      make quick      ") + " → compilación rápida (solo sintaxis)")
            print()
            print("  O sin make, desde PowerShell / CMD:")
            print(cyan("      lualatex -shell-escape main.tex"))
            print(cyan("      biber main"))
            print(cyan("      lualatex -shell-escape main.tex"))
            print(cyan("      lualatex -shell-escape main.tex"))
            print()
            print("  Ejecuta el revisor estático con:")
            print(cyan("      python scripts/revision-rapida.py"))
        else:
            print("  Compila el documento con:")
            print(cyan("      make            ") + " → compilación completa")
            print(cyan("      make quick      ") + " → compilación rápida (solo sintaxis)")
            print(cyan("      make watch      ") + " → compilación continua al guardar")
            print()
            print("  Ejecuta el revisor estático con:")
            print(cyan("      python3 scripts/revision-rapida.py"))
        print()
        return

    print()
    print(amarillo("  Hay dependencias que faltan. Sigue las instrucciones a continuación."))
    print()

    # ------------------------------------------------------------------
    # Instalar latexminted automáticamente
    # ------------------------------------------------------------------
    if not minted_ok and pip_ok:
        print(negrita("  [1/3] latexminted — paquete Python para resaltado de código"))
        print()
        instalado = instalar_pip_paquete("latexminted", modo_auto)
        if instalado:
            minted_ok = True
        else:
            print(amarillo("  Puedes instalarlo más tarde con:"))
            print("      pip install latexminted")
        print()

    # ------------------------------------------------------------------
    # Instrucciones para TeX Live / MiKTeX
    # ------------------------------------------------------------------
    if not (lua_ok and biber_ok and latexmk_ok):
        print(negrita("  [2/3] LaTeX (LuaLaTeX + Biber + latexmk)"))
        print()

        # En Debian/Ubuntu intentar instalar automáticamente
        if so == "linux-debian":
            instalado = intentar_instalar_latex_linux(so, modo_auto)
            if instalado:
                lua_ok, _ = comprobar_comando("lualatex")
                biber_ok, _ = comprobar_comando("biber")
                latexmk_ok, _ = comprobar_comando("latexmk")
                if lua_ok and biber_ok and latexmk_ok:
                    print(verde("  LaTeX instalado correctamente."))
                else:
                    print(amarillo("  Instalación completada pero algún comando no se detecta."))
                    print("  Cierra y abre la terminal e intenta compilar con 'make'.")
            else:
                instrucciones = INSTRUCCIONES_LATEX.get(so, INSTRUCCIONES_LATEX["linux"])
                print(instrucciones)
        else:
            instrucciones = INSTRUCCIONES_LATEX.get(so, INSTRUCCIONES_LATEX["desconocido"])
            print(instrucciones)

    # ------------------------------------------------------------------
    # Instrucciones para make en Windows
    # ------------------------------------------------------------------
    if not make_ok and so == "windows":
        print(negrita("  [3/3] Compilación en Windows"))
        print(INSTRUCCIONES_MAKE_WINDOWS)

    # ------------------------------------------------------------------
    # Instrucciones para make en otros SO
    # ------------------------------------------------------------------
    if not make_ok and so not in ("windows",):
        print(negrita("  make no encontrado"))
        print()
        if so == "linux-debian":
            print("  Instala 'make' con:")
            print("      sudo apt-get install make")
        elif so == "linux-fedora":
            print("  Instala 'make' con:")
            print("      sudo dnf install make")
        elif so == "macos":
            print("  Instala las herramientas de desarrollo de Xcode:")
            print("      xcode-select --install")
        print()

    # ------------------------------------------------------------------
    # Resumen final
    # ------------------------------------------------------------------
    print(negrita("━" * 60))
    print()
    print("  Resumen final:")
    print()
    todo_resuelto = py_ok and pip_ok and minted_ok and lua_ok and biber_ok and latexmk_ok
    if so != "windows":
        todo_resuelto = todo_resuelto and make_ok

    checks = [
        ("Python 3.8+", py_ok),
        ("pip", pip_ok),
        ("latexminted", minted_ok),
        ("LuaLaTeX", lua_ok),
        ("Biber", biber_ok),
        ("latexmk", latexmk_ok),
    ]
    if so != "windows":
        checks.append(("make", make_ok))

    for nombre, ok in checks:
        icono = verde("✔") if ok else rojo("✗")
        print(f"    {icono}  {nombre}")

    print()
    if todo_resuelto:
        if so == "windows":
            print(verde("  ✔ Todo listo. Compila con: make (Git Bash/WSL) o lualatex manualmente"))
        else:
            print(verde("  ✔ Todo listo. Compila con: make"))
    else:
        print(amarillo("  Sigue las instrucciones anteriores para completar la instalación."))
        print("  Si tienes dudas, consulta docs/GUIA_PRINCIPIANTES.md o")
        print("  abre Copilot/Claude y pega el prompt de instalación de")
        print("  docs/agents/prompts-instalacion.md")
    print()

    # Código de salida: 0 si todo OK, 1 si faltan dependencias
    sys.exit(0 if todo_resuelto else 1)


if __name__ == "__main__":
    main()
