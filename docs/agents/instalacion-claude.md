# Agente de instalación — Guía para Claude

Esta guía describe cómo usar Claude para instalar el entorno de trabajo
de la plantilla TFG/TFM EPS UA cuando `scripts/instalar.py` no puede
resolver el problema automáticamente.

---

## Cuándo usar Claude para la instalación

- El script `scripts/instalar.py` ha fallado o no se puede ejecutar
- Hay un error de compilación que no entiendes
- Necesitas instrucciones adaptadas a tu sistema operativo concreto
- Quieres configurar la verificación de plagio con `.env`

---

## Cómo adjuntar contexto en Claude

1. Adjunta la **salida del script de instalación** (texto copiado del terminal)
2. Si hay errores de compilación, adjunta **las últimas 30–50 líneas de `main.log`**
3. Usa los prompts de `docs/agents/prompts-instalacion.md` como punto de partida

---

## Qué puede hacer Claude en este contexto

- Interpretar mensajes de error de LaTeX y proponer soluciones concretas
- Dar instrucciones de instalación adaptadas al SO del alumno
- Guiar la configuración del archivo `.env` para la detección de plagio
  (las claves solo se usan con `scripts/revision-rapida.py --plagio ...`)
- Explicar qué hace cada herramienta (LuaLaTeX, Biber, latexmk, minted)
  en términos accesibles para estudiantes sin experiencia técnica
- Detectar si el problema está en el PATH, en permisos, o en la instalación

---

## Referencia técnica para Claude

Cuando ayudes con la instalación de esta plantilla, ten en cuenta:

### Dependencias obligatorias

| Herramienta | Para qué sirve | Forma de verificar |
| --- | --- | --- |
| TeX Live 2024+ (o MiKTeX actualizado) | Distribución LaTeX | `lualatex --version` (debe indicar TeX Live 2024 o posterior) |
| LuaLaTeX | Motor de compilación LaTeX | `lualatex --version` |
| latexminted | Resaltado de código (minted 3); viene con TeX Live 2024+ | `latexminted --version` |
| Python 3.9+ | Ejecutar los scripts del proyecto | `python3 --version` |
| Biber | Gestión de bibliografía | `biber --version` |
| latexmk | Automatización de compilación | `latexmk --version` |
| make | Atajos del Makefile | `make --version` |

### Instalación rápida por SO

**Ubuntu 26.04+ / Debian 13+** (TeX Live de la distribución ≥ 2024):

```bash
sudo apt-get update
sudo apt-get install texlive-full latexmk biber python3 make
latexminted --version   # lo incluye texlive-latex-extra
```

**Ubuntu 24.04, Debian 12 o anteriores:** su TeX Live es demasiado antiguo
(2023 o anterior). Instalar TeX Live desde TUG:
<https://www.tug.org/texlive/quickinstall.html>.

**macOS:**

```bash
brew install --cask mactex   # incluye latexminted
latexminted --version
```

**Windows:**

- TeX Live: <https://www.tug.org/texlive/> (incluye latexminted) o MiKTeX: <https://miktex.org/>
- Python: <https://www.python.org/downloads/> (marcar "Add to PATH"), para los scripts
- Solo con MiKTeX, si `latexminted --version` falla tras actualizar MiKTeX e
  instalar el paquete `minted`: `pipx install latexminted`

**No recomendar `pip install latexminted`:** no hace falta con TeX Live 2024+
y en Ubuntu 23.04+/Debian 12+/Homebrew falla por PEP 668
(«externally-managed-environment»). Si falta `latexminted` con TeX Live:
`tlmgr install minted` (TeX Live de TUG) o `texlive-latex-extra` (apt). Si el
`latexminted` del sistema falla al arrancar (p. ej. con Python 3.14), usar
`pipx install latexminted`.

### Compilación manual (sin make)

```bash
lualatex -shell-escape -interaction=nonstopmode main.tex
biber main
lualatex -shell-escape -interaction=nonstopmode main.tex
lualatex -shell-escape -interaction=nonstopmode main.tex
```

### Tabla de errores frecuentes

| Mensaje de error | Causa | Solución |
| --- | --- | --- |
| `command not found: lualatex` | LaTeX no instalado o no en PATH | Instalar TeX Live / MiKTeX |
| `You must invoke LaTeX with -shell-escape` | Falta el flag | Usar `make` o añadir `-shell-escape` |
| `minted v3+ executable is not installed` / `latexminted not found` | Falta `latexminted` o TeX Live anterior a 2024 | `latexminted --version`; `tlmgr install minted` o `texlive-latex-extra`; con MiKTeX `pipx install latexminted` |
| `Citation 'X' undefined` | Biber no ejecutado | Usar `make` completo, no `make quick` |
| `Font ... not found` | TeX Live incompleto | Instalar `texlive-fonts-recommended` o paquete completo |
| `I found no \bibdata command` | Usando BibTeX en lugar de Biber | El Makefile ya usa Biber; no invocar BibTeX manualmente |
| `Package block Error: Some keys specified on the itemize environment are unknown` | Copia antigua de la plantilla con LaTeX 2025-11+ | Actualizar la plantilla (`cls/`, `sty/`) |

---

## Estilo de comunicación recomendado

- Lenguaje claro, sin tecnicismos cuando sea posible
- Explicar cada comando antes de pedirle al alumno que lo ejecute
- Confirmar que cada paso funcionó antes de seguir
- Si hay un error, pedir el mensaje completo (no el resumen)
- Para Windows: tener en cuenta que `python3` puede ser `python`
