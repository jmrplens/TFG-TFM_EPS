# 📦 Paquetes de Estilo

Esta carpeta contiene los paquetes auxiliares de la plantilla.

> ⚠️ **IMPORTANTE**: Solo modificar si sabes lo que haces. Cambios aquí afectan a funcionalidades específicas.

---

## 📁 Archivos

| Archivo | Descripción |
| --------- | ------------- |
| `eps-portadas.sty` | Genera las portadas oficiales (color y B/N) |
| `eps-codigo.sty` | Estilos de código fuente tipo VS Code |
| `eps-componentes.sty` | Cargador modular de componentes: `\usepackage[software,telecom]{eps-componentes}` (opciones `software`, `telecom`, `arquitectura`, `quimica`, `geologia`, `prevencion`, `all`) |
| `componentes/eps-comunes.sty` | Cajas de aviso, contenedores y elementos comunes (siempre se carga) |
| `componentes/eps-*.sty` | Un módulo por disciplina (ver [docs/COMPONENTES.md](../docs/COMPONENTES.md)) |

---

## 🤖 Contexto para Asistentes de IA

### eps-portadas.sty

#### Descripción

Genera las portadas oficiales del TFG/TFM usando TikZ para el diseño gráfico.

#### Tecnologías

| Paquete | Uso |
| --------- | ----- |
| **tikz** | Dibujo de fondos, franjas y posicionamiento de logos |
| **tikzpagenodes** | Referencia a coordenadas de la página |
| **textpos** | Posicionamiento absoluto de bloques de texto |
| **geometry** | Ajuste temporal de márgenes para portada |
| **setspace**, **afterpage**, **fontspec** | Interlineado, salto tras la portada y fuentes de portada |
| **xstring** | Utilidades de cadenas (cargado por compatibilidad) |

#### Estructura

```text
eps-portadas.sty
├── FUENTES DE PORTADA
│   └── \FuenteTitulo, \FuentePortada
├── VARIABLES CONFIGURABLES
│   ├── Posiciones: \eps@portadaTituloX/Y, \eps@portadaInfoGradoX/Y...
│   ├── Tamaños: \eps@sizeTitulo, \eps@sizeGrado, \eps@sizeTipoTrabajo, \eps@sizeInfo
│   └── Interlineado: \eps@leadingTitulo, \eps@leadingGrado, \eps@leadingInfo
├── AJUSTE AUTOMÁTICO DE TÍTULO
│   └── \eps@optimizeTitleSize (reduce el tamaño de 2 en 2 pt si no cabe)
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
\generarportada[ambas]   % Color + B/N (por defecto); también solo-color, solo-bn
\portadacolor            % Portada con fondo del color del grado
\portadabn               % Portada en blanco y negro
```

#### Variables de la clase que utiliza

```latex
\EPStitulo           % Título del trabajo
\EPSsubtitulo        % Subtítulo (opcional)
\EPSautor            % Nombre del autor
\EPSetiquetaAutor    % "Autor" / "Autora" / "Autoría" (según genero)
\EPStutor            % Nombre del tutor
\EPSetiquetaTutor    % "Tutor" / "Tutora" / "Tutores" / "Tutoras"... (según
                     % tutor-genero y, si hay cotutor, cotutor-genero)
\EPScotutor          % Nombre del cotutor (opcional)
\EPSsiCotutor{con}{sin}  % Elige texto según haya cotutor o no
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

```text
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
| --------- | ----- |
| **minted** | Resaltado de sintaxis con latexminted/Pygments |
| **tcolorbox** | Cajas con estilo (bordes redondeados, títulos) |
| **fontawesome5** | Iconos para los títulos de los bloques |

#### Estructura

