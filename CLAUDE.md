# CLAUDE.md — Instrucciones para Claude

Plantilla LaTeX para TFG/TFM de la Escuela Politécnica Superior (EPS),
Universidad de Alicante. Versión 2.2.2 (2026).

Motor: **LuaLaTeX** (obligatorio). Bibliografía: **BibLaTeX + Biber** (APA 7).
Código: **minted 3.x** con `latexminted`.

---

## Comandos de compilación

```bash
make          # Compilación completa (lualatex + biber + 2× lualatex)
make quick    # Una pasada (verificar sintaxis rápidamente)
make clean    # Eliminar archivos auxiliares
make watch    # Compilación continua con latexmk
```

Para diagnosticar errores: leer las últimas 30 líneas de `main.log` o la
salida de `make quick`.

---

## Estructura de archivos

```text
main.tex              → Raíz. Solo estructura, nunca contenido.
configuracion.tex     → Datos del autor, título, titulación, idioma.
referencias.bib       → Entradas bibliográficas (BibLaTeX).
cls/eps-tfg.cls       → Clase principal (no modificar).
cls/eps-metadata.tex  → Etiquetado PDF y metadatos (no hace falta tocarlo).
sty/eps-codigo.sty    → Entornos de código con minted.
sty/eps-componentes.sty → Cargador modular de componentes.
sty/componentes/      → Módulos por disciplina (software, telecom, etc.).
contenido/capitulos/  → Un .tex por capítulo.
contenido/anexos/     → Anexos y acrónimos.
contenido/frontmatter/→ Resumen, agradecimientos.
recursos/logos/       → Logotipos institucionales.
docs/                 → Documentación técnica.
```

---

## Configuración del documento

Toda la configuración del usuario va en `configuracion.tex` mediante
`\EPSsetup{...}`.

### Claves principales

```latex
\EPSsetup{
  titulo      = {Título del trabajo},
  subtitulo   = {Subtítulo opcional},
  autor       = {Nombre Apellido1 Apellido2},
  genero      = m,   % m, f, n (neutro)
  email       = nombre@alu.ua.es,
  tutor       = {Dr. Nombre Apellido},
  tutor-genero = m,
  tutor-departamento = {Departamento de ...},
  % cotutor   = {Dra. Nombre Apellido},   % opcional
  titulacion  = informatica,
  idioma      = espanol,
  fecha       = {Junio 2026},
  borrador    = false,   % true: muestra las notas \todo{} (borradores)
}
```

Otras claves opcionales: `cotutor-genero`, `cotutor-departamento`,
`facultad`, `universidad`, `ubicacion`. `optimizar-tikz` es obsoleta: se
acepta, pero no tiene efecto.

- `titulacion` es obligatoria: si falta o no es válida, la compilación se
  detiene con un error que lista los valores admitidos.
- Si faltan `titulo`, `autor` o `tutor`, se muestra un aviso.
- El `configuracion.tex` que se distribuye trae `borrador = true`; hay que
  ponerlo a `false` para la versión final (oculta las notas `\todo{}`).

### Titulaciones disponibles

**Grados:** `arquitectura`, `arquitectura-tecnica`, `civil`, `informatica`,
`multimedia`, `quimica`, `robotica`, `teleco`

**Másteres (TFM):** `master-agua`, `master-caminos`, `master-ciberseguridad`,
`master-ciencia-datos`, `master-edificacion`, `master-geologica`, `master-informatica`,
`master-materiales`, `master-moviles`, `master-prevencion`, `master-quimica`,
`master-robotica`, `master-teleco`, `master-web`

---

## Idioma

`idioma` (`espanol`, `valenciano` o `ingles`) cambia el idioma del documento:
títulos automáticos (Tabla, Figura, Bibliografía...), nombres de listas y
teoremas, formato de citas, separación silábica e idioma del PDF (`es-ES`,
`ca-ES-valencia` o `en-GB`, inglés británico). **No** hay que editar
`cls/eps-metadata.tex`: la clase fija el idioma del PDF a partir de `idioma`.

La portada se mantiene siempre en español (formato oficial de la EPS): tipo
de trabajo, titulación, etiquetas Autor/Tutor y fecha.

