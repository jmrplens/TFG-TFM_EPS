# Auditoría de Calidada y Estándares LaTeX (2025)

**Fecha:** 5 de Febrero, 2026  
**Objetivo:** Verificar el cumplimiento de la clase `eps-tfg` y sus paquetes con los estándares modernos de desarrollo LaTeX, accesibilidad (PDF/UA) y distribución.

## Resumen Ejecutivo

El proyecto muestra una base sólida con una adopción parcial de tecnologías modernas (`expl3`, `l3keys`). Sin embargo, carece de características críticas de accesibilidad (PDF/UA) y presenta inconsistencias en la gestión de opciones entre sus módulos.

| Área | Estado | Puntuación | Hallazgos Clave |
| :--- | :---: | :---: | :--- |
| **Programación** | 🟡 Bueno | 7/10 | El núcleo (`cls`) usa `expl3`, pero los paquetes (`sty`) usan legacy LaTeX2e. |
| **Opciones** | 🟡 Mixto | 6/10 | Inconsistencia: `l3keys` (cls) vs `pgfkeys` (portadas) vs `\DeclareOption` (componentes). |
| **Accesibilidad** | 🔴 Crítico | 0/10 | Falta `\DocumentMetadata` y tagging. No cumple PDF/UA. |
| **Estructura** | 🟡 Regular | 5/10 | Estructura plana, no cumple TDS (`tex/latex/...`). CI básico presente. |
| **KOMA-Script** | 🟢 Excelente | 9/10 | Correcta herencia de `scrbook`. |

---

## Análisis Detallado

### 1. Gestión de Opciones

* **Estado Actual:**
  * `eps-tfg.cls`: Usa `l3keys2e`. **(Estándar Moderno)**
  * `eps-componentes.sty`: Usa `\DeclareOption` de LaTeX2e. **(Obsoleto)**
  * `eps-portadas.sty`: Usa `pgfkeys`. **(Válido, pero inconsistente)**
* **Recomendación:** Unificar todo el proyecto a `l3keys` para consistencia y mejor validación de argumentos.

### 2. Capa de Programación

* **Estado Actual:**
  * La clase principal adopta correctamente `expl3` con nomenclatura `\g__eps_...`.
  * Los paquetes satélite siguen usando comandos `\newcommand` y lógica condicional básica (`\newif`).
* **Recomendación:** Migrar lógica compleja de portadas y componentes a `expl3`.

### 3. Accesibilidad y PDF/UA (Normativa 2025)

* **Estado Actual:**
  * No se detectó `\DocumentMetadata{...}` en ningún archivo.
  * No hay gestión de *Tagging* para tablas o fórmulas.
* **Riesgo:** Los TFG/TFM generados no serán accesibles para lectores de pantalla, incumpliendo normativas de accesibilidad digital universitaria.
* **Acción Requerida:**
    1. Añadir `\DocumentMetadata{testphase={phase-III,math}, pdfstandard=ua-2, lang=es}` al inicio de `main.tex` (inyectado por la clase).
    2. Usar `tagpdf` o las nuevas APIs del kernel LaTeX 2024-2025.

### 4. Estructura y Distribución (TDS)

* **Estado Actual:**
  * Archivos en raíz: `cls/`, `sty/`. Esto es fácil para el usuario final pero no sigue el estándar TDS (`tex/latex/eps-tfg/`).
* **Recomendación:** Mantener estructura actual para repositorio de plantilla ("User Friendly"), pero crear script de *build* que genere estructura TDS para releases.

### 5. Integración Continua (CI)

* **Estado Actual:**
  * Existe `.github/workflows/build.yml`.
* **Recomendación:** Asegurar que el CI compile usando una imagen Docker moderna (TeX Live 2024/2025) y validar PDF/UA con `verapdf`.

## Plan de Acción Sugerido

1. **Prioridad Alta:** Implementar `\DocumentMetadata` en `eps-tfg.cls` para activar soporte PDF/UA.
2. **Prioridad Media:** Refactorizar `eps-componentes.sty` para usar `l3keys`.
3. **Prioridad Baja:** Organizar estructura interna compatible con TDS en el CI.
