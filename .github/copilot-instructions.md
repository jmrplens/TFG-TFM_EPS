# Instrucciones para GitHub Copilot — Plantilla TFG/TFM EPS UA

Plantilla LaTeX para TFG/TFM de la Escuela Politécnica Superior (EPS),
Universidad de Alicante. Versión 2.1.0 (2026).

---

## Reglas críticas

1. **Motor:** SIEMPRE **LuaLaTeX**. Nunca sugieras `pdflatex` ni `xelatex`.
   LuaLaTeX maneja UTF-8 nativamente; no usar `\usepackage[utf8]{inputenc}`.
2. **Bibliografía:** **BibLaTeX + Biber**, estilo APA 7. Nunca BibTeX puro ni
   `\bibliographystyle{}`.
3. **Código fuente:** Paquete **minted 3.x** con `latexminted`. Usar siempre
   los entornos predefinidos en `sty/eps-codigo.sty`, nunca `verbatim` ni
   `lstlisting`.
4. **Tablas:** Siempre con `booktabs`. Nunca `\hline`.
5. **Portadas:** Generadas automáticamente con `\generarportada[ambas]`.
   Nunca crear portadas manualmente.
6. **Paquetes obsoletos prohibidos:** `utf8x`, `subfigure`, `subfig`, `t1enc`,
   `ae`, `times`, `mathptmx`.

---

## Estructura del proyecto

```text
main.tex              → Raíz. Solo estructura (inputs, usepackage, addbibresource).
configuracion.tex     → Datos del usuario (\EPSsetup{...}).
referencias.bib       → Bibliografía BibLaTeX.
cls/eps-tfg.cls       → Clase principal (no modificar).
cls/eps-metadata.tex  → Metadatos PDF/UA-2 (solo cambiar lang= al cambiar idioma).
sty/eps-codigo.sty    → Entornos de código (minted).
sty/eps-componentes.sty → Cargador modular de componentes.
sty/componentes/      → Módulos: software, telecom, arquitectura, quimica, etc.
contenido/capitulos/  → Un .tex por capítulo.
contenido/anexos/     → Anexos y acrónimos.
contenido/frontmatter/→ Resumen, agradecimientos.
```

---

## Configuración del documento

```latex
% En configuracion.tex
\EPSsetup{
  titulo      = {Título del trabajo},
  subtitulo   = {Subtítulo opcional},
  autor       = {Nombre Apellido1 Apellido2},
  genero      = m,              % m, f, n (neutro → "Autoría")
  email       = nombre@alu.ua.es,
  tutor       = {Dr. Nombre Apellido},
  tutor-genero = m,
  tutor-departamento = {Departamento de ...},
  titulacion  = informatica,    % ver lista completa abajo
  idioma      = espanol,        % espanol, valenciano, ingles
  fecha       = {Junio 2026},
  optimizar-tikz = true,
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

## Regla de idioma

Al cambiar `idioma` en `configuracion.tex`, actualizar también `lang=` en
`cls/eps-metadata.tex`:

| `idioma` | `lang=` |
| --- | --- |
| `espanol` | `es-ES` |
| `valenciano` | `ca-ES` |
| `ingles` | `en-GB` |

---

## Componentes especializados

Activar en `main.tex`:

```latex
\usepackage[software]{eps-componentes}       % Informática, Multimedia, Robótica
\usepackage[telecom]{eps-componentes}        % Telecomunicaciones
\usepackage[arquitectura]{eps-componentes}   % Arquitectura, Civil
\usepackage[quimica]{eps-componentes}        % Química
\usepackage[geologia]{eps-componentes}       % Geología
\usepackage[prevencion]{eps-componentes}     % Prevención de Riesgos
\usepackage[all]{eps-componentes}            % Todos
```

### Cajas de aviso (siempre disponibles)

```latex
\begin{infobox}{Título}    Texto informativo.    \end{infobox}
\begin{warningbox}{Título} Texto de advertencia. \end{warningbox}
\begin{dangerbox}{Título}  Texto de peligro.     \end{dangerbox}
\begin{successbox}{Título} Operación correcta.   \end{successbox}
\begin{tipbox}{Título}     Consejo útil.         \end{tipbox}
\begin{notebox}{Título}    Nota adicional.       \end{notebox}
```

### Contenedores de contenido (siempre disponibles)

```latex
\begin{definitionbox}{Definición: término}
  Descripción del término.
