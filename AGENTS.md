# 🤖 Guía para Asistentes de IA

Este archivo proporciona contexto para que los asistentes de IA (ChatGPT, Claude, Copilot, etc.) puedan ayudar eficazmente a los estudiantes que usan esta plantilla LaTeX.

## 📋 Descripción del Proyecto

**TFG-TFM_EPS_UA** es una plantilla LaTeX profesional para la elaboración de:
- **TFG** (Trabajo Fin de Grado)
- **TFM** (Trabajo Fin de Máster)

En la **Escuela Politécnica Superior de la Universidad de Alicante** (España).

### Características principales
- Compilación con **LuaLaTeX** (obligatorio, no funciona con pdfLaTeX)
- Soporte para **21 titulaciones** diferentes (grados y másteres)
- Portadas oficiales en color y blanco/negro
- Bibliografía con BibLaTeX + Biber
- Código fuente con sintaxis resaltada (minted 3.x + latexminted)
- Glosarios y acrónimos integrados
- Cumple con la normativa de la EPS UA

---

## 📁 Estructura del Proyecto

```
/
├── main.tex                 # Documento principal (punto de entrada)
├── configuracion.tex        # ⭐ ARCHIVO CLAVE: Configuración del usuario
├── capitulos/               # Contenido del documento
│   ├── Introduccion.tex
│   ├── objetivos.tex
│   ├── marcoteorico.tex
│   ├── metodologia.tex
│   ├── desarrollo.tex
│   ├── resultados.tex
│   └── conclusiones.tex
├── anexos/                  # Anexos y apéndices
├── bibliografia/
│   └── bibliografia.bib     # Referencias en formato BibTeX
├── archivos/
│   ├── figuras/             # Imágenes del documento
│   └── ejemplos/            # Código fuente de ejemplo
├── cls/
│   └── eps-tfg.cls          # Clase principal (NO MODIFICAR)
├── sty/                     # Paquetes de estilo (NO MODIFICAR)
└── docs/                    # Documentación detallada
```

---

## ⚙️ Configuración Principal

El archivo `configuracion.tex` contiene todas las opciones personalizables mediante `\EPSsetup{}`:

### Datos básicos obligatorios
```latex
\EPSsetup{
    titulo = {Título del trabajo},
    autor = {Nombre Apellido1 Apellido2},
    genero = m,                          % m = masculino, f = femenino, n = neutro
    tutor = {Dr. Nombre del Tutor},
    tutor-departamento = {Nombre del Departamento},
    titulacion = informatica,            % Ver lista de titulaciones abajo
    fecha = {Junio 2026},
}
```

### Titulaciones disponibles (valor para `titulacion`)
**Grados:**
- `arquitectura`, `arquitectura-tecnica`, `civil`, `informatica`
- `multimedia`, `quimica`, `robotica`, `teleco`

**Másteres:**
- `master-agua`, `master-caminos`, `master-ciberseguridad`
- `master-edificacion`, `master-geologica`, `master-informatica`
- `master-materiales`, `master-moviles`, `master-prevencion`
- `master-quimica`, `master-robotica`, `master-teleco`, `master-web`

### Opciones de género
```latex
genero = m,           % Muestra "Autor" y "Tutor"
genero = f,           % Muestra "Autora" y "Tutora"  
genero = n,           % Muestra "Autoría" y "Tutoría" (neutro)

tutor-genero = m,     % Género del tutor: m/f/n
cotutor-genero = f,   % Género del cotutor: m/f/n
```

### Opciones adicionales comunes
```latex
\EPSsetup{
    % Subtítulo opcional
    subtitulo = {Subtítulo del trabajo},
    
    % Cotutor (opcional)
    cotutor = {Dra. Nombre Cotutora},
    cotutor-departamento = {Otro Departamento},
    
    % Email institucional
    email = nombre@alu.ua.es,
    
    % Palabras clave
    palabras-clave = {palabra1, palabra2, palabra3},
    keywords = {keyword1, keyword2, keyword3},
}
```

---

## 🔧 Comandos Principales

### Portadas
```latex
\portadacolor    % Portada a color (por defecto)
\portadabn       % Portada en blanco y negro
```

### Resúmenes
```latex
\begin{resumen}
Texto del resumen en español...
\end{resumen}

\begin{abstract}
Abstract text in English...
\end{abstract}
```

### Citas bibliográficas
```latex
\parencite{clave}      % (Autor, 2024)
\textcite{clave}       % Autor (2024)
\cite{clave}           % Cita numérica [1]
```

