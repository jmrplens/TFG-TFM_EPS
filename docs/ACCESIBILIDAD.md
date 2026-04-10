# ♿ Accesibilidad en Documentos LaTeX

Esta guía explica cómo crear PDFs accesibles usando LaTeX, cumpliendo con estándares PDF/UA para personas con discapacidades visuales o que usen lectores de pantalla.

---

## 📋 Índice

- [Introducción](#introducción)
- [Por qué es importante](#por-qué-es-importante)
- [Soporte en TeX Live 2025](#soporte-en-tex-live-2025)
- [Activar PDF etiquetado](#activar-pdf-etiquetado)
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

## Soporte en TeX Live 2025

TeX Live 2025 (lanzado en marzo 2025) incluye soporte completo para crear PDFs etiquetados gracias al **LaTeX Tagging Project**.

### Requisitos

- **TeX Live 2025** o superior
- **LuaLaTeX** (recomendado para mejor soporte de accesibilidad)
- Paquete `unicode-math` para matemáticas accesibles

---

## Activar PDF etiquetado

Para activar el etiquetado PDF/UA-2, añade el siguiente código **antes** de `\documentclass`:

```latex
\DocumentMetadata{
    lang = es-ES,           % Idioma del documento
    pdfstandard = ua-2,     % Estándar PDF/UA-2
    testphase = {
        phase-III,
        math,
        table,
        title,
        firstaid
    }
}

\documentclass{eps-tfg}
% ... resto del documento
```

### Opciones de idioma

| Valor | Idioma |
| ------- | -------- |
| `es-ES` | Español (España) |
| `ca-ES` | Valenciano/Catalán |
| `en-GB` | Inglés británico |
| `en-US` | Inglés americano |

---

## Texto alternativo para imágenes

Todas las imágenes deben tener texto alternativo que describa su contenido:

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

Las imágenes puramente decorativas deben marcarse como artefactos:

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth, decorative]{separador}
\end{figure}
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

```latex
\begin{table}[htbp]
    \centering
    \caption{Comparativa de algoritmos de ordenación}
    \label{tab:algoritmos}
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
| **PAC 2024** | Verificador PDF/UA gratuito | [pdfua.foundation](https://pdfua.foundation/en/pac-download) |
| **PAVE** | Validador online gratuito | [pave-pdf.org](https://pave-pdf.org/) |

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
| Overleaf - PDFs accesibles | [overleaf.com/learn](https://www.overleaf.com/learn/latex/Accessibility) |
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
