# Componentes Especializados para TFG/TFM

Este sistema proporciona componentes visuales especializados para diferentes disciplinas académicas de la EPS UA.

## Instalación y Uso

### Carga del paquete

El paquete se carga de forma modular para minimizar el tiempo de compilación:

```latex
% Solo componentes comunes (cajas de información, alertas, etc.)
\usepackage{eps-componentes}

% Componentes específicos (carga también los comunes)
\usepackage[software]{eps-componentes}       % IT/Informática
\usepackage[telecom]{eps-componentes}        % Telecomunicaciones
\usepackage[arquitectura]{eps-componentes}   % Arquitectura/Construcción
\usepackage[quimica]{eps-componentes}        % Química/Materiales
\usepackage[geologia]{eps-componentes}       % Geología
\usepackage[prevencion]{eps-componentes}     % Prevención de riesgos

% Múltiples módulos
\usepackage[software,telecom]{eps-componentes}

% Todos los componentes
\usepackage[all]{eps-componentes}
```

---

## Componentes Comunes (`eps-comunes.sty`)

Se cargan siempre automáticamente.

### Cajas de información

<!-- preview:start -->
```latex
\begin{infobox}
  Información general o nota importante.
\end{infobox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{warningbox}
  Advertencia que requiere atención.
\end{warningbox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{dangerbox}
  Peligro o error crítico.
\end{dangerbox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{successbox}
  Operación exitosa o buena práctica.
\end{successbox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{tipbox}
  Consejo o sugerencia útil.
\end{tipbox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{notebox}
  Nota o comentario secundario.
\end{notebox}
```
<!-- preview:end -->

### Cajas con título

<!-- preview:start -->
```latex
\begin{titlebox}{Mi Título}
  Contenido de la caja con título personalizado.
\end{titlebox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{definitionbox}{Algoritmo}
  Conjunto ordenado y finito de operaciones que permite hallar la solución de un problema.
\end{definitionbox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{examplebox}[Ejemplo de uso]
  Contenido del ejemplo práctico.
\end{examplebox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{importantbox}
  Este contenido es especialmente importante.
\end{importantbox}
```
<!-- preview:end -->

### Listas especiales

<!-- preview:start -->
```latex
\begin{checklist}
  \item[\checked] Tarea completada
  \item[\partialchecked] Tarea parcialmente completada
  \item[\unchecked] Tarea pendiente
\end{checklist}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{proscons}
  \pro Ventaja del sistema
  \pro Otra ventaja importante
  \con Desventaja menor
  \con Otra desventaja
\end{proscons}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{steplist}
  \step Primer paso del proceso
  \step Segundo paso
  \step Tercer y último paso
\end{steplist}
```
<!-- preview:end -->

### Badges e indicadores

<!-- preview:start -->
```latex
\badge{Estable} \quad
\badge[eps-success]{Completado} \quad
\badge[eps-warning]{En revisión} \quad
\badge[eps-danger]{Crítico}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\badgenew \quad \badgewip \quad \badgedeprecated \quad \badgebeta \quad \badgerequired \quad \badgeoptional
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\version{1.0.0} \quad \version{2.1.0} \quad \version{3.0.0-beta}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
Progreso: \progressbar{25} \quad \progressbar{50} \quad \progressbar{75} \quad \progressbar{100}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
Rating: \rating{3}{5} \quad \rating{4}{5} \quad \rating{5}{5}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
Nivel: \levelbar{2}{5} \quad \levelbar{4}{5} \quad \levelbar{5}{5}
```
<!-- preview:end -->

### Tarjetas de información

<!-- preview:start -->
```latex
\personcard{Juan García}{Desarrollador Senior}{Especialista en arquitectura de software con 10 años de experiencia.}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\statcard{1,234}{Usuarios}{\faUsers}{eps-primary}
\statcard{98.5\%}{Uptime}{\faChartLine}{eps-success}
```
<!-- preview:end -->

### Timeline

