
# Plantilla TFG/TFM 
Esta plantilla se ha creado después de observar la idea concebida por Pedro Pernías y otros colaboradores en su plantilla: <a href="https://github.com/lcg51/tfg">tfg</a>. Se ha mantenido algún contenido de los capítulos de esa plantilla, y la clase de documento _scrbook_ pero el resto de la plantilla esta realizada de cero.

Esta plantilla puede ser divulgada, modificada y compartida libremente. Este proyecto se ha realizado por y para los alumnos de la Escuela Politécnica Superior de la Universidad de Alicante, esperando facilitar un poco la introducción al trabajo con LaTex. Se ruega enviar sugerencias de todo tipo, el contenido de la plantilla intenta mostrar un poco de todo lo que se puede hacer con LaTex, pero si es complejo el uso y asi lo indicasen los usuarios se modificará para hacerla más manejable.

<!-- MarkdownTOC depth=4 -->

- [Características](#caracter%C3%ADsticas)
	- [Directrices de estilo](#directrices-de-estilo)
	- [Multitud de diseños predefinidos](#multitud-de-dise%C3%B1os-predefinidos)
	- [Contenido de ejemplo](#contenido-de-ejemplo)
- [Uso](#uso)
	- [Estructura de archivos](#estructura-de-archivos)
	- [Introduce la información del trabajo](#introduce-la-informaci%C3%B3n-del-trabajo)
	- [Selecciona tu titulación](#selecciona-tu-titulaci%C3%B3n)
	- [Contenido](#contenido)
		- [Precontenido](#precontenido)
		- [Capítulos](#cap%C3%ADtulos)
		- [Postcontenido](#postcontenido)
- [Control de errores](#control-de-errores)
		- [Longitud del título](#longitud-del-t%C3%ADtulo)

<!-- /MarkdownTOC -->

## Características

### Directrices de estilo
La plantilla respeta las directrices de estilo que determina la Escuela Politécnica Superior de La Universidad de Alicante para los TFG y TFM. Se pueden revisar estas directrices en: <a href="https://eps.ua.es/es/ingenieria-sonido-imagen-telecomunicacion/documentos/tfg/libro-de-estilo.pdf">Guía de estilo</a>

Lo márgenes se establecen en el archivo `configuracióninicial.tex`, que no es necesario editar salvo que las directrices de estilo se hayan modificado y esta plantilla no se haya actualizado.
Las líneas de código que definen los márgenes son:
```latex
% MARGENES DE LAS PÁGINAS
\usepackage[
  inner	=	2.5cm, % Margen interior
  outer	=	3.0cm, % Margen exterior
  top	=	2.5cm, % Margen superior
  bottom=	2.5cm, % Margen inferior
  includeheadfoot, % Incluye cabecera y pie de página en los márgenes
]{geometry}
```
Se ha dejado una función para mostrar una regla vertical y horizontal, para poder revisar los márgenes. Se encuentra comentada pero si se desea utilizar para revisar en algún momento los margenes, se puede eliminar el comentario:
```latex
% Muestra una regla para comprobar el formato de las páginas
%\usepackage[type=upperleft,showframe,marklength=8mm]{fgruler}
```
Se mostraría esto (haz clic sobre la imagen para verla más grande):

<img src="http://jmrplens.com/GitHub_TFGTemplate/PREGLA.png" width="30%"></img>

### Multitud de diseños predefinidos
La plantilla incluye los colores y logotipos que cada titulación determina para los TFG y TFM. Tán solo con cambiar un número, automaticamente se modifica la información para la titulación seleccionada.
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
| `8` | Grado en Ingeniería Robótica (falta definir color y logo)  |
| `A`  | Máster Universitario en Telecomunicación  |
| `B` | Máster Universitario en Ingeniería de Camino, Canales y Puentes  |
| `C`  | Máster Universitario en Gestión de la Edificación  |
| `D` | Máster Universitario en Desarrollo de Aplicaciones y Servicios Web  |
| `E`  | Máster Universitario en Ingeniería de los Materiales, Agua y Terreno  |
| `F` | Máster Universitario en Ingeniería Informática  |
| `G`  | Máster Universitario en Automática y Robótica  |
| `H` | Máster Universitario en Prevención de Riesgos Laborales  |
| `I`  | Máster Universitario en Gestión Sostenible y Tecnologías del Agua  |
| `J` | Máster Universitario en Desarrollo de Software para Dispositivos Móviles  |
| `K`  | Máster Universitario en Ingeniería Química  |

El lugar donde indicar la `ID` de la titulación es en el archivo principal `TFG-TFM_EPS_UA.tex`, en la siguiente línea:

```latex
\def\IDtitulo{X} % INTRODUCE LA ID DE TU TITULACIÓN
```
Donde `X` es la ID de la titulación correspondiente.


Los cambios en la plantilla al cambiar la `ID` suceden en la portada y en la subportada, estableciendo los logotipos correspondientes, color del texto, nombre de la titulación, tipo de trabajo (máster o grado).

Por ejemplo, para la titulación con el `ID=1` se genera automaticamente esta portada y subportada

<p align="center">
<img src="http://jmrplens.com/GitHub_TFGTemplate/P1.png" width="30%"></img><img src="http://jmrplens.com/GitHub_TFGTemplate/PN1.png" width="30%"></img>
</p>

A continuación se muestran el resto de portadas que se pueden generar automáticamente:

<p align="center">
<img src="http://jmrplens.com/GitHub_TFGTemplate/P2.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P3.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P4.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P5.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P6.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/P7.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PA.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PB.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PC.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PD.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PE.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PF.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PG.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PH.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PI.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PJ.png" width="20%"></img> <img src="http://jmrplens.com/GitHub_TFGTemplate/PK.png" width="20%"></img>
</p>

### Contenido de ejemplo
Se ha incluido contenido de ejemplo para mostrar, a aquellos que aun no conocen LaTeX, el potecial que tiene este sistema y enseñar sutílmente como manejarlo.

Para ello se ha utilizado los archivos de capítulos y en cada uno de ellos se ha introducido distintos temas de ejemplo (figuras, códigos, tablas, etc)

Estos capítulos son meramente de ejemplo y pueden ser eliminados sin miedo a que deje de funcionar alguna cosa o editados con el contenido del trabajo.

## Uso

### Estructura de archivos
La plantilla esta estructurada del siguiente modo:
* `anexos` -> Contiene los archivos de los anexos.
* `bibliografia` -> Contiene un archivo BibTeX con la bibliografía.
* `capitulos` -> Contiene los archivos de cada capítulo.
* `imagenes` -> Contiene las imágenes utilizadas en el contenido de ejemplo.
* `include` -> Contiene todo lo necesario para que la plantilla funcione.
* `TFG-TFM_EPS_UA.tex` -> Archivo principal de la plantilla.

El archivo principal es el lugar donde se introduce la información del trabajo, se indica que titulación para la que se realiza el trabajo y se incluyen los diferentes capitulos. En este archivo no se desarrolla el contenido, este se desarrolla en archivos separados tales como los capítulos o anexos.

La carpeta include tiene todo el codigo que hace funcionar la plantilla y por ello no debe ser modificada o alterada a no ser que sepas lo que estás haciendo.

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

El contenido a modificar es el que se encuentra entre `{}`, siempre el ultimo tramo de cada línea, por ejemplo, en la línea:
`\newcommand{\miNombre}{Nombre Apellido1 Apellido2 (alumno)}` solo se debe modificar el contenido dentro de los corchetes del ultimo bloque qué es: `{Nombre Apellido1 Apellido2 (alumno)}`, y quedaría tal que: `\newcommand{\miNombre}{Jose Manuel Requena Plens}`

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

Para indicar tu titulación tan solo debes editar el caracter contenido entre `{}` del último bloque. Por ejemplo, si tu trabajo es de Ingeniería en Imagen y Sonido en Telecomunicación, deberias editar la línea de codigo para indicar la ID de tu titulación, que en este caso es 1, del siguiente modo:
`\def\IDtitulo{1} % INTRODUCE LA ID DE TU TITULACIÓN`

Y listo, con este indicador ya estara tu trabajo prediseñado segun las directrices de estilo de tu grado o máster.

### Contenido
El contenido del trabajo se debe desarrollar en archivos separados, es una buena práctica. En el archivo principal de la plantilla (`TFG-TFM_EPS_UA.tex`) se encuentran las líneas que incluyen en el documento las portadas preconfiguradas, los diferentes capítulos, bibliografía y anexos.

#### Precontenido
 Las primeras páginas del documento deben estar dedicadas a las portadas, preámbulo, índice, listado de figuras, tablas, etc. En el archivo principal se definen estas partes justo despues de seleccionar la titulación:

```latex
%%%%%%%%%%%%%%%%%%%%%%%% 
% INICIO DEL DOCUMENTO
% A partir de aquí debes empezar a realizar tu TFG/TFM
%%%%%%%%%%%%%%%%%%%%%%%%
\begin{document}

% Numeros romanos hasta el mainmatter.
\frontmatter

% PORTADA
\input{include/portada/portada_color} % Portada Color
\input{include/portada/portada_bn} % Portada B/N

%%%%% PREÁMBULO
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
Después de los preliminares se ejecutan los comandos que incluyen en el documento el índice (`\tableofcontents`), la lista de figuras (`\listoffigures`), la lista de tablas (`\listoftables`) y la lista de códigos (`\lstlistoflistings`), si no vas a hacer uso de alguno de ellos puedes eliminar o comentar (con %) la línea que no quieras incluir en el documento. Por ultimo inicia la numeración de páginas normal (1,2,3,...).

#### Capítulos
Si creas un nuevo archivo de capítulo que deseas añadir al documento debes agregarlo en el archivo principal justo en el apartado indicado de capítulos. Estos se mostrarán en el mismo orden en el que esten escritos, por ejemplo, en la plantilla actualmente están declarados los siguientes capítulos:

```latex
%%%%
% CONTENIDO. CAPITULOS DEL TRABAJO - Añade o elimina según tus necesidades
%%%%
\input{capitulos/Introduccion}
\input{capitulos/marcoteorico}	% Plantilla: Se muestran listas
\input{capitulos/objetivos}		% Plantilla: Se muestran tablas
\input{capitulos/metodologia}	% Plantilla: Se muestran figuras
\input{capitulos/desarrollo}		% Plantilla: Se muestran listados
\input{capitulos/resultados}		% Plantilla: Se muestran gráficas
\input{capitulos/conclusiones}	% Plantilla: Se muestran matemáticas
```

Y en el documento generado se mostraran en ese orden.

#### Postcontenido
Despues del contenido principal del trabajo se debe incluir la bibliografía, y si es necesario un listado de acrónimos utilizados y anexos. En la plantilla están definidos del siguiente modo:

```latex
%%%%
% CONTENIDO. LISTA DE ACRÓNIMOS. Comenta la lineas si no lo deseas incluir.
%%%%
% Incluye el listado de acrónimos
\input{anexos/acronimos.tex}
% Incluye en el índice el listado de acrónimos
\addcontentsline{toc}{chapter}{Lista de Acrónimos}

%%%%
% CONTENIDO. BIBLIOGRAFÍA. Comenta la lineas si no lo deseas incluir.
%%%%
%\nocite{*} %incluye TODOS los documentos de la base de datos bibliográfica sean o no citados en el texto
\bibliography{bibliografia/bibliografia}
\addcontentsline{toc}{chapter}{Bibliografía} 
\bibliographystyle{apalike}

%%%%
% CONTENIDO. APENDICES - Añade o elimina según tus necesidades
%%%%
\appendix % Inicio de los apéndices
\input{anexos/anexo_I}
```

Hay tres partes diferenciadas:
* Acrónimos: Si se quiere mostrar un listado de acrónimos se debe mantener esas líneas, ademas de editar el archivo `anexos/acronimos.tex` con los acrónimos utilizados en tu trabajo.
* Bibliografía: Esta parte debe aparecer siempre en el trabajo y para poder generarla de la forma mas sencilla se pueden utilizar herramientas como <a href="http://www.jabref.org/">JabRef</a> o <a href="https://bibdesk.sourceforge.io/">BibDesk</a>. El archivo generado (.bib) se debe cargar con la línea de código mostrada en el bloque de arriba `\bibliography{bibliografia/bibliografia}`, donde `bibliografia/bibliografia` es la ruta del archivo.
* Apendices: Aquí se pueden incluir anexos del mismo modo que se hace con los capítulos, pero que al estar debajo de la línea `\appendix` se añaden al documento como anexos. Si tu trabajo no tiene anexos puedes eliminar esta parte.

## Control de errores
Se ha tenido en cuenta varias situaciones que podrían ser problemáticas para el diseño del documento, como:

#### Longitud del título
Hay gran variedad de títulos, desde unos pocos carácteres hasta incluso más de 200. Esto se ha tenido en cuenta y se ha primado el mantener consolidado el diseño frente al tamaño de fuente definido en la guía de estilo. 

El tamaño de fuente del título en la portada por defecto es 55, tal como establece la guía de estilo, pero en el caso de que el titulo exceda cierto número de carácteres, automaticamente se reduce el tamaño y el interlineado del titulo para que no sobrepase el espacio disponible. Este control del titulo se realiza a tráves de estas líneas:
```latex
% Según la longitud del titulo se determina un tamaño e interlineado para él
\StrLen{\titulo}[\longitudtitulo]
\def\FuenteTamano{55pt} % Tamaño por defecto
\def\interlinportada{5.0} % Interlineado por defecto

% Comprueba la longitud del titulo y según sea este determina unos valores nuevos
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
