Esta plantilla LaTeX es para TFG/TFM de la EPS (Universidad de Alicante).

**Reglas Críticas:**
1. **Motor de Compilación:** SIEMPRE asume **LuaLaTeX**. No sugieras soluciones que solo funcionen en pdfLaTeX (ej: no uses `inputenc` con utf8, LuaLaTeX ya maneja UTF-8 nativamente).
2. **Bibliografía:** Se usa **BibLaTeX** con **Biber** y estilo APA. No uses BibTeX puro.
3. **Código Fuente:** Se usa el paquete **minted**. Usa los entornos predefinidos en `sty/eps-codigo.sty`:
   - Lenguajes: `pythoncode`, `javacode`, `cppcode`, `jsoncode`, `sqlcode`, `bashcode`, `htmlcode`, etc.
   - Variantes: `*NN` (sin números), `*Dark` (tema oscuro).
4. **Gráficas:** Prioriza **PGFPlots** y **TikZ** (`\pgfplotsset{compat=1.18}`).
5. **Componentes:** Usa las cajas personalizadas definidas en `sty/eps-componentes.sty` en lugar de bloques genéricos:
   - **Avisos:** `infobox`, `warningbox`, `successbox`, `dangerbox`, `tipbox`, `notebox`.
   - **Contenedores:** `titlebox`, `definitionbox`, `examplebox`.
   - **Software:** `terminal`, `apiendpoint`, `dirtreebox`.
   - **Ingeniería:** `blockdiagram`, `protocolframe`, `riskmatrix`.
   - **Tablas:** Usa siempre `booktabs` (`\toprule`, `\midrule`, `\bottomrule`).

**Estructura del Proyecto:**
- `main.tex`: Archivo raíz. Editar SOLO para estructura (activar componentes, añadir capítulos/anexos). NO escribir contenido.
- `configuracion.tex`: Variables del usuario (`\EPSsetup`).
- `cls/eps-metadata.tex`: Estándares PDF y código de idioma para metadatos.
- `contenido/capitulos/`: Archivos `.tex` de contenido.
- `referencias.bib`: Archivo de bibliografía.

**Configuración de Idioma:**
La plantilla soporta tres idiomas. En `configuracion.tex`:
```latex
\EPSsetup{
  idioma = espanol,  % espanol (defecto), valenciano, ingles
}
```
Si el usuario cambia el idioma, DEBE editar también `cls/eps-metadata.tex`:
- `idioma = espanol` → `lang=es-ES`
- `idioma = valenciano` → `lang=ca-ES`  
- `idioma = ingles` → `lang=en-GB`

**Comandos Comunes:**
- Citar: `\cite{key}`, `\textcite{key}`, `\parencite{key}`.
- Referencias cruzadas: `\label{prefijo:nombre}` y `\ref{prefijo:nombre}`. Prefijos sugeridos: `fig:`, `tab:`, `eq:`, `sec:`.
- Acrónimos: `\gls{id}`, `\acrshort{id}`, `\acrlong{id}`.

Si el usuario pide ayuda con errores de compilación, pide ver las últimas líneas del archivo `.log` o la salida del terminal.