### Acrónimos y glosario
```latex
\gls{acronimo}         % Primera vez: "Nombre Completo (NC)", después: "NC"
\acrshort{acronimo}    % Solo las siglas: NC
\acrlong{acronimo}     % Solo el nombre completo
\acrfull{acronimo}     % Siempre completo: Nombre Completo (NC)
```

### Referencias cruzadas
```latex
\autoref{fig:nombre}   % "Figura 1" (automático)
\autoref{tab:nombre}   % "Tabla 1"
\autoref{sec:nombre}   % "Sección 1"
\autoref{eq:nombre}    % "Ecuación 1"
```

### Código fuente
```latex
% Código Python con números de línea
\begin{pythoncode}[title={script.py}]
def hello():
    print("Hello, World!")
\end{pythoncode}

% Código inline
\mintinline{python}{print("Hello")}
```

---

## ❌ Errores Comunes y Soluciones

### 1. "Package minted Error: You must invoke LaTeX with -shell-escape"
**Causa:** Minted necesita ejecutar comandos externos.
**Solución:** Compilar con `lualatex -shell-escape main.tex` o configurar el editor.

### 2. "Undefined control sequence: \EPSsetup"
**Causa:** No se está usando la clase correcta o hay error en main.tex.
**Solución:** Verificar que `main.tex` comienza con `\documentclass{eps-tfg}`.

### 3. "File 'eps-tfg.cls' not found"
**Causa:** Las rutas no están configuradas correctamente.
**Solución:** Verificar que existe el bloque `\input@path` en main.tex.

### 4. "Citation undefined" o "Reference undefined"
**Causa:** Falta ejecutar biber o hay errores en .bib.
**Solución:** Ejecutar: `lualatex → biber → lualatex → lualatex`.

### 5. La portada no tiene los colores correctos
**Causa:** Titulación mal escrita en configuracion.tex.
**Solución:** Verificar que el valor de `titulacion` coincide exactamente con la lista.

### 6. "Font not found" o errores de fuentes
**Causa:** LuaLaTeX no encuentra las fuentes del sistema.
**Solución:** 
- En Overleaf: Funciona automáticamente
- Local: Instalar TeX Live completo o las fuentes necesarias

---

## 💡 Consejos para Ayudar a Estudiantes

### Cuando pregunten sobre estructura
- Sugerir usar la estructura de capítulos existente
- Los archivos en `capitulos/` ya tienen el orden lógico típico
- Pueden añadir/eliminar capítulos modificando `main.tex`

### Cuando pregunten sobre bibliografía
- El archivo es `bibliografia/bibliografia.bib`
- Usar formato BibTeX estándar
- Herramientas útiles: Zotero, Mendeley, Google Scholar (exportar BibTeX)

### Cuando pregunten sobre imágenes
- Colocar en `archivos/figuras/`
- Formatos recomendados: PDF (vectorial), PNG (raster)
- Usar `\includegraphics[width=0.8\textwidth]{nombre}`

### Cuando pregunten sobre tablas
- Recomendar el paquete `booktabs` (ya incluido)
- Usar `\toprule`, `\midrule`, `\bottomrule`
- Para tablas largas: `longtable`

### Cuando pregunten sobre ecuaciones
- Entorno `equation` para ecuaciones numeradas
- Entorno `align` para ecuaciones alineadas
- Usar `\label{eq:nombre}` para referenciar

---

## 📚 Documentación Adicional

La carpeta `docs/` contiene guías detalladas:
- `ECUACIONES.md` - Guía completa de ecuaciones matemáticas
- `TABLAS.md` - Creación de tablas profesionales
- `FIGURAS_GRAFICAS.md` - Imágenes y gráficas con TikZ/PGFPlots
- `CODIGO_FUENTE.md` - Inserción de código con minted
- `BIBLIOGRAFIA.md` - Gestión de referencias
- `GLOSARIOS_ACRONIMOS.md` - Términos y acrónimos

---

## ⚠️ Advertencias Importantes

1. **NO modificar** los archivos en `cls/` y `sty/` a menos que sea absolutamente necesario
2. **Siempre compilar con LuaLaTeX**, no pdfLaTeX ni XeLaTeX
3. **Usar UTF-8** como codificación de todos los archivos .tex
4. **Respetar los nombres** de las titulaciones exactamente como están listados
5. La plantilla está diseñada para **español**, pero soporta contenido bilingüe

---

## 🔗 Enlaces Útiles

- **Repositorio:** https://github.com/jmrplens/TFG-TFM_EPS
- **Documentación LaTeX:** https://www.overleaf.com/learn
- **Comunidad TeX:** https://tex.stackexchange.com/

---

*Este archivo está diseñado para proporcionar contexto a asistentes de IA. Si eres un estudiante leyendo esto, ¡bienvenido! Puedes usar esta información como referencia rápida.*
