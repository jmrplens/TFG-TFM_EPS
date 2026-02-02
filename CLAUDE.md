# CLAUDE.md - Instructions for Claude AI

This file provides context for Claude when assisting users with this LaTeX template.

## Quick Facts

- **Project**: LaTeX template for TFG/TFM at University of Alicante (Spain)
- **Compiler**: LuaLaTeX only (NOT pdfLaTeX)
- **Language**: Spanish (primary), English (abstracts/keywords)
- **Users**: University students writing their thesis

## Critical Rules

1. **ALWAYS recommend LuaLaTeX** - pdfLaTeX will fail
2. **ALWAYS require `-shell-escape`** - minted needs it
3. **NEVER suggest modifying** files in `cls/` or `sty/`
4. **ALL configuration** goes in `configuracion.tex` via `\EPSsetup{}`

## Most Common User Questions

### "Mi documento no compila" (My document won't compile)
→ Check: LuaLaTeX? `-shell-escape`? Pygments installed?

### "¿Cómo cambio la titulación?" (How do I change the degree?)
→ In `configuracion.tex`: `titulacion = informatica` (exact ID required)

### "¿Cómo añado una cita?" (How do I add a citation?)
→ Add entry to `bibliografia/bibliografia.bib`, use `\parencite{key}`

### "¿Cómo pongo código?" (How do I add code?)
→ Use `\begin{pythoncode}...\end{pythoncode}` or similar

### "¿Cómo referencio una figura?" (How do I reference a figure?)
→ Use `\autoref{fig:label}` (automatic "Figura X")

## Available Degrees (titulacion values)

**Grados:** `arquitectura`, `arquitectura-tecnica`, `civil`, `informatica`, `multimedia`, `quimica`, `robotica`, `teleco`

**Másteres:** `master-agua`, `master-caminos`, `master-ciberseguridad`, `master-edificacion`, `master-geologica`, `master-informatica`, `master-materiales`, `master-moviles`, `master-prevencion`, `master-quimica`, `master-robotica`, `master-teleco`, `master-web`

## File Structure Summary

```
main.tex           → Entry point
configuracion.tex  → User settings (\EPSsetup{})
capitulos/         → Chapter files
anexos/            → Appendices
bibliografia/      → BibTeX file
docs/              → Documentation (point users here!)
```

## Response Guidelines

1. **Be practical**: Give copy-paste ready code
2. **Use Spanish**: Match the user's language
3. **Reference docs**: Point to `docs/*.md` for details
4. **Explain compilation**: Many issues are compilation-related
5. **Check basics first**: titulacion value, file paths, compiler

## Compilation Sequence

```bash
lualatex -shell-escape main.tex
biber main
lualatex -shell-escape main.tex
lualatex -shell-escape main.tex
```

Or simply: `latexmk -lualatex -shell-escape main.tex`
