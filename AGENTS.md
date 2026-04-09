# AGENTS.md — Instrucciones para agentes de IA

Este archivo define las reglas de trabajo para agentes de código autónomos
(Codex, Devin, OpenHands, Jules, etc.) y para cualquier asistente de IA que
opere sobre este repositorio.

> Para instrucciones específicas por herramienta:
> - **Claude / claude.ai**: ver `CLAUDE.md`
> - **GitHub Copilot**: ver `.github/copilot-instructions.md`
> - **Referencia técnica completa**: ver `docs/AI_CONTEXT.md`
> - **Flujos de trabajo**: ver `docs/AI_WORKFLOWS.md`

---

## Contexto del proyecto

Plantilla LaTeX para Trabajos de Fin de Grado (TFG) y Máster (TFM) de la
Escuela Politécnica Superior (EPS) de la Universidad de Alicante (UA).

- **Versión:** 2.1.0 (2026)
- **Motor de compilación:** LuaLaTeX (obligatorio, nunca pdfLaTeX)
- **Clase principal:** `cls/eps-tfg.cls` (basada en KOMA-Script `scrbook`)
- **Bibliografía:** BibLaTeX + Biber, estilo APA 7
- **Código fuente:** paquete `minted` 3.x con `latexminted`
- **Idiomas soportados:** español, valenciano, inglés

---

## Reglas de edición

### Archivos que el agente PUEDE editar libremente

| Archivo / Directorio | Propósito |
|---|---|
| `configuracion.tex` | Datos del autor, título, titulación, idioma |
| `contenido/capitulos/*.tex` | Contenido de cada capítulo |
| `contenido/anexos/*.tex` | Anexos (excepto `acronimos.tex` con cuidado) |
| `contenido/frontmatter/preliminares.tex` | Agradecimientos, resumen, abstract |
| `referencias.bib` | Entradas bibliográficas |
| `main.tex` | Solo para: añadir/quitar `\input{}` de capítulos, activar módulos de componentes, añadir `\addbibresource` |

### Archivos que el agente NO debe modificar sin instrucción explícita

| Archivo | Razón |
|---|---|
| `cls/eps-tfg.cls` | Clase principal; cambios rompen toda la plantilla |
| `sty/*.sty` | Paquetes de estilo; requieren conocimiento profundo |
| `sty/componentes/*.sty` | Módulos especializados |
| `cls/eps-metadata.tex` | Solo cambiar `lang=` si se cambia el idioma |
| `.latexmkrc` | Configuración de compilación |
| `Makefile` | Automatización de compilación |
| `.github/workflows/*.yml` | CI/CD |

### Regla crítica de idioma

Si se cambia `idioma` en `configuracion.tex`, **siempre** actualizar también
`cls/eps-metadata.tex`:

```
idioma = espanol    →  lang=es-ES
idioma = valenciano →  lang=ca-ES
idioma = ingles     →  lang=en-GB
```

---

## Comandos de compilación

```bash
make          # Compilación completa (lualatex + biber + 2× lualatex)
make quick    # Una sola pasada de lualatex (para verificar sintaxis)
make clean    # Eliminar archivos auxiliares
make watch    # Compilación continua con latexmk
```

Para verificar que el documento compila sin errores tras un cambio:

```bash
make quick 2>&1 | tail -20
```

Si hay errores de bibliografía o referencias cruzadas, usar `make` completo.

---

## Estructura del proyecto

```
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

### Claves obligatorias

```latex
\EPSsetup{
  titulo      = {Título del trabajo},
  autor       = {Nombre Apellido1 Apellido2},
  tutor       = {Dr./Dra. Nombre Apellido},
  tutor-departamento = {Departamento de ...},
  titulacion  = informatica,   % ver tabla de titulaciones
  fecha       = {Junio 2026},
}
```

### Titulaciones disponibles

**Grados (TFG):** `arquitectura`, `arquitectura-tecnica`, `civil`,
`informatica`, `multimedia`, `quimica`, `robotica`, `teleco`

**Másteres (TFM):** `master-agua`, `master-caminos`, `master-ciberseguridad`,
`master-edificacion`, `master-geologica`, `master-informatica`,
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
\begin{definitionbox}{Título} ... \end{definitionbox}
\begin{examplebox}{Título}    ... \end{examplebox}
```

