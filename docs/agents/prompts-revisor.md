# Prompts de revisión — Plantilla TFG/TFM EPS UA

Prompts listos para copiar y pegar en GitHub Copilot Chat o Claude.
Sustituir los valores entre `[corchetes]` por los datos reales del trabajo.

---

## Cómo usar estos prompts

**En GitHub Copilot Chat:**

1. Abrir Copilot Chat (`Ctrl+Alt+I`)
2. Escribir `@workspace` para dar contexto del repositorio completo
3. Pegar el prompt

**En Claude:**

1. Adjuntar los archivos `.tex` relevantes al chat
2. Adjuntar `configuracion.tex` y `referencias.bib`
3. Pegar el prompt

**Alternativa automática (sin IA):**

```bash
python3 scripts/revision-rapida.py
```

Genera `informe-revision.md` con análisis estático (referencias rotas,
comandos prohibidos, citas sin entrada `.bib`, etc.).

---

## Revisión completa

### R01 — Revisión completa del documento

```text
@workspace Actúa como un tribunal de TFG/TFM de la EPS de la Universidad
de Alicante. Revisa mi trabajo completo y genera un informe estructurado
siguiendo las instrucciones de .github/agents/revisor.md.

Datos del trabajo:
- Tipo: [TFG / TFM]
- Titulación: [titulación]
- Título: [título del trabajo]

Evalúa las 8 dimensiones (estructura, coherencia, bibliografía, lenguaje,
formato LaTeX, figuras/tablas, plagio semántico, normativa EPS UA) y genera
el informe con:
- Puntuación por dimensión (0-10)
- Problemas críticos, importantes y menores
- Puntos fuertes del trabajo
- Valoración global
```

---

### R02 — Revisión rápida antes de entregar

```text
@workspace Tengo que entregar mi TFG/TFM en [N días]. Haz una revisión
rápida y dime los 5 problemas más importantes que debo resolver antes
de la entrega.

Tipo: [TFG / TFM]
Titulación: [titulación]

Prioriza los problemas que más pueden afectar a la nota o que el tribunal
podría señalar en la defensa.
```

---

## Revisión por dimensión

### R03 — Revisar estructura y coherencia

```text
@workspace Revisa la estructura y coherencia de mi TFG/TFM.

Comprueba:
1. ¿Están presentes todos los capítulos obligatorios?
2. ¿El orden es lógico?
3. ¿Los objetivos planteados en la introducción se corresponden con los
   resultados y las conclusiones?
4. ¿La metodología descrita se aplica realmente en el desarrollo?
5. ¿Las conclusiones responden a los objetivos sin introducir información nueva?

Para cada problema, indica el capítulo/sección y sugiere cómo resolverlo.
```

---

### R04 — Revisar bibliografía y citas

```text
@workspace Revisa la bibliografía y las citas de mi TFG/TFM.

Comprueba:
1. ¿Hay afirmaciones relevantes sin citar?
2. ¿Se usan \parencite{} y \textcite{} correctamente (no \cite{} directo)?
3. ¿Las fuentes son actuales y académicas?
4. ¿Hay entradas en referencias.bib que no se citan en el texto?
5. ¿Hay citas en el texto que no tienen entrada en referencias.bib?
6. ¿El formato APA 7 es correcto?

Lista todos los problemas encontrados con la ubicación exacta.
```

---

### R05 — Revisar lenguaje y estilo

```text
@workspace Revisa el lenguaje y estilo académico de mi TFG/TFM.

Comprueba:
1. ¿Se usa voz impersonal o primera persona del plural?
2. ¿Hay registro informal (yo, mi, creo que, etc.)?
3. ¿Los párrafos tienen entre 3 y 6 oraciones?
4. ¿Los acrónimos están definidos la primera vez que aparecen?
5. ¿Los términos técnicos en inglés van en cursiva (\textit{})?
6. ¿Hay errores ortográficos o gramaticales evidentes?

Para cada problema, cita el fragmento exacto y propón la corrección.
```

---

### R06 — Revisar formato LaTeX

```text
@workspace Revisa el formato LaTeX de mi TFG/TFM.

Comprueba:
1. ¿Se usan \hline en tablas en lugar de booktabs?
2. ¿Se usa verbatim o lstlisting en lugar de los entornos *code?
3. ¿Hay figuras o tablas sin \caption{} o sin \label{}?
4. ¿Hay referencias \ref{} a etiquetas que no existen?
5. ¿Se usan comandos prohibidos por la plantilla EPS UA?
6. ¿Los prefijos de etiquetas son correctos (fig:, tab:, eq:, sec:, chap:)?

Lista todos los problemas con el archivo y número de línea aproximado.
```