\end{definitionbox}

\begin{examplebox}{Ejemplo práctico}
  Caso de uso ilustrativo.
\end{examplebox}
```

### Módulo `[software]`

```latex
% Terminal / consola
\begin{terminal}[title={bash}]
$ npm install && npm start
\end{terminal}

% Endpoint REST
\begin{apiendpoint}{POST}{/api/v1/login}{Autenticación de usuario}
  Body: { "email": "...", "password": "..." }
\end{apiendpoint}

% Árbol de directorios
\begin{dirtreebox}
  proyecto/
  ├── src/
  │   ├── main.py
  │   └── utils.py
  └── tests/
\end{dirtreebox}
```

### Módulo `[telecom]`

```latex
% Trama de protocolo
\begin{protocolframe}
  % Campos de la trama
\end{protocolframe}
```

---

## Entornos de código

Usar siempre los entornos de `sty/eps-codigo.sty`:

```latex
% Python
\begin{pythoncode}[title={clasificador.py}]
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
\end{pythoncode}

% JavaScript
\begin{jscode}[title={index.js}]
const app = require('./app');
app.listen(process.env.PORT || 3000);
\end{jscode}

% C++
\begin{cppcode}
#include <vector>
std::vector<int> v = {1, 2, 3};
\end{cppcode}

% Java
\begin{javacode}
public class Main {
    public static void main(String[] args) {}
}
\end{javacode}

% SQL
\begin{sqlcode}
SELECT nombre, email FROM usuarios WHERE activo = 1;
\end{sqlcode}

% JSON
\begin{jsoncode}
{
  "nombre": "Juan",
  "edad": 25,
  "activo": true
}
\end{jsoncode}

% Bash
\begin{bashcode}
#!/bin/bash
for f in *.tex; do echo "$f"; done
\end{bashcode}

% YAML
\begin{yamlcode}
version: '3.8'
services:
  web:
    image: nginx:latest
\end{yamlcode}
```

**Tema oscuro:** sufijo `Dark` → `pythoncodeDark`, `jscodeDark`, etc.

**Código inline:** `\mintinline{python}{len(lista)}`

**Opciones de bloque:**

```latex
\begin{pythoncode}[
  title={script.py},
  firstline=5,
  lastline=20,
  highlightlines={8,12-15},
  linenos=false,
]
```

---

## Tablas

```latex
\begin{table}[htbp]
  \centering
  \caption{Resultados de los experimentos.}
  \label{tab:resultados}
  \begin{tabular}{lrr}
    \toprule
    Método       & Precisión & Tiempo (ms) \\
    \midrule
    Baseline     & 78.3\%    & 12          \\
    Propuesto    & 91.7\%    & 18          \\
    Estado arte  & 89.2\%    & 45          \\
    \bottomrule
  \end{tabular}
\end{table}
```

---

## Figuras

```latex
% Figura simple
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{recursos/figuras/arquitectura}
  \caption{Arquitectura del sistema propuesto.}
  \label{fig:arquitectura}
\end{figure}

% Subfiguras
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{imagen-a}
    \caption{Escenario A.}
    \label{fig:escenario-a}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{imagen-b}
    \caption{Escenario B.}
    \label{fig:escenario-b}
  \end{subfigure}
  \caption{Comparativa de escenarios.}
  \label{fig:escenarios}
\end{figure}
```

---

## Ecuaciones

```latex
% Numerada
\begin{equation}
  \hat{y} = \sigma\!\left(\sum_{i=1}^{n} w_i x_i + b\right)
  \label{eq:neurona}
\end{equation}

% Alineadas
\begin{align}
  \nabla_\theta J(\theta) &= \frac{1}{m} X^T (X\theta - y) \\
                          &= \frac{1}{m} X^T \varepsilon
  \label{eq:gradiente}
\end{align}

% Sin numerar
\begin{equation*}
  P(A|B) = \frac{P(B|A)\,P(A)}{P(B)}
