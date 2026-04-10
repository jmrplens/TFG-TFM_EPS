# 🔧 Herramientas de Desarrollo

Esta carpeta contiene herramientas internas para el mantenimiento de la plantilla.

## � Herramientas disponibles

| Script | Descripción |
| -------- | ------------- |
| `actualizar_previews.py` | Genera e inserta previews de snippets LaTeX en la documentación |
| `generar_portadas.py` | Genera las imágenes de portadas para el README principal |

---

## 📸 Generador de Previews (`actualizar_previews.py`)

Herramienta unificada que extrae, compila e inserta previews de snippets LaTeX en los archivos de documentación.

**Características:**

- Compilación paralela usando todos los núcleos disponibles (máximo 8)
- Caché inteligente: solo recompila snippets modificados (manifest.json)
- Usa los paquetes EPS de la plantilla (`eps-componentes`) como preámbulo
- Conversión automática a WebP para menor tamaño
- Sistema opt-in: solo procesa snippets marcados

### Sistema de marcadores

Solo se procesan snippets marcados explícitamente con `<!-- preview -->`:

````markdown
```latex <!-- preview -->
% Se renderiza con 1 pasada de compilación
\begin{equation}
    E = mc^2
\end{equation}
```

```latex <!-- preview:2 -->
% Se renderiza con 2 pasadas (para referencias cruzadas)
La ecuación~\ref{eq:ejemplo} muestra...
```

```latex <!-- preview:3 mi_nombre_custom -->
% 3 pasadas + nombre personalizado para el archivo
```
````

### Uso

```bash
# Generar e insertar todos los previews
python3 .herramientas/actualizar_previews.py

# Listar snippets marcados (sin generar)
python3 .herramientas/actualizar_previews.py --listar

# Forzar regeneración de todos
python3 .herramientas/actualizar_previews.py --forzar

# Solo un archivo específico
python3 .herramientas/actualizar_previews.py --archivo ECUACIONES

# Solo generar (sin insertar enlaces)
python3 .herramientas/actualizar_previews.py --solo-generar

# Solo insertar enlaces (sin compilar)
python3 .herramientas/actualizar_previews.py --solo-insertar

# Limpiar previews huérfanos
python3 .herramientas/actualizar_previews.py --limpiar
```

### Requisitos

- Python 3.8+
- LuaLaTeX con `-shell-escape`
- poppler-utils (pdftoppm)
- (Opcional) cwebp para conversión a WebP

```bash
# Ubuntu/Debian
sudo apt install poppler-utils webp

# macOS
brew install poppler webp
```

### Estructura generada

```text
docs/
└── assets/
    └── previews/
        ├── manifest.json
        ├── ECUACIONES_001.pdf
        ├── ECUACIONES_001.webp
        ├── FIGURAS_GRAFICAS_003.pdf
        └── ...
```

---

## 🎨 Generador de Portadas (`generar_portadas.py`)

Genera las imágenes de portadas para cada titulación disponible.

### Uso

```bash
# Generar todas las portadas
python3 .herramientas/generar_portadas.py

# Solo listar titulaciones
python3 .herramientas/generar_portadas.py --listar

# Forzar regeneración
python3 .herramientas/generar_portadas.py --forzar
```

---

## 🔧 Makefile

Para mayor comodidad, se incluye un Makefile:

```bash
# Desde la raíz del proyecto
make -f .herramientas/Makefile previews     # Generar e insertar previews
make -f .herramientas/Makefile listar       # Listar snippets marcados
make -f .herramientas/Makefile limpiar      # Limpiar huérfanos
make -f .herramientas/Makefile portadas     # Generar portadas
```

---

## 📝 Workflow recomendado

1. **Marcar snippets en los archivos `.md`**:

   ````markdown
   ```latex <!-- preview -->
   \begin{equation}...
   ```
   ````

2. **Generar e insertar previews**:

   ```bash
   python3 .herramientas/actualizar_previews.py
   ```

3. **Verificar resultados** en `docs/assets/previews/`

4. **Commit de los cambios** (archivos .md + assets)

---

## 🧪 Verificación

Después de hacer cambios, ejecuta:

```bash
# Ver sintaxis del script
python3 -m py_compile .herramientas/actualizar_previews.py

# Ver ayuda completa
python3 .herramientas/actualizar_previews.py --help
```
