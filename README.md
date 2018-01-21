# TFG-TFM_EPS (En proceso - Previsto para Enero-Febrero 2018)
Plantilla LaTex para la elaboración de TFG y TFM en la Escuela Politécnica Superior de la Universidad de Alicante

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
  includeheadfoot, % Incluye cabecera y pide de página en los márgenes
]{geometry}
```
Se ha dejado una función para mostrar una regla vertical y horizontal, para poder revisar los márgenes. Se encuentra comentada pero si se desea utilizar para revisar en algún momento los margenes, se puede eliminar el comentario:
```latex
% Muestra una regla para comprobar el formato de las páginas
%\usepackage[type=upperleft,showframe,marklength=8mm]{fgruler}
```
Se mostraría esto:


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

### Control de errores
Se ha tenido en cuenta varias situaciones que podrían ser problemáticas para el diseño del documento, como:

#### Longitud del título
Hay gran variedad de títulos, desde unos pocos carácteres hasta incluso más de 200. Esto se ha tenido en cuenta y se ha primado el mantener consolidado el diseño frente al tamaño de fuente definido en la guía de estilo. 

El tamaño de fuente del título en la portada por defecto es 55, tal como establece la guía de estilo, pero en el caso de que el titulo exceda cierto número de carácteres, automaticamente se reduce el tamaño y el interlineado del titulo. Este control del titulo se realiza a tráves de estas líneas:
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
