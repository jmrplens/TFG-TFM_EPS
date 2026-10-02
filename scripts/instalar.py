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

Requisito principal: TeX Live 2024 o posterior (incluye minted 3 y su
programa auxiliar latexminted; no hace falta instalar nada con pip).
"""

from __future__ import annotations

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
import sysconfig
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


# Versión mínima de TeX Live que necesita la plantilla (minted 3 con
# latexminted, \DocumentMetadata y etiquetado PDF/UA). Se recomienda la última.
TEXLIVE_MINIMO = 2024
URL_TEXLIVE_QUICKINSTALL = "https://www.tug.org/texlive/quickinstall.html"


def detectar_version_tex() -> tuple[str, int | None]:
    """
    Detecta la distribución TeX instalada y, si es TeX Live, su año.

    Devuelve (distribucion, año): distribucion es 'texlive', 'miktex' o ''
    (no detectada); año es None si no se puede determinar.
    """
    for cmd in (["lualatex", "--version"], ["tex", "--version"], ["tlmgr", "--version"]):
        if shutil.which(cmd[0]) is None:
            continue
        _, salida = ejecutar(cmd)
        if "miktex" in salida.lower():
            return "miktex", None
        # «(TeX Live 2025/Debian)» o «TeX Live (https://tug.org/texlive) version 2025»
        m = re.search(r"TeX Live\D{0,40}?(\d{4})", salida)
        if m:
            return "texlive", int(m.group(1))
    # Instalación oficial de TUG: .../texlive/2025
    if shutil.which("kpsewhich"):
        _, salida = ejecutar(["kpsewhich", "-var-value=SELFAUTOPARENT"])
        m = re.search(r"texlive[/\\](\d{4})\b", salida)
        if m:
            return "texlive", int(m.group(1))
        if salida:
            return "texlive", None
    return "", None


def comprobar_latexminted(distribucion: str, anio: int | None) -> tuple[bool, str]:
    """
    Comprueba el ejecutable `latexminted` que usa minted 3.

    TeX Live 2024 o posterior lo incluye (paquete minted), así que no hace
    falta pip. Se busca el ejecutable en el PATH, que es lo que usa minted.
    """
    ruta = shutil.which("latexminted")
    if ruta:
        ok, salida = ejecutar(["latexminted", "--version"])
        if ok and salida:
            return True, salida.splitlines()[0][:40]
        # Está en el PATH pero no funciona (p. ej. Python incompatible)
        return False, f"{ruta} no funciona ('latexminted --version' falla)"
    if distribucion == "texlive" and anio is not None and anio >= TEXLIVE_MINIMO:
        return False, f"no está en el PATH (TeX Live {anio} lo incluye en el paquete minted)"
    return False, ""


def python_gestionado_externamente() -> bool:
    """
    True si el Python del sistema está protegido por la distribución
    (PEP 668, archivo EXTERNALLY-MANAGED): `pip install` fuera de un entorno
    virtual fallaría o podría romper paquetes del sistema.
    """
    if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return False  # dentro de un entorno virtual
    try:
        stdlib = sysconfig.get_path("stdlib")
    except Exception:
        return False
    return bool(stdlib) and (Path(stdlib) / "EXTERNALLY-MANAGED").exists()


def anio_texlive_apt() -> int | None:
    """Año de TeX Live que instalaría apt (versión candidata de texlive-base)."""
    if shutil.which("apt-cache") is None:
        return None
    # LC_ALL=C: salida en inglés («Candidate:») sea cual sea el idioma
    _, salida = ejecutar(["env", "LC_ALL=C", "apt-cache", "policy", "texlive-base"])
    m = re.search(r"Candidat[eo]:\s*(?:\d+:)?(\d{4})\.", salida)
    return int(m.group(1)) if m else None


def aviso_texlive_antiguo(anio: int | None, origen: str = "instalado") -> str:
    """Texto explicando que la versión de TeX Live es demasiado antigua."""
    if anio:
        cabecera = f"TeX Live {anio} ({origen}) es demasiado antiguo para esta plantilla:"
    else:
        cabecera = f"No se pudo comprobar la versión de TeX Live ({origen}); la plantilla"
    return f"""
  {cabecera}
  necesita TeX Live {TEXLIVE_MINIMO} o posterior (minted 3 con latexminted,
  \\DocumentMetadata y PDF accesible). Con versiones anteriores la
  compilación falla.

  Los paquetes de apt de Ubuntu 24.04 (TeX Live 2023), Ubuntu 22.04
  (TeX Live 2021) y Debian 12 (TeX Live 2022) son demasiado antiguos.
  Ubuntu 26.04 y Debian 13 (o posteriores) ya traen una versión válida.

  Solución recomendada: instalar TeX Live oficial de TUG (no necesita
  desinstalar el de la distribución; basta con que quede antes en el PATH):
      {URL_TEXLIVE_QUICKINSTALL}

  Resumen (Linux/macOS, ~8 GB con el esquema completo):
      cd /tmp
      wget https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
      zcat < install-tl-unx.tar.gz | tar xf -
      cd install-tl-2*
      sudo perl ./install-tl --no-interaction
      # y añadir al PATH, p.ej. en ~/.bashrc:
      export PATH=/usr/local/texlive/AÑO/bin/x86_64-linux:$PATH

  Alternativa sin instalar nada: compilar en Overleaf (ver docs/OVERLEAF.md).
