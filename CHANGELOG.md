# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [2.1.0] - 2026-02-06

### Añadido

- **Guía de accesibilidad**: Nueva guía `docs/ACCESIBILIDAD.md` para crear PDFs accesibles (PDF/UA-2)
- **Glosario de términos**: 29 definiciones de términos técnicos en `acronimos.tex` además de los acrónimos
- **Referencias actualizadas**: Enlaces a documentación oficial en todas las guías (CTAN, TikZ, PGFPlots, BibLaTeX, etc.)
- **Archivos de contexto para IA**: `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` y `docs/AI_CONTEXT.md` para ayudar a ChatGPT, Claude, Copilot y otros asistentes a dar respuestas precisas sobre la plantilla
- **CI/CD mejorado**: Comentarios automáticos en PRs con enlace al PDF compilado y tabla de estado de portadas
- **Opciones de género neutro**: `genero = n` muestra "Autoría" en lugar de "Autor/Autora"
- **Género para tutores**: Nuevas opciones `tutor-genero` y `cotutor-genero`
- **Script unificado**: `actualizar_previews.py` combina generación e inserción de previews
- **Paralelización**: Scripts de generación de portadas y previews ahora usan múltiples procesos

### Cambiado

- **TeX Live 2025**: Documentación actualizada para TeX Live 2025 (marzo 2025)
- **Minted 3.x**: Información actualizada sobre minted 3.x con latexminted
- **Documentación mejorada**: Secciones de recursos adicionales ampliadas con herramientas y tutoriales
- **Funding**: Simplificado a solo GitHub Sponsors (eliminado Ko-fi y PayPal)

### Corregido

- **Portadas**: Eliminado borde blanco de 1px en el borde derecho
- **Portadas**: Corregida altura de la barra negra (6.86cm según diseño original)
- **Glosario**: Habilitados números de página en el glosario (eliminado `nonumberlist`)

---

## [2.0.0] - 2026-02-02

### 🚀 Cambios mayores - Modernización completa

Esta versión representa una reescritura completa de la plantilla con tecnologías modernas de LaTeX.

### Añadido

- **Motor LuaLaTeX**: Soporte nativo Unicode, mejor manejo de fuentes
- **Sistema expl3/L3**: Programación moderna con interfaz key-value via `\EPSsetup{}`
- **Clase `eps-tfg.cls`**: Nueva clase documentada que encapsula toda la configuración
- **Paquete `eps-portadas.sty`**: Gestión modular de portadas (color y B/N)
- **Paquete `eps-codigo.sty`**: Resaltado de código con minted + tcolorbox
- **Base de datos de titulaciones**: 21 grados/másteres con colores y logos configurados
- **Makefile**: Comandos simplificados (`make`, `make clean`, `make view`)
- **latexmkrc**: Configuración para compilación automática con latexmk
- **Soporte multi-idioma**: Configuración automática español/inglés con polyglossia
- **Metadatos PDF**: Título, autor, keywords configurados automáticamente

### Cambiado

- **Estructura de carpetas** reorganizada:
  ```
  cls/          → Clase principal
  sty/          → Paquetes auxiliares  
  contenido/    → Capítulos, anexos, frontmatter
  recursos/     → Logos, figuras, fuentes, ejemplos
  ```
- **Logos** convertidos de EPS a PDF para mejor compatibilidad
- **Bibliografía**: Migración de BibTeX a Biblatex + Biber (estilo APA)
- **Configuración** centralizada en `configuracion.tex` con sintaxis simple

### Eliminado

- Dependencia de pdfLaTeX (ahora requiere LuaLaTeX)
- Archivos de configuración dispersos en `include/`
- Plantilla de póster (a reimplementar en versión futura)
- Fuentes Kurier no utilizadas (~3MB liberados)
- Figuras de ejemplo del proyecto anterior

### Corregido

- Conflicto minted/listings por extensión `.lol`
- Errores de fontspec con fuentes no encontradas (fallback a DejaVu Sans)
- Warning de marginparwidth para todonotes
- Codificación UTF-8 correcta en todos los archivos

### Seguridad

- Actualizado a LaTeX2e 2022/06/01 o posterior

---

## [1.0.0] - Versión original

### Características originales

- Motor pdfLaTeX
- Configuración manual mediante archivos en `include/`
- Logos en formato EPS
- BibTeX para bibliografía
- Soporte para póster académico

---

## Notas de migración

### De 1.x a 2.0

1. **Instalar LuaLaTeX** si no está disponible:
   ```bash
   # Ubuntu/Debian
   sudo apt install texlive-luatex
   
   # macOS con MacTeX
   # Ya incluido
   ```

2. **Cambiar comando de compilación**:
   ```bash
   # Antes
   pdflatex documento.tex
   
   # Ahora
   lualatex -shell-escape main.tex
   # O simplemente:
   make
   ```

3. **Actualizar configuración**: Mover datos de `include/configuracioninicial.tex` a `configuracion.tex` usando la nueva sintaxis:
   ```latex
   \EPSsetup{
     titulacion = informatica,
     titulo = Mi Título,
     autor = Nombre Apellido,
     ...
   }
   ```

4. **Bibliografía**: Convertir `.bib` a formato compatible con Biblatex si es necesario (generalmente compatible).

---

## Roadmap

### Versión 2.1 (planificada)

- [ ] Reimplementar plantilla de póster
- [ ] Añadir tema de presentación Beamer
- [x] ~~GitHub Actions para CI/CD~~ ✅ Implementado
- [ ] Plantilla de Overleaf verificada
- [x] ~~Archivos de contexto para asistentes IA~~ ✅ Implementado

### Versión 2.2 (futura)

- [ ] Soporte para múltiples idiomas adicionales
- [ ] Temas de color alternativos
- [ ] Exportación a formatos accesibles (PDF/A)
- [ ] Integración con Zotero/Mendeley
