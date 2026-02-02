# 📁 Figuras

Esta carpeta está destinada a almacenar todas las imágenes y gráficos del documento.

## 📋 Formatos Recomendados

| Formato | Uso Recomendado | Ventajas |
|---------|-----------------|----------|
| **PDF** | Gráficos vectoriales, diagramas | Escalable sin pérdida de calidad |
| **PNG** | Capturas de pantalla, interfaces | Buena calidad, soporta transparencia |
| **JPG** | Fotografías | Menor tamaño de archivo |
| **SVG** | Diagramas, iconos (convertir a PDF) | Vectorial, editable |

## 🗂️ Organización Sugerida

Se recomienda organizar las figuras en subcarpetas según el capítulo o temática:

```
figuras/
├── capitulo1/
│   ├── diagrama-arquitectura.pdf
│   └── captura-interfaz.png
├── capitulo2/
│   ├── grafica-resultados.pdf
│   └── foto-prototipo.jpg
└── logos/
    ├── logo-empresa.pdf
    └── logo-tecnologia.png
```

## 🔧 Uso en LaTeX

```latex
% Figura simple
\begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{recursos/figuras/mi-imagen}
    \caption{Descripción de la figura}
    \label{fig:mi-imagen}
\end{figure}

% Referencia en el texto
Como se muestra en la Figura~\ref{fig:mi-imagen}...
```

## 💡 Consejos

- **No incluir extensión**: LaTeX busca automáticamente `.pdf`, `.png`, `.jpg`
- **Usar rutas relativas**: `recursos/figuras/nombre` desde el archivo principal
- **Nombres descriptivos**: Evitar espacios y caracteres especiales en nombres
- **Alta resolución**: Mínimo 300 DPI para impresión
