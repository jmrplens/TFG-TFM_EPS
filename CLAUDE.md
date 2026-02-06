# Instrucciones para Claude (TFG-TFM_EPS)

Esta es una plantilla LaTeX para TFG/TFM de la EPS (Universidad de Alicante).
Motor: **LuaLaTeX**. Bibliografía: **BibLaTeX/Biber**.

## Comandos
- Compilar: `make` (completo) o `make quick` (rápido).
- Limpiar: `make clean`.
- Ver errores: Leer `main.log` o salida de terminal.

## Estilo de Código
- **Indentación:** 2 o 4 espacios.
- **Comentarios:** Usa `%` para comentarios en LaTeX.
- **Ecuaciones:** Usa `\begin{equation}`...`\end{equation}`. `$` para inline.
- **Referencias:** `\label{fig:nombre}`, `\ref{fig:nombre}`. Prefijos: `fig:`, `tab:`, `eq:`, `sec:`, `chap:`.

## Configuración de Idioma
La plantilla soporta tres idiomas. Configurar en `configuracion.tex`:
```latex
\EPSsetup{
  idioma = espanol,  % espanol (defecto), valenciano, ingles
}
```
**IMPORTANTE:** Si el alumno cambia el idioma, DEBE editar también `cls/eps-metadata.tex`:
- `idioma = espanol` → `lang=es-ES`
- `idioma = valenciano` → `lang=ca-ES`
- `idioma = ingles` → `lang=en-GB`

El idioma afecta a: títulos automáticos (Tabla, Figura, Bibliografía...), metadatos PDF, y accesibilidad.

## Componentes Específicos
- **Avisos:** `infobox`, `warningbox`, `dangerbox`, `successbox`, `tipbox`, `notebox`.
- **Especiales:** `terminal`, `apiendpoint`, `blockdiagram`, `protocolframe`, `riskmatrix`.
- **Código:** Entornos `*code` (ej: `pythoncode`, `javacode`) del paquete `minted`.
- **Estructura:** Capítulos en `contenido/capitulos/`. Configuración en `configuracion.tex`.

## Restricciones
- NO sugerir `pdflatex`. Usar siempre LuaLaTeX.
- NO sugerir paquetes obsoletos (ej: `utf8x`, `subfigure`).
- Usar `booktabs` para tablas.