<!-- preview:start -->
```latex
\begin{timeline}
  \timeitem{Ene 2024}{Inicio del proyecto}
  \timeitem{Mar 2024}{Diseño de arquitectura}
  \timeitem{Jun 2024}{Implementación principal}
  \timeitem{Dic 2024}{Entrega final}
\end{timeline}
```
<!-- preview:end -->

### Comparativas

<!-- preview:start -->
```latex
\begin{comparison}{Opción A}{Opción B}
  \comprow{Rendimiento}{Alto}{Medio}
  \comprow{Facilidad de uso}{Media}{Alta}
  \comprow{Coste}{Bajo}{Medio}
\end{comparison}
```
<!-- preview:end -->

### Citas destacadas

<!-- preview:start -->
```latex
\begin{quotebox}[Albert Einstein]
  La imaginación es más importante que el conocimiento.
\end{quotebox}
```
<!-- preview:end -->

---

## Componentes de Software (`eps-software.sty`)

Cargar con: `\usepackage[software]{eps-componentes}`

### API REST Endpoints

<!-- preview:start -->
```latex
\begin{apiendpoint}{GET}{/api/users}
  Obtiene la lista de usuarios.
  
  \apiresponse{200}{
    "users": [{"id": 1, "name": "Juan"}],
    "total": 150
  }
  
  \apiresponse{401}{
    "error": "No autorizado"
  }
\end{apiendpoint}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{apiendpoint}{POST}{/api/users}
  Crea un nuevo usuario.
  
  \apibody{application/json}{
    "name": "María",
    "email": "maria@email.com"
  }
  
  \apiresponse{201}{
    "id": 3,
    "message": "Usuario creado"
  }
\end{apiendpoint}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
Métodos HTTP: \httpget \quad \httppost \quad \httpput \quad \httppatch \quad \httpdelete
```
<!-- preview:end -->

### Terminal/Consola

<!-- preview:start -->
```latex
\begin{terminal}[Mi servidor]
  \prompt npm install
  \prompt npm run build
  \promptroot systemctl restart nginx
\end{terminal}
```
<!-- preview:end -->

### Diagramas UML

<!-- preview:start -->
```latex
\begin{umlclass}{Usuario}
  \visibility{-} id: int \\
  \visibility{-} nombre: string \\
  \visibility{+} getNombre(): string \\
  \visibility{+} setNombre(n: string): void
\end{umlclass}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{umlinterface}{IAutenticable}
  \visibility{+} login(user: string, pass: string): boolean \\
  \visibility{+} logout(): void \\
  \visibility{+} isAuthenticated(): boolean
\end{umlinterface}
```
<!-- preview:end -->

### Tablas de requisitos

<!-- preview:start -->
```latex
\begin{requirements}
  \reqrow{RF-001}{El sistema debe permitir registro}{Alta}{\statusdone}
  \reqrow{RF-002}{Los usuarios pueden modificar perfil}{Media}{\statusprogress}
  \reqrow{RF-003}{Implementar cache}{Baja}{\statustodo}
\end{requirements}
```
<!-- preview:end -->

### Esquemas de base de datos

<!-- preview:start -->
```latex
\begin{dbtable}{usuarios}
  \pkicon & id & INT & NOT NULL \\
  & nombre & VARCHAR(100) & NOT NULL \\
  \fkicon & rol\_id & INT & FK $\rightarrow$ roles.id \\
\end{dbtable}
```
<!-- preview:end -->

### Git y control de versiones

<!-- preview:start -->
```latex
\gitcommit{abc1234}{Añadir función de login}
\gitcommit{def5678}{Corregir error de validación}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\gitbranch{main} \quad \gitbranch{develop} \quad \gitbranch{feature/login}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\gittag{v1.0.0} \quad \gittag{v2.0.0} \quad \gittag{v2.1.0-beta}
```
<!-- preview:end -->

### Logs y métricas

