%% eps-tfg.cls
%% Clase LaTeX para TFG/TFM de la Escuela Politécnica Superior
%% Universidad de Alicante
%%
%% Versión 2.0 - Febrero 2026
%% Modernización completa con expl3, biblatex, LuaLaTeX
%%
%% Autor original: José Manuel Requena Plens
%% Modernización: GitHub Copilot
%%
\NeedsTeXFormat{LaTeX2e}[2022/06/01]
\ProvidesClass{eps-tfg}[2026/02/02 v2.0 Clase TFG/TFM EPS Universidad de Alicante]

%% ============================================================================
%% CONFIGURACIÓN EXPL3
%% ============================================================================
\RequirePackage{expl3}
\RequirePackage{xparse}
\RequirePackage{l3keys2e}

\ExplSyntaxOn

%% ============================================================================
%% VARIABLES INTERNAS
%% ============================================================================

% Información del documento
\tl_new:N \g__eps_titulo_tl
\tl_new:N \g__eps_subtitulo_tl
\tl_new:N \g__eps_autor_tl
\tl_new:N \g__eps_autor_genero_tl
\tl_new:N \g__eps_autor_email_tl
\tl_new:N \g__eps_tutor_tl
\tl_new:N \g__eps_tutor_dpto_tl
\tl_new:N \g__eps_cotutor_tl
\tl_new:N \g__eps_cotutor_dpto_tl
\tl_new:N \g__eps_fecha_tl
\tl_new:N \g__eps_facultad_tl
\tl_new:N \g__eps_facultad_corto_tl
\tl_new:N \g__eps_universidad_tl
\tl_new:N \g__eps_ubicacion_tl

% Configuración de titulación
\tl_new:N \g__eps_titulacion_tl
\tl_new:N \g__eps_titulacion_nombre_tl
\tl_new:N \g__eps_tipo_trabajo_tl
\tl_new:N \g__eps_color_grado_tl
\tl_new:N \g__eps_color_texto_tl

% Rutas de logos
\tl_new:N \g__eps_logo_facultad_tl
\tl_new:N \g__eps_logo_facultad_portada_tl
\tl_new:N \g__eps_logo_universidad_tl
\tl_new:N \g__eps_logo_universidad_portada_tl
\tl_new:N \g__eps_logo_grado_tl
\tl_new:N \g__eps_logo_grado_portada_tl

% Opciones booleanas
\bool_new:N \g__eps_optimizar_tikz_bool
\bool_new:N \g__eps_borrador_bool

% Establecer valores por defecto
\tl_gset:Nn \g__eps_facultad_tl {Escuela~Politécnica~Superior}
\tl_gset:Nn \g__eps_facultad_corto_tl {EPS~UA}
\tl_gset:Nn \g__eps_universidad_tl {Universidad~de~Alicante}
\tl_gset:Nn \g__eps_ubicacion_tl {Alicante}
\tl_gset:Nn \g__eps_autor_genero_tl {m}
\bool_gset_true:N \g__eps_optimizar_tikz_bool

%% ============================================================================
%% BASE DE DATOS DE TITULACIONES
%% ============================================================================

% Property list para almacenar datos de titulaciones
\prop_new:N \g__eps_titulaciones_prop

