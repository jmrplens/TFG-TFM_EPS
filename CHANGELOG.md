# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [Sin publicar]

### Accesibilidad

- **PDF/UA-2 por defecto**: nueva opción `accesible` en `\EPSsetup`, activada
  en `configuracion.tex` y como valor inicial de la clase. Con LaTeX 2025-11 o
  posterior declara el PDF conforme a PDF/UA-2 y avisa de `\diagbox` y
  `tblr`; el documento de ejemplo es conforme según veraPDF (PDF/UA-2 y
  WTPDF 1.0) en español, valenciano e inglés. Con LaTeX anterior a 2025-11 o
  sin `\input{eps-metadata}` solo avisa.
- **Texto alternativo automático**: una imagen sin `alt={...}` ya no recibe
  el nombre del archivo, sino su leyenda con el número («Figura 3.2: …») o
  «Imagen N», con un aviso claro que indica el archivo y el texto usado. La
  falta de texto alternativo no detiene la compilación.
- **Dibujos TikZ y gráficas pgfplots** sin `alt={...}` dentro de una figura:
  reciben el mismo texto automático que las imágenes (antes eran un artefacto
  que el lector de pantalla no leía, sin ningún aviso).
- **Enlaces de los índices asociados a su destino**: las entradas de la lista
  de figuras, la de tablas y los capítulos sin número del índice enlazaban con
  anclas sin estructura (59 avisos `Destination ... has no related structure`
  en el ejemplo). Los avisos de etiquetado bajan de 61 a 2.
- **`\paragraph` y `\subparagraph` como encabezados**: el título en línea es
  un encabezado y el texto que le sigue, un párrafo aparte. El aspecto no
  cambia.
- **Leyendas con su formato en el PDF etiquetado**: con el etiquetado, LaTeX
  componía las leyendas con su formato estándar y se perdían las fuentes de
  `\captionsetup` (etiqueta «Figura 1:» en negrita, texto en tamaño
  pequeño). Vuelven a verse igual que sin etiquetado.
- Compilar sin `\input{eps-metadata}` vuelve a funcionar con las cajas UML
  (`capture=hbox`).
- **CI**: veraPDF valida el PDF de cada idioma (español, valenciano e inglés)
  y la comprobación falla si alguno no es conforme con PDF/UA-2. El script de
  comprobación exige además encabezados, índice enlazado y texto alternativo
  en todas las figuras (veraPDF no lo detecta), y falla si el etiquetado
  empeora respecto a la línea base de `scripts/linea-base-accesibilidad.json`.
  Nueva configuración `texlive-2025` en la matriz (LaTeX 2025-11).

- **Texto de los bloques de código con espacios** (con LaTeX 2025-11 o
  posterior): el texto etiquetado y el copiado decían `deffibonacci(n):`.
- Las notas de `threeparttable` ya no quedan dentro de un párrafo (PDF 2.0 no
  lo permite).
- `\includepdf` ya no avisa de que falta el texto alternativo cuando lo tiene.
- **Compatibilidad con LaTeX 2026-06 (TeX Live 2026)**, que cambió el
  etiquetado de los títulos y de algunas cajas (el PDF con `accesible = true`
  no era conforme):
  - `\chapter` ya no se etiquetaba: el título quedaba como un párrafo que
    contenía todo el capítulo. Vuelve a ser un `H1` con su número dentro.
  - Las cajas de `tcolorbox` con `capture=hbox` y título o `varwidth upper`
    (las de UML del módulo `[software]`) dejaban abierto un párrafo con el
    resto del documento.
  - Las notas de `threeparttable` volvían a quedar dentro de un párrafo.

- **Títulos como encabezados** (con LaTeX 2025-11 o posterior): `\section`, `\subsection`... se etiquetan como
  `H2`, `H3`... dentro de secciones anidadas (antes eran párrafos), y el
  número del capítulo forma parte de su `H1`. El aspecto no cambia.
- **Índices navegables** (con LaTeX 2025-11 o posterior): el índice general y los de figuras, tablas y códigos
  se etiquetan como índices (antes eran artefactos que el lector de pantalla
  no leía) y cada entrada lleva su enlace (650 enlaces en el ejemplo, antes
  146). El aspecto no cambia.