---

## Componentes especializados

Activar en `main.tex` según la titulación del alumno:

```latex
\usepackage[software]{eps-componentes}       % Informática, Multimedia, Robótica
\usepackage[telecom]{eps-componentes}        % Telecomunicaciones
\usepackage[arquitectura]{eps-componentes}   % Arquitectura, Civil
\usepackage[quimica]{eps-componentes}        % Química
\usepackage[geologia]{eps-componentes}       % Geología
\usepackage[prevencion]{eps-componentes}     % Prevención de Riesgos
\usepackage[all]{eps-componentes}            % Todos los módulos
```

### Entornos comunes (siempre disponibles)

```latex
\begin{infobox}{Título del aviso}
  Texto informativo.
\end{infobox}

\begin{warningbox}{Advertencia}
  Texto de advertencia.
\end{warningbox}

\begin{dangerbox}{Peligro}
  Texto de peligro.
\end{dangerbox}

\begin{successbox}{Éxito}
  Operación completada.
\end{successbox}

\begin{tipbox}{Consejo}
  Sugerencia útil.
\end{tipbox}

\begin{notebox}{Nota}
  Información adicional.
\end{notebox}

\begin{definitionbox}{Término}
  Descripción del término.
\end{definitionbox}

\begin{examplebox}[Ejemplo de uso]
  Caso de uso.
\end{examplebox}
```

- En las cajas de aviso (`infobox`, `warningbox`, `dangerbox`, `successbox`,
  `tipbox`, `notebox`) el título `{...}` es opcional; admiten además opciones
  de tcolorbox entre corchetes: `\begin{infobox}[colback=white]{Título}`.
- `definitionbox` exige el término entre llaves: `{Término}`.
- `examplebox` e `importantbox` llevan el título **entre corchetes** y es
  opcional (por defecto «Ejemplo» / «Importante»).

### Entornos del módulo `[software]`

El contenido de `terminal`, `apiendpoint` y `dirtreebox` **no es literal**
(no es verbatim): se escribe como texto LaTeX, escapando los caracteres
especiales (`\&`, `\#`, `\%`, `\_`, `\{`, `\}`, `\$`) y separando las líneas
con `\\`. Para scripts o salidas largas copiadas tal cual, usar `bashcode`.

```latex
% Consola de terminal: título opcional entre corchetes
\begin{terminal}[Terminal]
\prompt git clone https://github.com/usuario/repo.git\\
\prompt cd repo \&\& make\\
\promptroot apt install make\\
\termcomment{Comentario}
\end{terminal}

% Endpoint REST: {MÉTODO}{/ruta}; la descripción va en \apidescription
\begin{apiendpoint}{GET}{/api/v1/usuarios}
  \apidescription{Obtiene la lista de usuarios}
  \apiparams{
    page  & int & Página de resultados & No \\
    limit & int & Elementos por página & No \\
  }
\end{apiendpoint}

% Árbol de directorios: \dirtreeitem[nivel]{nombre}; «/» final = carpeta
\begin{dirtreebox}[Estructura del proyecto]
  \dirtreeitem[0]{proyecto/}
  \dirtreeitem[1]{src/}
  \dirtreeitem[2]{main.py}
  \dirtreeitem[1]{tests/}
\end{dirtreebox}
```

`\promptuser{usuario}` muestra `usuario@host:~$`. Dentro de `apiendpoint`
también existen `\apiheaders{...}`, `\apibody{tipo}{contenido}` y
`\apiresponse{código}{contenido}`; para JSON largo es mejor un `jsoncode`
aparte (las llaves `{ }` se pierden si no se escapan).

### Entornos del módulo `[telecom]`

```latex
% Trama de bits / protocolo
\begin{protocolframe}
  % Definición de campos de la trama
\end{protocolframe}
```

---

## Entornos de código

Usar **siempre** los entornos de `sty/eps-codigo.sty`. Nunca `verbatim` ni
`lstlisting`.