% Comando para definir una titulación
\cs_new_protected:Nn \__eps_define_titulacion:nnnnnnn
  {
    % #1 = id
    % #2 = nombre completo
    % #3 = tipo (tfg/tfm)
    % #4 = color grado
    % #5 = color texto (blanco/negro)
    % #6 = logo variante portada (Blanco/Negro/Color)
    % #7 = logo variante normal (normalmente Negro)
    \prop_gput:Nnn \g__eps_titulaciones_prop { #1 / nombre } { #2 }
    \prop_gput:Nnn \g__eps_titulaciones_prop { #1 / tipo } { #3 }
    \prop_gput:Nnn \g__eps_titulaciones_prop { #1 / color } { #4 }
    \prop_gput:Nnn \g__eps_titulaciones_prop { #1 / texto } { #5 }
    \prop_gput:Nnn \g__eps_titulaciones_prop { #1 / logo-portada } { #6 }
    \prop_gput:Nnn \g__eps_titulaciones_prop { #1 / logo-normal } { #7 }
  }

%% --- GRADOS ---
\__eps_define_titulacion:nnnnnnn {teleco}
  {Grado~en~Ingeniería~en~Sonido~e~Imagen~en~Telecomunicación}
  {tfg} {teleco} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {civil}
  {Grado~en~Ingeniería~Civil}
  {tfg} {civil} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {quimica}
  {Grado~en~Ingeniería~Química}
  {tfg} {quimica} {negro} {Negro} {Negro}

\__eps_define_titulacion:nnnnnnn {informatica}
  {Grado~en~Ingeniería~Informática}
  {tfg} {informatica} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {multimedia}
  {Grado~en~Ingeniería~Multimedia}
  {tfg} {multimedia} {negro} {Negro} {Negro}

\__eps_define_titulacion:nnnnnnn {arquitectura-tecnica}
  {Grado~en~Arquitectura~Técnica}
  {tfg} {arquitecnica} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {arquitectura}
  {Grado~en~Arquitectura}
  {tfg} {arquitectura} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {robotica}
  {Grado~en~Ingeniería~Robótica}
  {tfg} {robotica} {negro} {Color} {Negro}

%% --- MÁSTERES ---
\__eps_define_titulacion:nnnnnnn {master-teleco}
  {Máster~Universitario~en~Ingeniería~de~Telecomunicación}
  {tfm} {masterteleco} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-caminos}
  {Máster~Universitario~en~Ingeniería~de~Caminos,~Canales~y~Puertos}
  {tfm} {caminos} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-edificacion}
  {Máster~Universitario~en~Gestión~de~la~Edificación}
  {tfm} {gestedif} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-web}
  {Máster~Universitario~en~Desarrollo~de~Aplicaciones~y~Servicios~Web}
  {tfm} {desweb} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-materiales}
  {Máster~Universitario~en~Ingeniería~de~los~Materiales,~del~Agua~y~del~Terreno}
  {tfm} {mataguaterre} {negro} {Negro} {Negro}

\__eps_define_titulacion:nnnnnnn {master-informatica}
  {Máster~Universitario~en~Ingeniería~Informática}
  {tfm} {masterinfor} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-robotica}
  {Máster~Universitario~en~Automática~y~Robótica}
  {tfm} {autorobo} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-prevencion}
  {Máster~Universitario~en~Prevención~de~Riesgos~Laborales}
  {tfm} {prevencion} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-agua}
  {Máster~Universitario~en~Gestión~Sostenible~y~Tecnologías~del~Agua}
  {tfm} {gestionagua} {negro} {Negro} {Negro}

\__eps_define_titulacion:nnnnnnn {master-moviles}
  {Máster~Universitario~en~Desarrollo~de~Software~para~Dispositivos~Móviles}
  {tfm} {moviles} {blanco} {Blanco} {Negro}

\__eps_define_titulacion:nnnnnnn {master-quimica}
  {Máster~Universitario~en~Ingeniería~Química}
  {tfm} {masterquimica} {negro} {Negro} {Negro}

\__eps_define_titulacion:nnnnnnn {master-ciberseguridad}
  {Máster~Universitario~en~Ciberseguridad}
  {tfm} {ciberseguridad} {blanco} {Color} {Negro}

\__eps_define_titulacion:nnnnnnn {master-geologica}
  {Máster~Universitario~en~Ingeniería~Geológica}
  {tfm} {geologica} {blanco} {Color} {Negro}

%% ============================================================================
%% MAPEO DE LOGOS POR TITULACIÓN
%% ============================================================================
\prop_new:N \g__eps_logos_map_prop

% Grados
\prop_gput:Nnn \g__eps_logos_map_prop {teleco} {LogoTeleco}
\prop_gput:Nnn \g__eps_logos_map_prop {civil} {LogoCivil}
\prop_gput:Nnn \g__eps_logos_map_prop {quimica} {LogoQuimica}
\prop_gput:Nnn \g__eps_logos_map_prop {informatica} {LogoInformatica}
\prop_gput:Nnn \g__eps_logos_map_prop {multimedia} {LogoMultimedia}
\prop_gput:Nnn \g__eps_logos_map_prop {arquitectura-tecnica} {LogoArqTecnica}
\prop_gput:Nnn \g__eps_logos_map_prop {arquitectura} {LogoArquitectura}
\prop_gput:Nnn \g__eps_logos_map_prop {robotica} {LogoRobotica}