<!-- preview:start -->
```latex
\begin{logbox}[Logs del servidor]
  \logentry{INFO}{2024-01-15 10:30:00}{Servidor iniciado}
  \logentry{WARN}{2024-01-15 10:35:22}{Intento de acceso sin autenticación}
  \logentry{ERROR}{2024-01-15 11:02:45}{Timeout en consulta}
\end{logbox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\metricbox{Tiempo de respuesta}{45}{ms}{eps-success}
\metricbox{Uso de CPU}{78}{\%}{eps-warning}
```
<!-- preview:end -->

---

## Componentes de Telecomunicaciones (`eps-telecom.sty`)

Cargar con: `\usepackage[telecom]{eps-componentes}`

### Carta de Smith

<!-- preview:start -->
```latex
\begin{smithchartbox}[Adaptación de impedancias]
  \begin{tikzpicture}[scale=0.8]
    \begin{smithchartenv}
      \smithpoint{0.5}{0.3}{$Z_L$}
      \smithpoint{0}{0}{$Z_0$}
    \end{smithchartenv}
  \end{tikzpicture}
\end{smithchartbox}
```
<!-- preview:end -->

### Diagrama de constelación

<!-- preview:start -->
```latex
\begin{tikzpicture}
  \begin{constellation}
    \qpsk  % Dibuja los 4 puntos de QPSK
  \end{constellation}
\end{tikzpicture}
```
<!-- preview:end -->

### Máquinas de estados finitos

<!-- preview:start -->
```latex
\begin{tikzpicture}[node distance=2.5cm]
  \node[fsmstate, initial] (s0) {$S_0$};
  \node[fsmstate, right of=s0] (s1) {$S_1$};
  \node[fsmstate, accepting, right of=s1] (s2) {$S_2$};
  
  \path[fsmtransition]
    (s0) edge[bend left] node[above] {a/0} (s1)
    (s1) edge[bend left] node[below] {b/1} (s0)
    (s1) edge node[above] {a/1} (s2);
\end{tikzpicture}
```
<!-- preview:end -->

### Tramas de protocolo

<!-- preview:start -->
```latex
\begin{protocolframe}[Trama Ethernet]
  \framefield{6}{Destino}
  \framefield{6}{Origen}
  \framefield{2}{Tipo}
  \framefield{46-1500}{Datos}
  \framefield{4}{FCS}
\end{protocolframe}
```
<!-- preview:end -->

### Parámetros S

<!-- preview:start -->
```latex
\begin{sparameters}
  \sparam{S_{11}}{-15.2}{dB}{Pérdidas de retorno}
  \sparam{S_{21}}{-0.3}{dB}{Pérdidas de inserción}
  \sparam{S_{12}}{-45.2}{dB}{Aislamiento inverso}
\end{sparameters}
```
<!-- preview:end -->

### Diagramas de temporización

<!-- preview:start -->
```latex
\begin{tikzpicture}
  \draw (0,2) node[left] {CLK};
  \timingclock{0}{2}{8}
  
  \draw (0,1) node[left] {DATA};
  \timinglow{0}{1}{1}
  \timinghigh{1}{1}{2}
  \timinglow{3}{1}{1}
  \timinghigh{4}{1}{3}
  \timinglow{7}{1}{1}
  
  \draw (0,0) node[left] {EN};
  \timinglow{0}{0}{2}
  \timinghigh{2}{0}{5}
  \timinglow{7}{0}{1}
\end{tikzpicture}
```
<!-- preview:end -->

---

## Componentes de Arquitectura (`eps-arquitectura.sty`)

Cargar con: `\usepackage[arquitectura]{eps-componentes}`

### Diagramas de Gantt

<!-- preview:start -->
```latex
\begin{ganttbox}[Planificación de obra]
  \begin{ganttchart}[gantt eps style]{1}{12}
    \gantttitle{2024}{12} \\
    \gantttitlelist{1,...,12}{1} \\
    \ganttbar{Cimentación}{1}{3} \\
    \ganttbar[bar/.append style={fill=eps-danger}]{Estructura}{3}{6} \\
    \ganttbar{Cerramientos}{5}{9} \\
    \ganttlink{elem0}{elem1}
    \ganttlink{elem1}{elem2}
  \end{ganttchart}
\end{ganttbox}
```
<!-- preview:end -->