```text
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
└── ENTORNOS DE CÓDIGO (46 lenguajes)
    ├── pythoncode, javacode, cppcode...        (con números de línea)
    ├── pythoncodeNN, javacodeNN...             (sin números de línea)
    ├── pythoncodeDark, pythoncodeDarkNN...     (tema oscuro)
    └── codigo, codigoNN, codigoDark, codigoDarkNN, codigosimple
                                                (lenguaje como argumento)
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
| --------- | ---------- | ------------ | ------------ |
| Python | python | `pythoncode` | `pythoncodeNN` |
| Java | java | `javacode` | `javacodeNN` |
| C++ | cpp | `cppcode` | `cppcodeNN` |
| C | c | `ccode` | `ccodeNN` |
| JavaScript | javascript | `jscode` | `jscodeNN` |
| HTML | html | `htmlcode` | `htmlcodeNN` |
| CSS | css | `csscode` | `csscodeNN` |
| SQL | sql | `sqlcode` | `sqlcodeNN` |
| LaTeX | latex | `latexcode` | `latexcodeNN` |
| Bash | bash | `bashcode` | `bashcodeNN` |
| MATLAB | matlab | `matlabcode` | `matlabcodeNN` |
| Genérico | (argumento) | `\begin{codigo}{lenguaje}` | `\begin{codigoNN}{lenguaje}` |

Lista completa y variantes `Dark`/`DarkNN` en [docs/CODIGO_FUENTE.md](../docs/CODIGO_FUENTE.md).

#### Uso de los entornos

```latex
% Con números de línea (por defecto); los _ del título se escapan
\begin{pythoncode}[title={mi\_script.py}]
def hello():
    print("Hello, World!")
\end{pythoncode}

% Sin números de línea
\begin{pythoncodeNN}[title={ejemplo.py}]
x = 42
\end{pythoncodeNN}

% Código inline
\mintinline{python}{print("Hello")}
```

#### Opciones disponibles en cada entorno

```latex
\begin{pythoncode}[
  title={nombre\_archivo.py},   % Título en la barra superior
  label={cod:ejemplo},          % Para referencias cruzadas
  minted options={firstline=2, highlightlines={3}},  % Opciones de minted
]
```

Las opciones son de tcolorbox; las de minted van dentro de `minted options={...}`.

---

## 🔧 Guía para modificaciones

### Añadir un nuevo lenguaje de programación

En `eps-codigo.sty`, añadir al final:

Sigue el patrón de los entornos existentes (`\newtcblisting` con contador
`listing` para que aparezcan en el índice de códigos). Ejemplo para Elixir:

```latex
%% Nuevo lenguaje: Elixir
\newtcblisting[use counter=listing, list inside=lol, list type=listing]{elixircode}[1][]{
  vscode-light-linenos,
  minted language=elixir,
  title={\faIcon{code}~~Elixir},
  list entry={\protect\numberline{\thelisting}Elixir},
  #1
}
\newtcblisting[use counter=listing, list inside=lol, list type=listing]{elixircodeNN}[1][]{
  vscode-light-nolinenos,
  minted language=elixir,
  title={\faIcon{code}~~Elixir},
  list entry={\protect\numberline{\thelisting}Elixir},
  #1
}
```

Para un uso puntual no hace falta definir nada: `\begin{codigo}{elixir} ... \end{codigo}`.

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

- **minted 3**: requiere `-shell-escape` y el programa `latexminted`, que viene con TeX Live 2024 o posterior (comprobar con `latexminted --version`; no hace falta `pip`)
- **fontawesome5**: Iconos incluidos en TeX Live
- **tcolorbox**: Versión 4.0+ para biblioteca minted

---

## 🔗 Archivos relacionados

| Archivo | Relación |
| --------- | ---------- |
| `cls/eps-tfg.cls` | Clase principal que carga estos paquetes |
| `recursos/logos/` | Logos usados por eps-portadas.sty |
| `docs/CODIGO_FUENTE.md` | Documentación para usuarios |

---

## 📚 Recursos de aprendizaje

- [Documentación tcolorbox](https://ctan.org/pkg/tcolorbox)
- [Documentación minted](https://ctan.org/pkg/minted)
- [TikZ & PGF Manual](https://ctan.org/pkg/pgf)
- [Pygments lexers](https://pygments.org/docs/lexers/) - Lista de lenguajes soportados