\end{equation*}
```

---

## Bibliografía

```latex
% En el texto
\parencite{apellido2024}          % (Apellido, 2024)
\textcite{apellido2024}           % Apellido (2024)
\parencite[pp.~10--15]{libro2023} % (Autor, 2023, pp. 10–15)

% En referencias.bib
@article{apellido2024,
  author  = {Apellido, Nombre},
  title   = {Título del artículo},
  journal = {Nombre de la Revista},
  year    = {2024},
  volume  = {10},
  pages   = {1--20},
  doi     = {10.xxxx/xxxxx},
}

@online{web2024,
  author  = {{Organización}},
  title   = {Título},
  url     = {https://ejemplo.com},
  urldate = {2024-06-01},
  year    = {2024},
}
```

---

## Glosarios y acrónimos

```latex
% Definir en contenido/anexos/acronimos.tex
\newacronym{ia}{IA}{Inteligencia Artificial}
\newacronym{api}{API}{Application Programming Interface}

% Usar en el texto
\gls{ia}       % Primera vez: "Inteligencia Artificial (IA)"; resto: "IA"
\acrshort{ia}  % Siempre: "IA"
\acrlong{ia}   % Siempre: "Inteligencia Artificial"
```

---

## Referencias cruzadas

Prefijos de etiquetas:

| Prefijo | Elemento |
| --- | --- |
| `chap:` | Capítulo |
| `sec:` | Sección |
| `fig:` | Figura |
| `tab:` | Tabla |
| `eq:` | Ecuación |
| `cod:` | Bloque de código |
| `teo:` | Teorema |
| `anexo:` | Anexo |

```latex
\label{fig:diagrama}
% ...
Como se muestra en la Figura~\ref{fig:diagrama}...
```

---

## Gráficas con PGFPlots

```latex
\begin{figure}[htbp]
  \centering
  \begin{tikzpicture}
    \begin{axis}[
      xlabel={Épocas},
      ylabel={Pérdida},
      grid=major,
      legend pos=north east,
    ]
      \addplot[blue, thick] coordinates {(1,0.9)(10,0.5)(50,0.2)(100,0.1)};
      \addlegendentry{Entrenamiento}
      \addplot[red, dashed] coordinates {(1,0.95)(10,0.6)(50,0.3)(100,0.15)};
      \addlegendentry{Validación}
    \end{axis}
  \end{tikzpicture}
  \caption{Curva de aprendizaje del modelo.}
  \label{fig:curva-aprendizaje}
\end{figure}
```

---

## Compilación

```bash
make          # Completa: lualatex + biber + 2× lualatex
make quick    # Solo lualatex (verificar sintaxis)
make clean    # Limpiar auxiliares
```

---

## Antipatrones — qué NO sugerir

- ❌ `pdflatex` o `xelatex`
- ❌ `\usepackage[utf8]{inputenc}`
- ❌ `\usepackage{subfigure}` o `subfig`
- ❌ `\begin{verbatim}` o `lstlisting` para código
- ❌ `\hline` en tablas
- ❌ `\bibliography{}` + `\bibliographystyle{}`
- ❌ Contenido en `main.tex`
- ❌ Portadas manuales con TikZ
- ❌ Paquetes: `utf8x`, `t1enc`, `ae`, `times`, `mathptmx`

---

## Diagnóstico de errores

Pedir siempre las últimas 30 líneas de `main.log`.

| Error | Solución |
| --- | --- |
| `You must invoke LaTeX with -shell-escape` | Usar `make` o añadir `-shell-escape` |
| `Pygments not found` | `pip install latexminted` |
| `Citation 'X' undefined` | Ejecutar `make` completo (biber) |
| `Font ... not found` | Instalar TeX Live completo |
| `Missing $ inserted` | Encerrar símbolo en `$...$` |
| `File 'X.sty' not found` | `tlmgr install X` |

---

## Archivos de referencia

- `AGENTS.md` — Instrucciones para agentes de código
- `CLAUDE.md` — Instrucciones para Claude
- `docs/AI_CONTEXT.md` — Referencia técnica completa
- `docs/AI_WORKFLOWS.md` — Flujos de trabajo para tareas comunes
- `docs/COMPONENTES.md` — Catálogo de componentes visuales