"""


def instrucciones_latexminted(distribucion: str, anio: int | None, so: str) -> str:
    """Cómo conseguir `latexminted` sin romper el Python del sistema."""
    if distribucion == "texlive" and anio is not None and anio >= TEXLIVE_MINIMO:
        if so == "linux-debian":
            return (
                "  Instala el paquete de TeX Live que lo contiene:\n"
                "      sudo apt-get install texlive-latex-extra\n"
                "  (con TeX Live oficial de TUG: sudo tlmgr install minted)"
            )
        return (
            "  Instala o actualiza el paquete minted de TeX Live:\n"
            "      sudo tlmgr update --self\n"
            "      sudo tlmgr install minted\n"
            "  (en Fedora: sudo dnf install texlive-minted; en Arch: texlive-latexextra)"
        )
    if distribucion == "texlive":
        return (
            "  Llegará con TeX Live 2024 o posterior (ver el aviso de LuaLaTeX):\n"
            "  no hace falta instalarlo aparte con pip."
        )
    if not distribucion:
        return "  Se instala junto con TeX Live 2024 o posterior (ver la sección de LaTeX)."
    # MiKTeX u otras distribuciones
    lineas = [
        "  Actualiza MiKTeX (MiKTeX Console → Updates) e instala el paquete 'minted'.",
        "  Si después sigue sin encontrarse el comando 'latexminted':",
    ]
    if shutil.which("pipx"):
        lineas.append("      pipx install latexminted")
    elif python_gestionado_externamente():
        lineas += [
            "      pipx install latexminted",
            "  (tu Python está gestionado por el sistema: no uses 'pip install' directamente;",
            "   instala pipx con el gestor de paquetes, p.ej. 'sudo apt-get install pipx')",
        ]
    else:
        cmd = "python" if so == "windows" else "python3"
        # Dentro de un entorno virtual '--user' no está permitido
        en_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
        usuario = "" if en_venv else " --user"
        lineas.append(f"      {cmd} -m pip install{usuario} latexminted")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Instalación automática
# ---------------------------------------------------------------------------

def instalar_latexminted_pip(modo_auto: bool = False) -> bool:
    """
    Instala latexminted con pip, solo cuando es seguro: dentro de un entorno
    virtual o en un Python que no esté gestionado por el sistema (PEP 668).
    """
    if python_gestionado_externamente():
        return False
    if not modo_auto:
        try:
            respuesta = input("  ¿Instalar latexminted con pip? [S/n] ").strip().lower()
        except EOFError:
            respuesta = "n"  # sin terminal interactivo: no instalar sin confirmación
        if respuesta == "n":
            return False

    cmd = [sys.executable, "-m", "pip", "install", "--upgrade"]
    if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
        cmd.append("--user")  # fuera de un entorno virtual: solo para este usuario
    cmd.append("latexminted")
    print("  Instalando latexminted...", end=" ", flush=True)
    ok, salida = ejecutar(cmd, timeout=300)  # 5 min: conexiones lentas
    if ok:
        print(verde("OK"))
        if not shutil.which("latexminted"):
            print(amarillo("  Instalado, pero 'latexminted' aún no está en el PATH."))
            print("  Cierra y abre la terminal (o añade la carpeta de scripts de Python al PATH).")
        return True
    print(rojo("ERROR"))
    print(f"  Detalle: {salida[:200]}")
    return False


def intentar_instalar_latex_linux(so: str, modo_auto: bool = False) -> str:
    """
    En distribuciones Debian/Ubuntu, intenta instalar TeX Live con apt-get,
    pero solo si la versión que ofrece apt es suficientemente reciente.

    Devuelve 'instalado', 'cancelado', 'antiguo' (apt ofrece una versión
    demasiado antigua; ya se ha explicado qué hacer) o 'error'.
    """
    if so != "linux-debian":
        return "cancelado"

    if not modo_auto:
        print()
        print(amarillo("  Se puede instalar TeX Live automáticamente en Ubuntu/Debian."))
        print(amarillo("  Requiere contraseña de administrador (sudo) y ~4-6 GB de espacio."))
        try:
            respuesta = input("  ¿Instalar TeX Live completo con sudo apt-get? [S/n] ").strip().lower()
        except EOFError:
            respuesta = "n"  # sin terminal interactivo: no lanzar sudo automáticamente
        if respuesta == "n":
            return "cancelado"

    print("  Actualizando la lista de paquetes (sudo apt-get update)...", flush=True)
    ok, _ = ejecutar(["sudo", "apt-get", "update"], capture=False, timeout=None)
    if not ok:
        print(rojo("  No se pudo actualizar la lista de paquetes."))
        return "error"

    anio_apt = anio_texlive_apt()
    if anio_apt is None:
        # Sin versión conocida no se instala: podría ser una versión antigua
        print(rojo("\n  No se pudo determinar qué versión de TeX Live ofrece apt: NO se instala."))
        print(aviso_texlive_antiguo(None, "versión de apt desconocida"))
        return "antiguo"
    if anio_apt < TEXLIVE_MINIMO:
        print(rojo(f"\n  apt ofrece TeX Live {anio_apt}: NO se instala."))
        print(aviso_texlive_antiguo(anio_apt, "versión de apt"))
        return "antiguo"

    cmd = [
        "sudo", "apt-get", "install", "-y",
        "texlive-full", "latexmk", "biber",
    ]
    version = f" {anio_apt}" if anio_apt else ""
    print(f"  Instalando TeX Live{version} (puede tardar varios minutos)...", flush=True)
    ok, _ = ejecutar(cmd, capture=False, timeout=None)  # sin límite: descarga ~4-6 GB
    return "instalado" if ok else "error"


# ---------------------------------------------------------------------------
# Instrucciones manuales por SO
# ---------------------------------------------------------------------------

INSTRUCCIONES_LATEX = {
    "linux-debian": f"""
  UBUNTU / DEBIAN / MINT
  ─────────────────────
  La plantilla necesita TeX Live {TEXLIVE_MINIMO} o posterior.

  Ubuntu 26.04, Debian 13 o posteriores: los paquetes de apt sirven.
  Abre una terminal (Ctrl+Alt+T) y ejecuta:

      sudo apt-get update
      sudo apt-get install texlive-full latexmk biber

  Nota: 'texlive-full' instala todos los paquetes (~4-6 GB).

  Ubuntu 24.04 / 22.04 o Debian 12: apt instala TeX Live 2023 o anterior,
  DEMASIADO ANTIGUO. Instala TeX Live oficial siguiendo:
      {URL_TEXLIVE_QUICKINSTALL}
  (o compila en Overleaf, ver docs/OVERLEAF.md).