---

### R07 — Revisar figuras, tablas y código

```text
@workspace Revisa las figuras, tablas y bloques de código de mi TFG/TFM.

Comprueba:
1. ¿Toda figura y tabla está referenciada en el texto?
2. ¿Los pies de figura/tabla son descriptivos y autocontenidos?
3. ¿Hay bloques de código demasiado largos que deberían ir en un anexo?
4. ¿Las tablas tienen encabezados claros y unidades donde corresponda?
5. ¿Hay figuras que aparecen sin contexto en el texto?

Para cada problema, indica la ubicación y sugiere la corrección.
```

---

### R08 — Análisis de plagio semántico

```text
@workspace Analiza este fragmento de mi TFG/TFM en busca de posibles
indicios de plagio o texto generado por IA sin revisión:

[pegar el fragmento a analizar]

Busca:
1. Cambios bruscos de registro o vocabulario
2. Definiciones técnicas sin citar que coinciden con definiciones estándar
3. Frases genéricas típicas de texto generado por IA
4. Párrafos que parecen copiados de fuentes externas
5. Texto que no refleja trabajo propio del alumno

Para cada indicio, indica el fragmento exacto y explica por qué es
sospechoso. Recuerda que es un análisis orientativo, no definitivo.
```

---

## Revisión de secciones específicas

### R09 — Revisar introducción

```text
@workspace Revisa la introducción de mi TFG/TFM.

Comprueba que contiene:
1. Motivación y contexto (¿por qué es relevante este trabajo?)
2. Planteamiento del problema (¿qué problema concreto se resuelve?)
3. Objetivos claros y medibles (lista numerada)
4. Descripción breve de la metodología
5. Estructura del documento (descripción de cada capítulo)

¿Falta alguno de estos elementos? ¿Están bien desarrollados?
¿La introducción engancha al lector y justifica el trabajo?
```

---

### R10 — Revisar conclusiones

```text
@workspace Revisa el capítulo de conclusiones de mi TFG/TFM.

Comprueba:
1. ¿Se responden todos los objetivos planteados en la introducción?
2. ¿Se mencionan las principales aportaciones del trabajo?
3. ¿Se reconocen las limitaciones del trabajo?
4. ¿Se proponen líneas de trabajo futuro?
5. ¿Las conclusiones introducen información nueva (no debería)?
6. ¿El tono es afirmativo y seguro?

Compara los objetivos de la introducción con las conclusiones y señala
cualquier objetivo no respondido.
```

---

### R11 — Comparar objetivos con resultados

```text
@workspace Compara los objetivos planteados en la introducción con los
resultados obtenidos en el capítulo de resultados y las conclusiones.

Para cada objetivo:
1. ¿Está abordado en el desarrollo?
2. ¿Tiene resultados cuantificables o demostrables?
3. ¿Se menciona en las conclusiones?

Genera una tabla de trazabilidad: Objetivo → Sección de desarrollo →
Resultado → Conclusión.
```

---

### R12 — Informe ejecutivo para el tutor

```text
@workspace Genera un informe ejecutivo de 1 página sobre el estado de
mi TFG/TFM, pensado para compartir con mi tutor/a.

El informe debe incluir:
- Estado general del trabajo (listo / necesita revisión / trabajo en progreso)
- Los 3 puntos fuertes más destacados
- Los 3 problemas más urgentes a resolver
- Estimación del tiempo necesario para las correcciones
- Recomendación: ¿está listo para defender?

Tipo: [TFG / TFM]
Titulación: [titulación]
Fecha objetivo de defensa: [fecha]
```

---

## Consejos de uso

- **Revisión iterativa:** usa R01 para una visión global, luego R03-R08
  para profundizar en las dimensiones con peor puntuación.
- **Antes de entregar:** usa R02 para identificar los problemas más urgentes.
- **Tras corregir:** vuelve a ejecutar `python3 scripts/revision-rapida.py`
  para verificar que los errores estáticos están resueltos.
- **Con el tutor:** usa R12 para preparar la reunión de seguimiento.
- **Plagio:** el análisis semántico (R08) es orientativo. Para verificación
  definitiva, configurar un token de API en `.env` y ejecutar el script.
- **Terminología de severidad:** los prompts de IA usan niveles «crítico /
  importante / menor» (alineados con `.github/agents/revisor.md`); el script
  `revision-rapida.py` usa «error / advertencia / info». La correspondencia
  aproximada es: crítico → error, importante → advertencia, menor → info.