### Fichas técnicas de materiales

<!-- preview:start -->
```latex
\begin{techsheet}{Hormigón HA-25}
  \techprop{Resistencia característica}{25 MPa}
  \techprop{Consistencia}{Blanda (6-9 cm)}
  \techprop{Tamaño máximo árido}{20 mm}
  \techprop{Ambiente de exposición}{IIa}
\end{techsheet}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\materialcard{Acero B500S}{
  \techprop{Límite elástico}{500 MPa}
  \techprop{Resistencia tracción}{550 MPa}
}
```
<!-- preview:end -->

### Presupuestos

<!-- preview:start -->
```latex
\begin{presupuesto}
  \partida{1}{Movimiento de tierras}{}{15000.00}
  \partida{1.1}{Excavación en zanjas}{120 m³}{3600.00}
  \partida{1.2}{Transporte a vertedero}{80 m³}{1200.00}
  \partida{2}{Cimentación}{}{45000.00}
  \totalpresupuesto{60000.00}
\end{presupuesto}
```
<!-- preview:end -->

### Normativa

<!-- preview:start -->
```latex
\begin{normativa}
  \norma{CTE DB-SE}{Seguridad estructural}
  \norma{EHE-08}{Instrucción de hormigón estructural}
  \norma{UNE-EN 1992-1-1}{Eurocódigo 2: Estructuras de hormigón}
\end{normativa}
```
<!-- preview:end -->

### Control de calidad

<!-- preview:start -->
```latex
\begin{controlcalidad}
  \controlitem{Hormigón HA-25}{Resistencia compresión}{28,5 MPa}{$\geq$ 25 MPa}{eps-success}
  \controlitem{Acero B500S}{Límite elástico}{512 MPa}{$\geq$ 500 MPa}{eps-success}
  \controlitem{Compactación}{Densidad relativa}{94\%}{$\geq$ 95\%}{eps-danger}
\end{controlcalidad}
```
<!-- preview:end -->

### Etiquetas energéticas

<!-- preview:start -->
```latex
\etiquetaenergetica{A} \quad
\etiquetaenergetica{B} \quad
\etiquetaenergetica{C} \quad
\etiquetaenergetica{D}
```
<!-- preview:end -->

### Certificaciones

<!-- preview:start -->
```latex
\certiso{9001} \quad \certiso{14001} \quad \certiso{45001} \quad \certce \quad \certune{12345}
```
<!-- preview:end -->

---

## Componentes de Química (`eps-quimica.sty`)

Cargar con: `\usepackage[quimica]{eps-componentes}`

### Reacciones químicas

<!-- preview:start -->
```latex
\begin{reactionbox}[Combustión del metano]
  \ch{CH4 + 2 O2 -> CO2 + 2 H2O}
  
  \reactionconditions{T = 800°C, catalizador Pt}
\end{reactionbox}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{mechanismbox}[Sustitución nucleofílica SN2]
  El mecanismo SN2 ocurre en un solo paso concertado.
  
  \ch{HO^- + CH3Br -> CH3OH + Br^-}
\end{mechanismbox}
```
<!-- preview:end -->

### Ficha de compuesto

<!-- preview:start -->
```latex
\begin{compoundsheet}{Ácido sulfúrico}
  \compprop{Fórmula}{\ch{H2SO4}}
  \compprop{Masa molar}{98.079 g/mol}
  \compprop{Densidad}{1.84 g/cm³}
  \compprop{Punto de fusión}{10°C}
\end{compoundsheet}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\compoundcard{Etanol}{\ch{C2H5OH}}{46.07 g/mol}
\compoundcard{Glucosa}{\ch{C6H12O6}}{180.16 g/mol}
```
<!-- preview:end -->

### Protocolos de laboratorio

