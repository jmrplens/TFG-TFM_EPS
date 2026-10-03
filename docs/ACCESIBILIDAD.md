# ♿ Accesibilidad en Documentos LaTeX

Esta guía explica qué hace la plantilla para generar PDFs accesibles (PDF etiquetado) y qué debes hacer tú al escribir para que el resultado sea útil a personas con discapacidades visuales o que usen lectores de pantalla.

> **Estado actual:** la plantilla genera un **PDF etiquetado** y, por defecto ([`accesible = true`](#pdf-accesible-accesible--true)), lo **declara conforme a PDF/UA-2**. El documento de ejemplo supera la validación de veraPDF (PDF/UA-2 y WTPDF 1.0) en los tres idiomas, aunque quedan [limitaciones conocidas](#limitaciones-conocidas).

---

## 📋 Índice

- [Introducción](#introducción)
- [Por qué es importante](#por-qué-es-importante)
- [Qué hace la plantilla](#qué-hace-la-plantilla)
- [PDF accesible (`accesible = true`)](#pdf-accesible-accesible--true)
- [Limitaciones conocidas](#limitaciones-conocidas)
- [Texto alternativo para imágenes](#texto-alternativo-para-imágenes)
- [Tablas accesibles](#tablas-accesibles)
- [Ecuaciones matemáticas](#ecuaciones-matemáticas)
- [Comprobación de accesibilidad](#comprobación-de-accesibilidad)
- [Recursos adicionales](#recursos-adicionales)

---

## Introducción

La accesibilidad en documentos PDF permite que personas con discapacidades visuales o motoras puedan:

- Navegar por el documento usando lectores de pantalla
- Comprender el contenido de imágenes mediante texto alternativo
- Entender la estructura del documento (capítulos, secciones)
- Leer tablas de forma lógica

### Estándares relevantes

| Estándar | Descripción |
| ---------- | ------------- |
| **PDF/UA-1** | ISO 14289-1:2014 - Accesibilidad universal para PDF |
| **PDF/UA-2** | ISO 14289-2:2024 - Versión actualizada del estándar |
| **WCAG 2.1** | Web Content Accessibility Guidelines (aplicable a PDFs) |

---

## Por qué es importante

A partir de 2025-2026, varias legislaciones exigen documentos accesibles:

- **European Accessibility Act (EAA)**: Vigente desde junio 2025
- **ADA Title II Update**: Vigente desde abril 2026 en EE.UU.
- **Normativa universitaria**: Muchas universidades requieren accesibilidad

> **Nota:** Aunque la EPS UA no exige actualmente PDFs accesibles para TFG/TFM, es buena práctica preparar documentos accesibles, especialmente si planeas publicar tu trabajo.

---

## Qué hace la plantilla

El etiquetado ya está activado en `cls/eps-metadata.tex`, que `main.tex` carga antes de `\documentclass`. **No tienes que añadir ni cambiar nada**:

```latex
\IfFormatAtLeastTF{2025-11-01}
  {\DocumentMetadata{tagging=on, pdfversion=2.0, lang=es-ES}}
  {\DocumentMetadata{testphase=phase-I, pdfversion=2.0, lang=es-ES}}
```

| Versión de LaTeX | Etiquetado |
| ------------------ | ------------ |
| LaTeX 2025-11 o posterior (TeX Live 2025 actualizado, TeX Live 2026) | `tagging=on`: árbol de estructura completo (párrafos, listas, figuras con texto alternativo, tablas, fórmulas, índice...) |
| Anterior a LaTeX 2025-11 (TeX Live 2024, mínimo soportado, o TeX Live 2025 sin actualizar) | `testphase=phase-I`: etiquetado básico |

- **Idioma:** el valor `lang=es-ES` es solo el inicial. La clase lo sustituye por el idioma de `idioma` en `configuracion.tex` (`es-ES`, `ca-ES-valencia` o `en-GB`), así que **no hay que editar `cls/eps-metadata.tex`** al cambiar de idioma.
- **Estándar:** por defecto se declara `pdfstandard=ua-2` (opción [`accesible`](#pdf-accesible-accesible--true)).
- **Compatibilidad:** la clase incluye ajustes para que las opciones de listas de `enumitem`, `\ch` de `chemformula` y `threeparttable` funcionen con el etiquetado.
- **Ajustes de accesibilidad automáticos** (sin efecto si no hay etiquetado):
  - los títulos de capítulo, sección, subsección... se etiquetan como encabezados (`H1`, `H2`, `H3`...) dentro de secciones anidadas, para que el lector de pantalla pueda recorrer el documento por títulos (con LaTeX 2025-11 o posterior). También los títulos en línea de `\paragraph` y `\subparagraph`: el título es un encabezado y el texto que le sigue, un párrafo aparte;
  - una imagen sin texto alternativo recibe uno automático (ver [Texto alternativo para imágenes](#texto-alternativo-para-imágenes)), en lugar del nombre del archivo;
  - el índice general y los de figuras, tablas y códigos se etiquetan como índices, con un enlace en cada entrada (con LaTeX 2025-11 o posterior);
  - la portada no deja estructuras sueltas en el árbol del PDF;
  - los iconos decorativos (los de las cajas de aviso, el árbol de directorios, etc.) se marcan como artefacto, para que el lector de pantalla no lea el nombre del glifo («INFO-CIRCLE»);
  - los iconos que transmiten información se leen como texto: las casillas de `checklist` («Hecho», «Pendiente», «En curso»), `\pro`/`\con` («Ventaja», «Inconveniente»), `\rating{4}{5}` («4 de 5») y los indicadores de cumplimiento (`\controlok`, `\sparamok`...). Para tus propios iconos con significado, usa `\EPSiconoTexto{texto}{icono}`, por ejemplo `\EPSiconoTexto{Aprobado}{\faCheck}`;
  - los fragmentos escritos en otro idioma con `otherlanguage` (el Abstract) llevan su propio idioma (`/Lang`), para que el lector de pantalla cambie de voz;
  - las leyendas de figuras y tablas se etiquetan como `Caption` aunque haya cajas de `tcolorbox` con título;
  - las figuras y tablas etiquetadas se agrupan al final de cada capítulo, en lugar de al final del documento;
  - el código en línea (`\mintinline`) no genera fórmulas vacías;
  - el texto de los bloques de código conserva los espacios (el lector de pantalla y el texto copiado leen `def fibonacci(n):`, no `deffibonacci(n):`), con LaTeX 2025-11 o posterior;
  - las notas de `threeparttable` (`tablenotes`) no quedan dentro de un párrafo, algo que PDF 2.0 no permite;
  - `\includepdf` solo pide el texto alternativo de las páginas que inserta (`alt={...}`), no el de la medida interna que hace `pdfpages`.
- **Desactivar el etiquetado:** con LaTeX 2025-11 o posterior, la única forma es quitar `\input{eps-metadata}` de `main.tex` (cualquier `\DocumentMetadata` carga ya los módulos de etiquetado). A cambio se pierden el etiquetado, los metadatos XMP y la comprobación de motor LuaLaTeX; la compilación apenas se acelera.

---

## PDF accesible (`accesible = true`)

La opción está activada en el `configuracion.tex` que se distribuye:

```latex
\EPSsetup{
  ...
  accesible = true,   % PDF/UA-2 (por defecto)
}
```

Con ella la plantilla:

- **declara el PDF conforme a PDF/UA-2** en los metadatos XMP (`pdfstandard=ua-2`);
- **avisa** si usas construcciones que estropean el PDF accesible: `\diagbox` y las tablas `tblr` de `tabularray`.

La falta de texto alternativo **no detiene la compilación**: la imagen recibe un texto automático y se muestra un aviso (ver [Texto alternativo para imágenes](#texto-alternativo-para-imágenes)). Revisa los avisos `Package eps-tfg Warning: Falta el texto alternativo...` antes de entregar.

Requiere LaTeX 2025-11 o posterior (TeX Live 2025 actualizado o TeX Live 2026). Con versiones anteriores (o si se ha quitado `\input{eps-metadata}` de `main.tex`) el etiquetado es parcial: la opción solo muestra un aviso y no declara nada. Para no declarar la conformidad, pon `accesible = false`.

La integración continua del repositorio compila el documento de ejemplo en español, valenciano e inglés y valida cada PDF con veraPDF (PDF/UA-2); la comprobación falla si alguno deja de ser conforme. Un validador comprueba lo que se puede comprobar automáticamente; lo demás depende de ti: que el texto alternativo describa la imagen, que las tablas de datos marquen su cabecera (`\EPScabeceraTabla`), que los enlaces tengan un texto con sentido... Repasa el [checklist](#checklist-básico) antes de entregar.

---

## Limitaciones conocidas

Aunque el documento de ejemplo supera la validación, quedan limitaciones ajenas a lo que escribas:

- **KOMA-Script (`scrbook`)**, base de la clase, aún no soporta oficialmente el etiquetado. La clase añade el etiquetado de títulos e índices con los ganchos documentados de KOMA y la interfaz de etiquetado de LaTeX, que todavía está en fase de pruebas y puede cambiar.
- `\minisec` se etiqueta como párrafo, no como encabezado (no tiene nivel en la jerarquía de títulos).
- LaTeX no asocia todavía los destinos de las referencias cruzadas a figuras y tablas con su estructura (aviso `Destination ... has no related structure`). Es una limitación del núcleo de LaTeX.
- Varios paquetes que usa la plantilla figuran como **incompatibles** en el estado oficial del etiquetado de LaTeX: `chemformula`, `chemfig`, `minted`, `caption`, `subcaption`, `dirtree`, `listings`, `multirow`, `pgfplots` y `threeparttable`.
- Las tablas con `booktabs` se etiquetan sin celdas de cabecera (`TH`) salvo que se indique (ver [Tablas accesibles](#tablas-accesibles)).

### Requisitos

- **TeX Live 2024** o posterior (etiquetado completo con LaTeX 2025-11 o posterior)
- **LuaLaTeX** (obligatorio en esta plantilla; necesario para MathML)
- Paquete `unicode-math` para matemáticas accesibles (ya incluido)

---

## Texto alternativo para imágenes

Todas las imágenes deben tener texto alternativo (`alt={...}`) que describa su contenido.

Si una imagen no lo tiene, la plantilla le pone uno automático, para que el lector de pantalla no lea el nombre del archivo:

- si está en una figura con leyenda, la leyenda con su número: «Figura 3.2: Arquitectura del sistema propuesto». La leyenda va después de la imagen, así que se toma de la compilación anterior: con `make` (o `latexmk`) aparece desde la segunda pasada;
- si no, «Imagen 1», «Imagen 2»...

Y avisa con el archivo y el texto que ha usado:

```text
Package eps-tfg Warning: Falta el texto alternativo de la imagen
(eps-tfg)                'recursos/figuras/arquitectura.pdf'.
(eps-tfg)                En el PDF se usa 'Figura 3.2: Arquitectura del sistema propuesto'.
```

El texto automático solo dice qué es la imagen, no lo que muestra: escribe una descripción de verdad con `alt={...}`.


### Imágenes informativas

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth, alt={Arquitectura del sistema 
    mostrando tres capas: presentación, lógica de negocio y datos}]{arquitectura}
    \caption{Arquitectura del sistema propuesto}
    \label{fig:arquitectura}
\end{figure}
```

### Diagramas y gráficas (TikZ, pgfplots)

Un `tikzpicture` sin texto alternativo **no existe para un lector de pantalla** (y LaTeX no avisa). Añade `alt` en sus opciones:

```latex
\begin{figure}[htbp]
    \centering
    \begin{tikzpicture}[alt={Diagrama de flujo: entrada, validación y,
      si es correcta, almacenamiento en la base de datos}]
        \node[draw] (a) {Entrada};
        \node[draw, right=of a] (b) {Validación};
        \draw[->] (a) -- (b);
    \end{tikzpicture}
    \caption{Flujo de validación de datos.}
    \label{fig:flujo-validacion}
\end{figure}
```

Si el dibujo es solo decorativo, usa `artifact` en lugar de `alt`.

### Imágenes decorativas

Las imágenes puramente decorativas deben marcarse como artefactos (los lectores de pantalla las ignoran):

```latex
\includegraphics[width=0.8\textwidth, artifact]{separador}
```

### Buenas prácticas para texto alternativo

| ✅ Hacer | ❌ Evitar |
| --------- | ---------- |
| Describir el **significado** de la imagen | Describir la apariencia visual |
| Ser conciso pero completo | Texto excesivamente largo |
| Incluir datos clave de gráficas | "Gráfica mostrando datos" |
| Describir tendencias y patrones | Listar todos los valores |

**Ejemplo para una gráfica:**

```latex
% Malo:
alt={Una gráfica de barras azules}

% Bueno:
alt={Comparativa de rendimiento: el algoritmo A es 40% más rápido 
que B en todos los casos de prueba}
```

---

## Tablas accesibles

Las tablas deben tener:

1. **Encabezados claramente marcados**
2. **Caption descriptivo**
3. **Estructura simple** (evitar celdas combinadas complejas)

Indica qué filas son de cabecera con `\EPScabeceraTabla` justo antes del `tabular` (dentro del entorno `table` solo afecta a esa tabla). Así las celdas de la primera fila se etiquetan como `TH` en lugar de `TD` y el lector de pantalla asocia cada dato con su columna. Si la cabecera ocupa dos filas, usa `\EPScabeceraTabla[2]`. Con versiones de LaTeX anteriores a 2025-11 no hace nada (no da error). En `longtable` no hace falta: las filas de `\endfirsthead`/`\endhead` ya son cabecera.

Para que las tablas se etiqueten bien:

- usa `tabular`, `tabularx` o `longtable` con `booktabs`, y `\multicolumn`/`\multirow` para combinar celdas;
- **evita** `tabularray` (`tblr`): sus tablas no se etiquetan como tablas;
- **evita** `\diagbox`: deja la tabla abierta y todo el texto que sigue queda dentro de ella. Usa una cabecera de texto, como «Impacto / Probabilidad»;
- no uses `[H]` en figuras y tablas (paquete `float`): la leyenda acaba dentro del párrafo anterior. Usa `[htbp]`.

```latex
\begin{table}[htbp]
    \centering
    \caption{Comparativa de algoritmos de ordenación}
    \label{tab:algoritmos}
    \EPScabeceraTabla  % la fila 1 es cabecera
    \begin{tabular}{lrrr}
        \toprule
        \textbf{Algoritmo} & \textbf{Mejor caso} & \textbf{Caso medio} & \textbf{Peor caso} \\
        \midrule
        Quicksort  & $O(n \log n)$ & $O(n \log n)$ & $O(n^2)$ \\
        Mergesort  & $O(n \log n)$ & $O(n \log n)$ & $O(n \log n)$ \\
        Heapsort   & $O(n \log n)$ & $O(n \log n)$ & $O(n \log n)$ \\
        \bottomrule
    \end{tabular}
\end{table}
```

---

## Ecuaciones matemáticas

Con LuaLaTeX y LaTeX 2025-11 o posterior, cada fórmula se etiqueta como `Formula` y lleva adjuntos, sin que tengas que hacer nada, su versión en MathML (generada por `luamml`) y su código LaTeX, que los lectores de pantalla compatibles usan para leerla:

```latex
\usepackage{unicode-math}  % Ya incluido en la plantilla

% Las ecuaciones se etiquetan automáticamente
\begin{equation}
    E = mc^2
    \label{eq:energia}
\end{equation}
```

Escribe las fórmulas siempre en modo matemático (`$...$`, `equation`, `align`...), no con texto en cursiva o símbolos sueltos: solo así se generan el MathML y la etiqueta `Formula`.

---

## Comprobación de accesibilidad

### Herramientas de validación

| Herramienta | Descripción | Enlace |
| ------------- | ------------- | -------- |
| **Adobe Acrobat Pro** | Comprobador de accesibilidad integrado | [adobe.com](https://www.adobe.com/acrobat) |
| **PAC** | Verificador PDF/UA gratuito | [pdfua.foundation](https://pdfua.foundation/en/pac-download) |
| **PAVE** | Validador online gratuito | [pave-pdf.org](https://pave-pdf.org/) |

También puedes comprobar que el PDF está etiquetado con `pdfinfo main.pdf` (línea `Tagged: yes`). La integración continua del repositorio valida además con veraPDF el PDF de cada idioma (artefacto `informe-accesibilidad`).

### Checklist básico

- [ ] El documento tiene un título definido
- [ ] El idioma está especificado correctamente
- [ ] Todas las imágenes informativas tienen texto alternativo
- [ ] Las tablas tienen encabezados marcados
- [ ] El orden de lectura es lógico
- [ ] Los enlaces tienen texto descriptivo
- [ ] El contraste de colores es suficiente

---

## Recursos adicionales

### Documentación oficial

| Recurso | URL |
| --------- | ----- |
| LaTeX Tagging Project | [latex3.github.io/tagging-project](https://latex3.github.io/tagging-project/documentation/usage-instructions) |
| PDF/UA Foundation | [pdfua.foundation](https://pdfua.foundation/) |

### Tutoriales

- [Creating Accessible PDFs with LaTeX](https://latex3.github.io/tagging-project/documentation/usage-instructions) - Guía oficial
- [Overleaf Blog: Accessible PDFs](https://www.overleaf.com/blog/accessible-pdfs-with-latex) - Tutorial práctico
- [Texas A&M: Accessible LaTeX](https://esail.tamu.edu/faculty-tutorials/accessible-latex-pdf-ua-2-overleaf-2025/) - Tutorial universitario

---

## Ver también

- [Figuras y Gráficas](FIGURAS_GRAFICAS.md) - Imágenes con texto alternativo
- [Tablas](TABLAS.md) - Tablas accesibles
- [Ecuaciones](ECUACIONES.md) - Matemáticas con unicode-math

---

> **Importante:** La accesibilidad completa con LaTeX sigue en desarrollo activo. El LaTeX Tagging Project está mejorando constantemente el soporte. Consulta la [documentación oficial](https://latex3.github.io/tagging-project/) para las últimas actualizaciones.
