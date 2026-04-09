# CLAUDE.md — Instrucciones para Claude

Plantilla LaTeX para TFG/TFM de la Escuela Politécnica Superior (EPS),
Universidad de Alicante. Versión 2.1.0 (2026).

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
cls/eps-metadata.tex  → Metadatos PDF/UA-2 (solo cambiar lang= si cambia idioma).
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
  optimizar-tikz = true,
  borrador    = false,
}
```

### Titulaciones disponibles

**Grados:** `arquitectura`, `arquitectura-tecnica`, `civil`, `informatica`,
`multimedia`, `quimica`, `robotica`, `teleco`

**Másteres:** `master-agua`, `master-caminos`, `master-ciberseguridad`,
`master-edificacion`, `master-geologica`, `master-informatica`,
`master-materiales`, `master-moviles`, `master-prevencion`, `master-quimica`,
`master-robotica`, `master-teleco`, `master-web`

---

## Regla crítica de idioma

Cuando se cambia `idioma` en `configuracion.tex`, **también** hay que editar
`cls/eps-metadata.tex` y cambiar el valor de `lang=`:

| `idioma` en `\EPSsetup` | `lang=` en `eps-metadata.tex` |
|---|---|
| `espanol` | `es-ES` |
| `valenciano` | `ca-ES` |
| `ingles` | `en-GB` |

El idioma afecta a: títulos automáticos (Tabla, Figura, Bibliografía...),
formato de citas, metadatos PDF y accesibilidad.

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

\begin{definitionbox}{Definición: término}
  Descripción del término.
\end{definitionbox}

\begin{examplebox}{Ejemplo}
  Caso de uso.
\end{examplebox}
```

### Entornos del módulo `[software]`

```latex
% Consola de terminal
\begin{terminal}[title={Terminal}]
$ git clone https://github.com/usuario/repo.git
$ cd repo && make
\end{terminal}

% Endpoint REST
\begin{apiendpoint}{GET}{/api/v1/usuarios}{Obtiene lista de usuarios}
  Parámetros: page (int), limit (int)
\end{apiendpoint}

% Árbol de directorios
\begin{dirtreebox}
  .
  ├── src/
  │   └── main.py
  └── tests/
\end{dirtreebox}
```

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

**Lenguajes disponibles:** `pythoncode`, `jscode`, `cppcode`, `javacode`,
`matlabcode`, `bashcode`, `sqlcode`, `jsoncode`, `yamlcode`, `htmlcode`,
`csscode`, `rcode`, `rustcode`, `gocode`, `phpcode`.

**Tema oscuro:** añadir sufijo `Dark` → `pythoncodeDark`, `jscodeDark`, etc.

**Código inline:** `\mintinline{python}{print("hola")}`

**Opciones útiles:**

```latex
\begin{pythoncode}[
  title={mi_script.py},
  firstline=10,
  lastline=25,
  highlightlines={12,15-18},
  linenos=false,
]
```

---

## Tablas

Usar siempre `booktabs`. Nunca `\hline`.

```latex
\begin{table}[htbp]
  \centering
  \caption{Comparativa de algoritmos.}
  \label{tab:comparativa}
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
  \includegraphics[width=0.8\textwidth]{recursos/figuras/diagrama}
  \caption{Diagrama de arquitectura del sistema.}
  \label{fig:arquitectura}
\end{figure}
```

Subfiguras:

```latex
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.45\textwidth}
    \includegraphics[width=\textwidth]{imagen1}
    \caption{Antes del procesado.}
    \label{fig:antes}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.45\textwidth}
    \includegraphics[width=\textwidth]{imagen2}
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
|---|---|
| `chap:` | Capítulo |
| `sec:` | Sección o subsección |
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

## Accesibilidad (PDF/UA-2)

El archivo `cls/eps-metadata.tex` ya está configurado con `pdfstandard=ua-2`.
Para añadir texto alternativo a imágenes:

```latex
\includegraphics[width=0.8\textwidth, alt={Descripción de la imagen}]{ruta}
```

Ver `docs/ACCESIBILIDAD.md` para la guía completa.

---

## Antipatrones — qué NO hacer

- ❌ Sugerir `pdflatex` o `xelatex`. Solo LuaLaTeX.
- ❌ Usar `\usepackage[utf8]{inputenc}`. LuaLaTeX es nativo UTF-8.
- ❌ Usar `\usepackage{subfigure}` o `subfig`. Usar `subcaption`.
- ❌ Usar `\begin{verbatim}` o `lstlisting` para código. Usar entornos `*code`.
- ❌ Escribir contenido en `main.tex`.
- ❌ Crear portadas con TikZ manualmente. Usar `\generarportada`.
- ❌ Usar `\hline` en tablas. Usar `\toprule`, `\midrule`, `\bottomrule`.
- ❌ Usar `\bibliography{}` + `\bibliographystyle{}`. Usar `\printbibliography`.
- ❌ Modificar `cls/eps-tfg.cls` para ajustes de formato menores.
- ❌ Usar paquetes obsoletos: `utf8x`, `t1enc`, `ae`, `times`, `mathptmx`.
- ❌ Usar `\include{}` para capítulos si no se quiere salto de página forzado.

---

## Diagnóstico de errores

Si el usuario reporta un error, pedir las últimas 30 líneas de `main.log`.

| Error | Causa probable | Solución |
|---|---|---|
| `Undefined control sequence` | Comando no definido o paquete no cargado | Verificar módulo de componentes activo |
| `You must invoke LaTeX with -shell-escape` | Falta flag | Usar `make` o añadir `-shell-escape` |
| `Pygments not found` | Python/minted no instalado | `pip install latexminted` |
| `Citation 'X' undefined` | Biber no ejecutado | `make` completo o `biber main` |
| `Font ... not found` | TeX Live incompleto | Instalar TeX Live completo |
| `Missing $ inserted` | Símbolo matemático fuera de modo math | Encerrar en `$...$` |
| `File 'X.sty' not found` | Paquete no instalado | `tlmgr install X` |
| `I found no \bibdata command` | Usando BibTeX en lugar de Biber | Verificar que se usa `biber`, no `bibtex` |

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
