# Plantilla TFG/TFM
**Para ver la información del póster haz clic <a href="https://github.com/jmrplens/TFG-TFM_EPS/wiki/P%C3%B3ster">aquí</a>.**

**Ejemplo real de TFG y póster:  <a href="http://jmrplens.com/GitHub_TFGTemplate/TFG+Poster.zip">Descargar proyecto LaTeX</a>**

**Novedades Diciembre 2018:** 
* Si utilizas figuras generadas con TikZ o PGF y quieres reducir el tiempo de compilado activa la optimización poniendo un `1` en la línea `\def\OptimizaTikZ{1}` que se encuentra al principio del archivo principal `TFG-TFM_EPS.tex`. Esto almacenará tus figuras en `archivos/figuras-procesadas` y mientras no sean editadas se cargarán desde ahi y no se ejecutará su código, además puedes darles otros usos (powerpoint, word, etc).
*  Se han añadido _comentarios mágicos_ en la cabecera del archivo principal para que el proyecto se compile con las opciones necesarias en TeXstudio, si eres un usuario/a medio o avanzado/a puedes seleccionarlas tu mismo/a en tu editor preferido, es necesario utilizar XeLaTeX y si quieres reducir el tiempo utilizando la externalización de TikZ debes añadir -shell-escape a tus comandos.
* Si vas a utilizar el proyecto en <a href="https://www.overleaf.com/">Overleaf</a> (recuerda cambiar el motor a XeLaTex) o si tienes problemas con la exportación de TikZ y PGF desactiva la optimización. En algunos casos es interesante activarlo en Overleaf aunque se muestre que se han producido errores ya que el resultado es el correcto y se reduce el tiempo de procesado (las cuentas gratuitas tienen limite de tiempo de ejecución).

---

Esta plantilla se ha creado después de observar la idea concebida por Pedro Pernías y otros colaboradores en su plantilla: <a href="https://github.com/lcg51/tfg">tfg</a>. Se ha mantenido algún contenido de los capítulos de esa plantilla, y la clase de documento _scrbook_ pero el resto de la plantilla está realizada de cero. El diseño se ha ajustado a lo indicado en la <a href="https://eps.ua.es/es/ingenieria-sonido-imagen-telecomunicacion/documentos/tfg/libro-de-estilo.pdf">Guía de estilo</a> de la EPS. Siempre se debe comprobar que no hayan cambiado los criterios, ya que esta plantilla se actualiza periódicamente y no cada vez que se establezca una modificación por parte de la EPS. Si algún parámetro cambia es sencillo actualizar ese cambio en la plantilla, se ha realizado de tal modo que todos los parámetros sean fácilmente editables.

Esta plantilla puede ser divulgada, modificada y compartida libremente. Este proyecto se ha realizado para los alumnos de la Escuela Politécnica Superior de la Universidad de Alicante, esperando facilitar un poco la introducción al trabajo con LaTeX. Se ruega enviar sugerencias de todo tipo, el contenido de la plantilla intenta mostrar un poco de todo lo que se puede hacer con LaTeX, pero si es complejo el uso y así lo indicasen los usuarios se modificará para hacerla más manejable.

## Índice
<!-- MarkdownTOC depth=5 bracket="round" style="ordered" -->

