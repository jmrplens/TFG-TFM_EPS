# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

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
- [ ] GitHub Actions para CI/CD
- [ ] Plantilla de overleaf

### Versión 2.2 (futura)

- [ ] Soporte para múltiples idiomas adicionales
- [ ] Temas de color alternativos
- [ ] Exportación a formatos accesibles (PDF/A)
