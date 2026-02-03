# 📦 Paquetes de Estilo

Esta carpeta contiene los paquetes auxiliares de la plantilla.

> ⚠️ **IMPORTANTE**: Solo modificar si sabes lo que haces. Cambios aquí afectan a funcionalidades específicas.

---

## 📁 Archivos

| Archivo | Descripción |
|---------|-------------|
| `eps-portadas.sty` | Genera las portadas oficiales (color y B/N) |
| `eps-codigo.sty` | Estilos de código fuente tipo VS Code |

---

## 🤖 Contexto para Asistentes de IA

### eps-portadas.sty

#### Descripción
Genera las portadas oficiales del TFG/TFM usando TikZ para el diseño gráfico.

#### Tecnologías

| Paquete | Uso |
|---------|-----|
| **tikz** | Dibujo de fondos, franjas y posicionamiento de logos |
| **tikzpagenodes** | Referencia a coordenadas de la página |
| **textpos** | Posicionamiento absoluto de bloques de texto |
| **geometry** | Ajuste temporal de márgenes para portada |
| **xstring** | Cálculo de longitud del título para ajuste automático |

#### Estructura

```
eps-portadas.sty
├── VARIABLES DE TAMAÑO
│   ├── \eps@FuenteTamano (tamaño título)
│   ├── \eps@interlinportada (interlineado)
│   └── \eps@TamTrabajo, \eps@TamOtros
├── AJUSTE AUTOMÁTICO DE TÍTULO
│   └── \eps@ajustar@tamano@titulo
├── PORTADA A COLOR
│   └── \portadacolor
│       ├── TikZ: fondo color + franja negra
│       ├── Logos: facultad, universidad, grado
│       └── Texto: título, autor, tutor, fecha
└── PORTADA BLANCO Y NEGRO
    └── \portadabn (similar estructura)
```

#### Comandos principales

```latex
\portadacolor    % Portada con fondo del color del grado
\portadabn       % Portada en blanco y negro
```

#### Variables de la clase que utiliza

```latex
\EPStitulo           % Título del trabajo
\EPSsubtitulo        % Subtítulo (opcional)
\EPSautor            % Nombre del autor
\EPSlabelAutor       % "Autor" / "Autora" / "Autoría"
\EPStutor            % Nombre del tutor
\EPSlabelTutor       % "Tutor" / "Tutora" / "Tutoría"
\EPScotutor          % Nombre del cotutor (opcional)
\EPSlabelCotutor     % "Cotutor" / "Cotutora" / "Cotutoría"
\EPSfecha            % Fecha de presentación
\EPStipoTrabajo      % "Trabajo Fin de Grado/Máster"
\EPStitulacion       % Nombre completo de la titulación
\EPScolorGrado       % Color del grado
\EPScolorTexto       % "blanco" o "negro" (contraste)
\EPSlogoFacultad     % Ruta al logo de la facultad
\EPSlogoUniversidad  % Ruta al logo de la universidad
\EPSlogoGrado        % Ruta al logo del grado
```

#### Medidas clave de la portada

```
┌─────────────────────────────────────┐
│  [Logo facultad]      [Logo UA]     │  ← 1.5cm del borde
│                                     │
│         [Logo grado grande]         │  ← centrado
│                                     │
│           TÍTULO DEL                │  ← Ajuste automático
│           TRABAJO                   │    según longitud
│                                     │
│        "Trabajo Fin de Grado"       │
│      en [Nombre Titulación]         │
│                                     │
├─────────────────────────────────────┤  ← 6.86cm desde abajo
│  ████████████████████████████████   │  ← Franja negra
│  Autor: Nombre                      │
│  Tutor: Nombre                      │
│  Fecha: Mes Año                     │
└─────────────────────────────────────┘
```

---

### eps-codigo.sty

#### Descripción
Define estilos para bloques de código fuente que imitan la apariencia de VS Code.

#### Tecnologías

| Paquete | Uso |
|---------|-----|
| **minted** | Resaltado de sintaxis con Pygments |
| **tcolorbox** | Cajas con estilo (bordes redondeados, títulos) |
| **fontawesome5** | Iconos para los títulos de los bloques |

#### Estructura