- **CI**: las métricas de accesibilidad cuentan también los encabezados y las
  entradas de índice enlazadas.

- **PDF etiquetado más útil para lectores de pantalla** (sin declarar todavía
  PDF/UA-2). En el documento de ejemplo los avisos de etiquetado bajan de 258 a
  66; los que quedan son, sobre todo, una limitación del núcleo de LaTeX.
  - La portada ya no deja estructuras abiertas: antes casi todo el documento
    colgaba de un párrafo en la raíz del árbol.
  - Los iconos decorativos se marcan como artefacto y los que transmiten
    información se leen como texto (casillas de `checklist`, `\pro`/`\con`,
    `\rating`, indicadores de cumplimiento). Nuevo `\EPSiconoTexto{texto}{icono}`.
  - Los fragmentos en otro idioma (el Abstract) llevan su propio `/Lang`.
  - Las leyendas vuelven a etiquetarse como `Caption` aunque haya cajas de
    `tcolorbox` con título, y las figuras y tablas se agrupan al final de cada
    capítulo en lugar de al final del documento.
  - `\mintinline` ya no genera una fórmula vacía por carácter.
  - `presupuesto` ya no oculta su contenido en el PDF etiquetado.
- **Nuevo `\EPScabeceraTabla[<filas>]`**: marca la cabecera de las tablas de
  datos (`TH`). Sin efecto con LaTeX anterior a 2025-11.
- **`alt`/`artifact` en `tikzpicture`** también con TeX Live 2024 (allí sin
  efecto), para que el mismo documento compile en todas las versiones.
- **Ejemplos**: sin `[H]`, `\diagbox` ni `tblr`; tablas de datos con cabecera
  y diagramas y gráficas con texto alternativo.
- **CI**: el resumen de compilación muestra métricas de accesibilidad
  (figuras con texto alternativo, cabeceras de tabla, idioma, enlaces y avisos
  de etiquetado por tipo), solo informativas.

### Corregido

- **`Infinite glue shrinkage found in box being split`** con `longtable` 4.24
  (TeX Live 2025): la clase aplica la corrección de `longtable` 4.25. El error
  hacía que `latexmk` se detuviera antes de terminar las pasadas y los números
  de página de los índices podían quedar mal.

- **La plantilla vuelve a compilar con TeX Live actual (LaTeX 2025-11 o
  posterior)**: con `\DocumentMetadata` el documento completo fallaba (opciones
  de listas de `enumitem`, `\ch` de `chemformula`, `threeparttable`). La clase
  incluye ahora ajustes de compatibilidad con el etiquetado.
- **`idioma` cambia de verdad el idioma del documento**: antes el cuerpo seguía
  en español. Títulos automáticos, índices, teoremas, listados de código,
  bibliografía, separación silábica y separador decimal siguen el idioma;
  `valenciano` usa `ca-ES-valencia` e `ingles` el inglés británico (`en-GB`).
  La portada se mantiene en español (formato oficial de la EPS).
- **Bibliografía APA**: `biblatex` ya no fuerza `language=spanish`, así que se
  respeta el `langid` de cada entrada y los títulos en inglés salen en
  minúscula de frase (sentence case) como exige APA 7.
- **`borrador = true/false`** en `\EPSsetup` funciona (antes no hacía nada) y
  las opciones de clase `[borrador]`/`[final]` ya no dan error.
- **Titulación desconocida**: error claro con la lista de valores admitidos en
  lugar de un bucle infinito; error si falta `titulacion` y aviso si faltan
  `titulo`, `autor` o `tutor`.
- **Sintaxis documentada de los componentes** (CLAUDE.md, AGENTS.md,
  instrucciones de Copilot, agentes, `llms.txt`, `docs/AI_CONTEXT.md`,
  `docs/AI_WORKFLOWS.md`): `terminal` con título entre corchetes y `\prompt`,
  `apiendpoint` con dos argumentos y `\apidescription`, `dirtreebox` con
  `\dirtreeitem`, `examplebox` con título entre corchetes, opciones de minted
  dentro de `minted options={...}` y `_` escapado en los títulos. Los ejemplos
  anteriores no compilaban o se veían mal.