1. [Introducción](#introducci%C3%B3n)
1. [Características](#caracter%C3%ADsticas)
	1. [Directrices de estilo](#directrices-de-estilo)
	1. [Multitud de diseños predefinidos](#multitud-de-dise%C3%B1os-predefinidos)
	1. [Fuente de texto](#fuente-de-texto)
	1. [Lenguajes de programación](#lenguajes-de-programaci%C3%B3n)
	1. [Contenido de ejemplo](#contenido-de-ejemplo)
1. [Uso](#uso)
	1. [Estructura de archivos](#estructura-de-archivos)
	1. [Introduce la información del trabajo](#introduce-la-informaci%C3%B3n-del-trabajo)
	1. [Selecciona tu titulación](#selecciona-tu-titulaci%C3%B3n)
	1. [Contenido](#contenido)
		1. [Precontenido](#precontenido)
		1. [Capítulos](#cap%C3%ADtulos)
		1. [Postcontenido](#postcontenido)
	1. [Archivos 'include'](#archivos-include)
	1. [Lista de acrónimos y abreviaturas](#lista-de-acr%C3%B3nimos-y-abreviaturas)
	1. [Bibliografía](#bibliograf%C3%ADa)
		1. [Citar bibliografía](#citar-bibliograf%C3%ADa)
	1. [Comentarios](#comentarios)
1. [Control de errores](#control-de-errores)
	1. [Longitud del título](#longitud-del-t%C3%ADtulo)
1. [Aspectos avanzados](#aspectos-avanzados)
	1. [Formato del documento](#formato-del-documento)
	1. [Idioma del documento](#idioma-del-documento)
	1. [Añadir/Editar formato de titulaciones](#a%C3%B1adireditar-formato-de-titulaciones)
	1. [Fuentes de la portada](#fuentes-de-la-portada)
1. [Contacto \(sugerencias, errores, etc\)](#contacto-sugerencias-errores-etc)

<!-- /MarkdownTOC -->

## Introducción
Para conocer mejor el entorno LaTeX he elegido algunas fuentes de información relevantes:

* <a href="https://tecdigital.tec.ac.cr/revistamatematica/Libros/LATEX/LaTeX_2014.pdf">Libro/Manual - Tecnológico de Costa Rica (español)</a>
* <a href="http://www.texdoc.net/"> TeXdoc - Web con documentación de paquetes y comandos LaTeX (inglés)</a>
* <a href="https://www.youtube.com/user/ShareLaTeX"> Canal de YouTube de ShareLaTeX con videotutoriales (inglés)</a>
* <a href="https://es.wikipedia.org/wiki/Ayuda:Uso_de_TeX">Artículo de la Wikipedia con muchos ejemplos (español)</a>
* <a href="https://upload.wikimedia.org/wikipedia/commons/2/2d/LaTeX.pdf">Manual LaTeX realizado por Wikimedia (inglés)</a>

Recomiendo utilizar programas LaTeX que permitan trabajar con estructura de archivos para poder editar el conjunto de capítulos en la misma ventana. Este tipo de función lo tienen programas como <a href="https://www.texstudio.org/">TexStudio</a> o <a href="http://www.xm1math.net/texmaker/">Texmaker</a>, ambos multiplataforma.

* Para Mac OS es necesario instalar en primer lugar <a href="http://www.tug.org/mactex/">MacTex</a>.
* En Windows o Linux recomiendo instalar en primer lugar <a href="https://miktex.org/">MiKTeX</a>.

Detalle de trabajar con la estructura de archivos en <a href="https://www.texstudio.org/">TexStudio</a> (en <a href="http://www.xm1math.net/texmaker/">Texmaker</a> es igual) :

<img src="http://jmrplens.com/GitHub_TFGTemplate/texstudio.png" width="30%"></img>

Existen herramientas de pago que facilitan más aún el trabajo con proyectos latex formados por varios archivos y generan más rapido los documentos como <a href="https://www.texpad.com/">Texpad</a> para Mac OS (utilizado para crear esta plantilla) o <a href="http://www.winedt.com/">WinEdt</a> para Windows.

## Características

### Directrices de estilo
La plantilla respeta las directrices de estilo que determina la Escuela Politécnica Superior de La Universidad de Alicante para los TFG y TFM. Se pueden revisar estas directrices en: <a href="https://eps.ua.es/es/ingenieria-sonido-imagen-telecomunicacion/documentos/tfg/libro-de-estilo.pdf">Guía de estilo</a>

Lo márgenes se establecen en el archivo `configuracióninicial.tex`, que no es necesario editar salvo que las directrices de estilo se hayan modificado y esta plantilla no se haya actualizado.
Las líneas de código que definen los márgenes son:
```latex
% MÁRGENES DE LAS PÁGINAS
\usepackage[
  inner	=	3.0cm, % Margen interior
  outer	=	2.5cm, % Margen exterior
  top	=	2.5cm, % Margen superior
  bottom=	2.5cm, % Margen inferior
  includeheadfoot, % Incluye cabecera y pie de página en los márgenes
]{geometry}
```
El interlineado indicado en la guía de estilo no se ha aplicado porque no creo que sea cómoda la lectura con el interlineado indicado en la guía. De todos modos he dejado el comando para modificarlo fácilmente:
```latex
% Valor de interlineado
\renewcommand{\baselinestretch}{1.0} % 1 línea de interlineado
```

Se ha dejado una función para mostrar una regla vertical y horizontal, para poder revisar los márgenes. Se encuentra comentada pero si se desea utilizar para revisar en algún momento los márgenes, se puede eliminar el comentario:
```latex
% Muestra una regla para comprobar el formato de las páginas
%\usepackage[type=upperleft,showframe,marklength=8mm]{fgruler}
```
Se mostraría esto (haz clic sobre la imagen para verla más grande):

<img src="http://jmrplens.com/GitHub_TFGTemplate/REG1.png" width="30%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/REG2.png" width="30%"></img>

Estilo de página par e impar o página izquierda y página derecha.

### Multitud de diseños predefinidos
La plantilla incluye los colores y logotipos que cada titulación determina para los TFG y TFM. Tan solo con cambiar un número, automáticamente se modifica la información para la titulación seleccionada.
La lista de titulaciónes prediseñadas a día de hoy (Enero 2018) son:

| ID  | Titulación |
| ------------- | ------------- |
| `1`  | Grado en Imagen y Sonido en Telecomunicación  |
| `2` | Grado en Ingeniería Civil  |
| `3`  | Grado en Ingeniería Química  |
| `4` | Grado en Ingeniería Informática  |
| `5`  | Grado en Ingerniería Multimedia  |
| `6` | Grado en Arquitectura Técnica  |
| `7`  | Grado en Arquitectura  |
| `8` | Grado en Ingeniería Robótica  |
| `A`  | Máster Universitario en Telecomunicación  |
| `B` | Máster Universitario en Ingeniería de Caminos, Canales y Puentes  |
| `C`  | Máster Universitario en Gestión de la Edificación  |
| `D` | Máster Universitario en Desarrollo de Aplicaciones y Servicios Web  |
| `E`  | Máster Universitario en Ingeniería de los Materiales, Agua y Terreno  |
| `F` | Máster Universitario en Ingeniería Informática  |
| `G`  | Máster Universitario en Automática y Robótica  |
| `H` | Máster Universitario en Prevención de Riesgos Laborales  |
| `I`  | Máster Universitario en Gestión Sostenible y Tecnologías del Agua  |
| `J` | Máster Universitario en Desarrollo de Software para Dispositivos Móviles  |
| `K`  | Máster Universitario en Ingeniería Química  |
| `L`  | Máster Universitario en Ciberseguridad  |

El lugar donde indicar la `ID` de la titulación es en el archivo principal `TFG-TFM_EPS_UA.tex`, en la siguiente línea:

```latex
\def\IDtitulo{X} % INTRODUCE LA ID DE TU TITULACIÓN
```
Donde `X` es la ID de la titulación correspondiente.


Los cambios en la plantilla al cambiar la `ID` suceden en la portada y en la subportada, estableciendo los logotipos correspondientes, color del texto, nombre de la titulación, tipo de trabajo (máster o grado).

Por ejemplo, para la titulación con el `ID=1` se genera automáticamente esta portada y subportada

<p align="center">
<img src="http://jmrplens.com/GitHub_TFGTemplate/P1.png" width="30%"></img><img src="http://jmrplens.com/GitHub_TFGTemplate/PN1.png" width="30%"></img>
</p>

A continuación se muestran el resto de portadas que se pueden generar automáticamente:

<p align="center">
<img src="http://jmrplens.com/GitHub_TFGTemplate/P2.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P3.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P4.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P5.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P6.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P7.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P8.jpg" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PA.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PB.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PC.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PD.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PE.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PF.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PG.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PH.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PI.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PJ.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PK.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PL.jpg" width="20%"></img>
</p>

### Fuente de texto

La fuente general para el documento es la estándar de LaTeX, pero tal como indica la guía de estilo, la fuente para la portada es 'Helvetica' y 'Helvetica LT STD Cond'.

### Lenguajes de programación
Se ha diseñado una 'caja' donde mostrar código de diferentes lenguajes de programación de forma sencilla y muy clara a la hora de leerlo.

Para utilizarlo en el documento, por ejemplo para lenguaje C++:

```latex
\begin{lstlisting}[style=C-color, caption={ejemplo código C en color},label=C_code-color]
	#include <stdio.h>
	// Comentario
	int main(int argc, char* argv[]) {
  	puts("Hola mundo!");
	}
\end{lstlisting}
```
Se puede mostrar el código en color o en blanco y negro, todos los estilos se encuentran definidos en el archivo `estiloscodigoprogramacion.tex`, donde se pueden añadir más lenguajes o modificar el estilo de los ya existentes.
El formato de la caja se define en el archivo `configuracioninicial.tex` en el apartado de código, si se desea se puede cambiar el formato del título de la caja o de la caja misma, o eliminar ambas.

El resultado obtenido dentro del documento para, por ejemplo, lenguaje Python en color y en blanco y negro es el siguiente:

<img src="http://jmrplens.com/GitHub_TFGTemplate/ECod.png" width="40%"></img>

### Contenido de ejemplo
Se ha incluido contenido de ejemplo para mostrar, a aquellos que aún no conocen LaTeX, el potencial que tiene este sistema y enseñar sutílmente cómo manejarlo.

Para ello se han utilizado los archivos de capítulos y en cada uno de ellos se han introducido distintos temas de ejemplo (figuras, códigos, tablas, etc)

Estos capítulos son meramente de ejemplo y pueden ser eliminados sin miedo a que deje de funcionar alguna cosa o editados con el contenido del trabajo.

## Uso
La plantilla necesita el motor XeLaTeX (el más recomendable actualmente), por lo que si el programa que utilizas compila la plantilla con el motor pdfLaTeX (el más habitual pero menos potente) debes cambiarlo por XeLaTeX en las opciones del programa. En el archivo principal se han añadido dos lineas de comandos que fuerza al programa TeXstudio a utilizar el motor XeLateX sin tener que configurar nada, de todos modos si no funcionan será necesario buscar en la ayuda del programa como elegir como motor XeLaTeX. 


El uso de la plantilla es muy sencillo si se conoce qué hace cada uno de los archivos. A continuación se describen cada uno de ellos.

### Estructura de archivos
La plantilla esta estructurada del siguiente modo:
* `anexos` -> Contiene los archivos de los anexos.
* `bibliografia` -> Contiene un archivo BibTeX con la bibliografía.
* `capitulos` -> Contiene los archivos de cada capítulo.
* `archivos` -> Contiene los archivos utilizados en el contenido de ejemplo.
	* `archivos/figuras-procesadas` -> Aquí se almacenan las figuras generadas con TikZ y PGF para no regenerarlas cada vez que se compila el proyecto (no elimines la carpeta sino se generará un error). Ademas puedes aprovechar las figuras generadas para utilizarlas en tu powerpoint o cualquier otro software que vayas a utilizar para presentar tu TFG o TFM.
* `include` -> Contiene todo lo necesario para que la plantilla funcione.
* `TFG-TFM_EPS_UA.tex` -> Archivo principal de la plantilla.

El archivo principal es el lugar donde se introduce la información del trabajo, se indica la titulación para la que se realiza el trabajo y se incluyen los diferentes capítulos. En este archivo no se desarrolla el contenido, este se desarrolla en archivos separados tales como los capítulos o anexos.

La carpeta 'include' tiene todo el código que hace funcionar la plantilla y por ello no debe ser modificada o alterada a no ser que sepas lo que estás haciendo.

### Introduce la información del trabajo
En el archivo principal `TFG-TFM_EPS_UA.tex` se encuentra remarcada la zona donde debes editar la información de tu trabajo y aparece del siguiente modo:

```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INFORMACIÓN DEL TFG
% Comentar lo que NO se desee añadir y sustituir con la información correcta.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Título y subtítulo
\newcommand{\titulo}{Título del Trabajo Fin de Grado/Master}
\newcommand{\subtitulo}{Subtítulo del proyecto}
% Datos del autor
\newcommand{\miNombre}{Nombre Apellido1 Apellido2 (alumno)}
\newcommand{\miEmail}{nombre@alu.ua.es}
% Datos del tutor/es
\newcommand{\miTutor}{Nombre Apellido1 Apellido2 (tutor1)}
\newcommand{\miTutorB}{Nombre Apellido1 Apellido2 (tutor2)}
\newcommand{\departamentoTutor}{Departamento del tutor}
\newcommand{\departamentoTutorB}{Departamento del cotutor}
% Datos de la facultada y universidad
\newcommand{\miFacultad}{Escuela Politécnica Superior}
\newcommand{\miFacultadCorto}{EPS UA}
\newcommand{\miUniversidad}{\protect{Universidad de Alicante}}
\newcommand{\miUbicacion}{Alicante}
``` 

* Si en tu caso no tienes dos tutores, puedes eliminar o comentar (con % delante) tanto la línea de código del nombre del tutor 2 como del departamento del cotutor.

El contenido a modificar es el que se encuentra entre `{}`, siempre el último tramo de cada línea, por ejemplo, en la línea:
`\newcommand{\miNombre}{Nombre Apellido1 Apellido2 (alumno)}` sólo se debe modificar el contenido dentro de los corchetes del último bloque qué es: `{Nombre Apellido1 Apellido2 (alumno)}`, y quedaría tal que: `\newcommand{\miNombre}{Jose Manuel Requena Plens}`

Así con el resto de la información
### Selecciona tu titulación
En el mismo archivo, justo a continuación de la información del trabajo se debe indicar la titulación. En el código se muestra así:
```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% INDICA TU TITULACION
% ID	GRADO -------------------------------------------------
% 1		Ingeniería en Imagen y Sonido en Telecomunicación
% 2		Ingeniería Civil
% 3		Ingeniería Química
% 4		Ingeniería Informática
% 5		Ingeniería Multimedia
% 6		Arquitectura Técnica
% 7		Arquitectura
% 8		Robótica
% %		%%%%%%%%%%%%
% ID	MÁSTER ------------------------------------------------
% A		Telecomunicación
% B		Caminos, Canales y Puertos
% C		Gestión en la Edificación
% D		Desarrollo Web
% E		Materiales, Agua, Terreno
% F		Informática
% G 	Automática y Robótica
% H		Prevención de riesgos laborales
% I		Gestión Sostenible Agua
% J		Desarrollo Aplicaciones Móviles
% K		Ingeniería Química
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!%%%
																		%
\def\IDtitulo{K} % INTRODUCE LA ID DE TU TITULACIÓN						%
																		%
%!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
``` 

Para indicar tu titulación tan solo debes editar el carácter contenido entre `{}` del último bloque. Por ejemplo, si tu trabajo es de Ingeniería en Imagen y Sonido en Telecomunicación, deberías editar la línea de código para indicar la ID de tu titulación, que en este caso es 1, del siguiente modo:
`\def\IDtitulo{1} % INTRODUCE LA ID DE TU TITULACIÓN`

Y listo, con este indicador ya estará tu trabajo prediseñado según las directrices de estilo de tu grado o máster.

### Contenido
El contenido del trabajo se debe desarrollar en archivos separados, es una buena práctica. En el archivo principal de la plantilla (`TFG-TFM_EPS_UA.tex`) se encuentran las líneas que incluyen en el documento las portadas preconfiguradas, los diferentes capítulos, bibliografía y anexos.

#### Precontenido
 Las primeras páginas del documento deben estar dedicadas a las portadas, preámbulo, índice, listado de figuras, tablas, etc. En el archivo principal se definen estas partes justo después de seleccionar la titulación:

```latex
%%%%%%%%%%%%%%%%%%%%%%%% 
% INICIO DEL DOCUMENTO
% A partir de aquí debes empezar a realizar tu TFG/TFM
%%%%%%%%%%%%%%%%%%%%%%%%
\begin{document}

% Números romanos hasta el mainmatter.
\frontmatter

% PORTADA
\input{include/portada/portada_color} % Portada Color
\input{include/portada/portada_bn} % Portada B/N

%%%%% PREAMBULO
% Incluye el .tex que contiene el preámbulo, agradecimientos y dedicatorias.
\input{capitulos/preliminaresconagradecimientos} 

% Incluye después del archivo anterior el indice y lista de figuras, tablas y códigos.
\tableofcontents
\listoffigures
\listoftables
\lstlistoflistings

% Inicia la numeración habitual.
\mainmatter
 ```

Como se puede observar, las líneas que comienzan con 'input' son aquellas que cargan archivos separados. En primer lugar se establece numeración de páginas romana, después se incluye la portada principal y la subportada, a continuación el archivo de preliminares (contiene el preámbulo, agradecimientos, dedicatorias,... a modificar por al autor del trabajo). 
Después de los preliminares se ejecutan los comandos que incluyen en el documento el índice (`\tableofcontents`), la lista de figuras (`\listoffigures`), la lista de tablas (`\listoftables`) y la lista de códigos (`\lstlistoflistings`), si no vas a hacer uso de alguno de ellos puedes eliminar o comentar (con %) la línea que no quieras incluir en el documento. Por último inicia la numeración de páginas normal (1,2,3,...).

#### Capítulos
Si creas un nuevo archivo de capítulo que deseas añadir al documento debes agregarlo en el archivo principal justo en el apartado indicado de capítulos. Estos se mostrarán en el mismo orden en el que estén escritos, por ejemplo, en la plantilla actualmente están declarados los siguientes capítulos:

```latex
%%%%
% CONTENIDO. CAPÍTULOS DEL TRABAJO - Añade o elimina según tus necesidades
%%%%
\input{capitulos/Introduccion}
\input{capitulos/marcoteorico}	% Plantilla: Se muestran listas
\input{capitulos/objetivos}	% Plantilla: Se muestran tablas
\input{capitulos/metodologia}	% Plantilla: Se muestran figuras
\input{capitulos/desarrollo}	% Plantilla: Se muestran listados
\input{capitulos/resultados}	% Plantilla: Se muestran gráficas
\input{capitulos/conclusiones}	% Plantilla: Se muestran matemáticas
```

Y en el documento generado se mostrarán en ese orden.

Un capítulo es tan solo un archivo .tex donde sus dos primeras líneas deben contener:

```latex
\chapter{Título del capítulo}
\label{etiquetacapitulo}
```

El comando `\chapter{}` genera el título del capítulo y lo incluye en el índice y el comando `\label{}` añade una etiqueta al capítulo por si quieres hacer referencia a él en algún punto del documento escribiendo `\ref{etiqueta}` (incluye el número de lo referenciado) o `\pageref{etiqueta}` (incluye el número de página de lo referenciado).

Después de estas dos líneas puedes desarrollar tu contenido, añadiendo texto, secciones (`\section{nombreseccion}`), etc.

#### Postcontenido
Después del contenido principal del trabajo se debe incluir la bibliografía, y si es necesario un listado de acrónimos utilizados y anexos. En la plantilla están definidos del siguiente modo:

```latex
%%%%
% CONTENIDO. BIBLIOGRAFÍA.
%%%%
\nocite{*} %incluye TODOS los documentos de la base de datos bibliográfica sean o no citados en el texto
\bibliography{bibliografia/bibliografia} % Archivo que contiene la bibliografía
\bibliographystyle{apacite}

%%%%
% CONTENIDO. LISTA DE ACRÓNIMOS. Comenta las líneas si no lo deseas incluir.
%%%%
% Incluye el listado de acrónimos utilizados en el trabajo. 
\printglossary[style=modsuper,type=\acronymtype,title={Lista de Acrónimos y Abreviaturas}]
% Añade el resto de acrónimos si así se desea. Si no elimina el comando siguiente
\glsaddallunused 

%%%%
% CONTENIDO. Anexos - Añade o elimina según tus necesidades
%%%%
\appendix % Inicio de los apéndices
\input{anexos/anexo_I}
\input{anexos/anexo_2}
\input{anexos/anexo_3}

\end{document}
```

Hay tres partes diferenciadas:
* Acrónimos: Si se quiere mostrar un listado de acrónimos se debe mantener esas líneas, además de editar el archivo `anexos/acronimos.tex` con los acrónimos utilizados en tu trabajo. Este archivo se carga justo antes del precontenido.
* Bibliografía: Esta parte debe aparecer siempre en el trabajo y para poder generarla de la forma más sencilla se pueden utilizar herramientas como <a href="http://www.jabref.org/">JabRef</a> o <a href="https://bibdesk.sourceforge.io/">BibDesk</a>. El archivo generado (.bib) se debe cargar con la línea de código mostrada en el bloque de arriba `\bibliography{bibliografia/bibliografia}`, donde `bibliografia/bibliografia` es la ruta del archivo.
* Apéndices: Aquí se pueden incluir anexos del mismo modo que se hace con los capítulos, pero que al estar debajo de la línea `\appendix` se añaden al documento como anexos. Si tu trabajo no tiene anexos puedes eliminar esta parte.

### Archivos 'include'
Los archivos de la carpeta 'include' son los que configuran la plantilla y por ello no deben ser modificados a no ser que sepas lo que haces.

El archivo `configuracioninicial.tex` define el formato del documento, e incluye todos los paquetes y comandos que pueden ser utilizados en la plantilla. Se han añadido muchísimos paquetes para diferentes cuestiones que serán útiles para realizar el documento. En este archivo se encuentran comentados los paquetes y lo que hacen cada uno de ellos, y si se desea incluir algún paquete a la plantilla es en este archivo donde se recomienda incluirlo.

El archivo `configuraciontitulacion.tex` es el archivo que diseña automaticamente las portadas segun la titulación seleccionada. En él se encuentran definidos los colores de cada titulación, los logotipos comunes y despues la información para cada titulación.

En el archivo `estiloscodigoprogramacion.tex` se definen los estilos para mostrar código de distintos lenguajes de programación. Si al mostrar código en tu trabajo, el código no se colorea correctamente o prefieres mostrarlo en otros colores, aquí es donde debes modificar esos detalles. El formato del cuadro donde se muestra el código dentro del documento está definido en el archivo `configuracioninicial.tex`.

La carpeta `portada` contiene los archivos que configuran tanto la portada como la subportada, no es necesario editar nada en ellos a no ser que cambien las directrices de estilo de la EPS.

Las carpetas `logos-universidad` y `logos-titulaciones` contienen todos los logotipos necesarios para cada una de la titulaciones prediseñadas.

La carpeta `fuentes` contiene las fuentes utilizadas para el texto de la portada tal como establece la guía de estilo de la EPS.

### Lista de acrónimos y abreviaturas
La plantilla tiene configurado un sistema para realizar una base de datos de acrónimos o abreviaturas para ser utilizadas en el documento.
El archivo donde se almacenan los acrónimos y el comando para mostrarlos o no, se encuentran en el bloque de [postcontenido](#postcontenido).

Tanto la introducción de acrónimos como el uso en el documento es sencillo. En el archivo de `acronimos.tex` se encuentran definidos algunos de ellos y la información para definirlos y usarlos:

```latex
% La forma de definir un acrónimo es la siguiente:
% \newacronyn{id}{siglas}{descripción}
% Donde:
% 	'id' es como vas a llamarlo desde el documento.
%	'siglas' son las siglas del acrónimo.
%	'descripción' es el texto que representan las siglas.
%
% Para usarlo en el documento tienes 4 formas:
% \gls{id} - Añade el acrónimo en su forma larga y con las siglas (tal que: descripcion (siglas)) si es la primera vez que se utiliza, el resto de veces solo añade las siglas. (No utilices este comando en títulos de capítulos o secciones).
% \glsentryshort{id} - Añade solo las siglas de la id
% \glsentrylong{id} - Añade solo la descripción de la id
% \glsentryfull{id} - Añade tanto la descripción como las siglas
```

### Bibliografía
Para la bibliografía es recomendable utilizar herramientas como <a href="http://www.jabref.org/">JabRef</a> para Windows, Mac OS y Linux.

Cualquier aplicación para bibliografía para LaTeX que utilices puede generar un archivo en formato `.bib` (BibTeX), que contiene toda la información de cada referencia que agregues.
Este archivo es el que se carga en el bloque de [postcontenido](#postcontenido) y automáticamente agrega un capítulo de bibliografía a tu documento con la información incluida en tu archivo `.bib` (BibTeX).

Si mantienes comentada la línea:

`%\nocite{*}`

Sólo se mostrará en el capítulo de bibliografía aquellos textos referenciados en tu documento, si eliminas el comentario (el carácter %), se incluirán todas las referencias que hayan en el archivo `.bib` (BibTeX).

Para realizar una referencia de un texto en tu documento debes escribir lo siguiente:

`\cite{XXXXX}`

Donde 'XXXX' es la ID que se refiere al texto (lo puedes buscas dentro del archivo .bib).

#### Citar bibliografía
Hay disponibles varios métodos para citar (todos ajustados al sistema APA en su última versión), gracias a los paquetes incluidos en la plantilla `apacite` y `natbib`.

Los comandos y un ejemplo de lo que generara en el documento son los siguientes (donde `idbib` es la id del texto a citar que está dentro de tu archivo .bib):

| Comando | Resultado | 
| ------------- | ------------- |
| `\citet{idbib}`  | Shaw y Garlan (1996)  |
| `\citep{idbib}`  | (Shaw y Garlan, 1996)  |
| `\citep[ver][cap. 2]{idbib}`  | (ver Shaw y Garlan, 1996, cap. 2)  |
| `\citep[ver][]{idbib}`  | (ver Shaw y Garlan, 1996)  |
| `\citep[cap. 2]{idbib}`  | (Shaw y Garlan, 1996, cap. 2)  |
| `\citep{idbib,idbib2}`  | (Shaw y Garlan, 1996; Akyildiz y cols., 1995)  |
| `\citet*{idbib2}`  | Akyildiz, Pompili, y Melodia (2005)  |
| `\citep*{idbib2}`  | (Akyildiz, Pompili, y Melodia, 2005)  |

Cuando hay una 't' delante del comando, la cita se mostrará como texto y el año entre paréntesis. Si hay una 'p' todo estará entre paréntesis. Si el documento a citar tiene mas de dos autores se mostrará 'Autor1 y cols', pero si se pone un asterisco delante del comando se mostrarán todos los autores.

### Comentarios
En todo proceso de realizar un documento hay momentos en los que se necesita dejar algún comentario para que más adelante se añada algun contenido o se corrija algo. Teniendo en cuenta esto se ha añadido un paquete que ayuda a dejar comentarios en el texto, tiene varios comandos para utilizar aunque los principales son:
```latex
\todo{tu comentario}
\todo[inline]{tu comentario}
\missingfigure{tu comentario}
```
Obteniendo estos resultados (estos ejemplos se encuentran en la plantilla):

<img src="http://jmrplens.com/GitHub_TFGTemplate/tareas.png" width="40%"></img>

## Control de errores
Se han tenido en cuenta varias situaciones que podrían ser problemáticas para el diseño del documento, como:

### Longitud del título
Hay gran variedad de títulos, desde unos pocos carácteres hasta incluso más de 200. Esto se ha tenido en cuenta y se ha primado el mantener consolidado el diseño frente al tamaño de fuente definido en la guía de estilo. 

El tamaño de fuente del título en la portada por defecto es 55, tal como establece la guía de estilo, pero en el caso de que el título exceda cierto número de carácteres, automáticamente se reduce el tamaño y el interlineado del título para que no sobrepase el espacio disponible. Este control del título se realiza a través de estas líneas:
```latex
% Según la longitud del título se determina un tamaño e interlineado para él
\StrLen{\titulo}[\longitudtitulo] % Cuenta los caracteres del título
% Comprueba la longitud del título y según sea este determina unos valores nuevos
\ifthenelse{\longitudtitulo > 180}{
\def\FuenteTamano{35pt}		% Si es mayor a 180 caracteres tamaño de fuente 35pt
\def\interlinportada{3.5}} 	% Establece nuevo interlineado
{\ifthenelse{\longitudtitulo > 140}{
\def\FuenteTamano{40pt}		% Si es mayor a 140 caracteres tamaño de fuente 40pt
\def\interlinportada{4.0}} 	% Establece nuevo interlineado
{\ifthenelse{\longitudtitulo > 120}{
\def\FuenteTamano{50pt}		% Si es mayor a 120 caracteres tamaño de fuente 50pt
\def\interlinportada{4.5}} 	% Establece nuevo interlineado
{} % Si no, no modifica el tamaño
} }
```

## Aspectos avanzados

### Formato del documento
El formato del documento está definido en el archivo `configuracioninicial.tex`. Tanto el tipo de documento, como el formato y contenido de cabecera y pie de página y los márgenes se definen en las siguientes líneas:

```latex
%%%%%%%%%%%%%%%%%%%%%%%%
% FORMATO DEL DOCUMENTO
%%%%%%%%%%%%%%%%%%%%%%%%
% scrbook es la clase de documento
% Si se desea que no haya página en blanco entre capítulos añadir "openany" en los parámetros de la clase. Sino siempre los capítulos empezarán en página impar.
\documentclass[a4paper,11pt,titlepage]{scrbook}
\KOMAoption{toc}{bib,chapterentryfill} % Opciones del índice
\usepackage{scrhack} % Previene algunos errores
% Paquete de formato para scrbook. Con marcas, linea-separador superior e inferior
\usepackage[automark,headsepline,footsepline]{scrlayer-scrpage}
\clearpairofpagestyles		% Borra los estilos por defecto
%%
% Formato y contenido de la información de cabecera y pie de página
%%
% Información de capítulo en cabecera e interno
\ihead{{\color{gray30}\scshape\small\headmark}}	
% Número de página en cabecera y externo
\ohead{\normalfont\pagemark} 
% Número de página en pie de página y externo. Sólo en páginas sin cabecera
\ofoot[\normalfont\pagemark]{}
%% 		
% Edición del contenido de las distintas partes de la cabecera
%%
\renewcommand{\chaptermark}[1]{\markboth{#1}{}} % Capítulo (Solo texto)
\renewcommand{\sectionmark}[1]{\markright{\thesection. #1}} % Sección (Número y texto)
\setkomafont{pagenumber}{} % Número de página (Sin nada añadido)
```

Las funciones de este primer bloque están definidas en el manual de la clase de documento, que es parte de un paquete llamado KOMA-Script y su manual se puede leer aquí: <a href="http://osl.ugr.es/CTAN/macros/latex/contrib/koma-script/doc/scrguien.pdf">Manual KOMA-Script</a>. Si modificas algo del formato definido en este bloque, confirma con tu tutor de TFG/TFM si el nuevo formato es correcto para el documento. 

```latex
% Añade al índice y numera hasta la profundidad 4.
% 1:section,2:subsection,3:subsubsection,4:paragraph
\setcounter{tocdepth}{4}
\setcounter{secnumdepth}{4}
% Muestra una regla para comprobar el formato de las páginas
%\usepackage[type=upperleft,showframe,marklength=8mm]{fgruler}
% MÁRGENES DE LAS PÁGINAS
\usepackage[
  inner	=	3.0cm, % Margen interior
  outer	=	2.5cm, % Margen exterior
  top	=	2.5cm, % Margen superior
  bottom=	2.5cm, % Margen inferior
  includeheadfoot, % Incluye cabecera y pie de página en los márgenes
]{geometry}
% Valor de interlineado
\renewcommand{\baselinestretch}{1.0} % 1 línea de interlineado
% Para poder generar páginas horizontales
\usepackage{lscape}
% Ancho de la zona para comentarios en el margen. (modificado para todonotes)
\setlength{\marginparwidth}{1.9cm}
```

En este segundo bloque se define hasta qué profundidad se genera el índice, el valor de los márgenes, también el interlineado y otros detalles. Si lo deseas puedes modificar la profundidad del índice pero los márgenes solo se deben modificar si las directrices de estilo de la EPS han cambiado.

### Idioma del documento

También en el archivo `configuracioninicial.tex` el documento está configurado para texto en español, por razones obvias, pero si se va a realizar en otro idioma o en varios idiomas se puede modificar (siguiendo este manual: <a href="http://osl.ugr.es/CTAN/macros/latex/contrib/polyglossia/polyglossia.pdf">Polyglossia</a>) en las líneas siguientes:

```latex
%%%%%%%%%%%%%%%%%%%%%%%%
% DOCUMENTO EN ESPAÑOL
%%%%%%%%%%%%%%%%%%%%%%%%
\usepackage{polyglossia}
\setmainlanguage{spanish}
\addto\captionsspanish{%
	\renewcommand{\listtablename}{Índice de tablas} 
	\renewcommand{\tablename}{Tabla}
	\renewcommand{\lstlistingname}{Código}
	\renewcommand{\lstlistlistingname}{Índice de \lstlistingname s}
	\renewcommand{\glossaryname}{Glosario}
	\renewcommand{\acronymname}{Acrónimos}
}
```

Las líneas que siguen a `\addto...` renombran algunos términos estándar para traducirlos al español. Si tu trabajo está en otro idioma cámbialos por el idioma del trabajo.

### Añadir/Editar formato de titulaciones

Si el color o logotipo de tu titulación ha cambiado, o tu titulación no se encuentra actualmente en la plantilla, en primer lugar ponte en contacto conmigo para que actualice la plantilla, y si no puedes esperar a la actualización puedes añadirlo tú del siguiente modo en el archivo `configuraciontitulacion.tex`

El formato de una titulación se define después de comprobar el valor de la ID introducida en el archivo principal, por lo que si deseas actualizar tu titulación debes buscar donde el condicional comprueba tu ID. Esto lo realiza en esta línea:

`\if\IDtitulo X`

Donde 'X' es la ID de la titulación. 

El condicional completo se compone de lo siguiente:
```latex
\if\IDtitulo 1 % Teleco
		% Logos
		\newcommand{\logoFacultadPortada}{include/logos-universidad/LogoEPSBlanco} % Logo EPS en portada
		\newcommand{\logoGradoPortada}{include/logos-titulaciones/LogoTelecoBlanco} % Logo titulación en portada
		\newcommand{\logoGrado}{include/logos-titulaciones/LogoTelecoNegro} % Logo titulación en subportada
		% Texto
		\newcommand{\miGrado}{Grado en Ingeniería en Sonido e Imagen en Telecomunicación} % Nombre de la titulación
		\newcommand{\tipotrabajo}{Trabajo Fin de Grado} % Tipo de trabajo (grado o máster)
		% Color
		\newcommand{\colorgrado}{teleco} % Color de la portada. Definido al inicio del archivo
		\newcommand{\colortexto}{blanco} % Color del texto de la portada (blanco o negro)
```

Si tu titulación ya está en la plantilla edita las líneas que hayan sido modificadas para tu titulación.

Si tu titulación no está en la plantilla y deseas añadirla, debes añadirla al final del condicional, justo encima de la línea:

`\fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi \fi`

Encima de esta linea deberás agregar el condicional con la ID que llevará la titulación que vayas a añadir tal que:

```latex
\else \if\IDtitulo X % ID de tu titulación añadida
% Logos
		\newcommand{\logoFacultadPortada}{include/logos-universidad/LogoEPS____} % Logo EPS en portada (blanco o negro)
		\newcommand{\logoGradoPortada}{include/logos-titulaciones/Logo_____} % Logo titulación en portada (blanco o negro)
		\newcommand{\logoGrado}{include/logos-titulaciones/Logo____Negro} % Logo titulación en subportada (solo negro)
		% Texto
		\newcommand{\miGrado}{_____________} % Nombre de la titulación
		\newcommand{\tipotrabajo}{Trabajo Fin de ______} % Tipo de trabajo (grado o máster)
		% Color
		\newcommand{\colorgrado}{_______} % Color de la portada. Definido al inicio del archivo
		\newcommand{\colortexto}{_______} % Color del texto de la portada (blanco o negro)
```

Según el color de fuente de la portada (blanco o negro) deberás incluir en el mismo color el logotipo de la EPS (ya incluido en la plantilla tanto en negro como en blanco) y el logotipo de tu titulación. Para la subportada el logotipo de tu titulación debe ser negro obligatoriamente. Introduce el texto de tu grado y titulación correspondiente. Y por último define tu color de grado al inicio del archivo (en RGB) y añade el nombre del color definido, e indica si la fuente de texto de la portada es negro o blanco.

### Fuentes de la portada

Las fuentes de la portada están establecidas en las directrices de estilo de la EPS, pero si cambian estas directrices puedes modificar las fuentes en el archivo `portada_color.tex` en las líneas:

```latex
% Establece las fuentes de texto de la portada
% Helvetica LS Std Cond. Uso: {\FuenteTitulo tutexto}
\newfontfamily\FuenteTitulo{HelveticaLTStd-Cond}[Path=./include/fuentes/]  
% Helvetica. Uso: {\FuentePortada tutexto}
\newfontfamily\FuentePortada{Helvetica}[Path=./include/fuentes/] 
```

Si tienes que cambiar la fuente debes modificar el tipo de fuente para el título de la portada (actualmente HelveticaLTStd-Cond) por el nuevo, y lo mismo para la otra fuente para el resto del texto de la portada (actualmente Helvetica). Estas fuentes deben estar en la carpeta `include/fuentes` para poder ser cargadas por la plantilla.

El tamaño de la fuente se puede modificar en las siguientes líneas del mismo archivo:
```latex
% Tamaño por defecto de la fuente de texto para:
\def\FuenteTamano{55pt}	  % Tamaño para el título del trabajo
\def\interlinportada{5.0} % Interlineado por defecto para el título
\def\TamTrabajo{20pt} 	  % Tamaño para el tipo de trabajo (grado o máster)
\def\TamTrabajoIn{20pt}   % Tamaño para el salto de línea después de tipo de trabajo
\def\TamOtros{12pt} 	  % Tamaño para datos personales y fecha
\def\TamOtrosIn{1pt} 	  % Tamaño para los saltos de línea en la info personal
```

## Contacto (sugerencias, errores, etc)
Si no deseas publicar en GitHub una sugerencia o algún error encontrado puedes ponerte en contacto conmigo a través de:

* Email: <a href="mailto:info@jmrplens.com">info@jmrplens.com</a>
* Telegram: <a href="https://t.me/jmrplens">@jmrplens</a>