<!-- preview:start -->
```latex
\begin{protocol}[Titulación ácido-base]
  \protocolstep{Preparar bureta con \ch{NaOH} 0.1 M}
  \protocolstep{Añadir 25 mL de muestra al erlenmeyer}
  \protocolstep{Agregar 3 gotas de fenolftaleína}
  \protocolwarning{Evitar salpicaduras de ácido}
  \protocolstep{Valorar hasta viraje de color}
\end{protocol}
```
<!-- preview:end -->

### Resultados analíticos

<!-- preview:start -->
```latex
\begin{analyticalresults}
  \analyte{Plomo (Pb)}{0.015}{mg/L}{< 0.010}{eps-danger}
  \analyte{Cobre (Cu)}{0.8}{mg/L}{< 2.0}{eps-success}
  \analyte{Zinc (Zn)}{2.3}{mg/L}{< 3.0}{eps-warning}
\end{analyticalresults}
```
<!-- preview:end -->

### Equipamiento

<!-- preview:start -->
```latex
\begin{equipmentlist}
  \item Espectrofotómetro UV-Vis
  \item pH-metro digital
  \item Balanza analítica (0.0001 g)
\end{equipmentlist}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\begin{reagentlist}
  \reagent{\ch{NaOH}}{0.1 M}{500 mL}
  \reagent{\ch{HCl}}{0.1 M}{250 mL}
  \reagent{Fenolftaleína}{1\%}{100 mL}
\end{reagentlist}
```
<!-- preview:end -->

---

## Componentes de Geología (`eps-geologia.sty`)

Cargar con: `\usepackage[geologia]{eps-componentes}`

### Columna estratigráfica

<!-- preview:start -->
```latex
\begin{stratigraphybox}[Sección A-A']
  \begin{tikzpicture}
    \begin{stratcolumn}
      \stratlayer{0}{1.5}{lito arenisca}{Arenisca calcárea}
      \stratlayer{1.5}{3}{lito arcilla}{Arcillas margosas}
      \stratlayer{3}{5}{lito caliza}{Caliza masiva}
    \end{stratcolumn}
  \end{tikzpicture}
\end{stratigraphybox}
```
<!-- preview:end -->

### Tabla de minerales

<!-- preview:start -->
```latex
\begin{mineraltable}
  \mineralrow{Cuarzo}{\ch{SiO2}}{7}{2.65}
  \mineralrow{Calcita}{\ch{CaCO3}}{3}{2.71}
  \mineralrow{Feldespato}{\ch{KAlSi3O8}}{6}{2.56}
\end{mineraltable}
```
<!-- preview:end -->

<!-- preview:start -->
```latex
\mineralcard{Pirita}{\ch{FeS2}}{6}{5.02}
\mineralcard{Galena}{\ch{PbS}}{2.5}{7.58}
```
<!-- preview:end -->

### Datos geotécnicos

<!-- preview:start -->
```latex
\begin{geotechdata}
  \geotechtest{Límite líquido}{LL}{45}{\%}
  \geotechtest{Índice de plasticidad}{IP}{22}{\%}
  \sptvalue{15}
  \cohesion{25}{kPa}
\end{geotechdata}
```
<!-- preview:end -->

### Clasificación de suelos

<!-- preview:start -->
```latex
El suelo se clasifica como \uscsclass{CL} según USCS.
La calidad del macizo es \rmrclass{III}{Regular}.
```
<!-- preview:end -->

### Eras geológicas

<!-- preview:start -->
```latex
\geoera{Cuaternario} \quad
\geoera{Neógeno} \quad
\geoera{Cretácico} \quad
\geoera{Jurásico}
```
<!-- preview:end -->

### Riesgos geológicos

<!-- preview:start -->
```latex
\georisk[4]{Deslizamientos activos en ladera norte}
\georisk[2]{Riesgo moderado de subsidencia}

\risklandslide \quad \riskflood \quad \riskseismic
```
<!-- preview:end -->

---

## Componentes de Prevención (`eps-prevencion.sty`)

Cargar con: `\usepackage[prevencion]{eps-componentes}`

