# AGENTS.md — Instrucciones para agentes de IA

Este archivo define las reglas de trabajo para agentes de código autónomos
(Codex, Devin, OpenHands, Jules, etc.) y para cualquier asistente de IA que
opere sobre este repositorio.

> Para instrucciones específicas por herramienta:
>
> - **Claude / claude.ai**: ver `CLAUDE.md`
> - **GitHub Copilot**: ver `.github/copilot-instructions.md`
> - **Referencia técnica completa**: ver `docs/AI_CONTEXT.md`
> - **Flujos de trabajo**: ver `docs/AI_WORKFLOWS.md`

---

## Contexto del proyecto

Plantilla LaTeX para Trabajos de Fin de Grado (TFG) y Máster (TFM) de la
Escuela Politécnica Superior (EPS) de la Universidad de Alicante (UA).

- **Versión:** 2.2.2 (2026)
- **Motor de compilación:** LuaLaTeX (obligatorio, nunca pdfLaTeX)
- **Clase principal:** `cls/eps-tfg.cls` (basada en KOMA-Script `scrbook`)
- **Bibliografía:** BibLaTeX + Biber, estilo APA 7
- **Código fuente:** paquete `minted` 3.x con `latexminted`
- **Idiomas soportados:** español, valenciano, inglés

---

## Reglas de edición

### Archivos que el agente PUEDE editar libremente

| Archivo / Directorio | Propósito |
| --- | --- |
| `configuracion.tex` | Datos del autor, título, titulación, idioma |
| `contenido/capitulos/*.tex` | Contenido de cada capítulo |
| `contenido/anexos/*.tex` | Anexos (excepto `acronimos.tex` con cuidado) |
| `contenido/frontmatter/preliminares.tex` | Agradecimientos, resumen, abstract |
| `referencias.bib` | Entradas bibliográficas |
| `main.tex` | Solo para: añadir/quitar `\input{}` de capítulos, activar módulos de componentes, añadir `\addbibresource` |

### Archivos que el agente NO debe modificar sin instrucción explícita

| Archivo | Razón |
| --- | --- |
| `cls/eps-tfg.cls` | Clase principal; cambios rompen toda la plantilla |
| `sty/*.sty` | Paquetes de estilo; requieren conocimiento profundo |
| `sty/componentes/*.sty` | Módulos especializados |
| `cls/eps-metadata.tex` | Etiquetado y metadatos del PDF; no hace falta tocarlo (tampoco al cambiar de idioma) |
| `.latexmkrc` | Configuración de compilación |
| `Makefile` | Automatización de compilación |
| `.github/workflows/*.yml` | CI/CD |
| `scripts/instalar.py` | Script de instalación; requiere coherencia con el agente |
| `scripts/revision-rapida.py` | Revisor estático; lógica de análisis sensible |

### Idioma

`idioma` en `configuracion.tex` (`espanol`, `valenciano`, `ingles`) cambia el
idioma de todo el documento y el del PDF (`es-ES`, `ca-ES-valencia`, `en-GB`).
**No** se edita `cls/eps-metadata.tex`: la clase fija el idioma del PDF a
partir de `idioma`. La portada se mantiene en español (formato oficial).

---

## Comandos de compilación

```bash
make          # Compilación completa (lualatex + biber + 2× lualatex)
make quick    # Una sola pasada de lualatex (para verificar sintaxis)
make clean    # Eliminar auxiliares, caché _minted/ e informe-revision.md
make watch    # Compilación continua con latexmk
```

Para verificar que el documento compila sin errores tras un cambio:

```bash
make quick 2>&1 | tail -20
```

Si hay errores de bibliografía o referencias cruzadas, usar `make` completo.

---

## Estructura del proyecto

```text
TFG-TFM_EPS/
├── main.tex                    # Archivo raíz (no escribir contenido aquí)
├── configuracion.tex           # Variables del usuario
├── referencias.bib             # Bibliografía
├── cls/
│   ├── eps-tfg.cls             # Clase principal
│   └── eps-metadata.tex        # Metadatos PDF y accesibilidad
├── sty/
│   ├── eps-codigo.sty          # Entornos de código (minted)
│   ├── eps-componentes.sty     # Cargador modular de componentes
│   ├── eps-portadas.sty        # Generación de portadas
│   └── componentes/            # Módulos especializados por disciplina
├── contenido/
│   ├── capitulos/              # Un .tex por capítulo
│   ├── anexos/                 # Anexos y acrónimos
│   └── frontmatter/            # Preliminares (resumen, agradecimientos)
├── recursos/
│   └── logos/                  # Logotipos institucionales
└── docs/                       # Documentación técnica
```

---

## Configuración del documento (`\EPSsetup`)