### Entornos del módulo `[software]`

```latex
\begin{terminal}[title={bash}]
  $ comando --opcion
\end{terminal}

\begin{apiendpoint}{GET}{/api/v1/recurso}{Descripción}
  ...
\end{apiendpoint}

\begin{jsoncode}
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

Variantes disponibles: `pythoncode`, `jscode`, `cppcode`, `javacode`,
`matlabcode`, `bashcode`, `sqlcode`, `jsoncode`, `yamlcode`, `htmlcode`,
`csscode`, `rcode`, `rustcode`, `gocode`, `phpcode`.

Sufijo `Dark` para tema oscuro: `pythoncodeDark`, `jscodeDark`, etc.

---

## Tablas y figuras

### Tablas (siempre con `booktabs`)

```latex
\begin{table}[htbp]
  \centering
  \caption{Título de la tabla.}
  \label{tab:nombre}
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
  \includegraphics[width=0.8\textwidth]{recursos/figuras/imagen}
  \caption{Descripción.}
  \label{fig:nombre}
\end{figure}
```

---

## Sistema de referencias

Prefijos de etiquetas a respetar:

| Prefijo | Tipo de elemento |
|---|---|
| `chap:` | Capítulo |
| `sec:` | Sección |
| `fig:` | Figura |
| `tab:` | Tabla |
| `eq:` | Ecuación |
| `cod:` | Bloque de código |
| `lst:` | Listado |
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
- ❌ Usar `\begin{verbatim}` para código. Usar los entornos `*code`.
- ❌ Usar `\begin{lstlisting}`. Usar los entornos `*code` de minted.
- ❌ Escribir contenido en `main.tex`. Solo estructura.
- ❌ Crear portadas manualmente. Usar `\generarportada[ambas]`.
- ❌ Usar `\include{}` para capítulos si no se quiere salto de página forzado. Usar `\input{}`.
- ❌ Modificar `cls/eps-tfg.cls` para ajustes menores de formato.
- ❌ Usar `\bibliographystyle{}` + `\bibliography{}`. Usar BibLaTeX con `\printbibliography`.
- ❌ Usar tablas sin `booktabs` (`\hline` en lugar de `\toprule`/`\midrule`/`\bottomrule`).

---

## Diagnóstico de errores frecuentes

| Error en `.log` | Causa | Solución |
|---|---|---|
| `Undefined control sequence \EPSsetup` | `configuracion.tex` cargado antes de la clase | Verificar orden en `main.tex` |
| `You must invoke LaTeX with -shell-escape` | Falta flag en compilación | Usar `make` o añadir `-shell-escape` |
| `Pygments not found` | `latexminted` no instalado | `pip install latexminted` |
| `Citation 'X' undefined` | Biber no ejecutado | Ejecutar `make` completo |
| `Font ... not found` | TeX Live incompleto | Instalar TeX Live completo |
| `File 'X.sty' not found` | Paquete no instalado | `tlmgr install X` |

---

## Agentes especializados

Además de las instrucciones generales de este archivo, existen agentes
especializados para las tareas más comunes:

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

### Revisión automática (sin IA)

```bash
python3 scripts/revision-rapida.py
```

Análisis estático que detecta referencias rotas, comandos prohibidos, citas
sin entrada `.bib` y más. Genera `informe-revision.md`. También se ejecuta
automáticamente como GitHub Action en cada push/PR que modifique archivos `.tex`.

---

## Prompt de contexto para chats de IA (uso humano)

Si un usuario quiere pegar contexto en un chat de IA externo (ChatGPT, Gemini,
etc.), debe copiar el contenido de `docs/AI_CONTEXT.md`, que contiene la
referencia técnica completa de la plantilla.