```latex
\begin{pythoncode}[title={algoritmo.py}]
def busqueda_binaria(lista, objetivo):
    izq, der = 0, len(lista) - 1
    while izq <= der:
        mid = (izq + der) // 2
        if lista[mid] == objetivo:
            return mid
        elif lista[mid] < objetivo:
            izq = mid + 1
        else:
            der = mid - 1
    return -1
\end{pythoncode}

\begin{jscode}[title={app.js}]
const express = require('express');
const app = express();
app.listen(3000);
\end{jscode}

\begin{sqlcode}
SELECT u.nombre, COUNT(p.id) AS total_pedidos
FROM usuarios u
LEFT JOIN pedidos p ON u.id = p.usuario_id
GROUP BY u.id;
\end{sqlcode}
```

**Lenguajes más usados:** `pythoncode`, `jscode`, `cppcode`, `javacode`,
`matlabcode`, `bashcode`, `sqlcode`, `jsoncode`, `yamlcode`, `htmlcode`,
`csscode`, `rcode`, `rustcode`, `gocode`, `phpcode`. La lista completa (46
lenguajes) está en `docs/CODIGO_FUENTE.md`; para cualquier otro lenguaje de
Pygments: `\begin{codigo}{lenguaje}`.

**Variantes:** sufijo `NN` sin números de línea (`pythoncodeNN`), `Dark` tema
oscuro (`pythoncodeDark`) y `DarkNN`.

**Código inline:** `\mintinline{python}{print("hola")}`

**Opciones útiles:** las opciones de minted van dentro de
`minted options={...}`; los `_` del título se escapan (`\_`).

```latex
\begin{pythoncode}[
  title={mi\_script.py},
  minted options={firstline=2, lastline=5, highlightlines={3,4}},
]
import math
def area(radio):
    r2 = radio ** 2
    return math.pi * r2
print(area(2))
\end{pythoncode}
```

Solo se muestran las líneas 2 a 5 (`firstline`, `lastline`) y se resaltan la 3
y la 4. Para quitar los números de línea, usar la variante `NN`
(`pythoncodeNN`).

---

## Tablas

Usar siempre `booktabs`. Nunca `\hline`. En tablas de datos, `\EPScabeceraTabla`
(`[2]` si la cabecera ocupa dos filas) antes del `tabular` marca la cabecera para
el PDF accesible.

```latex
\begin{table}[htbp]
  \centering
  \caption{Comparativa de algoritmos.}
  \label{tab:comparativa}
  \EPScabeceraTabla  % la fila 1 es cabecera (PDF accesible)
  \begin{tabular}{lccc}
    \toprule
    Algoritmo & Complejidad & Memoria & Estable \\
    \midrule
    Quicksort  & $O(n \log n)$ & $O(\log n)$ & No \\
    Mergesort  & $O(n \log n)$ & $O(n)$      & Sí \\
    Heapsort   & $O(n \log n)$ & $O(1)$      & No \\
    \bottomrule
  \end{tabular}
\end{table}
```

---

## Figuras

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth,
    alt={Diagrama de bloques: cliente, servidor y base de datos}]{recursos/figuras/diagrama}
  \caption{Diagrama de arquitectura del sistema.}
  \label{fig:arquitectura}
\end{figure}
```

Subfiguras:

```latex
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.45\textwidth}
    \includegraphics[width=\textwidth, alt={Imagen original}]{imagen1}
    \caption{Antes del procesado.}
    \label{fig:antes}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.45\textwidth}
    \includegraphics[width=\textwidth, alt={Imagen procesada}]{imagen2}
    \caption{Después del procesado.}
    \label{fig:despues}
  \end{subfigure}
  \caption{Comparativa del procesado de imagen.}
  \label{fig:comparativa}
\end{figure}
```

---

## Ecuaciones

```latex
% Ecuación numerada
\begin{equation}
  E = mc^2
  \label{eq:einstein}
\end{equation}

% Ecuaciones alineadas
\begin{align}
  f(x) &= x^2 + 2x + 1 \\
       &= (x + 1)^2
  \label{eq:cuadrado}
\end{align}

% Sin numerar
\begin{equation*}
  a^2 + b^2 = c^2
\end{equation*}

% Teoremas y definiciones
\begin{teorema}[Pitágoras]
  En un triángulo rectángulo, $a^2 + b^2 = c^2$.
  \label{teo:pitagoras}
