# Prompts de redacción — Plantilla TFG/TFM EPS UA

Prompts listos para copiar y pegar en GitHub Copilot Chat o Claude.
Sustituir los valores entre `[corchetes]` por los datos reales del trabajo.

---

## Cómo usar estos prompts

**En GitHub Copilot Chat:**
1. Abrir Copilot Chat (`Ctrl+Alt+I`)
2. Escribir `@workspace` al inicio para dar contexto del repositorio
3. Pegar el prompt y ajustar los valores entre corchetes

**En Claude:**
1. Adjuntar los archivos relevantes (p. ej. `configuracion.tex`, el capítulo
   existente si se quiere mejorar)
2. Pegar el prompt

---

## Prompts de estructura

### P01 — Proponer estructura de capítulo

```
@workspace Soy alumno de [titulación] en la EPS de la Universidad de Alicante.
Estoy escribiendo mi TFG/TFM sobre [tema del trabajo].

Necesito que me propongas la estructura de secciones para el capítulo
"[nombre del capítulo]". El capítulo debe cubrir:
- [punto 1]
- [punto 2]
- [punto 3]

Propón entre 4 y 6 secciones con una línea de descripción cada una.
Usa las convenciones de la plantilla TFG/TFM EPS UA.
```

---

### P02 — Generar capítulo completo

```
@workspace Genera el capítulo "[nombre del capítulo]" completo para mi
TFG/TFM de [titulación] sobre [tema].

Estructura acordada:
1. [Sección 1]: [descripción]
2. [Sección 2]: [descripción]
3. [Sección 3]: [descripción]

Requisitos:
- LaTeX válido para LuaLaTeX con los entornos de la plantilla EPS UA
- Idioma: [español/valenciano/inglés]
- Módulo de componentes activo: [software/telecom/arquitectura/quimica/ninguno]
- Incluir al menos [N] citas bibliográficas (usar \parencite{CLAVE})
- Incluir al menos una figura, tabla o bloque de código si el contenido
  lo justifica
- Añadir \label{} en todos los elementos referenciables
```

---

### P03 — Expandir esquema a texto académico

```
@workspace Convierte este esquema en texto académico LaTeX para mi TFG/TFM
de [titulación]. Sección: "[nombre de la sección]".

Esquema:
[pegar los bullet points aquí]

Requisitos:
- Registro académico, voz impersonal
- Añadir citas donde corresponda (marcar con \parencite{CLAVE} si no
  tengo las claves exactas)
- Párrafos de 3-5 oraciones
- Usar los entornos de la plantilla EPS UA (cajas, código, etc.) si
  el contenido lo justifica
```

---

## Prompts de mejora

### P04 — Revisar y mejorar fragmento

```
@workspace Mejora este fragmento de mi TFG/TFM. Identifica los problemas
primero y luego reescríbelo:

[pegar el fragmento LaTeX aquí]

Problemas a buscar:
- Registro informal o coloquial
- Afirmaciones sin citar
- Frases demasiado largas o ambiguas
- Uso incorrecto de entornos LaTeX
- Falta de etiquetas \label{}
- Uso de comandos prohibidos (verbatim, hline, cite directo, etc.)
```

---

### P05 — Mejorar coherencia entre secciones

```
@workspace Tengo estas dos secciones consecutivas en mi TFG/TFM. Mejora
las transiciones entre ellas y asegúrate de que hay coherencia temática:

SECCIÓN 1:
[pegar sección 1]

SECCIÓN 2:
[pegar sección 2]

Añade un párrafo de cierre a la sección 1 que enlace con la sección 2,
y un párrafo introductorio a la sección 2 que recoja el hilo de la 1.
```

---

### P06 — Añadir citas a un fragmento

```
@workspace Tengo este fragmento de mi TFG/TFM que necesita citas
bibliográficas. Indica qué afirmaciones deberían tener cita y sugiere
qué tipo de fuente buscar para cada una:

[pegar el fragmento]

Para cada afirmación que necesite cita, usa el formato:
\parencite{BUSCAR: descripción de la fuente necesaria}
```

---

## Prompts de secciones específicas

### P07 — Generar resumen y abstract

