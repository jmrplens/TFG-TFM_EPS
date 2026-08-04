# 🌐 Guía de uso en Overleaf

> **Nota:** el flujo de trabajo recomendado para esta plantilla es **en local**
> (TeX Live + un editor como VS Code con LaTeX Workshop, compilando con `make`);
> ver [Inicio Rápido](../README.md#-inicio-rápido) y la
> [Guía para Principiantes](GUIA_PRINCIPIANTES.md). **Overleaf es una
> alternativa** cuando no quieres instalar nada o necesitas colaborar en línea,
> a cambio de los límites de compilación de la plataforma.

Esta plantilla funciona en [Overleaf](https://www.overleaf.com), pero **solo con
LuaLaTeX**. Overleaf compila por defecto con pdfLaTeX (y a veces selecciona
XeLaTeX al importar proyectos con fuentes OpenType), lo que produce errores
confusos. Esta guía explica cómo dejar el proyecto compilando a la primera.

---

## ⚡ Resumen rápido

Si vas a trabajar en Overleaf, **la vía más cómoda es la plantilla publicada en
la galería**, que ya viene configurada con LuaLaTeX:

👉 **[Plantilla en la galería de Overleaf](https://www.overleaf.com/latex/templates/plantilla-latex-2026-tfg-y-tfm-para-la-eps-de-la-universidad-de-alicante-bachelors-slash-masters-thesis-template/qjntjjjpfjvv)**
→ *Open as Template*

Si prefieres subir el proyecto tú mismo:

1. **Sube el proyecto** (zip limpio, sin PDF ni archivos auxiliares).
2. **Menu → Compiler → LuaLaTeX** y **TeX Live version → 2025** (o superior).
3. **Recompile**. La primera compilación es la más lenta (caché de `minted`).

---

## 1. Importar el proyecto

> ℹ️ **El repositorio de GitHub es la fuente de la verdad.** La plantilla de la
> galería se corresponde con la última versión publicada allí y se actualiza
> reenviándola desde Overleaf, así que puede ir por detrás del repositorio
> durante un tiempo. Si necesitas la última versión exacta, usa el ZIP de
> GitHub.

| Método | Cómo |
| --- | --- |
| **Galería de Overleaf** (recomendado) | [Abrir la plantilla publicada](https://www.overleaf.com/latex/templates/plantilla-latex-2026-tfg-y-tfm-para-la-eps-de-la-universidad-de-alicante-bachelors-slash-masters-thesis-template/qjntjjjpfjvv) → *Open as Template*. El compilador y la versión de TeX Live vienen ya configurados |
| Botón directo desde GitHub | [![Abrir en Overleaf](https://img.shields.io/badge/Abrir%20en-Overleaf-47A141?logo=overleaf&logoColor=white)](https://www.overleaf.com/docs?snip_uri=https://github.com/jmrplens/TFG-TFM_EPS/archive/refs/heads/main.zip&engine=lualatex) — crea el proyecto con **todo el contenido de ejemplo** (más pesado de compilar, ver [sección 5](#5-tiempos-de-compilación-límites-de-overleaf)) |
| Subida manual | GitHub → *Code* → *Download ZIP* → Overleaf → *New Project* → *Upload Project* |
| GitHub Sync | Solo en planes de pago: *New Project* → *Import from GitHub* |

> ⚠️ **Sube el proyecto limpio.** Si el zip incluye el PDF y los auxiliares
> (`main.pdf`, `main.aux`, `_minted/`…), Overleaf puede mostrar avisos como
> *«This project contains a file called output.pdf»* y no enseñar el PDF
> generado. Un `git clone` o el ZIP de GitHub ya vienen limpios (están en
> `.gitignore`); si compilaste en local, ejecuta `make clean` antes de subir.

---

## 2. Seleccionar el compilador (paso imprescindible)

**Menu** (esquina superior izquierda) → **Compiler** → **LuaLaTeX**.

Overleaf **ignora** la línea mágica `% !TeX program = lualatex` que hay al
principio de `main.tex`: el motor se elige únicamente desde ese menú (o con el
parámetro `engine=lualatex` en el enlace «Abrir en Overleaf»).

### Red de seguridad incluida en la plantilla

Aunque olvides ese paso, el proyecto trae dos protecciones:

- **`.latexmkrc`**: redirige `pdflatex`, `xelatex` y `latex` a LuaLaTeX, de modo
  que Overleaf compila con LuaLaTeX aunque el menú indique otro motor. Verás en
  los logs un aviso inocuo (`lualatex: unrecognized option '-no-pdf'`) y una
  pasada extra: por eso conviene ajustar el menú de todos modos.
- **`cls/eps-metadata.tex`**: si por lo que sea se ejecuta pdfLaTeX o XeLaTeX
  directamente, la compilación se detiene con un mensaje claro
  (*ESTA PLANTILLA REQUIERE LuaLaTeX*) en lugar del críptico
  `TeX capacity exceeded, sorry [main memory size=5000000]`.

> 🧹 **Tras cambiar de compilador, limpia la caché.** En el panel de logs pulsa
> *Logs and output files* → **Clear cached files**. Los auxiliares que dejó la
> compilación fallida (`output.aux`, `output.xdv`, `output.bcf`…) pueden
> provocar errores extraños en la primera compilación con el motor nuevo.
>
> 💡 **¿Por qué falla con XeLaTeX/pdfLaTeX?** Esos motores tienen una memoria
> principal fija (5.000.000 de palabras) que no se puede ampliar en Overleaf. El
> preámbulo de la plantilla (KOMA + tagging PDF/UA + biblatex + glossaries +
> tcolorbox + minted + los módulos de componentes) no cabe en ella. LuaTeX
> reserva memoria dinámicamente y no tiene ese límite.

---

## 3. Versión de TeX Live

**Menu → TeX Live version → 2025** (o la más reciente disponible).

| Componente | Versión mínima | Motivo |
| --- | --- | --- |
| TeX Live | 2024 (recomendado 2025) | `\DocumentMetadata`, tagging PDF/UA-2 |
| minted | 3.x | Entornos de código (`pythoncode`, `jscode`…) |
| biblatex | 3.19+ | Estilo APA 7 con Biber |

Con TeX Live 2023 o anterior fallará el tagging PDF/UA y `minted` 3.

---

## 4. minted y `shell-escape`

Los entornos de código usan **minted 3**, que necesita `shell-escape`. No hay
que hacer nada: Overleaf lo activa automáticamente al detectar `minted`, y el
`.latexmkrc` de la plantilla también lo pasa explícitamente.

Si aun así aparece `You must invoke LaTeX with -shell-escape`, comprueba que la
versión de TeX Live sea 2024 o posterior.

---

## 5. Tiempos de compilación (límites de Overleaf)

Overleaf corta la compilación al llegar al límite del plan:

| Plan | Límite de compilación |
| --- | --- |
| Gratuito | 10 segundos |
| Premium | 240 segundos (4 minutos) |

*(Valores publicados por Overleaf en
[Plan limits](https://docs.overleaf.com/getting-started/free-and-premium-plans/plan-limits).)*

El proyecto **tal cual se descarga** (más de 130 páginas de contenido de
ejemplo, todos los módulos de componentes y decenas de bloques `minted`) es
demasiado pesado para el plan gratuito, y una compilación completa
(varias pasadas + Biber + glosarios) puede rozar también el límite de 240 s del
plan premium. Para tu TFG/TFM real, en cuanto sustituyas el contenido de
ejemplo, el tiempo baja drásticamente: lo que pesa es la *demostración* de
componentes, no la plantilla.

### Cómo reducir el tiempo de compilación

1. **Carga solo el módulo de tu titulación** en `main.tex` (el ejemplo trae
   `[all]`, que carga todos):

   ```latex
   % \usepackage[all]{eps-componentes}      % <- lento: carga todo
   \usepackage[software]{eps-componentes}   % <- solo lo que necesitas
   ```

2. **Sustituye el contenido de ejemplo** por el tuyo. Los capítulos de
   demostración (`contenido/capitulos/`) existen para enseñar componentes y son
   la mayor parte del coste.
3. **No borres la caché**: Overleaf reutiliza la carpeta `_minted` entre
   compilaciones. La primera compilación siempre es la más lenta.
4. **Comenta capítulos mientras escribes** (`\input`) y descoméntalos al final.
5. Activa **Stop on first error** para no perder tiempo con errores en cadena.

### Estrategia para la primera compilación (compilación progresiva)

El problema no es una pasada suelta, sino que la **primera** compilación necesita
varias pasadas seguidas (LaTeX → glosarios → Biber → LaTeX ×3) para resolver
índices, citas y referencias cruzadas, y todas juntas superan el límite:

| Situación (medido en local, documento de ejemplo completo) | Tiempo |
| --- | --- |
| Primera compilación completa (4-5 pasadas + Biber + glosarios) | varios minutos (≈5-10) |
| Recompilación posterior (1 pasada, auxiliares y caché ya generados) | ~70-90 s |

*(Los tiempos absolutos dependen de la máquina; lo relevante es la proporción:
la primera compilación cuesta 4-5 veces más que las siguientes.)*

Como Overleaf conserva los archivos auxiliares y la caché de `minted` entre
compilaciones, se puede **construir el documento por partes**:

1. Comenta casi todos los `\input` de capítulos en `main.tex` y compila.
2. Descomenta uno o dos capítulos más y vuelve a compilar.
3. Repite hasta tener el documento completo.

Cada compilación reutiliza el trabajo de la anterior (`.aux`, `.toc`, `.bbl`,
`_minted`), así que ninguna llega al límite de tiempo aunque el documento final
sí lo superaría desde cero. Es la forma normal de trabajar en Overleaf con
documentos grandes, y además es cómoda mientras escribes.

> ⚠️ Si en algún momento pulsas **Clear cached files**, la siguiente compilación
> vuelve a ser «desde cero»: repite el proceso progresivo.
>
> ℹ️ Desactivar el etiquetado de accesibilidad (comentar `testphase={phase-I}` y
> `pdfstandard=ua-2` en `cls/eps-metadata.tex`) apenas ahorra tiempo (~5 % en
> las pruebas realizadas) y sacrifica el PDF/UA-2: **no** es la palanca que
> buscas. El contenido —bloques `minted`, figuras TikZ y tablas largas— es lo
> que domina el tiempo de compilación.

---

## 6. Avisos normales (no son errores)

Con LuaLaTeX correctamente seleccionado, estos mensajes aparecen en el panel de
logs y **son inofensivos**:

| Mensaje | Significado |
| --- | --- |
| `You have requested document class 'cls/eps-tfg'` | Informativo: la clase está en una subcarpeta |
| `You have requested package 'sty/eps-...'` | Ídem para los paquetes de la plantilla |
| `Package pdfmanagement Warning: The loading of package hyperxmp is disabled` | Los metadatos XMP los gestiona `pdfmanagement`, no `hyperxmp` |
| `Package tracklang Warning: No 'datatool' support for dialect 'spanish'` | Limitación de `datatool`; no afecta a glosarios ni acrónimos |
| `Index style file output.ist not found` (primera pasada) | `glossaries` lanza `makeindex` antes de escribir el `.ist`; se resuelve en la siguiente pasada |
| `Underfull \hbox` / `Overfull \hbox` | Avisos tipográficos habituales |
| `lualatex: unrecognized option '-no-pdf'` | Solo si el menú *Compiler* no está en LuaLaTeX y actúa el `.latexmkrc` |

El aviso `Package tagpdf Warning: engine/output mode xetex doesn't support the
interword spaces` **sí** indica un problema: significa que estás compilando con
XeLaTeX. Cambia el compilador a LuaLaTeX.

---

## 7. Errores frecuentes

| Error | Causa | Solución |
| --- | --- | --- |
| `TeX capacity exceeded, sorry [main memory size=5000000]` | Compilando con XeLaTeX o pdfLaTeX | Menu → Compiler → **LuaLaTeX** |
| `ESTA PLANTILLA REQUIERE LuaLaTeX` | Ídem (mensaje propio de la plantilla) | Ídem |
| `This compile didn't produce a PDF` + `output.pdf` en el proyecto | Subiste PDFs/auxiliares junto al fuente | Borra `main.pdf`, `output.pdf` y auxiliares del proyecto |
| `Timed out` / *compile timeout* | El documento de ejemplo completo no cabe en el límite del plan | Compilación progresiva y reducción de contenido: ver [sección 5](#5-tiempos-de-compilación-límites-de-overleaf) |
| `File 'eps-tfg.cls' not found` | Se subió solo `main.tex` | Sube el proyecto completo con sus carpetas (`cls/`, `sty/`, `contenido/`…) |
| `Citation 'X' undefined` o glosario vacío | Falta una pasada de Biber/makeglossaries | Pulsa *Recompile* otra vez; Overleaf los ejecuta vía `latexmk` |
| `Package minted Error: ... latexminted` | TeX Live antiguo | Menu → TeX Live version → 2025 |
| Errores raros justo después de cambiar de compilador | Auxiliares de la compilación anterior | *Logs and output files* → **Clear cached files** y recompila |

---

## 8. Diferencias con la compilación local

| | Local (`make`) | Overleaf |
| --- | --- | --- |
| Motor | LuaLaTeX (fijado en el `Makefile`) | El del menú *Compiler* (redirigido a LuaLaTeX por `.latexmkrc`) |
| Orquestación | `make` / `latexmk` | Siempre `latexmk` |
| Nombre del trabajo | `main` | `output` (los logs hablan de `output.log`, `output.pdf`…) |
| Bibliografía y glosarios | `biber` + `makeglossaries` desde `.latexmkrc` | Igual (Overleaf lee el `.latexmkrc` del proyecto) |

---

## 📚 Enlaces

- [Selecting a TeX Live version and LaTeX compiler](https://docs.overleaf.com/getting-started/recompiling-your-project/selecting-a-tex-live-version-and-latex-compiler)
- [Fixing and preventing compile timeouts](https://docs.overleaf.com/troubleshooting-and-support/fixing-and-preventing-compile-timeouts)
- [Plan limits](https://docs.overleaf.com/getting-started/free-and-premium-plans/plan-limits)
- [`docs/GUIA_PRINCIPIANTES.md`](GUIA_PRINCIPIANTES.md) — primeros pasos con la plantilla