Toda la configuración se hace en `configuracion.tex` mediante `\EPSsetup{...}`.

### Claves principales

```latex
\EPSsetup{
  titulo      = {Título del trabajo},
  autor       = {Nombre Apellido1 Apellido2},
  tutor       = {Dr./Dra. Nombre Apellido},
  tutor-departamento = {Departamento de ...},
  titulacion  = informatica,   % ver tabla de titulaciones
  fecha       = {Junio 2026},
  borrador    = false,         % true muestra las notas \todo{}
}
```

- `titulacion` es obligatoria: si falta o tiene un valor no válido, la
  compilación se detiene con un error que lista los valores admitidos.
- Si faltan `titulo`, `autor` o `tutor` se muestra un aviso.
- Otras claves: `subtitulo`, `genero`, `email`, `tutor-genero`, `cotutor`,
  `cotutor-genero`, `cotutor-departamento`, `idioma`, `facultad`,
  `universidad`, `ubicacion`. `optimizar-tikz` es obsoleta (se acepta, pero
  no tiene efecto).
- El `configuracion.tex` distribuido trae `borrador = true`; para la versión
  final hay que ponerlo a `false`.
- `accesible = true` (opcional, versión final, LaTeX 2025-11 o posterior)
  declara el PDF conforme a PDF/UA-2 y hace que falte `alt={...}` en un
  `\includegraphics` sea un error. Ver `docs/ACCESIBILIDAD.md`.

### Titulaciones disponibles

**Grados (TFG):** `arquitectura`, `arquitectura-tecnica`, `civil`,
`informatica`, `multimedia`, `quimica`, `robotica`, `teleco`

**Másteres (TFM):** `master-agua`, `master-caminos`, `master-ciberseguridad`,
`master-ciencia-datos`, `master-edificacion`, `master-geologica`, `master-informatica`,
`master-materiales`, `master-moviles`, `master-prevencion`, `master-quimica`,
`master-robotica`, `master-teleco`, `master-web`

---

## Componentes especializados

Activar en `main.tex` según la titulación:

```latex
\usepackage[software]{eps-componentes}       % Informática / Multimedia
\usepackage[telecom]{eps-componentes}        % Telecomunicaciones
\usepackage[arquitectura]{eps-componentes}   % Arquitectura / Civil
\usepackage[quimica]{eps-componentes}        % Química
\usepackage[all]{eps-componentes}            % Todos (más lento)
```

### Entornos siempre disponibles (módulo `comunes`)

```latex
\begin{infobox}{Título}    ... \end{infobox}
\begin{warningbox}{Título} ... \end{warningbox}
\begin{dangerbox}{Título}  ... \end{dangerbox}
\begin{successbox}{Título} ... \end{successbox}
\begin{tipbox}{Título}     ... \end{tipbox}
\begin{notebox}{Título}    ... \end{notebox}
\begin{definitionbox}{Término} ... \end{definitionbox}
\begin{examplebox}[Título]     ... \end{examplebox}
```

En las cajas de aviso el título es opcional (`\begin{infobox} ... \end{infobox}`)
y admiten opciones de tcolorbox: `\begin{infobox}[colback=white]{Título}`.
`examplebox` e `importantbox` llevan el título opcional **entre corchetes**.

### Entornos del módulo `[software]`

El contenido de `terminal`, `apiendpoint` y `dirtreebox` no es literal:
escapar `\&`, `\#`, `\%`, `\_`, `\{`, `\}`, `\$` y separar líneas con `\\`.
Para scripts o salidas copiadas tal cual, usar `bashcode`.

```latex
\begin{terminal}[bash]
\prompt comando --opcion\\
\promptroot apt install paquete
\end{terminal}

\begin{apiendpoint}{GET}{/api/v1/recurso}
  \apidescription{Descripción}
\end{apiendpoint}

\begin{dirtreebox}[Estructura]
  \dirtreeitem[0]{proyecto/}
  \dirtreeitem[1]{main.py}
\end{dirtreebox}

\begin{jsoncode}[]
{ "clave": "valor" }
\end{jsoncode}
```

---

## Entornos de código

Definidos en `sty/eps-codigo.sty`. Usar siempre estos en lugar de `verbatim`
o `lstlisting`.

```latex
\begin{pythoncode}[title={script.py}]
def funcion():
    return True
\end{pythoncode}

\begin{jscode}
console.log("JavaScript");
\end{jscode}

\begin{cppcode}
int main() { return 0; }
\end{cppcode}
```

Lenguajes más usados: `pythoncode`, `jscode`, `cppcode`, `javacode`,
`matlabcode`, `bashcode`, `sqlcode`, `jsoncode`, `yamlcode`, `htmlcode`,
`csscode`, `rcode`, `rustcode`, `gocode`, `phpcode` (lista completa de 46
lenguajes en `docs/CODIGO_FUENTE.md`; otros: `\begin{codigo}{lenguaje}`).