- **`docs/AI_CONTEXT.md`** reescrito: eliminadas claves de `\EPSsetup`,
  archivos `.sty` y componentes que no existen; añadidas las claves reales
  (`facultad`, `universidad`, `ubicacion`, `borrador`, cotutor...).
- **Etiquetas**: una única convención (`chap:`, `sec:`, `fig:`, `tab:`, `eq:`,
  `cod:`, `teo:`, `def:`, `anexo:`, y `subsec:` opcional) en la documentación
  y en el contenido de ejemplo.
- **Contenido de ejemplo**: el ejemplo de tabla simple usa `booktabs` en lugar
  de `\hline`; el aviso sobre Wikipedia muestra las llaves de `note={...}`.
- **Scripts**: `revision-rapida.py` sin falsos positivos (de 123 avisos sobre
  la propia plantilla a 3), ignora bloques de código y reconoce
  `\footcite`/`\autocite`; `instalar.py` comprueba el año de TeX Live, detecta
  `latexminted` como ejecutable y no usa `pip` en sistemas PEP 668.
- **Enlaces rotos** en la documentación y emoji dañado en el README.

- **Componentes**:
  - Los recuadros de aviso (`infobox`, `warningbox`, `dangerbox`, `successbox`,
    `tipbox`, `notebox`) aceptan un título opcional `{Título}`; antes se
    imprimía como texto del cuerpo (13 usos en el propio contenido de ejemplo).
  - `\constpoint` admite la etiqueta como tercer argumento (en la constelación
    QPSK de ejemplo se perdían 00/01/11/10) y los comandos de diagramas de
    tiempo (`\timinglow`, `\timinghigh`, `\timingclock`, `\timingrise`,
    `\timingfall`) usan la sintaxis documentada `{x}{y}{...}`: el diagrama de
    ejemplo salía descolocado. Ambos fallos los ocultaba un
    `\tracinglostchars=0` global, eliminado.
  - Las etiquetas negativas de pgfplots vuelven a usar el signo menos (se
    quitó `assume math mode` global).
  - `terminal`: cada `\prompt` empieza línea por sí solo.
  - `checklist`, `\normaderogada` (tachado), `normativa` (compatible con el
    etiquetado) y `[geologia]` por separado (`\ch`) funcionaban mal o daban
    error.
  - Los módulos ya no cambian el separador decimal de todo el documento; lo
    decide el idioma.
  - Textos fijos de los componentes traducidos según el idioma.
- **Código**: todos los lenguajes tienen variante `Dark`/`DarkNN` (faltaban 13,
  aunque el contenido de ejemplo las anunciaba); el `title=` aparece en el
  índice de códigos; un entorno sin `[]` cuya primera línea empieza por `#`
  (`#include`, `#!/bin/bash`) ya no da error.
- **Portada**: texto alternativo en los logotipos y sin línea vacía cuando no
  hay departamento; la portada en blanco y negro ya no da error si no hay
  `subtitulo` (es opcional) y el departamento admite formato (`\textit{...}`).
- **Scripts**: `revision-rapida.py` deja de dar falsos positivos (de 123 avisos
  sobre la propia plantilla a 3 reales); `instalar.py` comprueba el año de TeX
  Live.

### Cambiado

- **PDF etiquetado sin declarar PDF/UA-2**: `cls/eps-metadata.tex` usa
  `tagging=on` con LaTeX 2025-11 o posterior (`testphase=phase-I` en TeX Live
  2024) y ya no declara `pdfstandard=ua-2`, porque el PDF todavía no cumple
  PDF/UA-2 (KOMA-Script no etiqueta las secciones y varios paquetes no son
  compatibles). Ver `docs/ACCESIBILIDAD.md`.
- **Ya no hay que editar `cls/eps-metadata.tex` al cambiar de idioma**: el
  idioma del PDF se toma de `idioma`. Eliminada la antigua «regla crítica de
  idioma» de toda la documentación.
- **Requisito mínimo unificado: TeX Live 2024** (LaTeX 2024-11) o MiKTeX
  actualizado. Ubuntu 26.04 y Debian 13 sirven con `apt`; en versiones
  anteriores hay que instalar TeX Live desde TUG.
