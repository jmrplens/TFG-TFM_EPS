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
- Explicar qué hace cada herramienta (LuaLaTeX, Biber, latexmk, minted)
  en términos accesibles para estudiantes sin experiencia técnica
- Detectar si el problema está en el PATH, en permisos, o en la instalación

---

## Referencia técnica para Claude

Cuando ayudes con la instalación de esta plantilla, ten en cuenta:

### Dependencias obligatorias

| Herramienta | Para qué sirve | Forma de verificar |
| --- | --- | --- |
| Python 3.8+ | Ejecutar scripts y minted | `python3 --version` |
| pip | Instalar paquetes Python | `pip --version` |
| latexminted | Resaltado de código en PDF | `pip show latexminted` |
| LuaLaTeX | Motor de compilación LaTeX | `lualatex --version` |
| Biber | Gestión de bibliografía | `biber --version` |
| latexmk | Automatización de compilación | `latexmk --version` |
| make | Atajos del Makefile | `make --version` |

### Instalación rápida por SO

**Ubuntu / Debian:**

```bash
sudo apt-get install texlive-full latexmk biber python3 python3-pip make
pip3 install latexminted
```

**macOS:**

```bash
brew install --cask mactex
pip3 install latexminted
```

**Windows:**

- TeX Live: <https://www.tug.org/texlive/> o MiKTeX: <https://miktex.org/>
- Python: <https://www.python.org/downloads/> (marcar "Add to PATH")
- Tras instalar: `pip install latexminted`

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
| `Pygments not found` / `latexminted not found` | Paquete Python no instalado | `pip install latexminted` |
| `Citation 'X' undefined` | Biber no ejecutado | Usar `make` completo, no `make quick` |
| `Font ... not found` | TeX Live incompleto | Instalar `texlive-fonts-recommended` o paquete completo |
| `I found no \bibdata command` | Usando BibTeX en lugar de Biber | El Makefile ya usa Biber; no invocar BibTeX manualmente |
| `Package minted Error: missing Pygments` | Python no en PATH | Comprobar que Python está en el PATH del sistema |

---

## Estilo de comunicación recomendado

- Lenguaje claro, sin tecnicismos cuando sea posible
- Explicar cada comando antes de pedirle al alumno que lo ejecute
- Confirmar que cada paso funcionó antes de seguir
- Si hay un error, pedir el mensaje completo (no el resumen)
- Para Windows: tener en cuenta que `python3` puede ser `python`
  y `pip3` puede ser `pip`