""",
    "linux-fedora": f"""
  FEDORA / RHEL / CENTOS / ALMALINUX
  ────────────────────────────────────
  Abre una terminal y ejecuta:

      sudo dnf install texlive-scheme-full latexmk

  El paquete 'biber' está incluido en texlive-scheme-full.
  Comprueba después la versión con 'lualatex --version': si es anterior a
  TeX Live {TEXLIVE_MINIMO}, instala TeX Live oficial:
      {URL_TEXLIVE_QUICKINSTALL}
""",
    "linux-arch": """
  ARCH LINUX / MANJARO / ENDEAVOUROS
  ────────────────────────────────────
  Abre una terminal y ejecuta (paquetes de TeX Live por colecciones):

      sudo pacman -S texlive-basic texlive-latex texlive-latexrecommended \\
          texlive-latexextra texlive-luatex texlive-fontsrecommended \\
          texlive-fontsextra texlive-langspanish texlive-bibtexextra \\
          texlive-mathscience texlive-pictures texlive-binextra biber

  O todo TeX Live de una vez:

      sudo pacman -S texlive-meta texlive-langspanish biber

  ('texlive-binextra' incluye latexmk; 'texlive-latexextra' incluye minted
  y latexminted.)
""",
    "linux-suse": """
  OPENSUSE
  ────────
  Abre una terminal y ejecuta:

      sudo zypper install texlive-scheme-full latexmk biber