- **`latexminted`**: la documentación ya no recomienda `pip install
  latexminted` (innecesario con TeX Live 2024+ y fallido por PEP 668), sino
  comprobar `latexminted --version` y usar `tlmgr`/`texlive-latex-extra`;
  `pipx` solo con MiKTeX.
- **Verificación de plagio opcional y explícita**: `revision-rapida.py` solo
  envía el texto con `--plagio copyleaks|turnitin|todos` y tras confirmar
  (`--si` sin terminal); tener claves en `.env` no envía nada. Copyleaks exige
  `COPYLEAKS_WEBHOOK_URL` (opcional `COPYLEAKS_SANDBOX=true`).
- **`make clean`** borra también la caché `_minted/` e `informe-revision.md`;
  `latexmk -c` conserva la caché de minted y `latexmk -C` la borra.
- **CI**: compila con `\DocumentMetadata` y comprueba que el PDF está
  etiquetado; matriz de TeX Live (actual y 2024) e idiomas (español,
  valenciano, inglés); informe veraPDF informativo; comprobación de enlaces con
  lychee (un enlace roto hace fallar el job); nuevo workflow que compila los
  ejemplos LaTeX de los archivos para IA (`scripts/comprobar-ejemplos-doc.py`).
- **Descarga más ligera**: `.gitattributes` excluye `docs/assets/`,
  `.github/images/` y `main.pdf` del ZIP de GitHub y del botón «Abrir en
  Overleaf».
- **Accesibilidad**: los ejemplos de figuras de la documentación incluyen
  `alt={...}`; `docs/ACCESIBILIDAD.md` reescrita según el estado real
  (limitaciones conocidas, cabeceras de tabla con `table/header-rows`).
- `\NeedsTeXFormat` exige LaTeX 2024-11-01.

### Añadido

- Filas nuevas en las tablas de diagnóstico: `Package block Error: Some keys
  specified on the itemize environment are unknown` (plantilla antigua con
  LaTeX 2025-11+) e `Infinite glue shrinkage found in box being split` (fallo
  conocido e inocuo de `longtable` 4.24).
- Agente de instalación y `scripts/instalar.py` listados en `llms.txt`.
- Sección «Sin publicar» y versiones 2.2.0 y 2.2.1 en este CHANGELOG.

### Eliminado

- **`optimizar-tikz`** queda obsoleta y sin efecto (la externalización de TikZ
  no es compatible con el etiquetado); se acepta para no romper
  configuraciones antiguas.
- `docs/AUDIT_2025.md` (desfasado).
- Paquetes innecesarios en la clase (`mathrsfs`, `l3keys2e`...): `\mathscr` lo
  proporciona `unicode-math`.
- Imágenes sin uso en `.github/images/` (entre ellas un póster de 13 MB) y
  previsualizaciones huérfanas en `docs/assets/previews/`.

---

## [2.2.2] - 2026-08-02

### Añadido

- **Guía de Overleaf**: Nueva guía `docs/OVERLEAF.md` (importación, selección de
  compilador, límites de compilación, avisos normales y errores frecuentes)
- **Plantilla publicada en la galería de Overleaf**, enlazada desde el README,
  `docs/OVERLEAF.md`, `docs/README.md`, `docs/GUIA_PRINCIPIANTES.md` y `llms.txt`
- **Botón «Abrir en Overleaf»** en el README, que crea el proyecto con el motor
  LuaLaTeX ya seleccionado (`engine=lualatex`)
- **Comprobación de motor** en `cls/eps-metadata.tex`: si se compila con
  pdfLaTeX o XeLaTeX, la compilación se detiene con un mensaje explicativo en
  lugar del error críptico `TeX capacity exceeded, sorry [main memory size=5000000]`

### Corregido

- **Compatibilidad con Overleaf**: `.latexmkrc` redirige los motores `pdflatex`,
  `xelatex` y `latex` a LuaLaTeX. Overleaf ignora la línea mágica
  `% !TeX program = lualatex` y pasa el motor por línea de órdenes (prioritaria
  sobre `$pdf_mode`), por lo que los proyectos importados fallaban al compilar
  con XeLaTeX/pdfLaTeX

---

## [2.2.1] - 2026-07-12

### Añadido

