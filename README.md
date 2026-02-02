# 📚 Plantilla TFG/TFM - Escuela Politécnica Superior

**Universidad de Alicante**

[![LaTeX](https://img.shields.io/badge/LaTeX-LuaLaTeX-008080?logo=latex)](https://www.latex-project.org/)
[![License](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Version](https://img.shields.io/badge/Versión-2.0-blue.svg)](https://github.com/jmrplens/TFG-TFM_EPS/releases)

Plantilla LaTeX moderna y profesional para la elaboración de **Trabajos de Fin de Grado (TFG)** y **Trabajos de Fin de Máster (TFM)** de la Escuela Politécnica Superior de la Universidad de Alicante.

---

## ✨ Características

- 🎨 **Portadas oficiales** a color y en blanco/negro con diseño profesional
- 🎓 **21 titulaciones** preconfiguradas (8 grados + 13 másteres)
- ⚙️ **Configuración simple** mediante un único archivo
- 📝 **Bibliografía APA 7** con BibLaTeX + Biber
- 💻 **Resaltado de código** para 25+ lenguajes con Minted
- 📊 **Gráficas y diagramas** con TikZ/PGFPlots
- 📖 **Glosarios y acrónimos** integrados
- 🚀 **Optimización TikZ** con caché de figuras
- 🔧 **Compatible con Overleaf** y editores locales

---

## 🚀 Inicio Rápido

### Requisitos

- **TeX Live 2024** o superior (recomendado: TeX Live 2025)
- **LuaLaTeX** como motor de compilación
- **Biber** para bibliografía
- **Python + Pygments** para resaltado de código (minted)

```bash
# Ubuntu/Debian
sudo apt install texlive-full python3-pygments

# macOS con Homebrew
brew install --cask mactex
pip3 install Pygments

# Windows con Chocolatey
choco install miktex
pip install Pygments
```

### Compilación

```bash
# Opción 1: Usando latexmk (recomendado)
latexmk main.tex

# Opción 2: Compilación manual
lualatex -shell-escape main.tex
biber main
makeglossaries main
lualatex -shell-escape main.tex
lualatex -shell-escape main.tex
```

---

## 📁 Estructura del Proyecto

```
TFG-TFM_EPS/
├── main.tex                    # Documento principal
├── configuracion.tex           # Configuración del usuario
├── referencias.bib             # Bibliografía
├── .latexmkrc                  # Configuración de latexmk
│
├── cls/
│   └── eps-tfg.cls             # Clase principal
│
├── sty/
│   ├── eps-portadas.sty        # Paquete de portadas
│   └── eps-codigo.sty          # Estilos de código
│
├── contenido/
│   ├── frontmatter/
│   │   └── preliminares.tex    # Agradecimientos, resumen...
│   ├── capitulos/
│   │   ├── introduccion.tex
│   │   ├── marco-teorico.tex
│   │   ├── objetivos.tex
│   │   ├── metodologia.tex
│   │   ├── desarrollo.tex
│   │   ├── resultados.tex
│   │   └── conclusiones.tex
│   └── anexos/
│       ├── acronimos.tex
│       ├── anexo-a.tex
│       └── anexo-b.tex
│
├── recursos/
│   ├── logos/                  # Logos en PDF
│   │   ├── titulaciones/
│   │   └── universidad/
│   └── fuentes/                # Fuentes tipográficas
│
└── archivos/
    └── figuras-procesadas/     # Caché de figuras TikZ
```

---

## ⚙️ Configuración

Toda la configuración se realiza en el archivo `configuracion.tex`:

```latex
\EPSsetup{
  % Información del trabajo
  titulo = {Mi Título del Trabajo},
  subtitulo = {Subtítulo opcional},
  
  % Autor
  autor = {Nombre Apellido1 Apellido2},
  genero = m,  % m = masculino, f = femenino
  email = nombre@alu.ua.es,
  
  % Tutor/es
  tutor = {Dr. Nombre Apellido},
  tutor-departamento = {Departamento de Ejemplo},
  % cotutor = {Dra. Nombre Apellido},  % Opcional
  
  % Titulación (ver lista completa abajo)
  titulacion = informatica,
  
  % Opciones
  optimizar-tikz = true,
  borrador = true,  % Muestra notas TODO
}
```

### Titulaciones Disponibles

#### Grados

| ID | Titulación |
|----|------------|
| `teleco` | Ingeniería en Sonido e Imagen en Telecomunicación |
| `civil` | Ingeniería Civil |
| `quimica` | Ingeniería Química |
| `informatica` | Ingeniería Informática |
| `multimedia` | Ingeniería Multimedia |
| `arquitectura-tecnica` | Arquitectura Técnica |
| `arquitectura` | Arquitectura |
| `robotica` | Ingeniería Robótica |

#### Másteres

| ID | Titulación |
|----|------------|
| `master-teleco` | Ingeniería de Telecomunicación |
| `master-caminos` | Caminos, Canales y Puertos |
| `master-edificacion` | Gestión de la Edificación |
| `master-web` | Desarrollo de Aplicaciones y Servicios Web |
| `master-materiales` | Materiales, Agua y Terreno |
| `master-informatica` | Ingeniería Informática |
| `master-robotica` | Automática y Robótica |
| `master-prevencion` | Prevención de Riesgos Laborales |
| `master-agua` | Gestión Sostenible y Tecnologías del Agua |
| `master-moviles` | Software para Dispositivos Móviles |
| `master-quimica` | Ingeniería Química |
| `master-ciberseguridad` | Ciberseguridad |
| `master-geologica` | Ingeniería Geológica |

---

## 🎨 Portadas

Puedes generar diferentes combinaciones de portadas:

```latex
% Ambas portadas (por defecto)
\generarportada[ambas]

% Solo portada a color
\generarportada[solo-color]

% Solo portada en blanco y negro
\generarportada[solo-bn]

% Portadas individuales
\portadacolor
\portadabn
```

---

## 💻 Código Fuente

La plantilla incluye entornos predefinidos para múltiples lenguajes:

### Lenguajes Soportados

Python, JavaScript, TypeScript, Java, C, C++, C#, Rust, Go, SQL, HTML, CSS, PHP, Ruby, Swift, Kotlin, R, MATLAB, Bash, PowerShell, LaTeX, YAML, JSON, XML, Dockerfile...

### Ejemplos de Uso

```latex
% Código Python con título
\begin{pythoncode}[title={Mi script}]
def hola_mundo():
    print("¡Hola, mundo!")
\end{pythoncode}

% Código JavaScript con tema oscuro
\begin{jscode*}
const mensaje = "Hola desde JavaScript";
console.log(mensaje);
\end{jscode*}

% Cualquier lenguaje
\begin{codigo}{rust}
fn main() {
    println!("Hello, Rust!");
}
\end{codigo}

% Código desde archivo
\codigoarchivo{python}{scripts/analisis.py}

% Código inline
El comando \code{python}{print()} muestra texto.
```

---

## 📚 Bibliografía

La plantilla usa **BibLaTeX con Biber** y estilo **APA 7**.

### Archivo `referencias.bib`

```bibtex
@book{autor2024,
  author    = {García, María},
  title     = {Título del Libro},
  publisher = {Editorial},
  year      = {2024},
  isbn      = {978-0000000000}
}

@article{ejemplo2024,
  author  = {López, Juan},
  title   = {Título del Artículo},
  journal = {Revista Científica},
  year    = {2024},
  volume  = {10},
  pages   = {1--15},
  doi     = {10.1234/ejemplo}
}
```

### Citar en el texto

```latex
Según \textcite{autor2024}, el tema es importante...
Esto ha sido estudiado previamente \parencite{ejemplo2024}.
```

---

## 📝 Acrónimos

Define acrónimos en `contenido/anexos/acronimos.tex`:

```latex
\newacronym{api}{API}{Application Programming Interface}
\newacronym{ml}{ML}{Machine Learning}
```

Usa en el texto:

```latex
La \gls{api} permite...          % Primera vez: Application Programming Interface (API)
Usando \gls{api}...              % Después: API
La \acrlong{ml} es...            % Machine Learning
```

---

## 🔧 Personalización

### Añadir Nueva Titulación

Para añadir una titulación que no esté incluida, contacta con el mantenedor o edita `cls/eps-tfg.cls`:

```latex
% En la sección de definición de titulaciones
\__eps_define_titulacion:nnnnnnn {mi-titulacion}
  {Nombre Completo de Mi Titulación}
  {tfg} % o tfm
  {mi-color} % definir color previamente
  {blanco} % o negro, según el fondo
  {Blanco} % variante del logo para portada
  {Negro}  % variante del logo normal
```

### Cambiar Colores

Los colores de las titulaciones se definen en la clase. Para personalizar:

```latex
% En configuracion.tex, después de \EPSsetup
\definecolor{mi-color}{RGB}{100,150,200}
```

---

## 🌐 Uso en Overleaf

1. Sube todos los archivos del proyecto a Overleaf
2. Configura el compilador como **LuaLaTeX**
3. Activa **shell-escape** en la configuración del proyecto
4. Compila `main.tex`

> ⚠️ **Nota:** Algunas funcionalidades como minted requieren shell-escape habilitado.

---

## 📋 Cambios respecto a v1.x

### Novedades en v2.0

- ✅ Motor actualizado a **LuaLaTeX**
- ✅ Bibliografía migrada a **BibLaTeX + Biber**
- ✅ Sistema de configuración **key-value** moderno
- ✅ Código con **Minted** (25+ lenguajes)
- ✅ Logos convertidos a **PDF**
- ✅ Estructura de carpetas reorganizada
- ✅ Eliminado conflicto babel/polyglossia
- ✅ Clase modular con paquetes separados
- ✅ Soporte mejorado para personalización

### Migración desde v1.x

Si tienes un documento con la versión anterior:

1. Copia tu contenido a los nuevos archivos en `contenido/`
2. Adapta la configuración al nuevo formato `\EPSsetup{}`
3. Convierte tu bibliografía al formato BibLaTeX si usabas `apacite`
4. Actualiza los entornos de código a los nuevos (ej: `lstlisting` → `pythoncode`)

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

Puedes:
- ✅ Usar la plantilla para tu TFG/TFM
- ✅ Modificar y adaptar a tus necesidades
- ✅ Compartir con otros estudiantes

Debes:
- 📝 Mantener la atribución al autor original
- 🔄 Compartir modificaciones bajo la misma licencia

---

## 👤 Autor

**José Manuel Requena Plens**

- 📧 Email: info@jmrplens.com
- 🐦 Twitter/X: [@jmrplens](https://twitter.com/jmrplens)
- 💬 Telegram: [@jmrplens](https://t.me/jmrplens)

---

## ⭐ Agradecimientos

- A la Escuela Politécnica Superior de la Universidad de Alicante
- A todos los estudiantes que han usado y mejorado esta plantilla
- A la comunidad LaTeX por las herramientas utilizadas

---

<p align="center">
  <i>¡Buena suerte con tu TFG/TFM! 🎓</i>
</p>