% Másteres
\prop_gput:Nnn \g__eps_logos_map_prop {master-teleco} {LogoTeleco}
\prop_gput:Nnn \g__eps_logos_map_prop {master-caminos} {LogoCivil}
\prop_gput:Nnn \g__eps_logos_map_prop {master-edificacion} {LogoMasterEdificacion}
\prop_gput:Nnn \g__eps_logos_map_prop {master-web} {LogoMasterDesarrollo}
\prop_gput:Nnn \g__eps_logos_map_prop {master-materiales} {LogoMasterMateriales}
\prop_gput:Nnn \g__eps_logos_map_prop {master-informatica} {LogoInformatica}
\prop_gput:Nnn \g__eps_logos_map_prop {master-robotica} {LogoMasterRobotica}
\prop_gput:Nnn \g__eps_logos_map_prop {master-prevencion} {LogoMasterPrevencion}
\prop_gput:Nnn \g__eps_logos_map_prop {master-agua} {LogoMasterAgua}
\prop_gput:Nnn \g__eps_logos_map_prop {master-moviles} {LogoMasterMoviles}
\prop_gput:Nnn \g__eps_logos_map_prop {master-quimica} {LogoQuimica}
\prop_gput:Nnn \g__eps_logos_map_prop {master-ciberseguridad} {LogoMasterCiberseguridad}
\prop_gput:Nnn \g__eps_logos_map_prop {master-geologica} {LogoMasterGeologica}