```
eps-codigo.sty
├── COLORES VS CODE
│   ├── Light: vscode-bg, vscode-border, vscode-titlebar...
│   └── Dark: vscode-dark-bg, vscode-dark-border...
├── CONFIGURACIÓN MINTED
│   └── \setminted{fontsize, breaklines, tabsize...}
├── ESTILOS BASE TCOLORBOX
│   ├── vscode-light-base
│   ├── vscode-light-linenos
│   └── vscode-dark-base...
└── ENTORNOS DE CÓDIGO
    ├── pythoncode, javacode, cppcode...
    ├── pythoncode*, javacode*... (sin líneas)
    └── genericcode (lenguaje configurable)
```

#### Colores definidos

```latex
% VS Code Light
\definecolor{vscode-bg}{HTML}{FFFFFF}
\definecolor{vscode-border}{HTML}{E5E5E5}
\definecolor{vscode-titlebar}{HTML}{F3F3F3}
\definecolor{vscode-titletext}{HTML}{616161}
\definecolor{vscode-linenos}{HTML}{237893}

% VS Code Dark
\definecolor{vscode-dark-bg}{HTML}{1E1E1E}
\definecolor{vscode-dark-border}{HTML}{3C3C3C}
\definecolor{vscode-dark-titlebar}{HTML}{252526}
\definecolor{vscode-dark-text}{HTML}{CCCCCC}
```

#### Entornos de código disponibles

| Entorno | Lenguaje | Con líneas | Sin líneas |
|---------|----------|------------|------------|
| Python | python | `pythoncode` | `pythoncode*` |
| Java | java | `javacode` | `javacode*` |
| C++ | cpp | `cppcode` | `cppcode*` |
| C | c | `ccode` | `ccode*` |
| JavaScript | javascript | `jscode` | `jscode*` |
| HTML | html | `htmlcode` | `htmlcode*` |
| CSS | css | `csscode` | `csscode*` |
| SQL | sql | `sqlcode` | `sqlcode*` |
| LaTeX | latex | `latexcode` | `latexcode*` |
| Bash | bash | `bashcode` | `bashcode*` |
| MATLAB | matlab | `matlabcode` | `matlabcode*` |
| Genérico | (param) | `genericcode` | `genericcode*` |

#### Uso de los entornos

```latex
% Con números de línea (por defecto)
\begin{pythoncode}[title={mi_script.py}]
def hello():
    print("Hello, World!")
\end{pythoncode}

% Sin números de línea
\begin{pythoncode*}[title={ejemplo.py}]
x = 42
\end{pythoncode*}

% Código inline
\mintinline{python}{print("Hello")}
```

#### Opciones disponibles en cada entorno

```latex
\begin{pythoncode}[
  title={nombre_archivo.py},    % Título en la barra superior
  label={lst:ejemplo},          % Para referencias cruzadas
]
```

---

## 🔧 Guía para modificaciones

### Añadir un nuevo lenguaje de programación

En `eps-codigo.sty`, añadir al final:

```latex
%% Nuevo lenguaje: Ruby
\DeclareTCBListing{rubycode}{ O{} }{
  vscode-light-linenos,
  minted language=ruby,
  title={\faCode~Ruby},
  #1
}
\DeclareTCBListing{rubycode*}{ O{} }{
  vscode-light-nolinenos,
  minted language=ruby,
  title={\faCode~Ruby},
  #1
}
```

### Cambiar colores del tema

Modificar los `\definecolor` en la sección de colores:

```latex
% Cambiar fondo a gris claro
\definecolor{vscode-bg}{HTML}{F5F5F5}
```

### Añadir tema oscuro por defecto

Cambiar los estilos base para usar `vscode-dark-*` en lugar de `vscode-light-*`.

---

## 📋 Requisitos

- **minted**: Requiere `-shell-escape` y Pygments instalado
- **fontawesome5**: Iconos incluidos en TeX Live
- **tcolorbox**: Versión 4.0+ para biblioteca minted

---

## 🔗 Archivos relacionados

| Archivo | Relación |
|---------|----------|
| `cls/eps-tfg.cls` | Clase principal que carga estos paquetes |
| `recursos/logos/` | Logos usados por eps-portadas.sty |
| `docs/CODIGO_FUENTE.md` | Documentación para usuarios |

---

## 📚 Recursos de aprendizaje

- [Documentación tcolorbox](https://ctan.org/pkg/tcolorbox)
- [Documentación minted](https://ctan.org/pkg/minted)
- [TikZ & PGF Manual](https://ctan.org/pkg/pgf)
- [Pygments lexers](https://pygments.org/docs/lexers/) - Lista de lenguajes soportados
