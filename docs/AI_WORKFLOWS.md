# Flujos de trabajo para agentes de IA

Este documento describe los flujos de trabajo paso a paso para las tareas más
comunes que un agente de IA puede realizar sobre esta plantilla. Complementa
la referencia técnica de `AI_CONTEXT.md`.

---

## Índice

- [Configurar un nuevo TFG/TFM](#1-configurar-un-nuevo-tfgtfm)
- [Añadir un capítulo nuevo](#2-añadir-un-capítulo-nuevo)
- [Añadir una referencia bibliográfica](#3-añadir-una-referencia-bibliográfica)
- [Insertar una figura](#4-insertar-una-figura)
- [Insertar una tabla](#5-insertar-una-tabla)
- [Insertar un bloque de código](#6-insertar-un-bloque-de-código)
- [Cambiar el idioma del documento](#7-cambiar-el-idioma-del-documento)
- [Activar componentes especializados](#8-activar-componentes-especializados)
- [Añadir un acrónimo o término al glosario](#9-añadir-un-acrónimo-o-término-al-glosario)
- [Diagnosticar un error de compilación](#10-diagnosticar-un-error-de-compilación)
- [Añadir un anexo](#11-añadir-un-anexo)
- [Crear una gráfica con PGFPlots](#12-crear-una-gráfica-con-pgfplots)

---

## 1. Configurar un nuevo TFG/TFM

**Archivo a editar:** `configuracion.tex`

**Pasos:**

1. Abrir `configuracion.tex`.
2. Rellenar las claves de `\EPSsetup{...}`:

```latex
\EPSsetup{
  titulo      = {Título del Trabajo},
  subtitulo   = {Subtítulo opcional},
  autor       = {Nombre Apellido1 Apellido2},
  genero      = m,                    % m=masculino, f=femenino, n=neutro
  email       = alumno@alu.ua.es,
  tutor       = {Dr. Nombre Apellido},
  tutor-genero = m,
  tutor-departamento = {Departamento de Ciencias de la Computación},
  titulacion  = informatica,
  idioma      = espanol,
  fecha       = {Junio 2026},
  optimizar-tikz = true,
  borrador    = false,
}
```

3. Si el idioma no es `espanol`, actualizar también `cls/eps-metadata.tex`
   (ver flujo 7).
4. Verificar con `make quick`.

**Titulaciones más comunes:**

| Titulación | ID |
|---|---|
| Ingeniería Informática | `informatica` |
| Ingeniería en Sonido e Imagen | `teleco` |
| Ingeniería Civil | `civil` |
| Ingeniería Química | `quimica` |
| Ingeniería Robótica | `robotica` |
| Ingeniería Multimedia | `multimedia` |
| Máster en Ing. Informática | `master-informatica` |
| Máster en Ciberseguridad | `master-ciberseguridad` |

---

## 2. Añadir un capítulo nuevo

**Archivos a editar:** `main.tex` + nuevo archivo en `contenido/capitulos/`

**Pasos:**

1. Crear el archivo del capítulo:

```latex
% contenido/capitulos/estado-del-arte.tex
\chapter{Estado del Arte}
\label{chap:estado-del-arte}

Texto introductorio del capítulo.

\section{Antecedentes}
\label{sec:antecedentes}

Contenido de la sección.
```

2. Registrar el capítulo en `main.tex`, dentro del bloque `\mainmatter`,
   en el orden deseado:

```latex
\mainmatter
\input{contenido/capitulos/introduccion}
\input{contenido/capitulos/estado-del-arte}   % ← añadir aquí
\input{contenido/capitulos/metodologia}
```

3. Verificar con `make quick`.

**Nota:** Usar `\input{}` en lugar de `\include{}` para evitar saltos de
página forzados entre capítulos si no se desean.

---

## 3. Añadir una referencia bibliográfica

**Archivo a editar:** `referencias.bib`

**Pasos:**

1. Añadir la entrada al final de `referencias.bib`:

```bibtex
% Artículo de revista
@article{apellido2024titulo,
  author  = {Apellido, Nombre and Coautor, Nombre},
  title   = {Título del artículo},
  journal = {Nombre de la Revista},
  year    = {2024},
  volume  = {15},
  number  = {3},
  pages   = {100--120},
  doi     = {10.1234/ejemplo},
}

% Libro
@book{autor2023libro,
  author    = {Autor, Nombre},
  title     = {Título del Libro},
  publisher = {Editorial},
  year      = {2023},
  address   = {Ciudad},
  isbn      = {978-84-xxxxx-xx-x},
}

% Recurso web
@online{org2024web,
  author  = {{Nombre de la Organización}},
  title   = {Título de la página},
  url     = {https://ejemplo.com/pagina},
  urldate = {2024-06-15},
  year    = {2024},
}

% Conferencia
@inproceedings{apellido2024conf,
  author    = {Apellido, Nombre},
  title     = {Título de la ponencia},
  booktitle = {Nombre del Congreso},
  year      = {2024},
  pages     = {50--55},
  address   = {Ciudad},
}
```

2. Citar en el texto del capítulo:

```latex
Según \textcite{apellido2024titulo}, los resultados muestran...
Este enfoque ha sido estudiado previamente \parencite{autor2023libro}.
```

3. Compilar con `make` completo (necesario para que Biber procese la nueva
   entrada).

**Clave de la entrada:** usar el formato `apellido+año+palabra` para evitar
colisiones (ej: `garcia2024redes`).

---

## 4. Insertar una figura

**Archivo a editar:** capítulo correspondiente en `contenido/capitulos/`

**Pasos:**

1. Colocar la imagen en `recursos/figuras/` (formatos: PDF, PNG, JPG, EPS).
   Preferir PDF o PNG para mejor calidad.

2. Insertar en el capítulo:

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{recursos/figuras/nombre-imagen}
  \caption{Descripción clara y concisa de la figura.}
  \label{fig:nombre-imagen}
\end{figure}
```

3. Referenciar en el texto:

```latex
Como se muestra en la Figura~\ref{fig:nombre-imagen}, el sistema...
```

**Para subfiguras:**

```latex
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{recursos/figuras/imagen-a}
    \caption{Primera variante.}
    \label{fig:imagen-a}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{recursos/figuras/imagen-b}
    \caption{Segunda variante.}
    \label{fig:imagen-b}
  \end{subfigure}
  \caption{Comparativa de las dos variantes.}
  \label{fig:comparativa}
\end{figure}
```

**Para accesibilidad (PDF/UA-2):**

```latex
\includegraphics[width=0.8\textwidth, alt={Descripción para lectores de pantalla}]{ruta}
```

---

## 5. Insertar una tabla

**Archivo a editar:** capítulo correspondiente

**Pasos:**

1. Insertar la tabla con `booktabs`:

```latex
\begin{table}[htbp]
  \centering
  \caption{Título descriptivo de la tabla.}
  \label{tab:nombre-tabla}
  \begin{tabular}{lcc}
    \toprule
    Columna 1 & Columna 2 & Columna 3 \\
    \midrule
    Fila 1    & Valor A   & 95\%      \\
    Fila 2    & Valor B   & 87\%      \\
    Fila 3    & Valor C   & 91\%      \\
    \bottomrule
  \end{tabular}
\end{table}
```

2. Referenciar en el texto:

```latex
Los resultados se muestran en la Tabla~\ref{tab:nombre-tabla}.
```

**Para tablas largas (varias páginas):**

```latex
\begin{longtable}{lcc}
  \caption{Tabla extensa con múltiples páginas.}
  \label{tab:larga} \\
  \toprule
  Col 1 & Col 2 & Col 3 \\
  \midrule
  \endfirsthead
  \multicolumn{3}{c}{Continuación} \\
  \toprule
  Col 1 & Col 2 & Col 3 \\
  \midrule
  \endhead
  \bottomrule
  \endfoot
  % Datos...
  Fila 1 & A & B \\
\end{longtable}
```

**Regla:** Nunca usar `\hline`. Siempre `\toprule`, `\midrule`, `\bottomrule`.

---

## 6. Insertar un bloque de código

**Archivo a editar:** capítulo correspondiente

**Pasos:**

1. Verificar que el módulo de componentes adecuado está activo en `main.tex`
   (para `jsoncode`, `sqlcode`, `bashcode` se necesita `[software]`).

2. Insertar el bloque:

```latex
\begin{pythoncode}[title={clasificador.py}]
import numpy as np
from sklearn.svm import SVC

clf = SVC(kernel='rbf', C=1.0)
clf.fit(X_train, y_train)
accuracy = clf.score(X_test, y_test)
print(f"Precisión: {accuracy:.2%}")
\end{pythoncode}
```

3. Para referenciar el bloque en el texto:

```latex
El Código~\ref{cod:clasificador} muestra la implementación del clasificador.
```

   Para que la referencia funcione, añadir `label` al entorno:

```latex
\begin{pythoncode}[title={clasificador.py}, label={cod:clasificador}]
```

**Lenguajes disponibles:**

| Entorno | Lenguaje |
|---|---|
| `pythoncode` | Python |
| `jscode` | JavaScript |
| `cppcode` | C++ |
| `javacode` | Java |
| `matlabcode` | MATLAB |
| `bashcode` | Bash/Shell |
| `sqlcode` | SQL |
| `jsoncode` | JSON |
| `yamlcode` | YAML |
| `htmlcode` | HTML |
| `csscode` | CSS |
| `rcode` | R |
| `rustcode` | Rust |
| `gocode` | Go |
| `phpcode` | PHP |

Añadir `Dark` al nombre para tema oscuro: `pythoncodeDark`, `jscodeDark`.

---

## 7. Cambiar el idioma del documento

**Archivos a editar:** `configuracion.tex` + `cls/eps-metadata.tex`

**Pasos:**

1. En `configuracion.tex`, cambiar la clave `idioma`:

```latex
\EPSsetup{
  idioma = valenciano,   % espanol | valenciano | ingles
}
```

2. En `cls/eps-metadata.tex`, actualizar el valor de `lang=`:

```latex
\DocumentMetadata{
  lang        = ca-ES,   % ← cambiar según idioma
  pdfstandard = ua-2,
  pdfversion  = 2.0,
  testphase   = {phase-I},
}
```

   Tabla de correspondencia:

   | `idioma` | `lang=` |
   |---|---|
   | `espanol` | `es-ES` |
   | `valenciano` | `ca-ES` |
   | `ingles` | `en-GB` |

3. Compilar con `make` completo.

**Qué cambia con el idioma:**
- Títulos automáticos: "Tabla" / "Taula" / "Table", "Figura" / "Figura" / "Figure", etc.
- Formato de fechas en bibliografía.
- Metadatos del PDF (accesibilidad).
- Separación silábica automática.

---

## 8. Activar componentes especializados

**Archivo a editar:** `main.tex`

**Pasos:**

1. Localizar la línea de `\usepackage` de componentes en `main.tex`.
2. Cambiar la opción según la titulación:

```latex
% Antes (ejemplo con [all]):
\usepackage[all]{eps-componentes}

% Después (solo software):
\usepackage[software]{eps-componentes}
```

**Opciones disponibles:**

| Opción | Módulos incluidos | Para titulaciones |
|---|---|---|
| *(sin opción)* | Solo comunes | Cualquiera |
| `[software]` | Comunes + Software | Informática, Multimedia, Robótica |
| `[telecom]` | Comunes + Telecom | Telecomunicaciones |
| `[arquitectura]` | Comunes + Arquitectura | Arquitectura, Civil |
| `[quimica]` | Comunes + Química | Química |
| `[geologia]` | Comunes + Geología | Geología |
| `[prevencion]` | Comunes + Prevención | Prevención de Riesgos |
| `[all]` | Todos | Cualquiera (más lento) |

Se pueden combinar: `\usepackage[software,telecom]{eps-componentes}`

3. Verificar con `make quick`.

---

## 9. Añadir un acrónimo o término al glosario

**Archivo a editar:** `contenido/anexos/acronimos.tex`

**Pasos:**

1. Añadir la definición:

```latex
% Acrónimo
\newacronym{id}{SIGLA}{Forma larga del acrónimo}

% Ejemplos:
\newacronym{cnn}{CNN}{Convolutional Neural Network}
\newacronym{api}{API}{Application Programming Interface}
\newacronym{rest}{REST}{Representational State Transfer}

% Término del glosario
\newglossaryentry{id}{
  name={Nombre del término},
  description={Definición del término en el glosario}
}
```

2. Usar en el texto del capítulo:

```latex
\gls{cnn}       % Primera vez: "Convolutional Neural Network (CNN)"; resto: "CNN"
\acrshort{cnn}  % Siempre: "CNN"
\acrlong{cnn}   % Siempre: "Convolutional Neural Network"
\acrfull{cnn}   % Siempre: "Convolutional Neural Network (CNN)"
\gls{id}        % Término del glosario (enlazado)
```

3. Compilar con `make` completo (necesario para que `makeglossaries` procese
   las nuevas entradas).

---

## 10. Diagnosticar un error de compilación

**Pasos:**

1. Ejecutar `make quick` y capturar la salida:

```bash
make quick 2>&1 | tail -40
```

2. Si el error no es claro, leer el archivo de log:

```bash
grep -n "^!" main.log | head -20
grep -n "Error\|error\|Warning" main.log | grep -v "^#" | head -30
```

3. Identificar el tipo de error:

| Síntoma | Causa | Solución |
|---|---|---|
| `Undefined control sequence \nombre` | Comando no definido | Verificar que el módulo de componentes está activo; revisar ortografía |
| `You must invoke LaTeX with -shell-escape` | Falta flag | Usar `make` en lugar de `lualatex` directo |
| `Pygments not found` / `latexminted` | Python no instalado | `pip install latexminted` |
| `Citation 'X' undefined` | Biber no ejecutado | Ejecutar `make` completo |
| `Missing $ inserted` | Símbolo matemático fuera de modo math | Encerrar en `$...$` |
| `File 'X.sty' not found` | Paquete TeX no instalado | `tlmgr install X` |
| `Font ... not found` | TeX Live incompleto | Instalar TeX Live completo |
| `I found no \bibdata command` | Usando BibTeX en lugar de Biber | Verificar `.latexmkrc` y usar `make` |
| `Package babel Error` | Conflicto de idioma | Verificar que `idioma` y `lang=` coinciden |
| `Runaway argument` | Llave `{` o `}` sin cerrar | Revisar el bloque indicado en el log |

4. Si el error persiste, buscar la línea exacta en el log:

```bash
grep -n "l\.[0-9]" main.log | head -10
```

---

## 11. Añadir un anexo

**Archivos a editar:** `main.tex` + nuevo archivo en `contenido/anexos/`

**Pasos:**

1. Crear el archivo del anexo:

```latex
% contenido/anexos/anexo-manual-usuario.tex
\chapter{Manual de Usuario}
\label{anexo:manual-usuario}

Contenido del anexo.

\section{Instalación}
\label{sec:instalacion-manual}

Pasos de instalación...
```

2. Registrar en `main.tex`, dentro del bloque `\appendix`:

```latex
\appendix
\input{contenido/anexos/anexo-tecnicas-avanzadas}
\input{contenido/anexos/anexo-manual-usuario}   % ← añadir aquí
```

3. Verificar con `make quick`.

---

## 12. Crear una gráfica con PGFPlots

**Archivo a editar:** capítulo correspondiente

**Pasos:**

1. Insertar la gráfica dentro de un entorno `figure`:

```latex
\begin{figure}[htbp]
  \centering
  \begin{tikzpicture}
    \begin{axis}[
      width=0.85\textwidth,
      height=6cm,
      xlabel={Eje X (unidades)},
      ylabel={Eje Y (unidades)},
      grid=major,
      legend pos=north west,
      xmin=0, xmax=100,
    ]
      \addplot[blue, thick, mark=*] coordinates {
        (0, 0) (25, 15) (50, 35) (75, 60) (100, 90)
      };
      \addlegendentry{Serie A}

      \addplot[red, dashed, mark=square] coordinates {
        (0, 5) (25, 20) (50, 40) (75, 55) (100, 75)
      };
      \addlegendentry{Serie B}
    \end{axis}
  \end{tikzpicture}
  \caption{Comparativa de las series A y B.}
  \label{fig:comparativa-series}
\end{figure}
```

2. Para gráficas de barras:

```latex
\begin{axis}[
  ybar,
  symbolic x coords={Método A, Método B, Método C},
  xtick=data,
  ylabel={Precisión (\%)},
  ymin=0, ymax=100,
  nodes near coords,
]
  \addplot coordinates {(Método A, 78) (Método B, 91) (Método C, 85)};
\end{axis}
```

3. Si la gráfica tarda en compilar, activar la caché de TikZ en
   `configuracion.tex`:

```latex
\EPSsetup{
  optimizar-tikz = true,
}
```

---

*Última actualización: Febrero 2026. Ver `docs/AI_CONTEXT.md` para la
referencia técnica completa.*