%% ============================================================================
%% FUNCIÓN PARA CONFIGURAR TITULACIÓN
%% ============================================================================
\cs_new_protected:Nn \__eps_setup_titulacion:n
  {
    \tl_gset:Nn \g__eps_titulacion_tl { #1 }
    
    % Obtener datos de la prop list
    \prop_get:NnNTF \g__eps_titulaciones_prop { #1 / nombre } \l_tmpa_tl
      {
        \tl_gset_eq:NN \g__eps_titulacion_nombre_tl \l_tmpa_tl
      }
      {
        \msg_error:nnn { eps-tfg } { titulacion-desconocida } { #1 }
      }
    
    \prop_get:NnN \g__eps_titulaciones_prop { #1 / tipo } \l_tmpa_tl
    \str_case:VnF \l_tmpa_tl
      {
        {tfg} { \tl_gset:Nn \g__eps_tipo_trabajo_tl {Trabajo~Fin~de~Grado} }
        {tfm} { \tl_gset:Nn \g__eps_tipo_trabajo_tl {Trabajo~Fin~de~Máster} }
      }
      {
        \tl_gset:Nn \g__eps_tipo_trabajo_tl {Trabajo~Fin~de~Estudios}
      }
    
    \prop_get:NnN \g__eps_titulaciones_prop { #1 / color } \l_tmpa_tl
    \tl_gset_eq:NN \g__eps_color_grado_tl \l_tmpa_tl
    
    \prop_get:NnN \g__eps_titulaciones_prop { #1 / texto } \l_tmpa_tl
    \tl_gset_eq:NN \g__eps_color_texto_tl \l_tmpa_tl
    
    % Configurar logos
    \prop_get:NnN \g__eps_logos_map_prop { #1 } \l_tmpb_tl
    \prop_get:NnN \g__eps_titulaciones_prop { #1 / logo-portada } \l_tmpa_tl
    \tl_gset:Nx \g__eps_logo_grado_portada_tl 
      { recursos/logos/titulaciones/ \l_tmpb_tl \l_tmpa_tl .pdf }
    
    \prop_get:NnN \g__eps_titulaciones_prop { #1 / logo-normal } \l_tmpa_tl
    \tl_gset:Nx \g__eps_logo_grado_tl 
      { recursos/logos/titulaciones/ \l_tmpb_tl \l_tmpa_tl .pdf }
    
    % Logo facultad según color de texto
    \str_case:VnF \g__eps_color_texto_tl
      {
        {blanco} { 
          \tl_gset:Nn \g__eps_logo_facultad_portada_tl {recursos/logos/universidad/LogoEPSBlanco.pdf}
        }
        {negro} { 
          \tl_gset:Nn \g__eps_logo_facultad_portada_tl {recursos/logos/universidad/LogoEPSNegro.pdf}
        }
      }
      {
        \tl_gset:Nn \g__eps_logo_facultad_portada_tl {recursos/logos/universidad/LogoEPSBlanco.pdf}
      }
  }

%% ============================================================================
%% MENSAJES DE ERROR
%% ============================================================================
\msg_new:nnn { eps-tfg } { titulacion-desconocida }
  { 
    La~titulación~'#1'~no~está~definida.~
    Consulta~la~documentación~para~ver~las~titulaciones~disponibles.
  }

\msg_new:nnn { eps-tfg } { campo-requerido }
  {
    El~campo~'#1'~es~obligatorio.~
    Usa~\token_to_str:N \EPSsetup \{#1~=~...\}~para~definirlo.
  }

%% ============================================================================
%% INTERFAZ DE USUARIO: \EPSsetup
%% ============================================================================
\keys_define:nn { eps-tfg }
  {
    % Información del documento
    titulo .tl_gset:N = \g__eps_titulo_tl,
    titulo .value_required:n = true,
    
    subtitulo .tl_gset:N = \g__eps_subtitulo_tl,
    
    autor .tl_gset:N = \g__eps_autor_tl,
    autor .value_required:n = true,
    
    genero .tl_gset:N = \g__eps_autor_genero_tl,
    genero .initial:n = {m},
    
    email .tl_gset:N = \g__eps_autor_email_tl,
    
    tutor .tl_gset:N = \g__eps_tutor_tl,
    tutor .value_required:n = true,
    
    tutor-genero .tl_gset:N = \g__eps_tutor_genero_tl,
    tutor-genero .initial:n = {m},
    
    tutor-departamento .tl_gset:N = \g__eps_tutor_dpto_tl,
    
    cotutor .tl_gset:N = \g__eps_cotutor_tl,
    
    cotutor-genero .tl_gset:N = \g__eps_cotutor_genero_tl,
    cotutor-genero .initial:n = {m},
    
    cotutor-departamento .tl_gset:N = \g__eps_cotutor_dpto_tl,
    
    fecha .tl_gset:N = \g__eps_fecha_tl,
    
    % Configuración institucional
    facultad .tl_gset:N = \g__eps_facultad_tl,
    facultad .initial:n = {Escuela~Politécnica~Superior},
    
    universidad .tl_gset:N = \g__eps_universidad_tl,
    universidad .initial:n = {Universidad~de~Alicante},
    
    ubicacion .tl_gset:N = \g__eps_ubicacion_tl,
    ubicacion .initial:n = {Alicante},
    
    % Titulación
    titulacion .code:n = { \__eps_setup_titulacion:n { #1 } },
    titulacion .value_required:n = true,
    
    % Opciones
    optimizar-tikz .bool_gset:N = \g__eps_optimizar_tikz_bool,
    optimizar-tikz .default:n = true,
    optimizar-tikz .initial:n = true,
    
    borrador .bool_gset:N = \g__eps_borrador_bool,
    borrador .default:n = true,
    borrador .initial:n = false,
  }

% +m permite párrafos (líneas en blanco) dentro del argumento
% Limpiamos los \par antes de procesar
\NewDocumentCommand{\EPSsetup}{ +m }
  {
    \tl_set:Nn \l_tmpa_tl { #1 }
    \regex_replace_all:nnN { \c{par} } { } \l_tmpa_tl
    \keys_set:nV { eps-tfg } \l_tmpa_tl
  }

%% ============================================================================
%% COMANDOS DE ACCESO A VARIABLES (para usar en el documento)
%% ============================================================================
% Usamos \tl_use:N para asegurar la expansión correcta
\NewExpandableDocumentCommand{\EPStitulo}{}{\tl_use:N \g__eps_titulo_tl}
\NewExpandableDocumentCommand{\EPSsubtitulo}{}{\tl_use:N \g__eps_subtitulo_tl}
\NewExpandableDocumentCommand{\EPSautor}{}{\tl_use:N \g__eps_autor_tl}
\NewExpandableDocumentCommand{\EPSautorEmail}{}{\tl_use:N \g__eps_autor_email_tl}
\NewExpandableDocumentCommand{\EPStutor}{}{\tl_use:N \g__eps_tutor_tl}
\NewExpandableDocumentCommand{\EPStutorDpto}{}{\tl_use:N \g__eps_tutor_dpto_tl}
\NewExpandableDocumentCommand{\EPScotutor}{}{\tl_use:N \g__eps_cotutor_tl}
\NewExpandableDocumentCommand{\EPScotutorDpto}{}{\tl_use:N \g__eps_cotutor_dpto_tl}
\NewExpandableDocumentCommand{\EPSfacultad}{}{\tl_use:N \g__eps_facultad_tl}
\NewExpandableDocumentCommand{\EPSuniversidad}{}{\tl_use:N \g__eps_universidad_tl}
\NewExpandableDocumentCommand{\EPSubicacion}{}{\tl_use:N \g__eps_ubicacion_tl}
\NewExpandableDocumentCommand{\EPStitulacion}{}{\tl_use:N \g__eps_titulacion_nombre_tl}
\NewExpandableDocumentCommand{\EPStipoTrabajo}{}{\tl_use:N \g__eps_tipo_trabajo_tl}
\NewExpandableDocumentCommand{\EPScolorGrado}{}{\tl_use:N \g__eps_color_grado_tl}
\NewExpandableDocumentCommand{\EPScolorTexto}{}{\tl_use:N \g__eps_color_texto_tl}
\NewExpandableDocumentCommand{\EPSlogoGrado}{}{\tl_use:N \g__eps_logo_grado_tl}
\NewExpandableDocumentCommand{\EPSlogoGradoPortada}{}{\tl_use:N \g__eps_logo_grado_portada_tl}
\NewExpandableDocumentCommand{\EPSlogoFacultadPortada}{}{\tl_use:N \g__eps_logo_facultad_portada_tl}

% Comando para obtener la fecha formateada
\NewDocumentCommand{\EPSfecha}{}
  {
    \tl_if_empty:NTF \g__eps_fecha_tl
      { \__eps_fecha_actual: }
      { \g__eps_fecha_tl }
  }

% Generar fecha actual
\cs_new_protected:Nn \__eps_fecha_actual:
  {
    \int_case:nn { \month }
      {
        {1}  {Enero}
        {2}  {Febrero}
        {3}  {Marzo}
        {4}  {Abril}
        {5}  {Mayo}
        {6}  {Junio}
        {7}  {Julio}
        {8}  {Agosto}
        {9}  {Septiembre}
        {10} {Octubre}
        {11} {Noviembre}
        {12} {Diciembre}
      }
    \c_space_tl
    \int_use:N \year
  }

% Comando para verificar si hay cotutor
\NewDocumentCommand{\EPSsiCotutor}{ m m }
  {
    \tl_if_empty:NTF \g__eps_cotutor_tl { #2 } { #1 }
  }

% Comando para obtener etiqueta de autor según género (m=masculino, f=femenino, n=neutro)
\NewDocumentCommand{\EPSetiquetaAutor}{}
  {
    \str_case:VnF \g__eps_autor_genero_tl
      {
        {f} {Autora}
        {m} {Autor}
        {n} {Autoría}
      }
      {Autoría}
  }

% Comando para obtener etiqueta de tutor según género (m=masculino, f=femenino, n=neutro)
\NewDocumentCommand{\EPSetiquetaTutor}{}
  {
    \tl_if_empty:NTF \g__eps_cotutor_tl
      {% Solo tutor principal
        \str_case:VnF \g__eps_tutor_genero_tl
          {
            {f} {Tutora}
            {m} {Tutor}
            {n} {Tutoría}
          }
          {Tutoría}
      }
      {% Hay cotutor - usar plural
        \str_case:VnF \g__eps_tutor_genero_tl
          {
            {f} {\str_case:VnF \g__eps_cotutor_genero_tl {{f}{Tutoras}}{{m}{Tutores}}{{n}{Tutorías}}{Tutorías}}
            {m} {\str_case:VnF \g__eps_cotutor_genero_tl {{f}{Tutores}}{{m}{Tutores}}{{n}{Tutorías}}{Tutorías}}
            {n} {Tutorías}
          }
          {Tutorías}
      }
  }

\ExplSyntaxOff

%% ============================================================================
%% OPCIONES DE CLASE
%% ============================================================================
\DeclareOption{borrador}{%
  \ExplSyntaxOn
  \bool_gset_true:N \g__eps_borrador_bool
  \ExplSyntaxOff
}

\DeclareOption{final}{%
  \ExplSyntaxOn
  \bool_gset_false:N \g__eps_borrador_bool
  \ExplSyntaxOff
}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrbook}}
\ProcessOptions\relax

%% ============================================================================
%% CLASE BASE
%% ============================================================================
\LoadClass[
  a4paper,
  11pt,
  titlepage,
  twoside=semi,
  headings=normal
]{scrbook}

%% ============================================================================
%% CONFIGURACIÓN KOMA-SCRIPT
%% ============================================================================
\KOMAoption{toc}{bib,chapterentryfill}

%% ============================================================================
%% PAQUETES FUNDAMENTALES
%% ============================================================================

% Previene errores con KOMA-Script
\RequirePackage{scrhack}

% Cabeceras y pies de página
\RequirePackage[automark,headsepline,footsepline]{scrlayer-scrpage}
\clearpairofpagestyles
\ihead{{\color{gray30}\scshape\small\headmark}}
\ohead{\normalfont\pagemark}
\ofoot[\normalfont\pagemark]{}

\renewcommand{\chaptermark}[1]{\markboth{#1}{}}
\renewcommand{\sectionmark}[1]{\markright{\thesection. #1}}
\setkomafont{pagenumber}{}

% Profundidad del índice
\setcounter{tocdepth}{4}
\setcounter{secnumdepth}{4}

%% ============================================================================
%% MÁRGENES Y GEOMETRÍA
%% ============================================================================
\RequirePackage[
  inner   = 3.0cm,
  outer   = 2.5cm,
  top     = 2.5cm,
  bottom  = 2.5cm,
  includeheadfoot,
  marginparwidth = 2cm,  % Necesario para todonotes
]{geometry}

% Interlineado
\renewcommand{\baselinestretch}{1.0}

% Páginas horizontales
\RequirePackage{pdflscape}

%% ============================================================================
%% IDIOMA (POLYGLOSSIA PARA LUALATEX)
%% ============================================================================
\RequirePackage{polyglossia}
\setdefaultlanguage{spanish}
\setotherlanguage{english}

% Redefinir nombres
\gappto\captionsspanish{%
  \renewcommand{\listtablename}{Índice de tablas}
  \renewcommand{\tablename}{Tabla}
  \renewcommand{\glossaryname}{Glosario}
  \renewcommand{\acronymname}{Acrónimos}
  \renewcommand{\bibname}{Bibliografía}
}

%% ============================================================================
%% FUENTES (FONTSPEC PARA LUALATEX)
%% ============================================================================
\RequirePackage{fontspec}

% Fuentes para portada - usando fallbacks del sistema si las personalizadas no están
% Usamos \IfFontExistsTF para comprobar si la fuente está en el sistema
% Si no, definimos comandos simples de formato

% Fuente condensada para títulos
\IfFontExistsTF{HelveticaNeue-CondensedBold}{%
  \newfontfamily\FuenteTitulo{HelveticaNeue-CondensedBold}%
}{%
  % Intentar con Arial Narrow como alternativa común
  \IfFontExistsTF{Arial Narrow}{%
    \newfontfamily\FuenteTitulo{Arial Narrow}[BoldFont=* Bold]%
  }{%
    % Fallback a sans-serif del sistema
    \newcommand{\FuenteTitulo}{\sffamily\bfseries}%
  }%
}

% Fuente principal para portada
\IfFontExistsTF{Helvetica}{%
  \newfontfamily\FuentePortada{Helvetica}%
}{%
  \IfFontExistsTF{Arial}{%
    \newfontfamily\FuentePortada{Arial}%
  }{%
    \IfFontExistsTF{DejaVu Sans}{%
      \newfontfamily\FuentePortada{DejaVu Sans}%
    }{%
      \newcommand{\FuentePortada}{\sffamily}%
    }%
  }%
}

% Fuente monoespaciada con soporte Unicode completo (para caracteres de caja)
\IfFontExistsTF{DejaVu Sans Mono}{%
  \setmonofont{DejaVu Sans Mono}[Scale=0.9]%
}{%
  \IfFontExistsTF{Noto Sans Mono}{%
    \setmonofont{Noto Sans Mono}[Scale=0.9]%
  }{% Latin Modern Mono por defecto (no soporta caracteres de caja)
  }%
}

%% ============================================================================
%% COLORES
%% ============================================================================
\RequirePackage[dvipsnames,svgnames,x11names]{xcolor}

% Colores básicos
\definecolor{gray97}{gray}{.97}
\definecolor{gray75}{gray}{.75}
\definecolor{gray45}{gray}{.45}
\definecolor{gray30}{gray}{.30}
\definecolor{negro}{RGB}{0,0,0}
\definecolor{blanco}{RGB}{255,255,255}

% Colores de grados
\definecolor{teleco}{RGB}{32,2,116}
\definecolor{civil}{RGB}{201,56,140}
\definecolor{quimica}{RGB}{41,199,255}
\definecolor{informatica}{RGB}{0,128,255}
\definecolor{multimedia}{RGB}{239,206,53}
\definecolor{arquitecnica}{RGB}{0,179,148}
\definecolor{arquitectura}{RGB}{181,0,0}
\definecolor{robotica}{RGB}{255,255,128}

% Colores de másteres
\definecolor{masterteleco}{RGB}{32,2,116}
\definecolor{caminos}{RGB}{201,56,140}
\definecolor{gestedif}{RGB}{50,120,50}
\definecolor{desweb}{RGB}{250,43,22}
\definecolor{mataguaterre}{RGB}{210,250,50}
\definecolor{masterinfor}{RGB}{0,128,255}
\definecolor{autorobo}{RGB}{83,145,201}
\definecolor{prevencion}{RGB}{0,100,0}
\definecolor{gestionagua}{RGB}{7,138,197}
\definecolor{moviles}{RGB}{121,11,21}
\definecolor{masterquimica}{RGB}{41,199,255}
\definecolor{ciberseguridad}{RGB}{9,111,192}
\definecolor{geologica}{RGB}{245,125,0}

% Colores para código
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{codeblue}{rgb}{0.13,0.13,1}
\definecolor{codered}{rgb}{0.6,0,0}
\definecolor{codeorange}{rgb}{0.9,0.4,0}
\definecolor{backcolour}{rgb}{0.97,0.97,0.97}

%% ============================================================================
%% BIBLIOGRAFÍA (BIBLATEX + BIBER)
%% ============================================================================
\RequirePackage[
  backend=biber,
  style=apa,
  sorting=nyt,
  natbib=true,
  language=spanish,
  url=true,
  doi=true,
  eprint=false
]{biblatex}

% Configuración de idioma para biblatex
\DeclareLanguageMapping{spanish}{spanish-apa}

%% ============================================================================
%% GRÁFICOS Y FIGURAS
%% ============================================================================
\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{tikzpagenodes}
\usetikzlibrary{
  tikzmark,
  calc,
  shapes.geometric,
  arrows,
  backgrounds,
  shadings,
  shapes.arrows,
  shapes.symbols,
  shadows,
  positioning,
  fit,
  automata,
  patterns,
  intersections
}

\RequirePackage{pgfplots}
\pgfplotsset{compat=1.18}
\pgfplotsset{colormap/viridis}
\usepgfplotslibrary{patchplots,groupplots,fillbetween,polar}
\RequirePackage{pgfplotstable}

% Gráficas circulares (pie charts)
\RequirePackage{pgf-pie}

% Optimización TikZ (deshabilitada por defecto para evitar problemas)
% Para habilitarla, descomentar las siguientes líneas:
% \usepgfplotslibrary{external}
% \tikzexternalize[prefix=archivos/figuras-procesadas/]

%% ============================================================================
%% TABLAS
%% ============================================================================
\RequirePackage{longtable}
\RequirePackage{booktabs}
\RequirePackage{array}
\RequirePackage{multirow}
\RequirePackage{multicol}
\RequirePackage{tabularx}
\RequirePackage{colortbl}       % Para \rowcolors y colores en tablas
\RequirePackage{ragged2e}

% Tipos de columna personalizados
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

%% ============================================================================
%% FIGURAS Y CAPTIONS
%% ============================================================================
\RequirePackage{subcaption}
\RequirePackage{caption}
\captionsetup{labelfont={bf,small},textfont=small}

\RequirePackage{setspace}
\setlength{\intextsep}{5mm}
\RequirePackage{scalefnt}

% Eliminar el punto entre numeración y texto
\renewcommand*{\figureformat}{\figurename~\thefigure}
\renewcommand*{\tableformat}{\tablename~\thetable}

%% ============================================================================
%% TEXTO Y POSICIONAMIENTO
%% ============================================================================
\RequirePackage{anyfontsize}
\RequirePackage{textpos}
\RequirePackage{mdframed}

% Comando para subrayar con color
\RequirePackage{soul}
\newcommand{\hlc}[2][yellow]{{\sethlcolor{#1}\hl{#2}}}

%% ============================================================================
%% OTROS PAQUETES ÚTILES
%% ============================================================================
\RequirePackage{pdfpages}
\RequirePackage{url}
\RequirePackage[pdfborder={0 0 0}]{hyperref}
\RequirePackage{float}
\RequirePackage{placeins}
\RequirePackage{afterpage}
\RequirePackage{rotating}

% Comentarios TODO (desactivar con borrador=false)
\ExplSyntaxOn
\bool_if:NTF \g__eps_borrador_bool
  {
    \RequirePackage[textsize=tiny,spanish,shadow,textwidth=2cm]{todonotes}
  }
  {
    \RequirePackage[disable]{todonotes}
  }
\ExplSyntaxOff

%% ============================================================================
%% GLOSARIOS Y ACRÓNIMOS
%% ============================================================================
\RequirePackage[acronym,nonumberlist,toc,automake]{glossaries}

% Estilo personalizado simple y robusto para acrónimos
\newglossarystyle{modsuper}{%
  \setglossarystyle{long}%
  \renewcommand{\glsgroupskip}{}%
}
\renewcommand{\glsnamefont}[1]{\textbf{#1}}

%% ============================================================================
%% MATEMÁTICAS
%% ============================================================================
\RequirePackage{mathtools}
\RequirePackage{amsthm}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{bm}
\RequirePackage{mathrsfs}
\RequirePackage{nicefrac}

% Entorno para describir variables en ecuaciones
\newenvironment{condiciones}[1][donde:]
  {%
   #1\tabularx{\textwidth-\widthof{#1}}[t]{
     >{$}l<{$} @{}>{${}}c<{{}$}@{} >{\raggedright\arraybackslash}X
   }%
  }
  {\endtabularx\\[\belowdisplayskip]}

%% ============================================================================
%% TEOREMAS Y DEFINICIONES
%% ============================================================================
\newtheorem{teorema}{Teorema}[chapter]
\newtheorem{theorem}{Theorem}[chapter]
\newtheorem{ejemplo}{Ejemplo}[chapter]
\newtheorem{definicion}{Definición}[chapter]
\newtheorem{definition}{Definition}[chapter]
\newtheorem{lema}{Lema}[chapter]
\newtheorem{corolario}{Corolario}[chapter]
\newtheorem{proposicion}{Proposición}[chapter]

%% ============================================================================
%% CARGAR PAQUETES ADICIONALES
%% ============================================================================
% Los paquetes eps-portadas y eps-codigo se cargan desde el directorio sty/
% El usuario debe incluir sty/ en el path de búsqueda en main.tex

% Intentar cargar paquetes (se cargarán si están en el path)
\IfFileExists{eps-portadas.sty}{%
  \RequirePackage{eps-portadas}%
}{}

\IfFileExists{eps-codigo.sty}{%
  \RequirePackage{eps-codigo}%
}{}

%% ============================================================================
%% CONFIGURACIÓN DE HYPERREF (al final)
%% ============================================================================
\AtBeginDocument{%
  \hypersetup{
    pdfauthor = {\EPSautor},
    pdftitle = {\EPStitulo},
    pdfsubject = {\EPStipoTrabajo},
    pdfkeywords = {TFG, TFM, Universidad de Alicante, EPS},
    colorlinks = true,
    linkcolor = black,
    citecolor = blue!50!black,
    urlcolor = blue!70!black,
  }
}

%% ============================================================================
%% LOGOS POR DEFECTO
%% ============================================================================
\ExplSyntaxOn
\tl_gset:Nn \g__eps_logo_facultad_tl {recursos/logos/universidad/LogoEPSNegro.pdf}
\tl_gset:Nn \g__eps_logo_universidad_tl {recursos/logos/universidad/LogoUANegro.pdf}
\tl_gset:Nn \g__eps_logo_universidad_portada_tl {recursos/logos/universidad/LogoUABlanco.pdf}

\NewExpandableDocumentCommand{\EPSlogoFacultad}{}{\tl_use:N \g__eps_logo_facultad_tl}
\NewExpandableDocumentCommand{\EPSlogoUniversidad}{}{\tl_use:N \g__eps_logo_universidad_tl}
\NewExpandableDocumentCommand{\EPSlogoUniversidadPortada}{}{\tl_use:N \g__eps_logo_universidad_portada_tl}
\ExplSyntaxOff

\endinput
