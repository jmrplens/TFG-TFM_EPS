# ♿ Accesibilidad en Documentos LaTeX

Esta guía explica qué hace la plantilla para generar PDFs accesibles (PDF etiquetado) y qué debes hacer tú al escribir para que el resultado sea útil a personas con discapacidades visuales o que usen lectores de pantalla.

> **Estado actual:** la plantilla genera un **PDF etiquetado**, pero **no declara conformidad PDF/UA-2**, porque todavía no se alcanza (ver [Limitaciones conocidas](#limitaciones-conocidas)).

---

## 📋 Índice

- [Introducción](#introducción)
- [Por qué es importante](#por-qué-es-importante)
- [Qué hace la plantilla](#qué-hace-la-plantilla)
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
- **Estándar:** no se declara `pdfstandard=ua-2`. Declararlo sin cumplirlo escribiría en los metadatos una conformidad falsa.
- **Compatibilidad:** la clase incluye ajustes para que las opciones de listas de `enumitem`, `\ch` de `chemformula` y `threeparttable` funcionen con el etiquetado.
- **Desactivar el etiquetado:** con LaTeX 2025-11 o posterior, la única forma es quitar `\input{eps-metadata}` de `main.tex` (cualquier `\DocumentMetadata` carga ya los módulos de etiquetado). A cambio se pierden el etiquetado, los metadatos XMP y la comprobación de motor LuaLaTeX; la compilación apenas se acelera.

---

## Limitaciones conocidas

La conformidad PDF/UA-2 completa no se alcanza todavía por motivos ajenos a lo que escribas:

- **KOMA-Script (`scrbook`)**, base de la clase, aún no soporta el etiquetado: las secciones y subsecciones se etiquetan como párrafos (`P`) en lugar de encabezados (`H2`, `H3`...).
- El validador encuentra relaciones padre-hijo no permitidas en la estructura (unas 184 en el documento de ejemplo).
- Varios paquetes que usa la plantilla figuran como **incompatibles** en el estado oficial del etiquetado de LaTeX: `chemformula`, `chemfig`, `minted`, `caption`, `subcaption`, `dirtree`, `listings`, `multirow`, `pgfplots` y `threeparttable`.
- Las tablas con `booktabs` se etiquetan sin celdas de cabecera (`TH`) salvo que se indique (ver [Tablas accesibles](#tablas-accesibles)).

### Requisitos

- **TeX Live 2024** o posterior (etiquetado completo con LaTeX 2025-11 o posterior)
- **LuaLaTeX** (obligatorio en esta plantilla; necesario para MathML)
- Paquete `unicode-math` para matemáticas accesibles (ya incluido)

---

## Texto alternativo para imágenes

Todas las imágenes deben tener texto alternativo (`alt={...}`) que describa su contenido. Sin él, el lector de pantalla solo puede leer el nombre del archivo y la compilación muestra el aviso `Alternative text for graphic is missing`:

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

Con LaTeX 2025-11 o posterior, indica qué filas son de cabecera con `\tagpdfsetup{table/header-rows={1}}` justo antes del `tabular` (dentro del entorno `table` solo afecta a esa tabla). Así las celdas de la primera fila se etiquetan como `TH` en lugar de `TD`. Con versiones anteriores de LaTeX la clave puede no existir: en ese caso, omítela.

```latex
\begin{table}[htbp]
    \centering
    \caption{Comparativa de algoritmos de ordenación}
    \label{tab:algoritmos}
    \tagpdfsetup{table/header-rows={1}}  % la fila 1 es cabecera (LaTeX 2025-11+)
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

Con LuaLaTeX y `unicode-math`, las ecuaciones se etiquetan automáticamente como MathML:

```latex
\usepackage{unicode-math}  % Ya incluido en la plantilla

% Las ecuaciones se etiquetan automáticamente
\begin{equation}
    E = mc^2
    \label{eq:energia}
\end{equation}
```

> **Nota:** Con pdfLaTeX, debes proporcionar archivos MathML separados para accesibilidad completa.

---

## Comprobación de accesibilidad

### Herramientas de validación

| Herramienta | Descripción | Enlace |
| ------------- | ------------- | -------- |
| **Adobe Acrobat Pro** | Comprobador de accesibilidad integrado | [adobe.com](https://www.adobe.com/acrobat) |
| **PAC** | Verificador PDF/UA gratuito | [pdfua.foundation](https://pdfua.foundation/en/pac-download) |
| **PAVE** | Validador online gratuito | [pave-pdf.org](https://pave-pdf.org/) |

También puedes comprobar que el PDF está etiquetado con `pdfinfo main.pdf` (línea `Tagged: yes`). La integración continua del repositorio genera además un informe de veraPDF a título informativo.

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