""",
    "linux": f"""
  LINUX (distribución no reconocida)
  ────────────────────────────────────
  Usa el gestor de paquetes de tu distribución para instalar TeX Live
  (versión {TEXLIVE_MINIMO} o posterior). Busca el paquete 'texlive-full' o
  'texlive-scheme-full'.

  Alternativa universal: instalar TeX Live desde la web oficial:
      {URL_TEXLIVE_QUICKINSTALL}
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
      sudo tlmgr install latexmk biber collection-luatex minted
    (BasicTeX no trae muchos paquetes que usa la plantilla: si falta
    alguno al compilar, instálalo con 'sudo tlmgr install NOMBRE').
""",
    "windows": f"""
  WINDOWS
  ───────
  Opción 1 — MiKTeX (recomendada para principiantes):
    Descarga e instala MiKTeX desde:
        https://miktex.org/download
    MiKTeX instala automáticamente los paquetes que faltan al compilar.
    Asegúrate de seleccionar "Instalar paquetes faltantes automáticamente".

  Opción 2 — TeX Live para Windows ({TEXLIVE_MINIMO} o posterior):
    Descarga el instalador de:
        https://www.tug.org/texlive/acquire-netinstall.html

  IMPORTANTE para Windows:
    - Después de instalar MiKTeX o TeX Live, abre MiKTeX Console y
      actualiza todos los paquetes.
    - Para usar 'make', instala Git for Windows (https://git-scm.com)
      que incluye una terminal Bash con make, o usa WSL (Windows
      Subsystem for Linux).
""",
    "desconocido": f"""
  SISTEMA NO RECONOCIDO
  ─────────────────────
  Instala TeX Live ({TEXLIVE_MINIMO} o posterior) desde la web oficial:
      {URL_TEXLIVE_QUICKINSTALL}
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


def _linea_resultado(nombre: str, ok: bool, detalle: str, estado_error: str = "NO ENCONTRADO") -> str:
    estado = verde("OK") if ok else rojo(estado_error)
    return f"{_icono(ok)}  {nombre:<22} {estado}   {detalle}"


def _comprobar_latex() -> dict:
    """Comprueba LuaLaTeX (y su versión), Biber, latexmk y latexminted."""
    r = {}
    r["lua_ok"], r["lua_ver"] = comprobar_comando("lualatex")
    r["dist"], r["anio"] = detectar_version_tex() if r["lua_ok"] else ("", None)
    # TeX Live anterior al mínimo: se instala pero la plantilla no compila
    r["tex_antiguo"] = (
        r["lua_ok"] and r["dist"] == "texlive"
        and r["anio"] is not None and r["anio"] < TEXLIVE_MINIMO
    )
    r["biber_ok"], r["biber_ver"] = comprobar_comando("biber")
    r["latexmk_ok"], r["latexmk_ver"] = comprobar_comando("latexmk")
    r["minted_ok"], r["minted_ver"] = comprobar_latexminted(r["dist"], r["anio"])
    return r


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
    # 2. LaTeX: LuaLaTeX (con versión de TeX Live), Biber, latexmk y
    #    latexminted (lo usa minted 3; viene con TeX Live 2024+)
    # ------------------------------------------------------------------
    lt = _comprobar_latex()

    detalle_lua = lt["lua_ver"][:50] if lt["lua_ver"] else ""
    if lt["tex_antiguo"]:
        print(_linea_resultado("LuaLaTeX", False, detalle_lua,
                               f"DEMASIADO ANTIGUO (< TeX Live {TEXLIVE_MINIMO})"))
    else:
        print(_linea_resultado("LuaLaTeX", lt["lua_ok"], detalle_lua))
    print(_linea_resultado("Biber (bibliografía)", lt["biber_ok"], lt["biber_ver"][:50]))
    print(_linea_resultado("latexmk (compilación)", lt["latexmk_ok"], lt["latexmk_ver"][:50]))
    print(_linea_resultado("latexminted (minted 3)", lt["minted_ok"], lt["minted_ver"]))

    # ------------------------------------------------------------------
    # 3. make (opcional en Windows)
    # ------------------------------------------------------------------
    make_ok, make_ver = comprobar_comando("make")
    sufijo_make = "" if so != "windows" else " (opcional en Windows)"
    print(_linea_resultado(f"make{sufijo_make}", make_ok, make_ver[:50] if make_ver else ""))

    # ------------------------------------------------------------------
    # Diagnóstico y acciones
    # ------------------------------------------------------------------
    print()
    print(negrita("━" * 60))

    def _todo_correcto() -> bool:
        ok = (lt["lua_ok"] and not lt["tex_antiguo"] and lt["biber_ok"]
              and lt["latexmk_ok"] and lt["minted_ok"])
        if so != "windows":
            ok = ok and make_ok
        return ok

    if _todo_correcto():
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
    # [1/3] TeX Live / MiKTeX
    # ------------------------------------------------------------------
    if lt["tex_antiguo"] or not (lt["lua_ok"] and lt["biber_ok"] and lt["latexmk_ok"]):
        print(negrita("  [1/3] LaTeX (LuaLaTeX + Biber + latexmk)"))
        if lt["tex_antiguo"]:
            print(aviso_texlive_antiguo(lt["anio"]))

        # En Debian/Ubuntu intentar instalar automáticamente (solo si apt
        # ofrece una versión suficientemente reciente)
        if so == "linux-debian":
            estado = intentar_instalar_latex_linux(so, modo_auto)
            if estado == "instalado":
                lt = _comprobar_latex()
                if lt["lua_ok"] and lt["biber_ok"] and lt["latexmk_ok"] and not lt["tex_antiguo"]:
                    print(verde("  LaTeX instalado correctamente."))
                else:
                    print(amarillo("  Instalación completada pero algún comando no se detecta."))
                    print("  Cierra y abre la terminal e intenta compilar con 'make'.")
            elif estado != "antiguo" and not lt["tex_antiguo"]:
                print(INSTRUCCIONES_LATEX[so])
        elif not lt["tex_antiguo"]:
            instrucciones = INSTRUCCIONES_LATEX.get(so, INSTRUCCIONES_LATEX["desconocido"])
            print(instrucciones)
        print()

    # ------------------------------------------------------------------
    # [2/3] latexminted
    # ------------------------------------------------------------------
    if not lt["minted_ok"]:
        print(negrita("  [2/3] latexminted — resaltado de código con minted 3"))
        print()
        print(instrucciones_latexminted(lt["dist"], lt["anio"], so))
        # pip solo como último recurso (MiKTeX), nunca en un Python del
        # sistema protegido (PEP 668)
        if (lt["dist"] == "miktex" and comprobar_pip()[0]
                and not python_gestionado_externamente()
                and instalar_latexminted_pip(modo_auto)):
            lt["minted_ok"] = bool(shutil.which("latexminted"))
        print()

    # ------------------------------------------------------------------
    # [3/3] make
    # ------------------------------------------------------------------
    if not make_ok and so == "windows":
        print(negrita("  [3/3] Compilación en Windows"))
        print(INSTRUCCIONES_MAKE_WINDOWS)
    elif not make_ok:
        print(negrita("  [3/3] make no encontrado"))
        print()
        if so == "linux-debian":
            print("  Instala 'make' con:")
            print("      sudo apt-get install make")
        elif so == "linux-fedora":
            print("  Instala 'make' con:")
            print("      sudo dnf install make")
        elif so == "linux-arch":
            print("  Instala 'make' con:")
            print("      sudo pacman -S make")
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
    todo_resuelto = _todo_correcto()

    texto_lua = "LuaLaTeX"
    if lt["anio"]:
        texto_lua += f" (TeX Live {lt['anio']}; mínimo {TEXLIVE_MINIMO})"
    checks = [
        ("Python 3.8+", py_ok),
        (texto_lua, lt["lua_ok"] and not lt["tex_antiguo"]),
        ("Biber", lt["biber_ok"]),
        ("latexmk", lt["latexmk_ok"]),
        ("latexminted", lt["minted_ok"]),
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