### Matriz de riesgos

<!-- preview:start -->
```latex
\begin{riskmatrixbox}
  \riskmatrix
\end{riskmatrixbox}
```
<!-- preview:end -->

### Evaluación de riesgos

<!-- preview:start -->
```latex
\begin{riskassessment}
  \riskentry{R-001}{Caída a distinto nivel}{3}{4}{}{Instalación de barandillas}
  \riskentry{R-002}{Contacto eléctrico}{2}{5}{}{Revisión de instalaciones}
\end{riskassessment}
```
<!-- preview:end -->

### Checklist de seguridad

<!-- preview:start -->
```latex
\begin{safetychecklist}
  \checkitem{EPIs disponibles}
  \checkitem{Zona señalizada}
  \uncheckitem{Revisión de andamios}
  \naitem{Trabajos en altura}
\end{safetychecklist}
```
<!-- preview:end -->

### Señalización

<!-- preview:start -->
```latex
\signwarning{Riesgo de caída}
\signprohibition{Prohibido fumar}
\signmandatory{Uso obligatorio de casco}
\signemergency{Salida de emergencia}
\signfire{Extintor}
```
<!-- preview:end -->

### Equipos de protección individual

<!-- preview:start -->
```latex
\begin{epilist}
  \item \epihardhat
  \item \epigloves
  \item \epigoggles
  \item \epiboots
  \item \epimask
  \item \epiearprotection
\end{epilist}
```
<!-- preview:end -->

### Indicadores de seguridad

<!-- preview:start -->
```latex
\indicatorIF{15.2}      % Índice de Frecuencia
\indicatorIG{0.45}      % Índice de Gravedad
\indicatorDaysSafe{127} % Días sin accidentes
```
<!-- preview:end -->

### Procedimiento de emergencia

<!-- preview:start -->
```latex
\begin{emergencyprocedure}[En caso de accidente]
  \begin{steplist}
    \step Proteger: Asegurar la zona
    \step Avisar: Llamar al 112
    \step Socorrer: Aplicar primeros auxilios
  \end{steplist}
  
  \emergencyphone{Emergencias}{112}
  \emergencyphone{Mutua}{900 123 456}
\end{emergencyprocedure}
```
<!-- preview:end -->

### Registro de formación

<!-- preview:start -->
```latex
\begin{trainingrecord}
  \trainingentry{PRL Básico (60h)}{60}{01/2024}{01/2029}{vigente}
  \trainingentry{Trabajos en altura}{8}{03/2024}{03/2025}{vigente}
  \trainingentry{Riesgo eléctrico}{20}{01/2022}{01/2024}{caducado}
\end{trainingrecord}
```
<!-- preview:end -->

### Informe de accidente

<!-- preview:start -->
```latex
\begin{accidentreport}[Informe de accidente]
  \reportfield{Fecha}{15 de enero de 2024}
  \reportfield{Lugar}{Zona de carga, nave 3}
  \reportfield{Trabajador}{Juan García}
  \reportfield{Tipo de lesión}{Contusión en pie}
  \reportfield{Gravedad}{\accidenttype{leve}}
\end{accidentreport}
```
<!-- preview:end -->

---

## Paleta de colores

Todos los componentes usan una paleta unificada:

| Color | Código | Uso |
|-------|--------|-----|
| `eps-primary` | #2563EB | Azul principal |
| `eps-secondary` | #7C3AED | Violeta |
| `eps-success` | #059669 | Verde éxito |
| `eps-warning` | #D97706 | Naranja advertencia |
| `eps-danger` | #DC2626 | Rojo peligro |
| `eps-info` | #0284C7 | Azul información |
| `eps-dark` | #1F2937 | Texto oscuro |
| `eps-gray` | #6B7280 | Gris medio |
| `eps-light` | #F3F4F6 | Fondos claros |

---

## Ejemplos completos

Ver el capítulo de componentes en el documento principal (`contenido/capitulos/componentes.tex`) para ejemplos detallados de todos los componentes renderizados.
