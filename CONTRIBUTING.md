# Guía de Contribución

¡Gracias por tu interés en contribuir a la plantilla TFG/TFM EPS UA! Este documento proporciona las pautas para colaborar en el proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo puedo contribuir?](#cómo-puedo-contribuir)
- [Configuración del entorno](#configuración-del-entorno)
- [Proceso de desarrollo](#proceso-de-desarrollo)
- [Guía de estilo](#guía-de-estilo)
- [Reportar bugs](#reportar-bugs)
- [Proponer mejoras](#proponer-mejoras)

## 📜 Código de Conducta

Este proyecto sigue un código de conducta basado en el respeto mutuo. Por favor:
- Sé respetuoso y constructivo en tus comentarios
- Acepta críticas constructivas con mentalidad abierta
- Enfócate en lo que es mejor para la comunidad

## 🤝 ¿Cómo puedo contribuir?

### Formas de contribuir

1. **Reportar errores**: Si encuentras un bug, abre un [issue](https://github.com/jmrplens/TFG-TFM_EPS/issues)
2. **Sugerir mejoras**: Propón nuevas funcionalidades o mejoras
3. **Documentación**: Mejora la documentación existente o añade ejemplos
4. **Código**: Corrige bugs o implementa nuevas características
5. **Traducciones**: Ayuda a traducir la documentación
6. **Testing**: Prueba la plantilla en diferentes sistemas y reporta problemas

### Contribuciones especialmente bienvenidas

- Nuevas titulaciones (grados/másteres) con sus logos y colores
- Mejoras en los estilos de código (nuevos lenguajes)
- Ejemplos de uso avanzado (TikZ, pgfplots, etc.)
- Compatibilidad con Overleaf
- Optimizaciones de rendimiento en compilación

## 🛠️ Configuración del entorno

### Requisitos

- **TeX Live 2023+** o **MiKTeX** con LuaLaTeX
- **Git** para control de versiones
- Editor recomendado: **VS Code** con [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)

### Clonar el repositorio

```bash
git clone https://github.com/jmrplens/TFG-TFM_EPS.git
cd TFG-TFM_EPS
```

### Compilar el proyecto

```bash
# Con Make
make

# Con latexmk
latexmk main.tex

# Compilación manual
lualatex -shell-escape main.tex
biber main
lualatex -shell-escape main.tex
lualatex -shell-escape main.tex
```

## 📝 Proceso de desarrollo

### 1. Crear una rama

```bash
# Para nuevas características
git checkout -b feature/nombre-caracteristica

# Para corrección de bugs
git checkout -b fix/descripcion-bug

# Para documentación
git checkout -b docs/descripcion-cambio
```

### 2. Realizar cambios

- Haz commits pequeños y frecuentes
- Escribe mensajes de commit claros y descriptivos
- Sigue la guía de estilo del proyecto

### 3. Probar los cambios

```bash
# Limpiar archivos auxiliares
make clean

# Compilar desde cero
make

# Verificar que no hay errores
```

### 4. Enviar Pull Request

1. Asegúrate de que tu código compila sin errores
2. Actualiza la documentación si es necesario
3. Añade una entrada al `CHANGELOG.md` si corresponde
4. Crea el Pull Request con una descripción clara

## 📐 Guía de estilo

### LaTeX

- **Indentación**: 2 espacios (no tabs)
- **Longitud de línea**: Máximo 100 caracteres cuando sea práctico
- **Comentarios**: En español, claros y concisos
- **Nombres de comandos**: En español, descriptivos (ej: `\generarportada`)

### Estructura de archivos

```
cls/          → Clases de documento
sty/          → Paquetes auxiliares
contenido/    → Contenido del documento
  ├── capitulos/
  ├── anexos/
  └── frontmatter/
recursos/     → Recursos estáticos
  ├── logos/
  ├── figuras/
  ├── fuentes/
  └── ejemplos/
```

### Documentación

- Documenta los nuevos comandos y entornos
- Incluye ejemplos de uso
- Mantén el README actualizado

## 🐛 Reportar bugs

Al reportar un bug, incluye:

1. **Descripción clara** del problema
2. **Pasos para reproducir** el error
3. **Comportamiento esperado** vs real
4. **Entorno**: Sistema operativo, versión de TeX Live/MiKTeX
5. **Log de errores** (archivo `.log`) si aplica
6. **MWE** (Minimal Working Example) que reproduzca el problema

### Plantilla de issue

```markdown
## Descripción
[Descripción clara del bug]

## Pasos para reproducir
1. ...
2. ...
3. ...

## Comportamiento esperado
[Qué debería pasar]

## Comportamiento actual
[Qué pasa realmente]

## Entorno
- SO: [ej. Windows 11, Ubuntu 22.04, macOS 14]
- TeX: [ej. TeX Live 2024, MiKTeX 24.1]
- Editor: [ej. VS Code, TeXstudio]

## Archivos relevantes
[Adjunta logs o MWE si es posible]
```

## 💡 Proponer mejoras

Para proponer una mejora:

1. Abre un **issue** describiendo la mejora
2. Explica **por qué** sería útil
3. Si es posible, sugiere **cómo** implementarla
4. Espera feedback antes de empezar a implementar cambios grandes

## 📄 Licencia

Al contribuir a este proyecto, aceptas que tus contribuciones se licenciarán bajo la [GNU General Public License v3.0](LICENSE).

---

¿Tienes preguntas? Abre un [issue](https://github.com/jmrplens/TFG-TFM_EPS/issues) o contacta con el mantenedor.

¡Gracias por contribuir! 🎉