```
@workspace Genera el resumen y el abstract para mi TFG/TFM.

Datos del trabajo:
- Título: [título]
- Titulación: [titulación]
- Tema: [descripción de 3-5 líneas del trabajo]
- Metodología empleada: [descripción breve]
- Principales resultados: [descripción breve]
- Idioma del documento: [español/valenciano/inglés]

Requisitos:
- Resumen en [idioma del documento], 200-300 palabras
- Abstract en inglés, 200-300 palabras
- Estructura: contexto → problema → metodología → resultados → conclusión
- Usar los entornos correctos del frontmatter de la plantilla EPS UA
```

---

### P08 — Generar conclusiones

```
@workspace Genera el capítulo de conclusiones para mi TFG/TFM de
[titulación] sobre [tema].

Objetivos planteados en la introducción:
1. [objetivo 1]
2. [objetivo 2]
3. [objetivo 3]

Principales resultados obtenidos:
- [resultado 1]
- [resultado 2]

Limitaciones encontradas:
- [limitación 1]
- [limitación 2]

Estructura obligatoria:
1. Recapitulación de objetivos cumplidos
2. Principales aportaciones
3. Limitaciones del trabajo
4. Líneas de trabajo futuro

Longitud: 600-1000 palabras. Tono afirmativo, sin información nueva.
```

---

### P09 — Generar introducción (al final del proceso)

```
@workspace Genera la introducción de mi TFG/TFM. La escribo al final
porque ya tengo el resto del documento.

Datos del trabajo:
- Título: [título]
- Titulación: [titulación]
- Problema que resuelve: [descripción]
- Metodología: [descripción breve]
- Capítulos del documento: [lista de capítulos con una línea cada uno]

Estructura obligatoria:
1. Motivación y contexto (por qué es relevante)
2. Planteamiento del problema (qué problema concreto se resuelve)
3. Objetivos (lista numerada de 3-5 objetivos específicos)
4. Metodología empleada (breve, 1 párrafo)
5. Estructura del documento (descripción de cada capítulo)
```

---

### P10 — Generar sección de trabajos relacionados

```
@workspace Genera la sección "Trabajos relacionados" para mi TFG/TFM
de [titulación] sobre [tema].

Trabajos que debo mencionar:
- [trabajo 1]: [descripción breve y clave bib si la tengo]
- [trabajo 2]: [descripción breve y clave bib si la tengo]
- [trabajo 3]: [descripción breve y clave bib si la tengo]

Requisitos:
- Organizar los trabajos por enfoque o cronología
- Para cada trabajo: qué propone, qué resultados obtiene, qué limitación
  tiene que mi trabajo supera o aborda de forma diferente
- Párrafo final de síntesis que posicione mi trabajo respecto al estado
  del arte
- Usar \parencite{} para todas las citas
```

---

### P11 — Generar descripción de figura o tabla

```
@workspace Genera el pie de figura/tabla y el párrafo de referencia en
el texto para este elemento de mi TFG/TFM:

Tipo: [figura / tabla]
Contenido: [descripción de qué muestra la figura o tabla]
Contexto: [en qué sección aparece y qué argumento apoya]

Genera:
1. El entorno LaTeX completo con \caption{} y \label{}
2. La frase de referencia en el texto (ej: "Como se muestra en la
   Figura~\ref{fig:nombre}...")
```

---

### P12 — Adaptar capítulo a otro idioma

```
@workspace Traduce este capítulo de mi TFG/TFM de [idioma origen] a
[idioma destino], manteniendo el LaTeX intacto y adaptando solo el texto:

[pegar el capítulo]

Requisitos:
- Mantener todos los comandos LaTeX sin cambios
- Adaptar el registro académico al idioma destino
- Si el idioma destino es valenciano, usar las convenciones académicas
  de la Universitat d'Alacant
- No traducir nombres propios, siglas ni términos técnicos establecidos
```

---

## Consejos de uso

- **Contexto es clave:** cuanto más detalle des sobre tu trabajo, mejor
  será el resultado. Describe el tema, la titulación y el módulo activo.
- **Itera:** usa P04 para mejorar lo que genera P02. Los agentes mejoran
  con retroalimentación.
- **Citas:** los agentes marcan con `\parencite{CLAVE}` o
  `\parencite{BUSCAR: ...}` donde hacen falta citas. Tú debes añadir las
  entradas reales a `referencias.bib`.
- **Verifica siempre:** el LaTeX generado puede tener errores menores.
  Compila con `make quick` tras cada inserción.