\end{teorema}

\begin{definicion}
  Se define la derivada de $f$ en $x_0$ como...
\end{definicion}
```

---

## Bibliografía

Comandos de cita:

```latex
\parencite{clave}           % (Autor, 2024)
\textcite{clave}            % Autor (2024)
\parencite[p.~50]{clave}    % (Autor, 2024, p. 50)
\parencite{clave1,clave2}   % (Autor1, 2024; Autor2, 2023)
\citeauthor{clave}          % Autor
\citeyear{clave}            % 2024
```

Formato de entradas `.bib`:

```bibtex
@article{apellido2024,
  author  = {Apellido, Nombre and Otro, Autor},
  title   = {Título del artículo},
  journal = {Nombre de la Revista},
  year    = {2024},
  volume  = {15},
  number  = {3},
  pages   = {100--120},
  doi     = {10.1234/ejemplo},
}

@book{garcia2023,
  author    = {García, María},
  title     = {Título del Libro},
  publisher = {Editorial Ejemplo},
  year      = {2023},
  address   = {Madrid},
  isbn      = {978-84-xxxxx-xx-x},
}

@online{web2024,
  author  = {{Nombre Organización}},
  title   = {Título de la página},
  url     = {https://ejemplo.com},
  urldate = {2024-06-15},
  year    = {2024},
}
```

---

## Glosarios y acrónimos

Definir en `contenido/anexos/acronimos.tex`:

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

Usar en el texto:

```latex
\gls{ia}       % Primera vez: "Inteligencia Artificial (IA)"; siguientes: "IA"
\acrshort{ia}  % Siempre: "IA"
\acrlong{ia}   % Siempre: "Inteligencia Artificial"
\acrfull{ia}   % Siempre: "Inteligencia Artificial (IA)"
```

---

## Referencias cruzadas

Prefijos de etiquetas:

| Prefijo | Elemento |
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

```latex
% Definir
\label{fig:diagrama}

% Referenciar
Como se muestra en la Figura~\ref{fig:diagrama}...
Ver la Tabla~\ref{tab:resultados} en la página~\pageref{tab:resultados}.
```

---

## Portadas

Las portadas se generan automáticamente. No crear manualmente.

```latex
\generarportada[ambas]    % Portada color + portada B/N
\generarportada[color]    % Solo portada a color
\generarportada[bn]       % Solo portada en blanco y negro
```

---

## Accesibilidad (PDF etiquetado)

`cls/eps-metadata.tex` activa el etiquetado del PDF (`tagging=on` con LaTeX
2025-11 o posterior; `testphase=phase-I` con versiones anteriores, como TeX Live
2024). El PDF sale
etiquetado, pero **no declara conformidad PDF/UA-2**: todavía no se alcanza
(varios paquetes aún no son compatibles con el etiquetado). Los títulos se
etiquetan como encabezados y los índices llevan enlaces. Ver
`docs/ACCESIBILIDAD.md`.

Añadir siempre texto alternativo a las imágenes:

```latex
\includegraphics[width=0.8\textwidth, alt={Descripción de la imagen}]{ruta}
```

---

## Antipatrones — qué NO hacer

- ❌ Sugerir `pdflatex` o `xelatex`. Solo LuaLaTeX.
- ❌ Usar `\usepackage[utf8]{inputenc}`. LuaLaTeX es nativo UTF-8.
- ❌ Usar `\usepackage{subfigure}` o `subfig`. Usar `subcaption`.
- ❌ Usar `\begin{verbatim}` o `lstlisting` para código. Usar entornos `*code`.
- ❌ Escribir contenido en `main.tex`.
- ❌ Crear portadas con TikZ manualmente. Usar `\generarportada`.
- ❌ Usar `\hline` en tablas. Usar `\toprule`, `\midrule`, `\bottomrule`.
- ❌ Usar `[H]` en figuras/tablas, `\diagbox` o `tblr` (tabularray): estropean el
  PDF accesible. Usar `[htbp]`, una cabecera de texto y `tabular`.
- ❌ Dejar un `tikzpicture` informativo sin `alt={...}` (o `artifact` si es decorativo).
- ❌ Usar `\bibliography{}` + `\bibliographystyle{}`. Usar `\printbibliography`.
- ❌ Modificar `cls/eps-tfg.cls` para ajustes de formato menores.
- ❌ Usar paquetes obsoletos: `utf8x`, `t1enc`, `ae`, `times`, `mathptmx`.
- ❌ Usar `\include{}` para capítulos si no se quiere salto de página forzado.

---

## Diagnóstico de errores

Si el usuario reporta un error, pedir las últimas 30 líneas de `main.log`.

| Error | Causa probable | Solución |
| --- | --- | --- |
| `TeX capacity exceeded [main memory size=5000000]` | Causa más probable: se está compilando con XeLaTeX/pdfLaTeX (memoria fija). También puede deberse a una macro recursiva o a un documento desmesurado | Comprobar primero el motor: usar LuaLaTeX (en Overleaf: Menu → Compiler → LuaLaTeX). Si ya se usa LuaLaTeX, revisar el contexto del error en `main.log`. Ver `docs/OVERLEAF.md` |
| `ESTA PLANTILLA REQUIERE LuaLaTeX` | Guard de motor en `cls/eps-metadata.tex`: el motor no es LuaTeX | Compilar con LuaLaTeX (`make`, o en Overleaf Menu → Compiler → LuaLaTeX) |
| `Undefined control sequence` | Comando no definido o paquete no cargado | Verificar módulo de componentes activo |
| `You must invoke LaTeX with -shell-escape` | Falta flag | Usar `make` o añadir `-shell-escape` |
| `minted v3+ executable is not installed` / `latexminted` no encontrado | Falta `latexminted` (viene con TeX Live 2024+) | Comprobar `latexminted --version`; si falta, `tlmgr install minted` o instalar `texlive-latex-extra`. No usar `pip install` (falla con PEP 668); `pipx install latexminted` solo con MiKTeX o si el de TeX Live falla |
| `Citation 'X' undefined` | Biber no ejecutado | `make` completo o `biber main` |
| `Font ... not found` | TeX Live incompleto | Instalar TeX Live completo |
| `Missing $ inserted` | Símbolo matemático fuera de modo math, `_` sin escapar (p. ej. en `title={...}` de un entorno de código) o `$` literal en `terminal` | Encerrar en `$...$`; escapar `\_`; en `terminal` usar `\prompt` |
| `File 'X.sty' not found` | Paquete no instalado | `tlmgr install X` |
| `I found no \bibdata command` | Usando BibTeX en lugar de Biber | Verificar que se usa `biber`, no `bibtex` |
| `Package block Error: Some keys specified on the itemize environment are unknown` | Versión antigua de la plantilla compilada con LaTeX 2025-11 o posterior (TeX Live 2025 actualizado, 2026) | Actualizar la plantilla (al menos `cls/` y `sty/`) a la última versión |
| `ignored error Infinite glue shrinkage found in box being split` | Fallo de `longtable` 4.24 (LaTeX 2025-11) al partir una tabla entre páginas, con una versión antigua de la plantilla | Actualizar `cls/` (la clase corrige `longtable` 4.24). Detiene `latexmk` antes de terminar las pasadas y los números de página de los índices pueden quedar mal |

---

## Flujo de trabajo para tareas de edición

1. Leer el archivo a modificar antes de editar.
2. Hacer el cambio mínimo necesario.
3. Verificar con `make quick` que no hay errores de sintaxis.
4. Si hay referencias o bibliografía nuevas, ejecutar `make` completo.
5. Revisar las últimas líneas del log si hay errores.

---

## Archivos de referencia adicional

- `docs/AI_CONTEXT.md` — Referencia técnica completa con ejemplos
- `docs/AI_WORKFLOWS.md` — Flujos de trabajo para tareas comunes
- `docs/COMPONENTES.md` — Catálogo visual de todos los componentes
- `docs/BIBLIOGRAFIA.md` — Guía de bibliografía BibLaTeX
- `docs/CODIGO_FUENTE.md` — Guía de entornos de código
- `docs/ECUACIONES.md` — Guía de ecuaciones matemáticas
- `docs/TABLAS.md` — Guía de tablas con booktabs