Sufijos: `NN` sin números de línea, `Dark` tema oscuro, `DarkNN`. Las opciones
de minted van en `minted options={firstline=2, highlightlines={3}}` y los `_`
del título se escapan: `title={mi\_script.py}`.

---

## Tablas y figuras

### Tablas (siempre con `booktabs`)

```latex
\begin{table}[htbp]
  \centering
  \caption{Título de la tabla.}
  \label{tab:nombre}
  \EPScabeceraTabla  % la fila 1 es cabecera (PDF accesible)
  \begin{tabular}{lcc}
    \toprule
    Columna 1 & Columna 2 & Columna 3 \\
    \midrule
    Dato      & 100       & 50\%      \\
    \bottomrule
  \end{tabular}
\end{table}
```

### Figuras

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth, alt={Descripción breve}]{recursos/figuras/imagen}
  \caption{Descripción.}
  \label{fig:nombre}
\end{figure}
```

---

## Sistema de referencias

Prefijos de etiquetas a respetar:

| Prefijo | Tipo de elemento |
| --- | --- |
| `chap:` | Capítulo |
| `sec:` | Sección |
| `subsec:` | Subsección (opcional; también vale `sec:`) |
| `fig:` | Figura |
| `tab:` | Tabla |
| `eq:` | Ecuación |
| `cod:` | Bloque de código |
| `teo:` | Teorema |
| `def:` | Definición |
| `anexo:` | Anexo |

---

## Bibliografía

Formato de cita en el texto:

```latex
\parencite{clave}          % (Autor, 2024)
\textcite{clave}           % Autor (2024)
\parencite[p.~50]{clave}   % (Autor, 2024, p. 50)
```

Formato de entrada en `referencias.bib`:

```bibtex
@article{apellido2024,
  author  = {Apellido, Nombre},
  title   = {Título del artículo},
  journal = {Nombre de la revista},
  year    = {2024},
  volume  = {10},
  pages   = {1--15},
  doi     = {10.xxxx/xxxxx},
}
```

---

## Antipatrones — qué NO hacer

- ❌ Usar `pdflatex` o `xelatex`. Solo LuaLaTeX.
- ❌ Usar `\usepackage[utf8]{inputenc}`. LuaLaTeX maneja UTF-8 nativamente.
- ❌ Usar `\usepackage{subfigure}`. Usar `subcaption` (ya incluido).
- ❌ Usar `\usepackage{subfig}`. Usar `subcaption`.
- ❌ Usar paquetes obsoletos: `utf8x`, `t1enc`, `ae`, `times`, `mathptmx`.
- ❌ Usar `\begin{verbatim}` para código. Usar los entornos `*code`.
- ❌ Usar `\begin{lstlisting}`. Usar los entornos `*code` de minted.
- ❌ Escribir contenido en `main.tex`. Solo estructura.
- ❌ Crear portadas manualmente. Usar `\generarportada[ambas]`.
- ❌ Usar `\include{}` para capítulos si no se quiere salto de página forzado. Usar `\input{}`.
- ❌ Modificar `cls/eps-tfg.cls` para ajustes menores de formato.
- ❌ Usar `\bibliographystyle{}` + `\bibliography{}`. Usar BibLaTeX con `\printbibliography`.
- ❌ Usar tablas sin `booktabs` (`\hline` en lugar de `\toprule`/`\midrule`/`\bottomrule`).
- ❌ Usar `[H]` en figuras/tablas, `\diagbox` o `tblr` (tabularray): estropean el PDF accesible. Usar `[htbp]`, una cabecera de texto y `tabular`.
- ❌ Dejar un `tikzpicture` informativo sin `alt={...}` (o `artifact` si es decorativo).

---

## Diagnóstico de errores frecuentes

| Error en `.log` | Causa | Solución |
| --- | --- | --- |
| `TeX capacity exceeded [main memory size=5000000]` | Casi siempre, motor incorrecto (XeLaTeX/pdfLaTeX, de memoria fija); si el motor ya es LuaLaTeX, revisar el contexto en `main.log` (macro recursiva, documento enorme) | Compilar con LuaLaTeX; en Overleaf, Menu → Compiler → LuaLaTeX (`docs/OVERLEAF.md`) |
| `ESTA PLANTILLA REQUIERE LuaLaTeX` | Guard de motor de la plantilla: el motor no es LuaTeX | Compilar con LuaLaTeX (`make`) |
| `Undefined control sequence \EPSsetup` | `configuracion.tex` cargado antes de la clase | Verificar orden en `main.tex` |
| `You must invoke LaTeX with -shell-escape` | Falta flag en compilación | Usar `make` o añadir `-shell-escape` |
| `minted v3+ executable is not installed` | Falta `latexminted` (viene con TeX Live 2024+) | Comprobar `latexminted --version`; si falta, `tlmgr install minted` o `texlive-latex-extra`. No usar `pip install` (PEP 668); `pipx install latexminted` solo con MiKTeX |
| `Citation 'X' undefined` | Biber no ejecutado | Ejecutar `make` completo |
| `Font ... not found` | TeX Live incompleto | Instalar TeX Live completo |
| `File 'X.sty' not found` | Paquete no instalado | `tlmgr install X` |
| `Missing $ inserted` | `_` sin escapar (p. ej. en `title={...}`) o `$` literal en `terminal` | Escapar `\_`; en `terminal` usar `\prompt` |
| `Package block Error: Some keys specified on the itemize environment are unknown` | Versión antigua de la plantilla compilada con LaTeX 2025-11 o posterior | Actualizar la plantilla (al menos `cls/` y `sty/`) a la última versión |
| `ignored error Infinite glue shrinkage found in box being split` | Fallo de `longtable` 4.24 (LaTeX 2025-11) al partir una tabla entre páginas, con una versión antigua de la plantilla | Actualizar `cls/` (la clase corrige `longtable` 4.24). Detiene `latexmk` antes de terminar las pasadas y los números de página de los índices pueden quedar mal |

---

## Agentes especializados

Además de las instrucciones generales de este archivo, existen agentes
especializados para las tareas más comunes:

### Agente de instalación

Ayuda a un estudiante sin experiencia a instalar y configurar el entorno
completo (LaTeX, Python, latexminted, make) en Windows, macOS o Linux.

- **GitHub Copilot:** `.github/agents/instalacion.md`
- **Claude:** `docs/agents/instalacion-claude.md`
- **Prompts listos:** `docs/agents/prompts-instalacion.md`

Flujos cubiertos: instalación desde cero, diagnóstico tras ejecutar
`scripts/instalar.py`, errores de compilación, instalación en Windows sin
experiencia, configuración de verificación de plagio.

### Agente de redacción

Ayuda a redactar secciones y capítulos completos en LaTeX respetando las
convenciones de la plantilla.

- **GitHub Copilot:** `.github/agents/redaccion.md`
- **Claude:** `docs/agents/redaccion-claude.md`
- **Prompts listos:** `docs/agents/prompts-redaccion.md`

Flujos cubiertos: capítulo desde cero, expandir esquema, mejorar fragmento,
resumen/abstract, conclusiones, introducción.

### Agente revisor tipo tribunal

Evalúa el documento completo en 8 dimensiones y genera un informe de revisión
estructurado antes de la defensa.

- **GitHub Copilot:** `.github/agents/revisor.md`
- **Claude:** `docs/agents/revisor-claude.md`
- **Prompts listos:** `docs/agents/prompts-revisor.md`

Dimensiones: estructura, coherencia, bibliografía, lenguaje, formato LaTeX,
figuras/tablas, plagio semántico, normativa EPS UA.

### Herramientas de diagnóstico e instalación (sin IA)

**Comprobación e instalación del entorno:**

```bash
python3 scripts/instalar.py   # Linux / macOS
python  scripts/instalar.py   # Windows
```

Detecta dependencias faltantes (LaTeX, Python, latexminted, make) y ofrece
instalarlas automáticamente. Acepta `--auto` para ejecución no interactiva.

**Revisión estática del documento:**

```bash
python3 scripts/revision-rapida.py   # Linux / macOS
python  scripts/revision-rapida.py   # Windows
```

Análisis estático que detecta referencias rotas, comandos prohibidos, citas
sin entrada `.bib` y más. Genera `informe-revision.md`. También se ejecuta
automáticamente como GitHub Action en cada push/PR que modifique archivos `.tex`.

**Verificación de plagio (opcional):**
Copiar `.env.example` a `.env` y rellenar las claves de Copyleaks o Turnitin.
Tener claves en `.env` no envía nada: el texto solo se manda con
`--plagio copyleaks|turnitin|todos` y tras confirmar (`--si` para confirmar sin
terminal interactiva). Copyleaks exige además `COPYLEAKS_WEBHOOK_URL`
(opcional `COPYLEAKS_SANDBOX=true` para pruebas).

---

## Prompt de contexto para chats de IA (uso humano)

Si un usuario quiere pegar contexto en un chat de IA externo (ChatGPT, Gemini,
etc.), debe copiar el contenido de `docs/AI_CONTEXT.md`, que contiene la
referencia técnica completa de la plantilla.
