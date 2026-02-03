# GitHub Copilot Instructions for TFG-TFM_EPS

## Project Overview

This is a **LaTeX template** for Bachelor's (TFG) and Master's (TFM) thesis at the Polytechnic School of the University of Alicante (Spain). 

**Key facts:**
- Must compile with **LuaLaTeX** (not pdfLaTeX)
- Requires `-shell-escape` flag for minted package
- Spanish is the primary language
- Supports 21 different degree programs

## File Structure

- `main.tex` - Entry point, includes all chapters
- `configuracion.tex` - User configuration via `\EPSsetup{}`
- `capitulos/*.tex` - Chapter content files
- `anexos/*.tex` - Appendix files
- `bibliografia/bibliografia.bib` - BibTeX references
- `cls/eps-tfg.cls` - Main class file (DO NOT MODIFY)
- `sty/*.sty` - Style packages (DO NOT MODIFY)

## When Helping Users

### For LaTeX content questions:
- Always suggest using the template's built-in commands
- Reference the `docs/` folder for detailed guides
- Use `\autoref{}` for cross-references (auto-detects type)
- Use `\parencite{}` for citations (BibLaTeX style)

### For configuration questions:
- All settings go in `configuracion.tex` inside `\EPSsetup{}`
- Available degrees: `informatica`, `teleco`, `arquitectura`, `civil`, `quimica`, `robotica`, `multimedia`, `arquitectura-tecnica`, and masters with `master-` prefix

### For compilation issues:
1. Check LuaLaTeX is being used
2. Verify `-shell-escape` is enabled
3. Run full compilation: `lualatex → biber → lualatex → lualatex`

## Code Style

When writing LaTeX code for this project:
- Use Spanish for comments and content
- Indent with 2 spaces inside environments
- Use `%` comments to explain complex macros
- Prefer semantic commands (`\autoref`) over manual references

## Common Commands

```latex
% Configuration
\EPSsetup{
    titulo = {Title},
    autor = {Name},
    titulacion = informatica,
}

% Citations
\parencite{key}     % (Author, Year)
\textcite{key}      % Author (Year)

% Cross-references
\autoref{fig:name}  % "Figure 1"
\autoref{tab:name}  % "Table 1"

% Acronyms
\gls{acronym}       % Smart expansion
\acrshort{acronym}  % Short form only

% Code
\begin{pythoncode}
# Python code here
\end{pythoncode}
```

## Documentation

Point users to these files in `docs/`:
- `ECUACIONES.md` - Math equations
- `TABLAS.md` - Tables
- `FIGURAS_GRAFICAS.md` - Figures and graphics
- `CODIGO_FUENTE.md` - Source code listings
- `BIBLIOGRAFIA.md` - Bibliography management
- `GLOSARIOS_ACRONIMOS.md` - Glossaries and acronyms

## Important Warnings

1. Never suggest pdfLaTeX - this template requires LuaLaTeX
2. Don't modify files in `cls/` or `sty/` directories
3. The `titulacion` value must match exactly (case-sensitive)
4. Bibliography uses Biber, not BibTeX
