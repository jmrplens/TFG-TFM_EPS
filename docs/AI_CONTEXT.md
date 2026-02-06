# 📖 Contexto Técnico para IA - Plantilla TFG/TFM EPS UA

Este documento proporciona información técnica detallada para que los asistentes de IA puedan dar respuestas precisas sobre esta plantilla LaTeX.


## 📋 Índice

- [� Contexto Técnico para IA - Plantilla TFG/TFM EPS UA](#-contexto-técnico-para-ia-plantilla-tfgtfm-eps-ua)
  - [📋 Índice](#-índice)
  - [🏗️ Arquitectura de la Plantilla](#️-arquitectura-de-la-plantilla)
    - [Clase Principal: `eps-tfg.cls`](#clase-principal-eps-tfgcls)
    - [Paquetes de Estilo (`sty/`)](#paquetes-de-estilo-sty)
  - [📋 Referencia Completa de `\EPSsetup{}`](#-referencia-completa-de-epssetup)
    - [Información del Documento](#información-del-documento)
    - [Información del Autor](#información-del-autor)
    - [Información del Tutor](#información-del-tutor)
    - [Información del Cotutor (opcional)](#información-del-cotutor-opcional)
    - [Metadatos](#metadatos)
    - [Idioma](#idioma)
  - [🎨 Titulaciones y sus Identificadores](#-titulaciones-y-sus-identificadores)
    - [Grados (TFG)](#grados-tfg)
    - [Másteres (TFM)](#másteres-tfm)
  - [📝 Entornos de Código Disponibles](#-entornos-de-código-disponibles)
    - [Entornos con colores claros (fondo blanco/gris)](#entornos-con-colores-claros-fondo-blancogris)
    - [Entornos con colores oscuros (tema dark)](#entornos-con-colores-oscuros-tema-dark)
    - [Código inline](#código-inline)
    - [Opciones comunes](#opciones-comunes)
  - [📊 Entornos de Ecuaciones](#-entornos-de-ecuaciones)
    - [Ecuación simple numerada](#ecuación-simple-numerada)
    - [Ecuaciones alineadas](#ecuaciones-alineadas)
    - [Ecuación sin numerar](#ecuación-sin-numerar)
    - [Sistema de ecuaciones](#sistema-de-ecuaciones)
    - [Teoremas y definiciones](#teoremas-y-definiciones)
  - [🧩 Componentes Especializados (Nuevo en v2.1)](#-componentes-especializados-nuevo-en-v21)
    - [Activación](#activación)
    - [Módulos Disponibles](#módulos-disponibles)
      - [Comunes (Siempre activos)](#comunes-siempre-activos)
      - [`[software]`](#software)
      - [`[telecom]`](#telecom)
      - [`[arquitectura]`](#arquitectura)
      - [`[quimica]`](#quimica)
  - [📚 Sistema de Bibliografía](#-sistema-de-bibliografía)
    - [Formato del archivo `.bib`](#formato-del-archivo-bib)
    - [Comandos de cita](#comandos-de-cita)
  - [🔤 Glosarios y Acrónimos](#-glosarios-y-acrónimos)
    - [Definir términos en `anexos/acronimos.tex`](#definir-términos-en-anexosacronimostex)
    - [Usar en el documento](#usar-en-el-documento)
  - [🖼️ Figuras y Gráficas](#️-figuras-y-gráficas)
    - [Figura simple](#figura-simple)
    - [Subfiguras](#subfiguras)
    - [Gráfica con PGFPlots](#gráfica-con-pgfplots)
  - [📋 Tablas](#-tablas)
    - [Tabla con booktabs (recomendado)](#tabla-con-booktabs-recomendado)
    - [Tabla larga (múltiples páginas)](#tabla-larga-múltiples-páginas)
  - [⚡ Compilación](#-compilación)
    - [Orden de compilación completa](#orden-de-compilación-completa)
    - [Con latexmk (recomendado)](#con-latexmk-recomendado)
    - [Configuración de latexmk (`.latexmkrc`)](#configuración-de-latexmk-latexmkrc)
  - [🐛 Diagnóstico de Errores](#-diagnóstico-de-errores)
    - [Errores de compilación](#errores-de-compilación)
    - [Errores de minted](#errores-de-minted)
    - [Errores de bibliografía](#errores-de-bibliografía)
  - [🔧 Personalización Avanzada](#-personalización-avanzada)
    - [Añadir un nuevo capítulo](#añadir-un-nuevo-capítulo)
    - [Añadir un nuevo anexo](#añadir-un-nuevo-anexo)
    - [Cambiar estilo de bibliografía](#cambiar-estilo-de-bibliografía)

---

## 🏗️ Arquitectura de la Plantilla

### Clase Principal: `eps-tfg.cls`

La clase utiliza **LaTeX3** (`expl3`) para la configuración:

```latex
% Sintaxis interna (NO exponer a usuarios)
\keys_define:nn { eps-tfg } {
    titulo .tl_gset:N = \g__eps_titulo_tl,
    autor .tl_gset:N = \g__eps_autor_tl,
    % ... más claves
}
```

El usuario interactúa mediante:
```latex
\EPSsetup{
    clave = valor,
    otra-clave = {valor con espacios},
}
```

### Paquetes de Estilo (`sty/`)

| Archivo | Función |
|---------|---------|
| `eps-portadas.sty` | Generación de portadas con TikZ |
| `eps-fuentes.sty` | Configuración de tipografía |
| `eps-colores.sty` | Paleta de colores por titulación |
| `eps-codigo.sty` | Entornos de código con minted |
| `eps-componentes.sty` | Componentes visuales y especializados (Modular) |
| `eps-estilos.sty` | Estilos generales del documento |

---

## 📋 Referencia Completa de `\EPSsetup{}`

### Información del Documento

| Clave | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `titulo` | texto | ✅ | Título principal del trabajo |
| `subtitulo` | texto | ❌ | Subtítulo opcional |
| `fecha` | texto | ✅ | Fecha de presentación (ej: "Junio 2026") |
| `titulacion` | id | ✅ | Identificador de la titulación |

### Información del Autor

| Clave | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `autor` | texto | ✅ | Nombre completo del autor |
| `genero` | m/f/n | ❌ | Género para etiquetas (default: m) |
| `email` | texto | ❌ | Email institucional |

### Información del Tutor

| Clave | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `tutor` | texto | ✅ | Nombre completo del tutor |
| `tutor-genero` | m/f/n | ❌ | Género del tutor (default: m) |
| `tutor-departamento` | texto | ✅ | Departamento del tutor |
| `tutor-centro` | texto | ❌ | Centro del tutor (si difiere) |

### Información del Cotutor (opcional)

| Clave | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `cotutor` | texto | ❌ | Nombre completo del cotutor |
| `cotutor-genero` | m/f/n | ❌ | Género del cotutor (default: m) |
| `cotutor-departamento` | texto | ❌ | Departamento del cotutor |
| `cotutor-centro` | texto | ❌ | Centro del cotutor |

### Metadatos

| Clave | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `palabras-clave` | lista | ❌ | Palabras clave en español |
| `keywords` | lista | ❌ | Keywords en inglés |

### Idioma

| Clave | Tipo | Obligatorio | Descripción |
|-------|------|-------------|-------------|
| `idioma` | texto | ❌ | Idioma del documento: `espanol` (defecto), `valenciano`, `ingles` |

> ⚠️ **Importante:** Si se cambia el idioma, también se debe actualizar el código de idioma en `cls/eps-metadata.tex` para que los metadatos PDF/UA-2 sean correctos:
> - `idioma = espanol` → `lang=es-ES`
> - `idioma = valenciano` → `lang=ca-ES`
> - `idioma = ingles` → `lang=en-GB`

---

## 🎨 Titulaciones y sus Identificadores

### Grados (TFG)

| ID | Nombre Completo | Color Principal |
|----|-----------------|-----------------|
| `arquitectura` | Grado en Fundamentos de la Arquitectura | #B5121B |
| `arquitectura-tecnica` | Grado en Arquitectura Técnica | #BA6831 |
| `civil` | Grado en Ingeniería Civil | #6E9B3A |
| `informatica` | Grado en Ingeniería Informática | #1A4776 |
| `multimedia` | Grado en Ingeniería Multimedia | #78A5C1 |
| `quimica` | Grado en Ingeniería Química | #45818E |
| `robotica` | Grado en Ingeniería Robótica | #7030A0 |
| `teleco` | Grado en Ingeniería en Sonido e Imagen | #1B9CD9 |

### Másteres (TFM)

| ID | Nombre Completo |
|----|-----------------|
| `master-agua` | Máster en Gestión Sostenible del Agua |
| `master-caminos` | Máster en Ingeniería de Caminos, Canales y Puertos |
| `master-ciberseguridad` | Máster en Ciberseguridad |
| `master-edificacion` | Máster en Gestión de la Edificación |
| `master-geologica` | Máster en Ingeniería Geológica |
| `master-informatica` | Máster en Ingeniería Informática |
| `master-materiales` | Máster en Ingeniería de Materiales |
| `master-moviles` | Máster en Desarrollo de Aplicaciones Móviles |
| `master-prevencion` | Máster en Prevención de Riesgos Laborales |
| `master-quimica` | Máster en Ingeniería Química |
| `master-robotica` | Máster en Automática y Robótica |
| `master-teleco` | Máster en Ingeniería de Telecomunicación |
| `master-web` | Máster en Desarrollo de Aplicaciones Web |

---

## 📝 Entornos de Código Disponibles

### Entornos con colores claros (fondo blanco/gris)

```latex
\begin{pythoncode}[title={Título opcional}]
def funcion():
    pass
\end{pythoncode}

\begin{jscode}
console.log("JavaScript");
\end{jscode}

\begin{cppcode}
int main() { return 0; }
\end{cppcode}

\begin{matlabcode}
x = linspace(0, 2*pi, 100);
\end{matlabcode}
```

### Entornos con colores oscuros (tema dark)

```latex
\begin{pythoncodeDark}
# Código con fondo oscuro
\end{pythoncodeDark}
```

### Código inline

```latex
En Python usamos \mintinline{python}{print("Hola")} para imprimir.
```

### Opciones comunes

```latex
\begin{pythoncode}[
    title={mi_script.py},      % Título del bloque
    firstline=5,               % Empezar desde línea 5
    lastline=15,               % Terminar en línea 15
    highlightlines={3,7-9},    % Resaltar líneas
    linenos=false,             % Sin números de línea
]
```

---

## 📊 Entornos de Ecuaciones

### Ecuación simple numerada
```latex
\begin{equation}
    E = mc^2
    \label{eq:einstein}
\end{equation}
```

### Ecuaciones alineadas
```latex
\begin{align}
    f(x) &= x^2 + 2x + 1 \\
         &= (x + 1)^2
    \label{eq:cuadrado}
\end{align}
```

### Ecuación sin numerar
```latex
\begin{equation*}
    a^2 + b^2 = c^2
\end{equation*}
```

### Sistema de ecuaciones
```latex
\begin{cases}
    x + y = 10 \\
    x - y = 2
\end{cases}
```

### Teoremas y definiciones
```latex
\begin{teorema}[Pitágoras]
    En un triángulo rectángulo...
    \label{teo:pitagoras}
\end{teorema}

\begin{definicion}
    Se define derivada como...
\end{definicion}

\begin{lema}
    ...
\end{lema}
```

---

## 🧩 Componentes Especializados (Nuevo en v2.1)

El paquete `eps-componentes` introduce un sistema modular para cargar solo los entornos necesarios.

### Activación
En `main.tex`:
```latex
% Opciones: software, telecom, arquitectura, quimica, geologia, prevencion, all
\usepackage[software,telecom]{eps-componentes}
```

### Módulos Disponibles

#### Comunes (Siempre activos)
- **Cajas de aviso:** `infobox`, `warningbox`, `dangerbox`, `successbox`, `tipbox`, `notebox`.
- **Contenedores:** `titlebox`, `definitionbox`, `examplebox`.

#### `[software]`
- **Entornos:** `terminal` (simula consola), `apiendpoint` (documentación REST), `dirtreebox` (árbol de archivos).
- **Código:** `jsoncode`, `sqlcode`, `yamlcode`, `bashcode`.
- **Diagramas:** `umlclass`, `umlseq` (basados en TikZ/pgf-umlcd).

#### `[telecom]`
- **Redes:** `protocolframe` (tramas de bits), `rackcabinet` (armarios).
- **Circuitos:** `circuit` (wrapper de circuitikz).
- **RF:** Carta de Smith (`smithchart`).

#### `[arquitectura]`
- **Planificación:** `ganttchart` (diagramas de Gantt).
- **Planos:** `compass` (norte), `scalebar`.

#### `[quimica]`
- **Fórmulas:** `chemscheme`, `reaction` (chemfig/chemmacros).
- **Seguridad:** `riskmatrix` (matriz de riesgos).

---

## 📚 Sistema de Bibliografía

### Formato del archivo `.bib`

```bibtex
@article{smith2024,
    author = {Smith, John and Doe, Jane},
    title = {Título del Artículo},
    journal = {Nombre de la Revista},
    year = {2024},
    volume = {10},
    pages = {100--120},
    doi = {10.1234/ejemplo},
}

@book{garcia2023,
    author = {García, María},
    title = {Título del Libro},
    publisher = {Editorial},
    year = {2023},
    isbn = {978-84-xxxxx-xx-x},
}

@inproceedings{conference2024,
    author = {López, Pedro},
    title = {Título de la Ponencia},
    booktitle = {Nombre del Congreso},
    year = {2024},
    pages = {50--55},
}

@online{web2024,
    author = {{Organización}},
    title = {Título de la Página},
    url = {https://ejemplo.com},
    urldate = {2024-01-15},
    year = {2024},
}
```

### Comandos de cita

| Comando | Resultado | Uso |
|---------|-----------|-----|
| `\parencite{key}` | (Autor, 2024) | Cita parentética |
| `\textcite{key}` | Autor (2024) | Cita textual |
| `\cite{key}` | [1] | Cita numérica |
| `\citeauthor{key}` | Autor | Solo autor |
| `\citeyear{key}` | 2024 | Solo año |
| `\parencite[p.~50]{key}` | (Autor, 2024, p. 50) | Con página |
| `\parencite{key1,key2}` | (Autor1, 2024; Autor2, 2023) | Múltiples |

---

## 🔤 Glosarios y Acrónimos

### Definir términos en `anexos/acronimos.tex`

```latex
% Acrónimos
\newacronym{ia}{IA}{Inteligencia Artificial}
\newacronym{ml}{ML}{Machine Learning}
\newacronym{api}{API}{Application Programming Interface}

% Términos del glosario
\newglossaryentry{latex}{
    name={LaTeX},
    description={Sistema de composición de textos de alta calidad}
}
```

### Usar en el documento

```latex
% Primera vez: "Inteligencia Artificial (IA)"
% Siguientes: "IA"
La \gls{ia} está revolucionando...

% Forzar forma específica
\acrshort{ia}  % IA
\acrlong{ia}   % Inteligencia Artificial
\acrfull{ia}   % Inteligencia Artificial (IA)

% Términos del glosario
\gls{latex}    % LaTeX (enlazado al glosario)
```

---

## 🖼️ Figuras y Gráficas

### Figura simple
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{archivos/figuras/imagen}
    \caption{Descripción de la figura.}
    \label{fig:ejemplo}
\end{figure}
```

### Subfiguras
```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth]{imagen1}
        \caption{Primera imagen}
        \label{fig:sub1}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth]{imagen2}
        \caption{Segunda imagen}
        \label{fig:sub2}
    \end{subfigure}
    \caption{Figura con dos subfiguras.}
    \label{fig:conjunto}
\end{figure}
```

### Gráfica con PGFPlots
```latex
\begin{figure}[htbp]
    \centering
    \begin{tikzpicture}
        \begin{axis}[
            xlabel={Eje X},
            ylabel={Eje Y},
            grid=major,
        ]
            \addplot[blue, thick] {x^2};
            \addlegendentry{$f(x) = x^2$}
        \end{axis}
    \end{tikzpicture}
    \caption{Gráfica de función cuadrática.}
    \label{fig:grafica}
\end{figure}
```

---

## 📋 Tablas

### Tabla con booktabs (recomendado)
```latex
\begin{table}[htbp]
    \centering
    \caption{Título de la tabla.}
    \label{tab:ejemplo}
    \begin{tabular}{lcc}
        \toprule
        Columna 1 & Columna 2 & Columna 3 \\
        \midrule
        Dato 1 & 100 & 50\% \\
        Dato 2 & 200 & 75\% \\
        Dato 3 & 150 & 60\% \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Tabla larga (múltiples páginas)
```latex
\begin{longtable}{lcc}
    \caption{Tabla que ocupa varias páginas.}
    \label{tab:larga} \\
    \toprule
    Col 1 & Col 2 & Col 3 \\
    \midrule
    \endfirsthead
    
    \multicolumn{3}{c}{Continuación de la tabla} \\
    \toprule
    Col 1 & Col 2 & Col 3 \\
    \midrule
    \endhead
    
    \bottomrule
    \endfoot
    
    % Datos aquí...
    Fila 1 & A & B \\
    Fila 2 & C & D \\
\end{longtable}
```

---

## ⚡ Compilación

### Orden de compilación completa

```bash
lualatex -shell-escape main.tex   # Primera pasada
biber main                        # Procesar bibliografía
makeglossaries main               # Procesar glosarios (si se usan)
lualatex -shell-escape main.tex   # Segunda pasada
lualatex -shell-escape main.tex   # Tercera pasada (resolver referencias)
```

### Con latexmk (recomendado)
```bash
latexmk -lualatex -shell-escape main.tex
```

### Configuración de latexmk (`.latexmkrc`)
```perl
$pdf_mode = 4;  # LuaLaTeX
$lualatex = 'lualatex -shell-escape %O %S';
```

---

## 🐛 Diagnóstico de Errores

### Errores de compilación

| Error | Causa probable | Solución |
|-------|---------------|----------|
| `Undefined control sequence` | Comando no definido | Verificar paquete cargado |
| `Missing $ inserted` | Símbolo matemático fuera de math mode | Añadir `$...$` |
| `File not found` | Ruta incorrecta | Verificar nombre y ubicación |
| `Missing \begin{document}` | Error en preámbulo | Revisar sintaxis antes de `\begin{document}` |
| `Font ... not found` | Fuente no instalada | Usar TeX Live completo |

### Errores de minted

| Error | Solución |
|-------|----------|
| `You must invoke LaTeX with -shell-escape` | Añadir `-shell-escape` al comando |
| `Pygments not found` | Instalar: `pip install latexminted` |
| `Cannot find ... lexer` | Verificar nombre del lenguaje |

### Errores de bibliografía

| Error | Solución |
|-------|----------|
| `Citation undefined` | Ejecutar `biber main` |
| `I couldn't open file` | Verificar nombre del archivo .bib |
| `Biber error` | Revisar sintaxis del archivo .bib |

---

## ♿ Accesibilidad y PDF/UA

### Crear PDFs accesibles (TeX Live 2025+)

Para generar PDFs que cumplan con PDF/UA-2, añadir antes de `\documentclass`:

```latex
\DocumentMetadata{
    lang = es-ES,
    pdfstandard = ua-2,
    testphase = {phase-III, math, table, title, firstaid}
}
```

### Requisitos

| Requisito | Descripción |
|-----------|-------------|
| LuaLaTeX | Obligatorio para MathML automático |
| TeX Live 2025+ | Soporte completo del LaTeX Tagging Project |
| Texto alternativo | Usar `alt={...}` en `\includegraphics` |

### Más información

Ver la guía completa en [docs/ACCESIBILIDAD.md](ACCESIBILIDAD.md).

---

## 🔧 Personalización Avanzada

### Añadir un nuevo capítulo

1. Crear archivo en `capitulos/nuevo_capitulo.tex`
2. Añadir en `main.tex`:
   ```latex
   \include{capitulos/nuevo_capitulo}
   ```

### Añadir un nuevo anexo

1. Crear archivo en `anexos/anexo_X.tex`
2. Añadir en `main.tex` después de `\appendix`:
   ```latex
   \include{anexos/anexo_X}
   ```

### Cambiar estilo de bibliografía

En `configuracion.tex`, antes de cargar la clase:
```latex
% No recomendado cambiar, pero posible:
\PassOptionsToPackage{style=ieee}{biblatex}
```

---

*Este documento se actualiza con cada versión de la plantilla. Última actualización: Febrero 2026.*
