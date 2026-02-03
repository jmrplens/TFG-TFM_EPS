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

```latex
\begin{infobox}
  Información general o nota importante.
\end{infobox}

\begin{warningbox}
  Advertencia que requiere atención.
\end{warningbox}

\begin{dangerbox}
  Peligro o error crítico.
\end{dangerbox}

\begin{successbox}
  Operación exitosa o buena práctica.
\end{successbox}

\begin{tipbox}
  Consejo o sugerencia útil.
\end{tipbox}
```

### Cajas con título

```latex
\begin{titlebox}{Mi Título}
  Contenido de la caja.
\end{titlebox}

\begin{definitionbox}{Término}
  Definición del término.
\end{definitionbox}

\begin{examplebox}{Ejemplo 1}
  Contenido del ejemplo.
\end{examplebox}
```

### Listas especiales

```latex
\begin{checklist}
  \checkmark Tarea completada
  \checkmark Otra tarea
  \item Tarea pendiente
\end{checklist}

\begin{proscons}
  \pro Ventaja del sistema
  \con Desventaja menor
\end{proscons}

\begin{steplist}
  \step Primer paso
  \step Segundo paso
  \step Tercer paso
\end{steplist}
```

### Badges e indicadores

```latex
\badge{Estable}
\badge[eps-success]{Completado}
\badgenew
\badgewip
\version{2.1.0}

\progressbar{75}
\rating{4}
\levelbar[Experiencia]{3}
```

### Timeline

```latex
\begin{timeline}
  \timeitem{2024-01}{Inicio del proyecto}
  \timeitem{2024-03}{Hito importante}
  \timeitem{2024-06}{Finalización}
\end{timeline}
```

---

## Componentes de Software (`eps-software.sty`)

Cargar con: `\usepackage[software]{eps-componentes}`

### API REST Endpoints

```latex
\begin{apiendpoint}{GET}{/api/users}
  Obtiene la lista de usuarios.
  
  \apiresponse{200}
  {
    "users": [...]
  }
  
  \apiresponse{401}
  {
    "error": "No autorizado"
  }
\end{apiendpoint}
```

Métodos HTTP disponibles: `\httpget`, `\httppost`, `\httpput`, `\httppatch`, `\httpdelete`

### Terminal/Consola

```latex
\begin{terminal}[Mi servidor]
  \prompt npm install
  \prompt npm run build
  \promptroot systemctl restart nginx
\end{terminal}
```

### Diagramas UML

```latex
\begin{umlclass}{Usuario}
  \visibility{-} id: int \\
  \visibility{-} nombre: string \\
  \visibility{+} getNombre(): string \\
  \visibility{+} setNombre(n: string): void
\end{umlclass}
```

### Tablas de requisitos

```latex
\begin{requirements}
  \reqrow{RF-001}{El sistema debe...}{Alta}{\statusdone}
  \reqrow{RF-002}{El usuario puede...}{Media}{\statusprogress}
  \reqrow{RF-003}{Implementar cache}{Baja}{\statustodo}
\end{requirements}
```

### Esquemas de base de datos

```latex
\begin{dbtable}{usuarios}
  \pkicon & id & INT & NOT NULL \\
  & nombre & VARCHAR(100) & NOT NULL \\
  \fkicon & rol\_id & INT & FK $\rightarrow$ roles.id \\
\end{dbtable}
```

### Git

```latex
\gitcommit{abc1234}{Añadir función de login}
\gitbranch{feature/login}
\gittag{v2.0.0}
```

---

## Componentes de Telecomunicaciones (`eps-telecom.sty`)

Cargar con: `\usepackage[telecom]{eps-componentes}`

### Carta de Smith

```latex
\begin{smithchartbox}[Adaptación de impedancias]
  \begin{tikzpicture}
    \begin{smithchartenv}
      \smithpoint{0.5}{0.3}{$Z_L$}
    \end{smithchartenv}
  \end{tikzpicture}
\end{smithchartbox}
```

### Diagrama de constelación

```latex
\begin{tikzpicture}
  \begin{constellation}
    \qpsk  % Dibuja los 4 puntos de QPSK
  \end{constellation}
\end{tikzpicture}
```

### Máquinas de estados finitos

```latex
\begin{tikzpicture}
  \node[fsmstate, initial] (s0) {$S_0$};
  \node[fsmstate, right=of s0] (s1) {$S_1$};
  \node[fsmstate, accepting, right=of s1] (s2) {$S_2$};
  
  \path[fsmtransition]
    (s0) edge node {0} (s1)
    (s1) edge node {1} (s2);
\end{tikzpicture}
```

### Tramas de protocolo

```latex
\begin{protocolframe}[Trama Ethernet]
  \framefield{6}{Destino}
  \framefield{6}{Origen}
  \framefield{2}{Tipo}
  \framefield{46-1500}{Datos}
  \framefield{4}{FCS}
\end{protocolframe}
```

### Parámetros S

```latex
\begin{sparameters}
  \sparam{S_{11}}{-15.2}{dB}{Pérdidas de retorno}
  \sparam{S_{21}}{-0.3}{dB}{Pérdidas de inserción}
\end{sparameters}
```

---

## Componentes de Arquitectura (`eps-arquitectura.sty`)

Cargar con: `\usepackage[arquitectura]{eps-componentes}`

### Diagramas de Gantt

