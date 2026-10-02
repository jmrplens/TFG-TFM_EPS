# 📖 Contexto Técnico para IA - Plantilla TFG/TFM EPS UA

Este documento proporciona información técnica detallada para que los asistentes de IA puedan dar respuestas precisas sobre esta plantilla LaTeX (versión 2.2.2). Todo lo que aparece aquí existe en `cls/` y `sty/`: si un comando no está en este documento ni en [COMPONENTES.md](COMPONENTES.md), no lo inventes.

## Índice📋

- [📋 Índice](#índice)
  - [🏗️ Arquitectura de la Plantilla](#️-arquitectura-de-la-plantilla)
    - [Clase Principal: `eps-tfg.cls`](#clase-principal-eps-tfgcls)
    - [Paquetes de Estilo (`sty/`)](#paquetes-de-estilo-sty)
  - [📋 Referencia Completa de `\EPSsetup{}`](#-referencia-completa-de-epssetup)
    - [Información del Documento](#información-del-documento)
    - [Información del Autor](#información-del-autor)
    - [Información del Tutor](#información-del-tutor)
    - [Información del Cotutor (opcional)](#información-del-cotutor-opcional)
    - [Datos institucionales](#datos-institucionales)
    - [Opciones](#opciones)
    - [Idioma](#idioma)
  - [🎨 Titulaciones y sus Identificadores](#-titulaciones-y-sus-identificadores)
    - [Grados (TFG)](#grados-tfg)
    - [Másteres (TFM)](#másteres-tfm)
  - [📝 Entornos de Código Disponibles](#-entornos-de-código-disponibles)
    - [Entornos con colores claros (fondo blanco/gris)](#entornos-con-colores-claros-fondo-blancogris)
    - [Variantes: sin números de línea y tema oscuro](#variantes-sin-números-de-línea-y-tema-oscuro)
    - [Código inline](#código-inline)
    - [Opciones comunes](#opciones-comunes)
  - [📊 Entornos de Ecuaciones](#-entornos-de-ecuaciones)
    - [Ecuación simple numerada](#ecuación-simple-numerada)
    - [Ecuaciones alineadas](#ecuaciones-alineadas)
    - [Ecuación sin numerar](#ecuación-sin-numerar)
    - [Sistema de ecuaciones](#sistema-de-ecuaciones)
    - [Teoremas y definiciones](#teoremas-y-definiciones)
  - [🧩 Componentes Especializados](#-componentes-especializados)
    - [Activación](#activación)
    - [Módulos Disponibles](#módulos-disponibles)
      - [Comunes (Siempre activos)](#comunes-siempre-activos)
      - [`[software]`](#software)
      - [`[telecom]`](#telecom)
      - [`[arquitectura]`](#arquitectura)
      - [`[quimica]`](#quimica)
      - [`[geologia]`](#geologia)
      - [`[prevencion]`](#prevencion)
  - [📚 Sistema de Bibliografía](#-sistema-de-bibliografía)
    - [Formato del archivo `.bib`](#formato-del-archivo-bib)
    - [Comandos de cita](#comandos-de-cita)
  - [🔤 Glosarios y Acrónimos](#-glosarios-y-acrónimos)
    - [Definir términos en `contenido/anexos/acronimos.tex`](#definir-términos-en-contenidoanexosacronimostex)
    - [Usar en el documento](#usar-en-el-documento)
  - [🖼️ Figuras y Gráficas](#️-figuras-y-gráficas)
    - [Figura simple](#figura-simple)
    - [Subfiguras](#subfiguras)
    - [Gráfica con PGFPlots](#gráfica-con-pgfplots)
  - [📋 Tablas](#-tablas)
    - [Tabla con booktabs (recomendado)](#tabla-con-booktabs-recomendado)
    - [Tabla larga (múltiples páginas)](#tabla-larga-múltiples-páginas)
  - [⚡ Compilación](#-compilación)
    - [Requisitos](#requisitos)
    - [Orden de compilación completa](#orden-de-compilación-completa)
    - [Con latexmk (recomendado)](#con-latexmk-recomendado)
    - [Configuración de latexmk (`.latexmkrc`)](#configuración-de-latexmk-latexmkrc)
  - [🐛 Diagnóstico de Errores](#-diagnóstico-de-errores)
    - [Errores de compilación](#errores-de-compilación)
    - [Errores de minted](#errores-de-minted)
    - [Errores de bibliografía](#errores-de-bibliografía)
  - [♿ Accesibilidad (PDF etiquetado)](#-accesibilidad-pdf-etiquetado)
  - [🔧 Personalización Avanzada](#-personalización-avanzada)
    - [Añadir un nuevo capítulo](#añadir-un-nuevo-capítulo)
    - [Añadir un nuevo anexo](#añadir-un-nuevo-anexo)
    - [Cambiar estilo de bibliografía](#cambiar-estilo-de-bibliografía)

---

## 🏗️ Arquitectura de la Plantilla

### Clase Principal: `eps-tfg.cls`

La clase (basada en KOMA-Script `scrbook`) utiliza **LaTeX3** (`expl3`) para la configuración:

```latex
% Sintaxis interna (NO exponer a usuarios)
\keys_define:nn { eps-tfg } {
    titulo .tl_gset:N = \g__eps_titulo_tl,
    autor .tl_gset:N = \g__eps_autor_tl,
    % ... más claves
}
```

El usuario interactúa mediante `\EPSsetup{...}` en `configuracion.tex`:

```latex
\EPSsetup{
    clave = valor,
    otra-clave = {valor con espacios},
}
```

Otros archivos de `cls/`:

| Archivo | Función |
| --------- | --------- |
| `cls/eps-tfg.cls` | Clase principal: tipografía, colores, idioma (polyglossia), bibliografía, glosarios, cabeceras |
| `cls/eps-metadata.tex` | `\DocumentMetadata` (etiquetado del PDF) y comprobación del motor LuaLaTeX. Se carga antes de `\documentclass` y no hace falta editarlo |

### Paquetes de Estilo (`sty/`)

| Archivo | Función |
| --------- | --------- |
| `eps-portadas.sty` | Generación de portadas (`\generarportada`) |
| `eps-codigo.sty` | Entornos de código con minted |
| `eps-componentes.sty` | Cargador modular de componentes visuales y especializados |
| `componentes/eps-comunes.sty` | Cajas de aviso, contenedores, listas visuales (siempre activo) |
| `componentes/eps-software.sty` | Módulo `[software]` |
| `componentes/eps-telecom.sty` | Módulo `[telecom]` |
| `componentes/eps-arquitectura.sty` | Módulo `[arquitectura]` |
| `componentes/eps-quimica.sty` | Módulo `[quimica]` |
| `componentes/eps-geologia.sty` | Módulo `[geologia]` |
| `componentes/eps-prevencion.sty` | Módulo `[prevencion]` |

---

## 📋 Referencia Completa de `\EPSsetup{}`

Estas son **todas** las claves que existen. Cualquier otra clave produce el error `The key 'eps-tfg/...' is unknown`.

### Información del Documento

| Clave | Tipo | Obligatorio | Descripción |
| ------- | ------ | ------------- | ------------- |
| `titulo` | texto | ⚠️ aviso si falta | Título principal del trabajo |
| `subtitulo` | texto | ❌ | Subtítulo opcional |
| `fecha` | texto | ❌ | Fecha de presentación (ej: "Junio 2026") |
| `titulacion` | id | ✅ error si falta | Identificador de la titulación (ver tabla) |

Si `titulacion` falta o tiene un valor no válido, la compilación se detiene con un error que lista los valores admitidos.

### Información del Autor

| Clave | Tipo | Obligatorio | Descripción |
| ------- | ------ | ------------- | ------------- |
| `autor` | texto | ⚠️ aviso si falta | Nombre completo del autor |
| `genero` | m/f/n | ❌ | Género para etiquetas (por defecto: m) |
| `email` | texto | ❌ | Email institucional |

### Información del Tutor

| Clave | Tipo | Obligatorio | Descripción |
| ------- | ------ | ------------- | ------------- |
| `tutor` | texto | ⚠️ aviso si falta | Nombre completo del tutor |
| `tutor-genero` | m/f/n | ❌ | Género del tutor (por defecto: m) |
| `tutor-departamento` | texto | ❌ | Departamento del tutor |

### Información del Cotutor (opcional)

| Clave | Tipo | Obligatorio | Descripción |
| ------- | ------ | ------------- | ------------- |
| `cotutor` | texto | ❌ | Nombre completo del cotutor |
| `cotutor-genero` | m/f/n | ❌ | Género del cotutor (por defecto: m) |
| `cotutor-departamento` | texto | ❌ | Departamento del cotutor |

### Datos institucionales

| Clave | Tipo | Por defecto | Descripción |
| ------- | ------ | ------------- | ------------- |
| `facultad` | texto | Escuela Politécnica Superior | Centro |
| `universidad` | texto | Universidad de Alicante | Universidad |
| `ubicacion` | texto | Alicante | Ciudad |

### Opciones

| Clave | Tipo | Por defecto | Descripción |
| ------- | ------ | ------------- | ------------- |
| `borrador` | booleano | false | `true` muestra las notas `\todo{}` (modo borrador). El `configuracion.tex` distribuido trae `borrador = true`: ponerlo a `false` para la versión final. También vale `\documentclass[borrador]{eps-tfg}` |
| `optimizar-tikz` | booleano | — | **Obsoleta, sin efecto.** Se acepta para no romper configuraciones antiguas (la externalización de TikZ no es compatible con el etiquetado del PDF) |

### Idioma

| Clave | Tipo | Obligatorio | Descripción |
| ------- | ------ | ------------- | ------------- |
| `idioma` | texto | ❌ | Idioma del documento: `espanol` (defecto), `valenciano`, `ingles` |

`idioma` cambia el idioma de todo el documento: títulos automáticos (Tabla, Figura, Índice, Bibliografía...), nombres de listas y teoremas, formato de citas y bibliografía, separación silábica y el idioma del PDF (`es-ES`, `ca-ES-valencia` o `en-GB`; el inglés es británico). **No hay que editar `cls/eps-metadata.tex`**: la clase fija el idioma del PDF a partir de `idioma`.

La portada se mantiene siempre en español (formato oficial de la EPS): tipo de trabajo, titulación, etiquetas Autor/Tutor y fecha.

---

## 🎨 Titulaciones y sus Identificadores

### Grados (TFG)

| ID | Nombre Completo |
| ---- | ----------------- |
| `arquitectura` | Grado en Arquitectura |
| `arquitectura-tecnica` | Grado en Arquitectura Técnica |
| `civil` | Grado en Ingeniería Civil |
| `informatica` | Grado en Ingeniería Informática |
| `multimedia` | Grado en Ingeniería Multimedia |
| `quimica` | Grado en Ingeniería Química |
| `robotica` | Grado en Ingeniería Robótica |
| `teleco` | Grado en Ingeniería en Sonido e Imagen en Telecomunicación |

### Másteres (TFM)

| ID | Nombre Completo |
| ---- | ----------------- |
| `master-agua` | Máster Universitario en Gestión Sostenible y Tecnologías del Agua |
| `master-caminos` | Máster Universitario en Ingeniería de Caminos, Canales y Puertos |
| `master-ciberseguridad` | Máster Universitario en Ciberseguridad |
| `master-ciencia-datos` | Máster Universitario en Ciencia de Datos |
| `master-edificacion` | Máster Universitario en Gestión de la Edificación |
| `master-geologica` | Máster Universitario en Ingeniería Geológica |
| `master-informatica` | Máster Universitario en Ingeniería Informática |
| `master-materiales` | Máster Universitario en Ingeniería de los Materiales, del Agua y del Terreno |
| `master-moviles` | Máster Universitario en Desarrollo de Software para Dispositivos Móviles |
| `master-prevencion` | Máster Universitario en Prevención de Riesgos Laborales |
| `master-quimica` | Máster Universitario en Ingeniería Química |
| `master-robotica` | Máster Universitario en Automática y Robótica |
| `master-teleco` | Máster Universitario en Ingeniería de Telecomunicación |
| `master-web` | Máster Universitario en Desarrollo de Aplicaciones y Servicios Web |

Cada titulación define su color institucional y su logotipo en la portada.

---

## 📝 Entornos de Código Disponibles

Definidos en `sty/eps-codigo.sty` (46 lenguajes; lista completa en [CODIGO_FUENTE.md](CODIGO_FUENTE.md)). Nunca usar `verbatim` ni `lstlisting`.

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

Para un lenguaje de Pygments sin entorno propio: `\begin{codigo}{lenguaje} ... \end{codigo}`.

### Variantes: sin números de línea y tema oscuro

| Sufijo | Ejemplo | Efecto |
| ------ | ------- | ------ |
| (ninguno) | `pythoncode` | Tema claro con números de línea |
| `NN` | `pythoncodeNN` | Tema claro sin números de línea |
| `Dark` | `pythoncodeDark` | Tema oscuro con números de línea |
| `DarkNN` | `pythoncodeDarkNN` | Tema oscuro sin números de línea |

Las variantes oscuras disponibles para cada lenguaje están en la tabla de [CODIGO_FUENTE.md](CODIGO_FUENTE.md). Genérico oscuro: `\begin{codigoDark}{lenguaje}`.

### Código inline

```latex
En Python usamos \mintinline{python}{print("Hola")} para imprimir.
```

### Opciones comunes

Las opciones del entorno son de tcolorbox (`title`, `list entry`...). Las opciones de minted van **dentro** de `minted options={...}`. Los `_` del título se escapan (`\_`).

```latex
\begin{pythoncode}[
    title={mi\_script.py},
    minted options={firstline=5, lastline=15, highlightlines={3,7-9}},
]
...
\end{pythoncode}
```

Para quitar los números de línea, usar la variante `NN`.

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
\begin{equation}
    \begin{cases}
        x + y = 10 \\
        x - y = 2
    \end{cases}
\end{equation}
```

### Teoremas y definiciones

Entornos definidos por la clase (numerados por capítulo, con nombre según el idioma): `teorema`, `definicion`, `lema`, `corolario`, `proposicion`, `ejemplo` (y los sinónimos `theorem`, `definition`).

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

## 🧩 Componentes Especializados

El paquete `eps-componentes` carga solo los módulos necesarios. Catálogo completo con capturas: [COMPONENTES.md](COMPONENTES.md).

### Activación

En `main.tex`:

```latex
% Opciones: software, telecom, arquitectura, quimica, geologia, prevencion, all
\usepackage[software,telecom]{eps-componentes}
```

### Módulos Disponibles

#### Comunes (Siempre activos)

- **Cajas de aviso:** `infobox`, `warningbox`, `dangerbox`, `successbox`, `tipbox`, `notebox`. Título opcional entre llaves y opciones de tcolorbox opcionales entre corchetes: `\begin{warningbox}[colback=white]{Título} ... \end{warningbox}`.
- **Contenedores:** `titlebox` (`[opciones]{Título}`), `definitionbox` (`{Término}`), `examplebox` e `importantbox` (título opcional **entre corchetes**: `\begin{examplebox}[Ejemplo práctico]`), `quotebox`.
- **Listas y otros:** `checklist`, `proscons` (`\pro`, `\con`), `steplist`, `comparison`, `timeline` (`\timeitem`), `\badge`, `\progressbar`, `\rating`, `\levelbar`, `\personcard`, `\statcard`.

#### `[software]`

El contenido de `terminal`, `apiendpoint` y `dirtreebox` **no es literal**: se escriben como texto LaTeX (escapar `\&`, `\#`, `\%`, `\_`, `\{`, `\}`, `\$`; separar líneas con `\\`). Para scripts o salidas copiadas tal cual, usar `bashcode`.

- **`terminal`**: consola; título opcional entre corchetes (`\begin{terminal}[Mi consola]`). Cada orden con `\prompt` (`$`), `\promptroot` (`#`) o `\promptuser{usuario}`; comentarios con `\termcomment{...}`.
- **`apiendpoint`**: `\begin{apiendpoint}{GET}{/api/v1/usuarios}` con `\apidescription{...}`, `\apiheaders{...}`, `\apiparams{...}` (filas `nombre & tipo & descripción & requerido \\`), `\apibody{tipo}{contenido}` y `\apiresponse{código}{contenido}` dentro.
- **`dirtreebox`**: árbol de directorios; título opcional `[Título]`; cada elemento con `\dirtreeitem[nivel]{nombre}` (una `/` final indica carpeta).
- **Diagramas UML:** comando `\umlclass{Nombre}{atributos}{métodos}` (3 argumentos, dibujado con tcolorbox) y `\umlinterface{Nombre}{métodos}`; visibilidad con `\public`, `\private`, `\protectedvis`.
- **Otros:** `requirements` (`\requirement`), `logbox` (`\logentry`), `configbox`, `\metricbox`, `\gitcommit`, `\gitbranch`, `\httpget`/`\httppost`...

```latex
\begin{terminal}[Terminal]
\prompt git clone https://github.com/usuario/repo.git\\
\prompt cd repo \&\& make
\end{terminal}

\begin{apiendpoint}{GET}{/api/v1/usuarios}
  \apidescription{Obtiene la lista de usuarios}
\end{apiendpoint}

\begin{dirtreebox}[Estructura del proyecto]
  \dirtreeitem[0]{proyecto/}
  \dirtreeitem[1]{src/}
  \dirtreeitem[2]{main.py}
\end{dirtreebox}
```

#### `[telecom]`

- **Tramas:** `protocolframe` (`\begin{protocolframe}[32]` con `\framefield{bits}{nombre}`, `\framefieldmulti`, `\framebitheader`...).
- **Circuitos:** `circuitbox` (contenedor para `circuitikz`).
- **RF y señales:** `smithchartbox` / `smithplot` (carta de Smith), `constellationbox`, `bodeplot`, `spectrumbox`, `eyediagrambox`, `radiationbox`, `sparameters`, `rfspecs`.
- **Sistemas:** `blockdiagram` (`\sysblock`, `\sysarrow`), `timingbox` (cronogramas), `fsmdiagram` (`\fsmstate`, `\fsmtrans`).

#### `[arquitectura]`

- **Planificación:** `ganttbox` (contenedor para `ganttchart` de pgfgantt).
- **Documentación técnica:** `techsheet`, `presupuesto` (`\partida`, `\capitulo`...), `cuadroprecios`, `normativa` (`\norma`), `leyenda`, `detalleconstructivo`, `organigramabox`, `controlcalidad`, `cuadrosuperficies`.
- **Planos:** `\cota`, `\escala` (texto de escala), símbolos de instalaciones (`\simboloagua`, `\simboloelec`...).

#### `[quimica]`

- **Fórmulas:** `\ch{...}` (chemformula), `reactionbox`, `mechanismbox`; `reaction` de chemmacros.
- **Datos:** `compoundsheet`, `proptable`, `analyticalresults`, `chemspectrumbox`, `phasediagrambox`, `kineticdata`, `massbalancebox`, `waterquality`.
- **Laboratorio:** `protocol` (`\protocolstep`, `\protocolwarning`), `equipmentlist`, `reagentlist`.

#### `[geologia]`

- `stratigraphybox`, `stratcolumn` (`\stratlayer`), `geologicsectionbox`, `mineraltable`, `rosebox`, `structuraldata`, `geotechdata`, `boreholebox`, `isolinebox`.

#### `[prevencion]`

- **Riesgos:** `riskmatrixbox` / `riskmatrixplot` (matriz de riesgos; `\riskmatrix` es un alias antiguo), `riskassessment`, `riskmapbox`.
- **Seguridad:** `safetysheet`, `epilist` (`\epihardhat`, `\epigloves`...), `safetychecklist`, `emergencyprocedure`, `accidentreport`, `trainingrecord`.

---

## 📚 Sistema de Bibliografía

BibLaTeX + Biber con estilo APA 7. Los títulos en inglés con `langid = {english}` se escriben en minúscula de frase (sentence case) según APA.

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
| --------- | ----------- | ----- |
| `\parencite{key}` | (Autor, 2024) | Cita parentética |
| `\textcite{key}` | Autor (2024) | Cita textual |
| `\citeauthor{key}` | Autor | Solo autor |
| `\citeyear{key}` | 2024 | Solo año |
| `\parencite[p.~50]{key}` | (Autor, 2024, p. 50) | Con página |
| `\parencite{key1,key2}` | (Autor1, 2024; Autor2, 2023) | Múltiples |

No usar `\cite{}` directamente: en estilo APA da una cita sin paréntesis; usar `\parencite` o `\textcite`.

---

## 🔤 Glosarios y Acrónimos

### Definir términos en `contenido/anexos/acronimos.tex`

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

La clase carga `glossaries` con `automake`, así que `main.tex` debe mantener `\makeglossaries`.

---

## 🖼️ Figuras y Gráficas

Añadir siempre texto alternativo (`alt={...}`) a las imágenes: el PDF está etiquetado y los lectores de pantalla lo leen.

### Figura simple

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth, alt={Descripción breve de la imagen}]{recursos/figuras/imagen}
    \caption{Descripción de la figura.}
    \label{fig:ejemplo}
\end{figure}
```

### Subfiguras

```latex
\begin{figure}[htbp]
    \centering
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth, alt={Primera imagen}]{imagen1}
        \caption{Primera imagen}
        \label{fig:sub1}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.45\textwidth}
        \includegraphics[width=\textwidth, alt={Segunda imagen}]{imagen2}
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

### Requisitos

- **TeX Live 2024 o posterior** (LaTeX 2024-11) o MiKTeX actualizado. El etiquetado completo del PDF requiere LaTeX 2025-11 o posterior (TeX Live 2025 actualizado o TeX Live 2026).
- `latexminted` para minted 3: viene con TeX Live 2024+ (comprobar con `latexminted --version`). No hace falta `pip install`.
- En Overleaf: compilador **LuaLaTeX** y TeX Live 2024 o posterior (ver [OVERLEAF.md](OVERLEAF.md)).

### Orden de compilación completa

```bash
lualatex -shell-escape main.tex   # Primera pasada
biber main                        # Procesar bibliografía
lualatex -shell-escape main.tex   # Segunda pasada (glosarios con automake)
lualatex -shell-escape main.tex   # Tercera pasada (resolver referencias)
```

O simplemente `make` (y `make clean` para borrar auxiliares, la caché `_minted/` e `informe-revision.md`).

### Con latexmk (recomendado)

```bash
latexmk main.tex      # usa .latexmkrc del proyecto
latexmk -c            # limpia auxiliares (conserva la caché de minted)
latexmk -C            # limpia todo, incluida la caché _minted/
```

### Configuración de latexmk (`.latexmkrc`)

```perl
$pdf_mode = 4;  # LuaLaTeX
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
```

---

## 🐛 Diagnóstico de Errores

### Errores de compilación

| Error | Causa probable | Solución |
| ------- | --------------- | ---------- |
| `ESTA PLANTILLA REQUIERE LuaLaTeX` / `TeX capacity exceeded` | Motor incorrecto (pdfLaTeX/XeLaTeX) | Compilar con LuaLaTeX |
| `Undefined control sequence` | Comando no definido | Verificar paquete o módulo de componentes cargado |
| `Missing $ inserted` | Símbolo matemático fuera de math mode, `_` sin escapar (también en `title={...}`) o `$` literal en `terminal` | Añadir `$...$`, escapar `\_`, usar `\prompt` |
| `The key 'eps-tfg/...' is unknown` | Clave de `\EPSsetup` inexistente | Usar solo las claves de este documento |
| `La titulación '...' no está definida` | Valor de `titulacion` no válido | Usar uno de los identificadores de la tabla |
| `Package block Error: Some keys specified on the itemize environment are unknown` | Versión antigua de la plantilla con LaTeX 2025-11+ | Actualizar la plantilla (`cls/`, `sty/`) |
| `ignored error Infinite glue shrinkage found in box being split` | Fallo conocido de `longtable` 4.24 (LaTeX 2025-11) al partir una `longtable` entre páginas | Ninguna: es un error ignorado y el PDF es correcto |
| `File not found` | Ruta incorrecta | Verificar nombre y ubicación |
| `Font ... not found` | Fuente no instalada | Usar TeX Live completo |

### Errores de minted

| Error | Solución |
| ------- | ---------- |
| `You must invoke LaTeX with -shell-escape` | Añadir `-shell-escape` al comando (o usar `make`) |
| `minted v3+ executable is not installed or is not added to PATH` | Comprobar `latexminted --version`. Si falta: `tlmgr install minted` (TeX Live de TUG) o `sudo apt install texlive-latex-extra` (Debian/Ubuntu). No usar `pip install` (falla con PEP 668); `pipx install latexminted` solo con MiKTeX o si el de TeX Live no funciona |
| `I do not know the key '/tcb/firstline'` | Opción de minted fuera de `minted options={...}` |
| `Cannot find ... lexer` | Verificar nombre del lenguaje |

### Errores de bibliografía

| Error | Solución |
| ------- | ---------- |
| `Citation undefined` | Ejecutar `biber main` |
| `I couldn't open file` | Verificar nombre del archivo .bib |
| `Biber error` | Revisar sintaxis del archivo .bib |

---

## ♿ Accesibilidad (PDF etiquetado)

`cls/eps-metadata.tex` ya activa el etiquetado (no hay que añadir nada):

- LaTeX 2025-11 o posterior: `\DocumentMetadata{tagging=on, pdfversion=2.0, lang=es-ES}`.
- Versiones anteriores (TeX Live 2024, TeX Live 2025 sin actualizar): `testphase=phase-I` (etiquetado básico).

El PDF resultante está **etiquetado pero no declara conformidad PDF/UA-2**: todavía no se alcanza (KOMA-Script no etiqueta las secciones y varios paquetes, como minted, caption o pgfplots, aún no son compatibles con el etiquetado). El idioma (`lang`) lo fija la clase a partir de `idioma`.

Buenas prácticas: `alt={...}` en cada `\includegraphics`, tablas con cabecera clara y texto descriptivo en los enlaces. Ver [ACCESIBILIDAD.md](ACCESIBILIDAD.md).

---

## 🔧 Personalización Avanzada

### Añadir un nuevo capítulo

1. Crear el archivo `contenido/capitulos/nuevo-capitulo.tex` (empieza con `\chapter{...}` y `\label{chap:nuevo-capitulo}`).
2. Añadir en `main.tex`, después de `\mainmatter`:

   ```latex
   \input{contenido/capitulos/nuevo-capitulo}
   ```

### Añadir un nuevo anexo

1. Crear el archivo `contenido/anexos/anexo-x.tex` (con `\label{anexo:x}`).
2. Añadir en `main.tex` después de `\appendix`:

   ```latex
   \input{contenido/anexos/anexo-x}
   ```

### Cambiar estilo de bibliografía

El estilo APA 7 es el exigido habitualmente; cambiarlo no está recomendado. Si el tutor lo pide, se puede cambiar en `cls/eps-tfg.cls` (opción `style=` de `biblatex`).

---

*Este documento se actualiza con cada versión de la plantilla.*
