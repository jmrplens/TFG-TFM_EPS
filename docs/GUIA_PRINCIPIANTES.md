# 📚 Guía de LaTeX para Principiantes

**¿Nunca has usado LaTeX?** Esta guía es para ti.

Si vienes de Word, Google Docs o similar, LaTeX puede parecer intimidante al principio. Pero no te preocupes: esta plantilla está diseñada para que puedas empezar a escribir tu TFG/TFM sin ser un experto.

---

## 📖 Índice

- [📖 Índice](#-índice)
- [🤔 ¿Qué es LaTeX y por qué usarlo?](#-qué-es-latex-y-por-qué-usarlo)
  - [¿Qué es?](#qué-es)
  - [¿Por qué usarlo para el TFG/TFM?](#por-qué-usarlo-para-el-tfgtfm)
  - [¿Cuál es el inconveniente?](#cuál-es-el-inconveniente)
- [📝 Conceptos básicos](#-conceptos-básicos)
  - [Archivos y extensiones](#archivos-y-extensiones)
  - [Estructura de un documento LaTeX](#estructura-de-un-documento-latex)
  - [Comandos básicos](#comandos-básicos)
  - [Entornos](#entornos)
  - [Comentarios](#comentarios)
- [💻 Instalación paso a paso](#-instalación-paso-a-paso)
  - [Opción 1: Overleaf (sin instalar nada) ⭐ Recomendado para empezar](#opción-1-overleaf-sin-instalar-nada-recomendado-para-empezar)
  - [Opción 2: Instalación local en Windows](#opción-2-instalación-local-en-windows)
  - [Opción 3: Instalación local en macOS](#opción-3-instalación-local-en-macos)
  - [Opción 4: Instalación local en Linux (Ubuntu/Debian)](#opción-4-instalación-local-en-linux-ubuntudebian)
- [✍️ Eligiendo un editor](#-eligiendo-un-editor)
  - [VS Code + LaTeX Workshop ⭐ Recomendado](#vs-code-latex-workshop-recomendado)
  - [TeXstudio - Alternativa popular](#texstudio---alternativa-popular)
  - [Texmaker - Similar a TeXstudio](#texmaker---similar-a-texstudio)
  - [Comparativa rápida](#comparativa-rápida)
- [🚀 Tu primera compilación](#-tu-primera-compilación)
  - [Con VS Code](#con-vs-code)
  - [Con TeXstudio/Texmaker](#con-texstudiotexmaker)
  - [Desde terminal](#desde-terminal)
  - [¿Por qué hay que compilar varias veces?](#por-qué-hay-que-compilar-varias-veces)
- [✏️ Escribiendo contenido](#-escribiendo-contenido)
  - [Lo que debes editar](#lo-que-debes-editar)
  - [Ejemplo: Escribir un capítulo](#ejemplo-escribir-un-capítulo)
  - [Añadir figuras](#añadir-figuras)
  - [Añadir tablas](#añadir-tablas)
  - [Añadir código fuente](#añadir-código-fuente)
  - [Citar bibliografía](#citar-bibliografía)
- [📚 Recursos de aprendizaje](#-recursos-de-aprendizaje)
  - [Tutoriales recomendados](#tutoriales-recomendados)
  - [Vídeos](#vídeos)
  - [Cheatsheets (hojas de referencia rápida)](#cheatsheets-hojas-de-referencia-rápida)
  - [Herramientas útiles](#herramientas-útiles)
- [🤖 Uso de IA para ayuda](#-uso-de-ia-para-ayuda)
  - [Proporcionar contexto](#proporcionar-contexto)
  - [Qué puedes pedirles](#qué-puedes-pedirles)
- [❗ Errores comunes y soluciones](#-errores-comunes-y-soluciones)
  - ["File not found" / "Archivo no encontrado"](#file-not-found-archivo-no-encontrado)
  - ["Undefined control sequence"](#undefined-control-sequence)
  - ["Missing $ inserted" / "Falta $"](#missing-inserted-falta-)
  - [La bibliografía no aparece](#la-bibliografía-no-aparece)
  - [El código no tiene colores](#el-código-no-tiene-colores)
  - [Compilación muy lenta](#compilación-muy-lenta)
  - ["You must invoke LaTeX with -shell-escape"](#you-must-invoke-latex-with--shell-escape)
- [💡 Consejos finales](#-consejos-finales)

---

## 🤔 ¿Qué es LaTeX y por qué usarlo?

### ¿Qué es?

LaTeX es un sistema de preparación de documentos. A diferencia de Word, donde ves el documento final mientras escribes (WYSIWYG), en LaTeX escribes **código** que luego se **compila** para generar un PDF.

```latex
% Esto es código LaTeX
\section{Introducción}
Este es un párrafo de ejemplo con una ecuación: $E = mc^2$
```

### ¿Por qué usarlo para el TFG/TFM?

| Ventaja | Descripción |
|---------|-------------|
| 📐 **Formato profesional** | Genera documentos con tipografía y maquetación de calidad editorial |
| 🔢 **Ecuaciones** | El mejor sistema para escribir fórmulas matemáticas |
| 📚 **Bibliografía** | Gestión automática de citas y referencias |
| 🔗 **Referencias cruzadas** | "Ver Figura 3.2" se actualiza automáticamente |
| 📑 **Índices** | Genera índices de contenido, figuras y tablas automáticamente |
| 🎨 **Consistencia** | El formato es siempre uniforme en todo el documento |
| 🔄 **Control de versiones** | Funciona perfectamente con Git |

### ¿Cuál es el inconveniente?

Hay una **curva de aprendizaje inicial**. Necesitas aprender algunos comandos básicos y acostumbrarte a no ver el resultado final mientras escribes. Pero esta plantilla minimiza ese esfuerzo: la mayor parte de la configuración ya está hecha.

---

## 📝 Conceptos básicos

### Archivos y extensiones

| Extensión | Qué es |
|-----------|--------|
| `.tex` | Archivo de código LaTeX (tu contenido) |
| `.pdf` | El documento final generado |
| `.bib` | Base de datos de bibliografía |
| `.cls` | Clase de documento (define el formato) |
| `.sty` | Paquete (añade funcionalidades) |

### Estructura de un documento LaTeX

```latex
% PREÁMBULO (configuración)
\documentclass{eps-tfg}        % Tipo de documento
\usepackage{graphicx}          % Paquetes adicionales

% DOCUMENTO (contenido)
\begin{document}
  Tu contenido aquí...
\end{document}
```

### Comandos básicos

Los comandos en LaTeX empiezan con `\` (barra invertida):

```latex
\textbf{texto en negrita}
\textit{texto en cursiva}
\section{Título de sección}
\ref{etiqueta}                 % Referencia cruzada
\cite{clave}                   % Cita bibliográfica
```

### Entornos

Los entornos encierran contenido especial entre `\begin{}` y `\end{}`:

```latex
\begin{figure}
  \includegraphics{imagen.png}
  \caption{Descripción de la imagen}
\end{figure}

\begin{equation}
  E = mc^2
\end{equation}
```

### Comentarios

Todo lo que viene después de `%` en una línea es un comentario (no aparece en el PDF):

```latex
% Esto es un comentario
Esto sí aparece en el PDF  % Esto también es comentario
```

---

## 💻 Instalación paso a paso

### Opción 0: Script de instalación automática ⭐ Recomendado para instalación local

Si vas a trabajar en tu propio ordenador, la forma más sencilla es ejecutar el script de instalación incluido en el proyecto. Se encarga de comprobar qué tienes instalado y guiarte para instalar lo que falta:

```bash
# Linux / macOS
python3 scripts/instalar.py

# Windows (desde PowerShell o CMD)
python scripts/instalar.py
```

> **¿No tienes Python todavía?** Descárgalo desde [python.org](https://www.python.org/downloads/) y asegúrate de marcar **"Add Python to PATH"** durante la instalación. Luego vuelve a ejecutar el script.

Si prefieres que una IA te guíe paso a paso, usa el **agente de instalación**:
- En GitHub Copilot Chat: carga [`.github/agents/instalacion.md`](../.github/agents/instalacion.md) y pide ayuda
- En Claude: consulta [agents/instalacion-claude.md](agents/instalacion-claude.md) o usa los [prompts listos](agents/prompts-instalacion.md)

Si prefieres instalar manualmente, sigue las opciones a continuación.

### Opción 1: Overleaf (sin instalar nada) ⭐ Recomendado para empezar

[Overleaf](https://www.overleaf.com) es un editor LaTeX online. No necesitas instalar nada.

1. Crea una cuenta en [overleaf.com](https://www.overleaf.com)
2. Sube los archivos de la plantilla (o usa "Upload Project" con el ZIP)
3. Configura el compilador como **LuaLaTeX** (menú ☰ → Settings)
4. ¡Listo! Puedes empezar a editar

**Ventajas:** Sin instalación, funciona en cualquier ordenador, colaboración en tiempo real.

**Desventajas:** Necesitas internet, versión gratuita tiene límite de tiempo de compilación.

### Opción 2: Instalación local en Windows

#### Paso 1: Instalar MiKTeX

1. Descarga [MiKTeX](https://miktex.org/download) 
2. Ejecuta el instalador
3. **Importante:** Selecciona "Install missing packages on-the-fly: Yes"
4. Completa la instalación (puede tardar 15-30 minutos)

#### Paso 2: Instalar Python y latexminted (para código fuente con colores)

1. Descarga [Python](https://www.python.org/downloads/)
2. **Importante:** Marca ✅ "Add Python to PATH" durante la instalación
3. Abre PowerShell o CMD y ejecuta:
   ```
   pip install latexminted
   ```

#### Paso 3: Instalar un editor (ver sección siguiente)

### Opción 3: Instalación local en macOS

#### Paso 1: Instalar MacTeX

1. Descarga [MacTeX](https://www.tug.org/mactex/) (~4GB)
2. Abre el archivo .pkg y sigue las instrucciones
3. Reinicia el terminal

#### Paso 2: Instalar latexminted

```bash
pip3 install latexminted
```

### Opción 4: Instalación local en Linux (Ubuntu/Debian)

```bash
# Instalar TeX Live completo (recomendado, ~5GB)
sudo apt install texlive-full

# O instalación más pequeña (~1GB)
sudo apt install texlive-latex-extra texlive-fonts-extra \
                 texlive-luatex texlive-bibtex-extra biber

# latexminted para código con colores (minted 3.x)
pip3 install latexminted
```

> **Nota:** Ubuntu/Debian pueden tener versiones antiguas de TeX Live en sus repositorios. Para obtener TeX Live 2025, considera usar la [instalación oficial de TeX Live](https://www.tug.org/texlive/quickinstall.html) en lugar de los paquetes de la distribución.

---

## ✍️ Eligiendo un editor

### VS Code + LaTeX Workshop ⭐ Recomendado

**Visual Studio Code** es un editor moderno y gratuito. Con la extensión **LaTeX Workshop** se convierte en un excelente entorno para LaTeX.

#### Instalación:

1. Descarga [VS Code](https://code.visualstudio.com/)
2. Abre VS Code
3. Ve a Extensions (Ctrl+Shift+X)
4. Busca "LaTeX Workshop" e instálala
5. Abre la carpeta de la plantilla (File → Open Folder)

#### Ventajas:
- Previsualización del PDF integrada
- Autocompletado inteligente
- Detección de errores en tiempo real
- La plantilla ya incluye configuración optimizada (`.vscode/settings.json`)

### TeXstudio - Alternativa popular

[TeXstudio](https://www.texstudio.org/) es un editor dedicado exclusivamente a LaTeX.

#### Ventajas:
- Diseñado específicamente para LaTeX
- Muy completo "out of the box"
- Vista de estructura del documento

#### Configuración inicial:
1. Descarga e instala TeXstudio
2. Ve a Options → Configure TeXstudio
3. En "Build", cambia:
   - Default Compiler: **LuaLaTeX**
   - Default Bibliography Tool: **Biber**
4. En "Commands", añade `-shell-escape` al comando de LuaLaTeX

### Texmaker - Similar a TeXstudio

[Texmaker](https://www.xm1math.net/texmaker/) es otra opción popular, similar a TeXstudio.

### Comparativa rápida

| Editor | Facilidad | Características | Para quién |
|--------|-----------|-----------------|------------|
| **Overleaf** | ⭐⭐⭐⭐⭐ | Online, colaborativo | Principiantes, equipos |
| **VS Code** | ⭐⭐⭐⭐ | Muy extensible | Programadores, avanzados |
| **TeXstudio** | ⭐⭐⭐⭐ | Todo incluido | Uso general |
| **Texmaker** | ⭐⭐⭐⭐ | Sencillo | Principiantes locales |

---

## 🚀 Tu primera compilación

### Con VS Code

1. Abre la carpeta de la plantilla
2. Abre el archivo `main.tex`
3. Pulsa **Ctrl+Alt+B** (o Ctrl+S para guardar, que compila automáticamente)
4. Espera a que termine (primera vez puede tardar 1-2 minutos)
5. El PDF aparecerá en el panel derecho

### Con TeXstudio/Texmaker

1. Abre `main.tex`
2. Pulsa **F5** (o Build & View)
3. Si da error, asegúrate de que el compilador es LuaLaTeX

### Desde terminal

```bash
# Compilación completa (recomendado)
make

# O manualmente
lualatex -shell-escape main.tex
biber main
lualatex -shell-escape main.tex
lualatex -shell-escape main.tex
```

### ¿Por qué hay que compilar varias veces?

LaTeX necesita múltiples pasadas para:
1. **Primera pasada**: Procesa el documento, crea archivos auxiliares
2. **Biber**: Procesa la bibliografía
3. **Segunda pasada**: Resuelve citas bibliográficas
4. **Tercera pasada**: Actualiza referencias cruzadas y números de página

**latexmk** (la herramienta que usa esta plantilla por defecto) hace esto automáticamente.

---

## ✏️ Escribiendo contenido

### Lo que debes editar

| Archivo | Qué contiene |
|---------|--------------|
| `configuracion.tex` | Tu nombre, título, titulación, tutor... |
| `contenido/capitulos/*.tex` | El texto de cada capítulo |
| `contenido/anexos/*.tex` | Anexos |
| `contenido/frontmatter/preliminares.tex` | Agradecimientos, resumen |
| `referencias.bib` | Tu bibliografía |

### Ejemplo: Escribir un capítulo

Abre `contenido/capitulos/introduccion.tex`:

```latex
\chapter{Introducción}
\label{chap:introduccion}

Este es el primer párrafo de mi introducción.

La tecnología \gls{ml} ha revolucionado muchos campos.

\section{Motivación}

Como se demuestra en \cite{garcia2024}, el problema es relevante.

\section{Estructura del documento}

Este documento se organiza de la siguiente manera:
\begin{itemize}
  \item Capítulo~\ref{chap:marco-teorico}: Marco teórico
  \item Capítulo~\ref{chap:metodologia}: Metodología
\end{itemize}
```

### Añadir figuras

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{recursos/figuras/mi-imagen}
  \caption{Descripción de la figura}
  \label{fig:mi-imagen}
\end{figure}

% En el texto:
Como se muestra en la Figura~\ref{fig:mi-imagen}...
```

### Añadir tablas

```latex
\begin{table}[htbp]
  \centering
  \caption{Comparativa de métodos}
  \label{tab:comparativa}
  \begin{tabular}{lcc}
    \toprule
    Método & Precisión & Tiempo \\
    \midrule
    A & 95\% & 10s \\
    B & 87\% & 5s \\
    \bottomrule
  \end{tabular}
\end{table}
```

### Añadir código fuente

```latex
\begin{pythoncode}{Ejemplo de código Python}{cod:ejemplo}
def hola_mundo():
    print("¡Hola, mundo!")
    
if __name__ == "__main__":
    hola_mundo()
\end{pythoncode}

% En el texto:
El Código~\ref{cod:ejemplo} muestra un ejemplo básico.
```

### Citar bibliografía

1. Añade la referencia en `referencias.bib`:
```bibtex
@article{garcia2024,
  author  = {García, Juan},
  title   = {Un estudio importante},
  journal = {Revista de Ejemplo},
  year    = {2024},
  volume  = {10},
  pages   = {1--15}
}
```

2. Cita en el texto:
```latex
Según García \cite{garcia2024}, el resultado es...
```

---

## 📚 Recursos de aprendizaje

### Tutoriales recomendados

| Recurso | Idioma | Descripción |
|---------|--------|-------------|
| [Overleaf Learn](https://www.overleaf.com/learn) | EN/ES | Tutorial completo y ejemplos |
| [LaTeX en 30 minutos](https://www.overleaf.com/learn/latex/Learn_LaTeX_in_30_minutes) | EN | Introducción rápida |
| [LaTeX Project](https://www.latex-project.org/help/documentation/) | EN | Documentación oficial |
| [Manual TEC Costa Rica](https://tecdigital.tec.ac.cr/revistamatematica/Libros/LATEX/LaTeX_2014.pdf) | ES | Libro completo en español |
| [WikiBooks LaTeX](https://en.wikibooks.org/wiki/LaTeX) | EN | Referencia exhaustiva |
| [CTAN](https://ctan.org/) | EN | Repositorio de paquetes |
| [WikiBooks LaTeX](https://en.wikibooks.org/wiki/LaTeX) | EN | Referencia exhaustiva |

### Vídeos

- [Canal de Overleaf en YouTube](https://www.youtube.com/c/Overleaf) - Tutoriales oficiales
- Busca "LaTeX tutorial español" en YouTube para contenido en español

### Cheatsheets (hojas de referencia rápida)

- [LaTeX Cheat Sheet](https://wch.github.io/latexsheet/)
- [Símbolos matemáticos](https://www.overleaf.com/learn/latex/List_of_Greek_letters_and_math_symbols)

### Herramientas útiles

| Herramienta | Para qué sirve |
|-------------|----------------|
| [Overleaf Learn](https://www.overleaf.com/learn) | Documentación excelente (aunque uses editor local) |
| [Detexify](https://detexify.kirelabs.org/) | Dibuja un símbolo y te dice el comando |
| [Tables Generator](https://www.tablesgenerator.com/) | Crea tablas visualmente |
| [Mathpix](https://mathpix.com/) | Convierte imágenes de ecuaciones a LaTeX |
| [BibTeX Online](https://www.bibtex.com/c/doi-to-bibtex-converter/) | Genera BibTeX desde DOI |
| [Zotero](https://www.zotero.org/) | Gestor de bibliografía (exporta a BibTeX) |

---

## 🤖 Uso de IA para ayuda

Si utilizas herramientas como ChatGPT, Claude o GitHub Copilot para redactar o solucionar problemas con tu TFG, te recomendamos lo siguiente:

### Agentes especializados

El proyecto incluye agentes preconfigurados para las tareas más comunes:

| Tarea | GitHub Copilot | Claude |
|-------|---------------|--------|
| Instalar el entorno | [instalacion.md](../.github/agents/instalacion.md) | [instalacion-claude.md](agents/instalacion-claude.md) |
| Redactar capítulos | [redaccion.md](../.github/agents/redaccion.md) | [redaccion-claude.md](agents/redaccion-claude.md) |
| Revisar antes de la defensa | [revisor.md](../.github/agents/revisor.md) | [revisor-claude.md](agents/revisor-claude.md) |

Cada agente tiene también una carpeta de **prompts listos para copiar y pegar** en `docs/agents/prompts-*.md`. Úsalos si no tienes integración directa con la IA.

### Proporcionar contexto
Las IAs funcionan mejor si saben cómo está configurado tu proyecto. 
1. Abre el archivo **`AGENTS.md`** (en la raíz del proyecto).
2. Copia todo su contenido.
3. Pégalo al inicio de tu conversación con la IA.

Esto le enseñará a la IA qué paquetes usamos, cómo se hacen las portadas y las reglas específicas de la Universidad de Alicante.

### Qué puedes pedirles
- **Instalar el entorno:** "Necesito instalar todo para usar la plantilla en Windows 11"
- **Generar tablas:** "Hazme una tabla LaTeX con 3 columnas (Concepto, Descripción, Valor) para..."
- **Corregir errores:** Pega el error de la consola y la IA te dirá qué falla.
- **Escribir fórmulas:** "Escribe la fórmula de la Entropía de Shannon en LaTeX".
- **Resumir textos:** "Resumen este texto para ponerlo en el Abstract".

---

## ❗ Errores comunes y soluciones

### "File not found" / "Archivo no encontrado"

**Causa:** LaTeX no encuentra un archivo que intentas incluir.

**Solución:** 
- Verifica que la ruta es correcta
- No incluyas la extensión `.tex` en `\input{}`
- Usa rutas relativas desde `main.tex`

### "Undefined control sequence"

**Causa:** Usas un comando que LaTeX no conoce.

**Solución:**
- Revisa que no haya errores tipográficos
- Asegúrate de que el paquete necesario está cargado

### "Missing $ inserted" / "Falta $"

**Causa:** Hay contenido matemático fuera del modo matemático.

**Solución:**
- Encierra las fórmulas entre `$...$` (inline) o `\[...\]` (display)
- Caracteres como `_` y `^` necesitan modo matemático

### La bibliografía no aparece

**Solución:**
1. Asegúrate de que has citado algo con `\cite{}`
2. Compila varias veces o usa `make`
3. Verifica que `referencias.bib` no tiene errores de sintaxis

### El código no tiene colores

**Solución:**
- Instala latexminted: `pip install latexminted`
- Verifica con: `latexminted --version`

### Compilación muy lenta

**Solución:**
- La primera compilación siempre es lenta
- Activa `optimizar-tikz = true` en `configuracion.tex`
- Las siguientes compilaciones serán más rápidas

### "You must invoke LaTeX with -shell-escape"

**Solución:**
- Usa `make` que ya incluye esta opción
- O configura tu editor para añadir `-shell-escape`

---

## 💡 Consejos finales

1. **Compila frecuentemente**: Es más fácil encontrar errores cuando has cambiado poco
2. **Un capítulo, un archivo**: Mantén cada capítulo en su archivo `.tex`
3. **Usa Git**: Versiona tu trabajo, nunca perderás nada
4. **No te obsesiones con el formato**: Escribe primero, ajusta después
5. **Guarda la bibliografía desde el principio**: Es más fácil que añadirla al final
6. **Pide ayuda**: Abre un Issue si algo no funciona

---

<p align="center">
  <b>¿Tienes dudas? Abre un <a href="https://github.com/jmrplens/TFG-TFM_EPS/issues/new?template=question.yml">Issue</a> y te ayudamos.</b>
</p>

<p align="center">
  <i>¡Ánimo con tu TFG/TFM! 🎓</i>
</p>
