# 📦 Clase Principal - eps-tfg.cls

Este archivo contiene la clase LaTeX principal de la plantilla TFG/TFM.

> ⚠️ **IMPORTANTE**: Solo modificar si sabes lo que haces. Cambios aquí afectan a todo el documento.

---

## 🤖 Contexto para Asistentes de IA

### Descripción del archivo

`eps-tfg.cls` es una clase LaTeX3 que:

- Define la estructura del documento TFG/TFM
- Configura todas las opciones mediante `\EPSsetup{}`
- Gestiona 21 titulaciones con sus colores y logos
- Carga los paquetes necesarios (biblatex, hyperref, etc.)

### Tecnologías utilizadas

| Tecnología | Uso |
|------------|-----|
| **expl3** | Programación LaTeX3 moderna |
| **xparse** | Definición de comandos con sintaxis avanzada |
| **l3keys2e** | Sistema de claves key=value |
| **Property lists** | Base de datos de titulaciones |

### Estructura del archivo

```text
eps-tfg.cls
├── CONFIGURACIÓN EXPL3
│   └── Variables \tl_new:N, \bool_new:N
├── BASE DE DATOS TITULACIONES
│   └── \prop_gput:Nnn con datos de cada grado/máster
├── DEFINICIÓN DE CLAVES (\EPSsetup)
│   ├── titulo, autor, tutor, etc.
│   ├── titulacion (selecciona de la BD)
│   └── opciones booleanas
├── CARGA DE CLASE BASE
│   └── scrbook (KOMA-Script)
├── CARGA DE PAQUETES
│   ├── Fuentes (fontspec)
│   ├── Idioma (babel, csquotes)
│   ├── Bibliografía (biblatex)
│   └── Enlaces (hyperref)
├── COMANDOS PÚBLICOS
│   └── \EPStitulo, \EPSautor, etc.
└── ENTORNOS
    └── resumen, abstract
```

### Convenciones de nomenclatura expl3

```latex
% Variables privadas del módulo eps
\g__eps_titulo_tl        % g = global, __ = privado, eps = módulo, tl = token list

% Funciones privadas
\__eps_define_titulacion:nnnnnnn    % __ = privado, :nnnnnnn = 7 args tipo n

% Claves públicas
\keys_define:nn { eps } { ... }
```

### Variables principales

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `\g__eps_titulo_tl` | token list | Título del trabajo |
| `\g__eps_autor_tl` | token list | Nombre del autor |
| `\g__eps_titulacion_tl` | token list | ID de titulación |
| `\g__eps_titulaciones_prop` | property list | BD de titulaciones |
| `\g__eps_optimizar_tikz_bool` | bool | Externalizar TikZ |

### Base de datos de titulaciones

Cada titulación se define con:

```latex
\__eps_define_titulacion:nnnnnnn {id}
  {Nombre completo de la titulación}
  {tfg/tfm}           % tipo de trabajo
  {color-id}          % color del grado (definido en colores)
  {blanco/negro}      % color del texto sobre el fondo
  {Blanco/Negro}      % variante del logo para portada
  {Negro}             % variante del logo normal
```

### Comandos públicos exportados

```latex
% Acceso a datos (solo lectura)
\EPStitulo          % Título del trabajo
\EPSsubtitulo       % Subtítulo (si existe)
\EPSautor           % Nombre del autor
\EPStutor           % Nombre del tutor
\EPScotutor         % Nombre del cotutor
\EPSfecha           % Fecha
\EPStitulacion      % Nombre completo de la titulación
\EPStipoTrabajo     % "Trabajo Fin de Grado" o "Trabajo Fin de Máster"
\EPScolorGrado      % Color del grado
\EPScolorTexto      % Color del texto (blanco/negro)

% Portadas (definidas en eps-portadas.sty)
\portadacolor       % Genera portada a color
\portadabn          % Genera portada blanco y negro
```

---

## 🔧 Guía para modificaciones

### Añadir una nueva titulación

1. Añadir la definición después de las existentes:

```latex
\__eps_define_titulacion:nnnnnnn {nueva-titulacion}
  {Grado~en~Nueva~Titulación}
  {tfg}
  {nueva-color}
  {blanco}
  {Blanco}
  {Negro}
```

1. Definir el color en la sección de colores:

```latex
\definecolor{nueva-color}{HTML}{RRGGBB}
```

1. Añadir los logos en `recursos/logos/titulaciones/`:
   - `nueva-titulacion_Blanco.pdf`
   - `nueva-titulacion_Negro.pdf`

### Añadir una nueva opción a \EPSsetup

```latex
\keys_define:nn { eps }
{
  nueva-opcion .tl_gset:N = \g__eps_nueva_opcion_tl,
  nueva-opcion .initial:n = {valor-defecto},
}
```

### Añadir un nuevo comando público

```latex
% Al final de ExplSyntaxOn
\cs_new:Npn \EPSnuevoComando { \g__eps_nueva_opcion_tl }

% O fuera de ExplSyntax
\ExplSyntaxOff
\newcommand{\EPSnuevoComando}{\EPSnuevovalor}
```

---

## 📋 Requisitos de compilación

- **Motor**: LuaLaTeX (obligatorio para fontspec y unicode)
- **Flags**: `-shell-escape` (para minted)
- **Formato**: LaTeX2e 2022/06/01 o posterior
- **Distribución**: TeX Live 2023+ o MiKTeX actualizado

---

## 🔗 Archivos relacionados

| Archivo | Relación |
|---------|----------|
| `sty/eps-portadas.sty` | Define `\portadacolor` y `\portadabn` |
| `sty/eps-codigo.sty` | Estilos para bloques de código |
| `configuracion.tex` | Usuario llama a `\EPSsetup{}` |
| `recursos/logos/` | Logos referenciados por la clase |

---

## 📚 Recursos de aprendizaje

- [Documentación expl3](https://ctan.org/pkg/expl3)
- [interface3.pdf](https://ctan.org/pkg/interface3) - Referencia completa de funciones
- [xparse documentation](https://ctan.org/pkg/xparse)
- [KOMA-Script (scrbook)](https://ctan.org/pkg/koma-script)