```latex
\begin{ganttbox}[Planificación de obra]
  \begin{ganttchart}[gantt eps style]{1}{12}
    \gantttitle{2024}{12} \\
    \gantttitlelist{1,...,12}{1} \\
    \ganttbar{Cimentación}{1}{3} \\
    \ganttbar[bar/.append style={fill=eps-danger}]{Estructura}{3}{6} \\
    \ganttlink{elem0}{elem1}
  \end{ganttchart}
\end{ganttbox}
```

### Fichas técnicas de materiales

```latex
\begin{techsheet}{Hormigón HA-25}
  \techprop{Resistencia característica}{25 MPa}
  \techprop{Consistencia}{Blanda (6-9 cm)}
  \techprop{Tamaño máximo árido}{20 mm}
\end{techsheet}
```

### Presupuestos

```latex
\begin{presupuesto}
  \partida{1}{Movimiento de tierras}{}{15000.00}
  \partida{1.1}{Excavación en zanjas}{120 m³}{3600.00}
  \partida{1.2}{Transporte a vertedero}{80 m³}{1200.00}
  \partida{2}{Cimentación}{}{45000.00}
  \totalpresupuesto{60000.00}
\end{presupuesto}
```

### Normativa

```latex
\begin{normativa}
  \norma{CTE DB-SE}{Seguridad estructural}
  \norma{EHE-08}{Instrucción de hormigón estructural}
  \norma{UNE-EN 1992-1-1}{Eurocódigo 2: Estructuras de hormigón}
\end{normativa}
```

### Etiquetas energéticas

```latex
\etiquetaenergetica{A}
\etiquetaenergetica{B}
\etiquetaenergetica{G}
```

---

## Componentes de Química (`eps-quimica.sty`)

Cargar con: `\usepackage[quimica]{eps-componentes}`

### Reacciones químicas

```latex
\begin{reactionbox}[Combustión del metano]
  \ch{CH4 + 2 O2 -> CO2 + 2 H2O}
  
  \reactionconditions{T = 800°C, catalizador Pt}
\end{reactionbox}
```

### Ficha de compuesto

```latex
\begin{compoundsheet}{Ácido sulfúrico}
  \compprop{Fórmula}{\ch{H2SO4}}
  \compprop{Masa molar}{98.079 g/mol}
  \compprop{Densidad}{1.84 g/cm³}
  \compprop{Punto de fusión}{10°C}
\end{compoundsheet}
```

### Protocolos de laboratorio

```latex
\begin{protocol}[Titulación ácido-base]
  \protocolstep{Preparar bureta con \ch{NaOH} 0.1 M}
  \protocolstep{Añadir 25 mL de muestra al erlenmeyer}
  \protocolstep{Agregar 3 gotas de fenolftaleína}
  \protocolwarning{Evitar salpicaduras de ácido}
\end{protocol}
```

### Resultados analíticos

```latex
\begin{analyticalresults}
  \analyte{Plomo (Pb)}{0.015}{mg/L}{< 0.010}{eps-danger}
  \analyte{Cobre (Cu)}{0.8}{mg/L}{< 2.0}{eps-success}
\end{analyticalresults}
```

---

## Componentes de Geología (`eps-geologia.sty`)

Cargar con: `\usepackage[geologia]{eps-componentes}`

### Columna estratigráfica

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

### Tabla de minerales

```latex
\begin{mineraltable}
  \mineralrow{Cuarzo}{\ch{SiO2}}{7}{2.65}
  \mineralrow{Calcita}{\ch{CaCO3}}{3}{2.71}
  \mineralrow{Feldespato}{\ch{KAlSi3O8}}{6}{2.56}
\end{mineraltable}
```

### Datos geotécnicos

```latex
\begin{geotechdata}
  \geotechtest{Límite líquido}{LL}{45}{\%}
  \geotechtest{Índice de plasticidad}{IP}{22}{\%}
  \sptvalue{15}
  \cohesion{25}{kPa}
\end{geotechdata}
```

### Clasificación de suelos

```latex
El suelo se clasifica como \uscsclass{CL} según USCS.
La calidad del macizo es \rmrclass{III}{Regular}.
```

---

## Componentes de Prevención (`eps-prevencion.sty`)

Cargar con: `\usepackage[prevencion]{eps-componentes}`

### Matriz de riesgos

```latex
\begin{riskmatrixbox}
  \riskmatrix
\end{riskmatrixbox}
```

### Evaluación de riesgos

```latex
\begin{riskassessment}
  \riskentry{R-001}{Caída a distinto nivel}{3}{4}{}{Instalación de barandillas}
  \riskentry{R-002}{Contacto eléctrico}{2}{5}{}{Revisión de instalaciones}
\end{riskassessment}
```

### Checklist de seguridad

```latex
\begin{safetychecklist}
  \checkitem{EPIs disponibles}
  \checkitem{Zona señalizada}
  \uncheckitem{Revisión de andamios}
  \naitem{Trabajos en altura}
\end{safetychecklist}
```

### Señalización

```latex
\signwarning{Riesgo de caída}
\signprohibition{Prohibido fumar}
\signmandatory{Uso obligatorio de casco}
\signemergency{Salida de emergencia}
\signfire{Extintor}
```

### EPIs

```latex
\begin{epilist}
  \item \epihardhat
  \item \epigloves
  \item \epigoggles
  \item \epiboots
\end{epilist}
```

### Indicadores de seguridad

```latex
\indicatorIF{15.2}      % Índice de Frecuencia
\indicatorIG{0.45}      % Índice de Gravedad
\indicatorDaysSafe{127} % Días sin accidentes
```

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

Ver el archivo `docs/ejemplos/componentes-demo.tex` para ejemplos detallados de todos los componentes.