- **DOI de Zenodo** (10.5281/zenodo.21315904): `.zenodo.json`, `CITATION.cff`
  (botón «Cite» en GitHub) e insignia de DOI en el README (#32, #33)

### Cambiado

- **Licencia GPL-3.0 → MIT**, con el consentimiento de los contribuidores:
  `LICENSE`, cabeceras de `.cls`/`.sty`, `Makefile` y scripts (#32, #34)
- Marcadores de versión alineados a 2.2.1 en todo el repositorio (#33, #34)
- CI: `actions/checkout` v7, actualizaciones de Dependabot y workflow de
  asignación automática de PRs

### Corregido

- Workflow de revisión estática: código de salida correcto en CI
- Contenido de ejemplo: títulos de bloques de código, `codigosimple` anidado,
  `\label` en todos los elementos, sección de citas ampliada, argumentos de
  `\metricbox`, colores de `\apibody`/`\apiresponse` y captions de
  `mineraltable`/`geotechdata`
- Errores de markdownlint y anclas rotas en la documentación (#21)

---

## [2.2.0] - 2026-04-10

### Añadido

- **Agentes de IA**: redacción (`.github/agents/redaccion.md`,
  `docs/agents/redaccion-claude.md`), revisor tipo tribunal
  (`.github/agents/revisor.md`, `docs/agents/revisor-claude.md`) e
  instalación guiada (`.github/agents/instalacion.md`,
  `docs/agents/instalacion-claude.md`), con prompts listos para usar
  (`docs/agents/prompts-*.md`) (#18)
- **Revisor estático** `scripts/revision-rapida.py` (genera
  `informe-revision.md` y se ejecuta en GitHub Actions) con integración
  opcional con Copyleaks y Turnitin
- **Script de instalación** `scripts/instalar.py`
- Configuración de markdownlint (`.markdownlint.json`)
- Variantes oscuras para Lua (`lualangcodeDark`, `lualangcodeDarkNN`)

### Cambiado

- `luacode` renombrado a `lualangcode` (evita el conflicto con el paquete
  `luacode`); previsualizaciones de minted regeneradas (#15)
- CI: mejoras en los workflows de build y release (#14)

---

## [2.1.0] - 2026-02-06

### Añadido

- **Guía de accesibilidad**: Nueva guía `docs/ACCESIBILIDAD.md` para crear PDFs accesibles (PDF/UA-2)
- **Glosario de términos**: 28 definiciones de términos técnicos en `acronimos.tex` además de los acrónimos
- **Referencias actualizadas**: Enlaces a documentación oficial en todas las guías (CTAN, TikZ, PGFPlots, BibLaTeX, etc.)
- **Archivos de contexto para IA**: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` y `docs/AI_CONTEXT.md` para ayudar a ChatGPT, Claude, Copilot y otros asistentes a dar respuestas precisas sobre la plantilla
- **CI/CD mejorado**: Comentarios automáticos en PRs con enlace al PDF compilado y tabla de estado de portadas
- **Opciones de género neutro**: `genero = n` muestra "Autoría" en lugar de "Autor/Autora"
- **Género para tutores**: Nuevas opciones `tutor-genero` y `cotutor-genero`
- **Script unificado**: `actualizar_previews.py` combina generación e inserción de previews
- **Paralelización**: Scripts de generación de portadas y previews ahora usan múltiples procesos

### Cambiado

- **TeX Live 2025**: Documentación actualizada para TeX Live 2025 (marzo 2025)
- **Minted 3.x**: Información actualizada sobre minted 3.x con latexminted
- **Documentación mejorada**: Secciones de recursos adicionales ampliadas con herramientas y tutoriales
- **Funding**: Simplificado a solo GitHub Sponsors (eliminado Ko-fi y PayPal)

### Corregido

- **Portadas**: Eliminado borde blanco de 1px en el borde derecho
- **Portadas**: Corregida altura de la barra negra (6.86cm según diseño original)
- **Glosario**: Habilitados números de página en el glosario (eliminado `nonumberlist`)

---

## [2.0.0] - 2026-02-02

### 🚀 Cambios mayores - Modernización completa

Esta versión representa una reescritura completa de la plantilla con tecnologías modernas de LaTeX.

### Añadido

- **Motor LuaLaTeX**: Soporte nativo Unicode, mejor manejo de fuentes
- **Sistema expl3/L3**: Programación moderna con interfaz key-value via `\EPSsetup{}`
- **Clase `eps-tfg.cls`**: Nueva clase documentada que encapsula toda la configuración
- **Paquete `eps-portadas.sty`**: Gestión modular de portadas (color y B/N)
- **Paquete `eps-codigo.sty`**: Resaltado de código con minted + tcolorbox
- **Base de datos de titulaciones**: 21 grados/másteres con colores y logos configurados
- **Makefile**: Comandos simplificados (`make`, `make clean`, `make view`)
- **latexmkrc**: Configuración para compilación automática con latexmk
- **Soporte multi-idioma**: Configuración automática español/inglés con polyglossia
- **Metadatos PDF**: Título, autor, keywords configurados automáticamente

### Cambiado

- **Estructura de carpetas** reorganizada:

  ```text
  cls/          → Clase principal
  sty/          → Paquetes auxiliares  
  contenido/    → Capítulos, anexos, frontmatter
  recursos/     → Logos, figuras, fuentes, ejemplos
  ```

- **Logos** convertidos de EPS a PDF para mejor compatibilidad
- **Bibliografía**: Migración de BibTeX a Biblatex + Biber (estilo APA)
- **Configuración** centralizada en `configuracion.tex` con sintaxis simple

### Eliminado

- Dependencia de pdfLaTeX (ahora requiere LuaLaTeX)
- Archivos de configuración dispersos en `include/`
- Plantilla de póster (a reimplementar en versión futura)
- Fuentes Kurier no utilizadas (~3MB liberados)
- Figuras de ejemplo del proyecto anterior

### Corregido

- Conflicto minted/listings por extensión `.lol`
- Errores de fontspec con fuentes no encontradas (fallback a DejaVu Sans)
- Warning de marginparwidth para todonotes
- Codificación UTF-8 correcta en todos los archivos

### Seguridad

- Actualizado a LaTeX2e 2022/06/01 o posterior

---

## [1.0.0] - Versión original

### Características originales

- Motor pdfLaTeX
- Configuración manual mediante archivos en `include/`
- Logos en formato EPS
- BibTeX para bibliografía
- Soporte para póster académico

---

## Notas de migración

### De 1.x a 2.0

1. **Instalar LuaLaTeX** si no está disponible:

   ```bash
   # Ubuntu/Debian
   sudo apt install texlive-luatex
   
   # macOS con MacTeX
   # Ya incluido
   ```

2. **Cambiar comando de compilación**:

   ```bash
   # Antes
   pdflatex documento.tex
   
   # Ahora
   lualatex -shell-escape main.tex
   # O simplemente:
   make
   ```

3. **Actualizar configuración**: Mover datos de `include/configuracioninicial.tex` a `configuracion.tex` usando la nueva sintaxis:

   ```latex
   \EPSsetup{
     titulacion = informatica,
     titulo = Mi Título,
     autor = Nombre Apellido,
     ...
   }
   ```

4. **Bibliografía**: Convertir `.bib` a formato compatible con Biblatex si es necesario (generalmente compatible).

---

## Roadmap

### Hecho

- [x] GitHub Actions para CI/CD
- [x] Archivos de contexto y agentes para asistentes de IA
- [x] Plantilla publicada en la galería de Overleaf (2.2.2)
- [x] Español, valenciano e inglés funcionales (sin publicar)

### Próximas versiones

- [ ] Conformidad PDF/UA-2 (ver `docs/ACCESIBILIDAD.md`)
- [ ] Reimplementar plantilla de póster
- [ ] Añadir tema de presentación Beamer
- [ ] Temas de color alternativos
- [ ] Integración con Zotero/Mendeley

[Sin publicar]: https://github.com/jmrplens/TFG-TFM_EPS/compare/v2.2.2...HEAD
[2.2.2]: https://github.com/jmrplens/TFG-TFM_EPS/compare/v2.2.1...v2.2.2
[2.2.1]: https://github.com/jmrplens/TFG-TFM_EPS/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/jmrplens/TFG-TFM_EPS/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/jmrplens/TFG-TFM_EPS/compare/v2.0.0...v2.1.0
