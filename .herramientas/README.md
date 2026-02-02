# 🔧 Herramientas de Desarrollo

Esta carpeta contiene herramientas internas para el mantenimiento de la plantilla.

## 📸 Generador de Previsualizaciones

Genera imágenes de previsualización para los snippets LaTeX de la documentación.

### Sistema Opt-In

**Solo se procesan snippets marcados explícitamente** con el comentario HTML `<!-- preview -->`.

#### Marcadores disponibles

```markdown
```latex <!-- preview -->
% Se renderiza con 1 pasada de compilación
\begin{equation}
    E = mc^2
\end{equation}
```

```latex <!-- preview:2 -->
% Se renderiza con 2 pasadas (para referencias cruzadas)
La Figura~\ref{fig:ejemplo} muestra...
```

```latex <!-- preview:3 mi_nombre -->
% 3 pasadas + nombre personalizado para el archivo
```
```

### Uso

```bash
# Listar TODOS los bloques latex (para decidir cuáles marcar)
python3 .herramientas/generar_previews.py --listar-todos

# Listar solo snippets marcados con <!-- preview -->
python3 .herramientas/generar_previews.py --listar

# Generar previews PDF
python3 .herramientas/generar_previews.py

# Generar PDF + PNG
python3 .herramientas/generar_previews.py --png

# Solo un archivo específico
python3 .herramientas/generar_previews.py --archivo docs/ECUACIONES.md

# Forzar regeneración (ignora caché)
python3 .herramientas/generar_previews.py --forzar

# Limpiar previsualizaciones huérfanas
python3 .herramientas/generar_previews.py --limpiar
```

### Requisitos

- Python 3.8+
- LuaLaTeX con `-shell-escape`
- Paquetes LaTeX de la plantilla instalados
- (Opcional) poppler-utils o ImageMagick para conversión a PNG

```bash
# Ubuntu/Debian
sudo apt install poppler-utils

# macOS
brew install poppler
```

### Estructura generada

```
docs/
└── assets/
    └── previews/
        ├── ECUACIONES_001.pdf
        ├── ECUACIONES_001.png
        ├── FIGURAS_GRAFICAS_003.pdf
        └── ...
```

### Workflow recomendado

1. **Identificar snippets renderizables**:
   ```bash
   python3 .herramientas/generar_previews.py --listar-todos
   ```

2. **Marcar snippets en los .md**:
   ```markdown
   ```latex <!-- preview -->
   \begin{equation}...
   ```
   ```

3. **Generar previews**:
   ```bash
   python3 .herramientas/generar_previews.py --png
   ```

4. **Verificar resultados** en `docs/assets/previews/`

5. **(Opcional) Insertar enlaces**:
   ```bash
   python3 .herramientas/insertar_previews.py
   ```
