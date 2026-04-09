# Agentes IA y prompts — Plantilla TFG/TFM EPS UA

Índice de todos los archivos de agentes y prompts incluidos en el proyecto.

Cada agente existe en dos versiones: una para **GitHub Copilot** (en `.github/agents/`)
y otra para **Claude** (aquí, en `docs/agents/`). Los archivos de prompts son
válidos para cualquier IA.

---

## Agente de instalación

Guía a un estudiante sin experiencia para instalar y configurar el entorno
completo (LaTeX, Python, latexminted, make) en Windows, macOS o Linux.

| Archivo | Descripción |
|---------|-------------|
| [../../.github/agents/instalacion.md](../../.github/agents/instalacion.md) | Versión para GitHub Copilot |
| [instalacion-claude.md](instalacion-claude.md) | Versión para Claude |
| [prompts-instalacion.md](prompts-instalacion.md) | Prompts listos (I01–I08) |

---

## Agente de redacción

Ayuda a redactar secciones y capítulos completos en LaTeX respetando las
convenciones de la plantilla EPS UA.

| Archivo | Descripción |
|---------|-------------|
| [../../.github/agents/redaccion.md](../../.github/agents/redaccion.md) | Versión para GitHub Copilot |
| [redaccion-claude.md](redaccion-claude.md) | Versión para Claude |
| [prompts-redaccion.md](prompts-redaccion.md) | Prompts listos |

---

## Agente revisor tipo tribunal

Evalúa el documento completo en 8 dimensiones antes de la defensa y genera
un informe estructurado de mejora.

| Archivo | Descripción |
|---------|-------------|
| [../../.github/agents/revisor.md](../../.github/agents/revisor.md) | Versión para GitHub Copilot |
| [revisor-claude.md](revisor-claude.md) | Versión para Claude |
| [prompts-revisor.md](prompts-revisor.md) | Prompts listos |

---

## Cómo usar los agentes

### GitHub Copilot (VS Code)

1. Abre Copilot Chat (`Ctrl+Alt+I`)
2. Selecciona el modo **Agente** (icono de agente o `@workspace`)
3. Carga el archivo de agente con `#file:.github/agents/instalacion.md` (o el que corresponda)
4. Escribe tu petición

### Claude (claude.ai o Claude Code)

1. Abre una nueva conversación con Claude
2. Adjunta el archivo `docs/agents/instalacion-claude.md` (o el que corresponda)
3. Escribe tu petición

### Prompts sin integración directa

Si usas ChatGPT, Gemini u otra IA sin integración de archivos:

1. Abre el archivo de prompts correspondiente (`prompts-*.md`)
2. Copia el prompt que necesites (están identificados como I01, I02... / R01, R02... / V01, V02...)
3. Sustituye los valores entre `[corchetes]` y pégalo en el chat

---

## Revisión automática (sin IA)

Además de los agentes, el proyecto incluye un revisor estático que no
requiere IA:

```bash
python3 scripts/revision-rapida.py   # Linux / macOS
python  scripts/revision-rapida.py   # Windows
```

Genera `informe-revision.md` con problemas detectados y también se ejecuta
automáticamente en cada push/PR mediante GitHub Actions.
