%% eps-tfg.cls
%% Clase principal para TFG/TFM de la Escuela Politécnica Superior (UA)
%%
%% Proyecto: Plantilla TFG/TFM EPS Universidad de Alicante
%% Autor:    José Manuel Requena Plens
%% Enlace:   https://github.com/jmrplens/TFG-TFM_EPS
%% Licencia: MIT
%% Versión:  2.2.2 (2026/08/02)
%%
%% -----------------------------------------------------------------------------
\NeedsTeXFormat{LaTeX2e}[2024/11/01]
\ProvidesClass{eps-tfg}[2026/08/02 v2.2.2 Clase TFG/TFM EPS Universidad de Alicante]

%% ============================================================================
%% COMPROBACIÓN DEL MOTOR: LuaLaTeX obligatorio
%% ============================================================================
%% Con pdfLaTeX o XeLaTeX el documento falla más adelante con errores confusos
%% (p. ej. «TeX capacity exceeded»). Normalmente esto ya se detecta en
%% cls/eps-metadata.tex; esta comprobación cubre el caso de cargar la clase sin
%% ese archivo. Ver docs/OVERLEAF.md.
\ifdefined\directlua\else
  \ClassError{eps-tfg}{%
    Esta plantilla requiere LuaLaTeX\MessageBreak
    (en Overleaf: Menu -> Compiler -> LuaLaTeX)%
  }{%
    Compila con `make' o `lualatex -shell-escape main.tex'.\MessageBreak
    Mas informacion en docs/OVERLEAF.md%
  }%
  \csname @@end\endcsname
\fi

%% ============================================================================
%% ARQUITECTURA DE LA CLASE
%% ============================================================================
%% Esta clase se basa en 'scrbook' (KOMA-Script) y utiliza 'expl3' para la
%% gestión de variables y lógica interna.
%%
%% Estructura principal:
%% 1. Carga de expl3 y xparse para definiciones modernas.
%% 2. Definición de variables globales (prefijo g__eps_).
%% 3. Base de datos de titulaciones (Property List):
%%    Almacena colores, logos y textos específicos de cada grado/máster.
%% 4. Interfaz de usuario (\EPSsetup):
%%    Permite configurar el documento mediante pares clave-valor.
%% 5. Configuración de KOMA-Script y paquetes base (geometría, fuentes, idioma).
%% 6. Definición de comandos de portada y metadatos.
%%
%% Las variables internas siguen la convención de nombres de LaTeX3:
%% \g__eps_nombre_tipo (g=global, eps=módulo, tipo=tl/bool/prop/...)
%% ============================================================================

%% ============================================================================
%% CONFIGURACIÓN EXPL3
%% ============================================================================
% tracklang para datatool y glossaries
\PassOptionsToPackage{spanish}{tracklang}

% expl3 y xparse forman parte del núcleo de LaTeX: no hace falta cargarlos.
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
\tl_new:N \g__eps_titulacion_pedida_tl % valor escrito por el usuario (válido o no)
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
\bool_new:N \g__eps_accesible_bool

% Idioma del documento
\tl_new:N \g__eps_idioma_tl
\tl_new:N \g__eps_idioma_polyglossia_tl
\tl_new:N \g__eps_idioma_variante_tl % opciones de polyglossia (p. ej. variant=british)
\tl_new:N \g__eps_idioma_codigo_tl
\tl_new:N \g__eps_idioma_biblatex_tl

% Establecer valores por defecto
\tl_gset:Nn \g__eps_facultad_tl {Escuela~Politécnica~Superior}
\tl_gset:Nn \g__eps_facultad_corto_tl {EPS~UA}
\tl_gset:Nn \g__eps_universidad_tl {Universidad~de~Alicante}
\tl_gset:Nn \g__eps_ubicacion_tl {Alicante}
\tl_gset:Nn \g__eps_autor_genero_tl {m}
\bool_gset_true:N \g__eps_optimizar_tikz_bool
% Idioma por defecto: español
\tl_gset:Nn \g__eps_idioma_tl {espanol}
\tl_gset:Nn \g__eps_idioma_polyglossia_tl {spanish}
\tl_gset:Nn \g__eps_idioma_codigo_tl {es-ES}
\tl_gset:Nn \g__eps_idioma_biblatex_tl {spanish}

%% ============================================================================
%% BASE DE DATOS DE TITULACIONES
%% ============================================================================

% Property list para almacenar datos de titulaciones
\prop_new:N \g__eps_titulaciones_prop
% Lista de identificadores válidos (para los mensajes de error)
\clist_new:N \g__eps_titulaciones_clist

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
    \clist_gput_right:Nn \g__eps_titulaciones_clist { #1 }
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

\__eps_define_titulacion:nnnnnnn {master-ciencia-datos}
  {Máster~Universitario~en~Ciencia~de~Datos}
  {tfm} {cienciadatos} {blanco} {Color} {Negro}

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
\prop_gput:Nnn \g__eps_logos_map_prop {master-ciencia-datos} {LogoMasterCienciaDatos}

%% ============================================================================
%% FUNCIÓN PARA CONFIGURAR TITULACIÓN
%% ============================================================================
\cs_new_protected:Nn \__eps_setup_titulacion:n
  {
    \tl_gset:Nn \g__eps_titulacion_pedida_tl { #1 }
    % Si la titulación no existe se avisa y no se toca nada más: el resto de
    % datos (colores, logos) no existen y expandirlos colgaría la compilación.
    \prop_if_in:NnTF \g__eps_titulaciones_prop { #1 / nombre }
      { \__eps_setup_titulacion_datos:n { #1 } }
      {
        \msg_error:nnne { eps-tfg } { titulacion-desconocida } { #1 }
          { \clist_use:Nn \g__eps_titulaciones_clist { ,~ } }
      }
  }

\cs_new_protected:Nn \__eps_setup_titulacion_datos:n
  {
    \tl_gset:Nn \g__eps_titulacion_tl { #1 }

    % Obtener datos de la prop list
    \prop_get:NnN \g__eps_titulaciones_prop { #1 / nombre } \l_tmpa_tl
    \tl_gset_eq:NN \g__eps_titulacion_nombre_tl \l_tmpa_tl

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
%% FUNCIÓN PARA CONFIGURAR IDIOMA
%% ============================================================================
\cs_new_protected:Nn \__eps_setup_idioma:n
  {
    \tl_gset:Nn \g__eps_idioma_tl { #1 }
    \str_case:nnF { #1 }
      {
        {espanol} {
          \tl_gset:Nn \g__eps_idioma_polyglossia_tl {spanish}
          \tl_gclear:N \g__eps_idioma_variante_tl
          \tl_gset:Nn \g__eps_idioma_codigo_tl {es-ES}
          \tl_gset:Nn \g__eps_idioma_biblatex_tl {spanish}
        }
        {valenciano} {
          \tl_gset:Nn \g__eps_idioma_polyglossia_tl {catalan}
          \tl_gclear:N \g__eps_idioma_variante_tl
          \tl_gset:Nn \g__eps_idioma_codigo_tl {ca-ES-valencia}
          \tl_gset:Nn \g__eps_idioma_biblatex_tl {catalan}
        }
        {ingles} {
          \tl_gset:Nn \g__eps_idioma_polyglossia_tl {english}
          \tl_gset:Nn \g__eps_idioma_variante_tl {variant=british}
          \tl_gset:Nn \g__eps_idioma_codigo_tl {en-GB}
          \tl_gset:Nn \g__eps_idioma_biblatex_tl {english}
        }
      }
      {
        \msg_error:nnn { eps-tfg } { idioma-desconocido } { #1 }
      }
  }

%% ============================================================================
%% MENSAJES DE ERROR
%% ============================================================================
\msg_new:nnn { eps-tfg } { titulacion-desconocida }
  {
    La~titulación~'#1'~no~está~definida.~
    Valores~válidos:~#2.
  }

\msg_new:nnn { eps-tfg } { idioma-desconocido }
  {
    El~idioma~'#1'~no~está~soportado.~
    Valores~válidos:~espanol,~valenciano,~ingles.
  }

\msg_new:nnn { eps-tfg } { campo-requerido }
  {
    El~campo~'#1'~es~obligatorio.~
    Usa~\token_to_str:N \EPSsetup \{#1~=~...\}~en~configuracion.tex~para~definirlo.
  }

\msg_new:nnn { eps-tfg } { campo-vacio }
  {
    El~campo~'#1'~está~vacío.~
    Defínelo~con~\token_to_str:N \EPSsetup \{#1~=~...\}~en~configuracion.tex.
  }

\msg_new:nnn { eps-tfg } { accesible-sin-etiquetado }
  {
    accesible~=~true~necesita~LaTeX~2025-11~o~posterior~y~el~PDF~etiquetado~
    (\token_to_str:N \input{eps-metadata}~en~main.tex).~
    No~se~declara~la~conformidad~PDF/UA-2.~
    Para~quitar~este~aviso:~accesible~=~false~en~configuracion.tex.
  }
\msg_new:nnn { eps-tfg } { alt-falta }
  {
    Falta~el~texto~alternativo~de~la~imagen~'#1'.\\
    En~el~PDF~se~usa~'#2'.\\
    Describe~la~imagen~con~
    \token_to_str:N \includegraphics[alt={...}]{...}~
    (o~'artifact'~si~es~decorativa).~Ver~docs/ACCESIBILIDAD.md.
  }
\msg_new:nnn { eps-tfg } { accesible-no-compatible }
  {
    #1~no~es~compatible~con~el~PDF~accesible:~#2.~
    Ver~docs/ACCESIBILIDAD.md.
  }

% Comprobación de los datos imprescindibles (al empezar el documento, cuando
% ya se ha leído configuracion.tex)
\cs_new_protected:Nn \__eps_comprobar_campos:
  {
    % (si se escribió un valor no válido ya se avisó al leerlo)
    \tl_if_empty:NT \g__eps_titulacion_pedida_tl
      { \msg_error:nnn { eps-tfg } { campo-requerido } { titulacion } }
    \tl_if_empty:NT \g__eps_titulo_tl
      { \msg_warning:nnn { eps-tfg } { campo-vacio } { titulo } }
    \tl_if_empty:NT \g__eps_autor_tl
      { \msg_warning:nnn { eps-tfg } { campo-vacio } { autor } }
    \tl_if_empty:NT \g__eps_tutor_tl
      { \msg_warning:nnn { eps-tfg } { campo-vacio } { tutor } }
  }
\AddToHook { begindocument / before } [ eps-tfg / campos ]
  { \__eps_comprobar_campos: }

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
    % optimizar-tikz: OBSOLETA y sin efecto. Se acepta para no romper
    % configuraciones antiguas (la externalización de TikZ no es compatible
    % con el etiquetado del PDF).
    optimizar-tikz .bool_gset:N = \g__eps_optimizar_tikz_bool,
    optimizar-tikz .default:n = true,
    optimizar-tikz .initial:n = true,

    borrador .bool_gset:N = \g__eps_borrador_bool,
    borrador .default:n = true,
    borrador .initial:n = false,

    % Declarar el PDF conforme a PDF/UA-2 (ver docs/ACCESIBILIDAD.md)
    accesible .bool_gset:N = \g__eps_accesible_bool,
    accesible .default:n = true,
    accesible .initial:n = true,

    % Idioma del documento (espanol, valenciano, ingles)
    idioma .code:n = { \__eps_setup_idioma:n { #1 } },
    idioma .initial:n = {espanol},
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
\NewExpandableDocumentCommand{\EPSidioma}{}{\tl_use:N \g__eps_idioma_tl}
\NewExpandableDocumentCommand{\EPSidiomaCodigo}{}{\tl_use:N \g__eps_idioma_codigo_tl}
\NewExpandableDocumentCommand{\EPSidiomaBiblatex}{}{\tl_use:N \g__eps_idioma_biblatex_tl}

% Selecciona un texto según el idioma del documento (expandible):
%   \EPSsegunidioma{<español>}{<valenciano>}{<inglés>}
% Lo usan la clase y los componentes para no dejar textos fijos en español.
\NewExpandableDocumentCommand{\EPSsegunidioma}{ m m m }
  {
    \str_case:VnF \g__eps_idioma_tl
      {
        {espanol} {#1}
        {valenciano} {#2}
        {ingles} {#3}
      }
      {#1}
  }

% Títulos de las listas de acrónimos y del glosario (usados en main.tex)
\NewExpandableDocumentCommand{\EPStituloAcronimos}{}
  {
    \EPSsegunidioma
      {Lista~de~Acrónimos~y~Abreviaturas}
      {Llista~d'Acrònims~i~Abreviatures}
      {List~of~Acronyms~and~Abbreviations}
  }
\NewExpandableDocumentCommand{\EPStituloGlosario}{}
  {
    \EPSsegunidioma
      {Glosario~de~Términos}
      {Glossari~de~Termes}
      {Glossary~of~Terms}
  }

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

% Comandos para comprobar si hay departamento de tutor/cotutor
\NewDocumentCommand{\EPSsiTutorDpto}{ m m }
  {
    \tl_if_blank:VTF \g__eps_tutor_dpto_tl { #2 } { #1 }
  }
\NewDocumentCommand{\EPSsiCotutorDpto}{ m m }
  {
    \tl_if_blank:VTF \g__eps_cotutor_dpto_tl { #2 } { #1 }
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
      {
        % Solo tutor principal
        \str_case:VnF \g__eps_tutor_genero_tl
          {
            {f} {Tutora}
            {m} {Tutor}
          }
          {Tutoría}
      }
      {
        % Hay cotutor - concatenamos géneros en variable temporal
        \tl_set:Nx \l_tmpa_tl { \g__eps_tutor_genero_tl \g__eps_cotutor_genero_tl }
        \str_case:VnF \l_tmpa_tl
          {
            {mm} {Tutores}
            {mf} {Tutores}
            {fm} {Tutores}
            {ff} {Tutoras}
          }
          {Tutorías}
      }
  }

%% ============================================================================
%% OPCIONES DE CLASE
%% ============================================================================
% \documentclass[borrador]{eps-tfg} equivale a borrador = true en \EPSsetup.
% (Se declaran con la sintaxis expl3 activa: el código de una opción se lee
% al declararla, no al ejecutarla.)
\DeclareOption{borrador}{ \bool_gset_true:N \g__eps_borrador_bool }
\DeclareOption{final}{ \bool_gset_false:N \g__eps_borrador_bool }

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrbook}}
\ProcessOptions\relax

\ExplSyntaxOff

%% ============================================================================
%% COMPATIBILIDAD CON EL ETIQUETADO (latex-lab)
%% ============================================================================
%% Con \DocumentMetadata (cls/eps-metadata.tex) LaTeX carga los módulos de
%% etiquetado de latex-lab. Desde LaTeX 2025-11 se cargan TODOS (block, math,
%% table...) y algunos paquetes que usa la plantilla dejan de funcionar.
%% Estos ajustes no tienen efecto cuando no se usa \DocumentMetadata.
%%
%% (1) enumitem: el módulo 'block' redefine itemize/enumerate/description al
%%     empezar el documento y descarta las opciones de enumitem (noitemsep,
%%     leftmargin, label=...). Se restauran las versiones de enumitem después
%%     de 'block'; las listas se siguen etiquetando (L/LI/Lbl/LBody).
\AddToHook{package/enumitem/after}{%
  \NewEnvironmentCopy{eps@enit@itemize}{itemize}%
  \NewEnvironmentCopy{eps@enit@enumerate}{enumerate}%
  \NewEnvironmentCopy{eps@enit@description}{description}%
  \AddToHook{begindocument/before}[eps-tfg/enumitem]{%
    \RenewEnvironmentCopy{itemize}{eps@enit@itemize}%
    \RenewEnvironmentCopy{enumerate}{eps@enit@enumerate}%
    \RenewEnvironmentCopy{description}{eps@enit@description}}%
  \DeclareHookRule{begindocument/before}{eps-tfg/enumitem}{after}{latex-lab-testphase-block}%
}
%% (2) chemformula: \ch usa un $ implícito para subíndices y el módulo 'math'
%%     (que busca el $ de cierre) falla. Se desactiva esa recogida dentro de \ch.
\AddToHook{package/chemformula/after}{%
  \NewCommandCopy\eps@ch@original\ch
  \RenewDocumentCommand\ch{O{}m}{%
    {\ifdefined\MathCollectFalse\MathCollectFalse\fi\eps@ch@original[#1]{#2}}}%
}
%% (3) threeparttable copia \endlist al cargarse ('\let\endtablenotes\endlist');
%%     'block' redefine las listas después y el par queda desemparejado.
\AddToHook{package/threeparttable/after}{%
  \AddToHook{begindocument/before}[eps-tfg/threeparttable]{%
    \let\endtablenotes\endlist}%
  \DeclareHookRule{begindocument/before}{eps-tfg/threeparttable}{after}{latex-lab-testphase-block}%
  % threeparttable empieza con \noindent: todo el entorno queda dentro de un
  % párrafo y la lista de notas (tablenotes) quedaba dentro de un P, lo que
  % PDF 2.0 no permite. Ese párrafo exterior se etiqueta como Div (que sí
  % puede contener la tabla y la lista); los de dentro vuelven a ser P.
  \AddToHook{env/threeparttable/begin}{\eps@tpt@div}%
  \AddToHook{env/tablenotes/begin}{\eps@tpt@texto}%
}
\ExplSyntaxOn
\tl_new:N \l__eps_tpt_para_tl
\tl_new:N \l__eps_tpt_bloque_tl
% Desde LaTeX 2026-06 el párrafo que sigue a la tabla se abre con el nombre
% de estructura 'para/textblock' en lugar de \l__tag_para_tag_tl: también
% se hace Div dentro del entorno (asignación local).
\cs_new_protected:Npn \eps@tpt@div
  {
    \bool_lazy_and:nnT { \tag_if_active_p: } { \cs_if_exist_p:N \l__tag_para_tag_tl }
      {
        \tl_set_eq:NN \l__eps_tpt_para_tl \l__tag_para_tag_tl
        \tl_set:Nn \l__tag_para_tag_tl { Div }
        \cs_if_exist:cT { l__tag_name_para/textblock_tl }
          {
            \tl_set_eq:Nc \l__eps_tpt_bloque_tl { l__tag_name_para/textblock_tl }
            \tl_set:cn { l__tag_name_para/textblock_tl } { Div }
          }
      }
  }
\cs_new_protected:Npn \eps@tpt@texto
  {
    \tl_if_empty:NF \l__eps_tpt_para_tl
      { \tl_set_eq:NN \l__tag_para_tag_tl \l__eps_tpt_para_tl }
    \tl_if_empty:NF \l__eps_tpt_bloque_tl
      { \tl_set_eq:cN { l__tag_name_para/textblock_tl } \l__eps_tpt_bloque_tl }
  }
\ExplSyntaxOff
%% (4) longtable 4.24 (LaTeX 2025-11, TeX Live 2025): al partir una tabla
%%     entre páginas daba «Infinite glue shrinkage found in box being split».
%%     TeX lo trata como error ignorado (el PDF sale bien), pero latexmk se
%%     detiene antes de terminar las pasadas y quedan mal los números de página
%%     de los índices. Se aplica la misma corrección que longtable 4.25
%%     (latex3/latex2e gh/1907): encogimiento finito en lugar de \vss. Solo
%%     afecta a la versión 4.24; las demás no se tocan.
\ExplSyntaxOn
\cs_new_protected:Npn \__eps_longtable_encogimiento_finito:
  {
    % (\vss está dentro de \vbox{...}: regex busca también en los grupos)
    \tl_set_eq:NN \l_tmpa_tl \LT@output
    \regex_replace_all:nnN
      { \c{copy} \c{LT@foot} \c{vss} }
      { \c{copy} \c{LT@foot} \c{vskip} \c{z@} \c{@plus} 1fil \c{@minus} \c{normalbaselineskip} }
      \l_tmpa_tl
    \cs_set_eq:NN \LT@output \l_tmpa_tl
  }
\cs_new_eq:NN \eps@longtable@finito \__eps_longtable_encogimiento_finito:
\ExplSyntaxOff
\AddToHook{package/longtable/after}{%
  \@ifpackagelater{longtable}{2025/10/13}%
    {\@ifpackagelater{longtable}{2025/12/23}{}{\eps@longtable@finito}}%
    {}%
}
%% (5) pdfpages cuenta las páginas del PDF incluido con un \includegraphics
%%     sin texto alternativo dentro de una caja de medida (que no llega al
%%     PDF): cada \includepdf daba el aviso «Alternative text for graphic is
%%     missing» aunque llevara alt={...}. Esa medida se hace sin etiquetado.
\ExplSyntaxOn
\cs_new_protected:Npn \__eps_pdfpages_medida_sin_etiquetado:
  {
    \cs_if_exist:NT \AM@getpagecount
      {
        \tl_set_eq:NN \l_tmpa_tl \AM@getpagecount
        \regex_replace_once:nnN
          { \c{includegraphics} }
          { \c{SuspendTagging} \cB\{ eps-pdfpages \cE\} \c{includegraphics} }
          \l_tmpa_tl
        \cs_set_eq:NN \AM@getpagecount \l_tmpa_tl
      }
  }
\cs_new_eq:NN \eps@pdfpages@medida \__eps_pdfpages_medida_sin_etiquetado:
\ExplSyntaxOff
\AddToHook{package/pdfpages/after}{\eps@pdfpages@medida}

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
%% SOPORTE PARA PÁGINAS LANDSCAPE CON HEADERS CORRECTOS
%% ============================================================================
% Comando para iniciar sección landscape con headers correctos
% Usa las primitivas de LuaTeX para cambiar las dimensiones de la página
% y geometry con layoutwidth/layoutheight para calcular textwidth correcto
\NewDocumentCommand{\BeginLandscapePage}{O{2cm}}{%
  \clearpage
  % Cambiar dimensiones de la página PDF (LuaTeX primitives)
  \pagewidth=297mm  % A4 landscape width
  \pageheight=210mm % A4 landscape height
  % Aplicar nuevos márgenes Y layout para landscape
  % layoutwidth/layoutheight fuerzan a geometry a recalcular textwidth
  \newgeometry{%
    layoutwidth=297mm,
    layoutheight=210mm,
    left=#1,
    right=#1,
    top=#1,
    bottom=#1,
    includeheadfoot,
    headheight=14pt,
    headsep=1cm,
    footskip=1.5cm
  }%
  % Actualizar anchos de header/footer al nuevo textwidth con offset 0
  \KOMAoptions{paper=landscape, headwidth=\textwidth:0pt, footwidth=\textwidth:0pt}%
}

% Comando para restaurar orientación portrait
\NewDocumentCommand{\EndLandscapePage}{}{%
  \clearpage
  % Restaurar dimensiones de la página PDF (A4 portrait)
  \pagewidth=210mm
  \pageheight=297mm
  % Restaurar márgenes
  \restoregeometry
  % Restaurar anchos de header/footer con offset 0
  \KOMAoptions{paper=portrait, headwidth=\textwidth:0pt, footwidth=\textwidth:0pt}%
}

%% ============================================================================
%% IDIOMA (POLYGLOSSIA PARA LUALATEX)
%% ============================================================================
\RequirePackage{polyglossia}

% Cargar todos los idiomas soportados (el predeterminado se selecciona en AtBeginDocument)
\setdefaultlanguage{spanish}
\setotherlanguage{english}
\setotherlanguage{catalan}

% Redefinir nombres para español
\gappto\captionsspanish{%
  \renewcommand{\listtablename}{Índice de tablas}
  \renewcommand{\tablename}{Tabla}
  \renewcommand{\glossaryname}{Glosario}
  \renewcommand{\acronymname}{Acrónimos}
  \renewcommand{\bibname}{Bibliografía}
}

% Redefinir nombres para valenciano/catalán
\gappto\captionscatalan{%
  \renewcommand{\listtablename}{Índex de taules}
  \renewcommand{\tablename}{Taula}
  \renewcommand{\glossaryname}{Glossari}
  \renewcommand{\acronymname}{Acrònims}
  \renewcommand{\bibname}{Bibliografia}
  \renewcommand{\contentsname}{Índex}
  \renewcommand{\listfigurename}{Índex de figures}
  \renewcommand{\figurename}{Figura}
  \renewcommand{\chaptername}{Capítol}
  \renewcommand{\appendixname}{Apèndix}
}

% Redefinir nombres para inglés
\gappto\captionsenglish{%
  \renewcommand{\listtablename}{List of Tables}
  \renewcommand{\tablename}{Table}
  \renewcommand{\glossaryname}{Glossary}
  \renewcommand{\acronymname}{Acronyms}
  \renewcommand{\bibname}{Bibliography}
}

%% ============================================================================
%% FUENTES (FONTSPEC PARA LUALATEX)
%% ============================================================================
\RequirePackage{fontspec}

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
\definecolor{cienciadatos}{RGB}{121,11,21}

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
  % language=auto: los textos siguen el idioma del documento (polyglossia) y
  % cada entrada conserva su 'langid', necesario para que biblatex-apa aplique
  % la capitalización APA a los títulos en inglés. (Forzar language=spanish
  % la desactivaba.)
  language=auto,
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

% siunitx (lo cargan los módulos de componentes): coma decimal en español y
% valenciano, punto en inglés. Se puede cambiar con \sisetup en el preámbulo.
\AddToHook{package/siunitx/after}{%
  \sisetup{output-decimal-marker={\EPSsegunidioma{{,}}{{,}}{.}}}%
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
% Fix para conflicto colortbl + multirow (evita números fantasma)
\renewcommand\multirowsetup{}
\RequirePackage{ragged2e}
\RequirePackage{threeparttable} % Para tablas con notas al pie
\RequirePackage{diagbox}        % Para celdas diagonales en encabezados
\RequirePackage{tabularray}     % Tablas modernas (alternativa a multirow/multicolumn)

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
\RequirePackage{hyperxmp}  % Metadatos XMP extendidos para PDF
\RequirePackage{float}
\RequirePackage{placeins}
\RequirePackage{afterpage}
\RequirePackage{rotating}

% Comentarios TODO (visibles solo con borrador = true)
% El paquete se carga siempre para que \setuptodonotes y similares funcionen
% en el preámbulo. La opción 'borrador' se lee en configuracion.tex, DESPUÉS
% de cargar la clase, así que las notas se desactivan al empezar el documento.
\RequirePackage[textsize=tiny,shadow,textwidth=2cm]{todonotes}
\ExplSyntaxOn
\cs_new_protected:Nn \__eps_configurar_todonotes:
  {
    % Textos de todonotes según el idioma
    \str_case:Vn \g__eps_idioma_tl
      {
        {espanol}
          {
            \use:c { @todonotes@SetTodoListName } { Lista~de~tareas~pendientes }
            \use:c { @todonotes@SetMissingFigureText } { Figura }
            \use:c { @todonotes@SetMissingFigureUp } { Figura }
            \use:c { @todonotes@SetMissingFigureDown } { pendiente }
          }
        {valenciano}
          {
            \use:c { @todonotes@SetTodoListName } { Llista~de~tasques~pendents }
            \use:c { @todonotes@SetMissingFigureText } { Figura }
            \use:c { @todonotes@SetMissingFigureUp } { Figura }
            \use:c { @todonotes@SetMissingFigureDown } { pendent }
          }
      }
    % Modo final: mismo efecto que la opción 'disable' de todonotes
    \bool_if:NF \g__eps_borrador_bool
      {
        \use:c { @todonotes@disabledtrue }
        \exp_args:Nc \RenewDocumentCommand { @todo } { O{} m } { }
        \RenewDocumentCommand \missingfigure { O{} m } { }
        \RenewDocumentCommand \listoftodos { O{} } { }
      }
  }
\AddToHook { begindocument / before } [ eps-tfg / todonotes ]
  { \__eps_configurar_todonotes: }
\ExplSyntaxOff

%% ============================================================================
%% GLOSARIOS Y ACRÓNIMOS
%% ============================================================================
\RequirePackage[acronym,toc,automake]{glossaries}

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
\RequirePackage{nicefrac}
% \mathscr lo proporciona unicode-math (mathrsfs no tendría efecto)

% Soporte Unicode Math (Debe cargarse después de mathtools y otros paquetes ams)
% Desactivamos comandos de mathtools que entran en conflicto con unicode-math para evitar warnings
\let\underbracket\relax
\let\overbracket\relax
\let\dblcolon\relax
\let\coloneqq\relax
\let\Coloneqq\relax
\let\eqqcolon\relax
\RequirePackage{unicode-math}


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
% Los nombres siguen el idioma del documento (teorema y theorem son sinónimos)
\newtheorem{teorema}{\EPSsegunidioma{Teorema}{Teorema}{Theorem}}[chapter]
\newtheorem{theorem}{\EPSsegunidioma{Teorema}{Teorema}{Theorem}}[chapter]
\newtheorem{ejemplo}{\EPSsegunidioma{Ejemplo}{Exemple}{Example}}[chapter]
\newtheorem{definicion}{\EPSsegunidioma{Definición}{Definició}{Definition}}[chapter]
\newtheorem{definition}{\EPSsegunidioma{Definición}{Definició}{Definition}}[chapter]
\newtheorem{lema}{\EPSsegunidioma{Lema}{Lema}{Lemma}}[chapter]
\newtheorem{corolario}{\EPSsegunidioma{Corolario}{Corol·lari}{Corollary}}[chapter]
\newtheorem{proposicion}{\EPSsegunidioma{Proposición}{Proposició}{Proposition}}[chapter]

%% ============================================================================
%% ACCESIBILIDAD DEL PDF ETIQUETADO
%% ============================================================================
%% Ajustes para que el árbol de estructura del PDF sea útil para los lectores
%% de pantalla. Sin \DocumentMetadata (o sin etiquetado activo) no tienen
%% ningún efecto. Ver docs/ACCESIBILIDAD.md.
\ExplSyntaxOn
%% (1) Iconos (fontawesome5). Por defecto son decorativos: se marcan como
%%     artefacto para que el lector de pantalla no lea el nombre del glifo
%%     («INFO-CIRCLE», «FOLDER-OPEN»...). Los iconos que transmiten
%%     información (estado de una tarea, conforme/no conforme...) se escriben
%%     con \EPSiconoTexto{texto}{icono}, que lee «texto» en su lugar.
\bool_new:N \l__eps_icono_artefacto_bool
\bool_set_true:N \l__eps_icono_artefacto_bool
\cs_new_protected:Npn \__eps_icono_artefacto:n #1
  {
    \bool_lazy_and:nnTF { \tag_if_active_p: } { \l__eps_icono_artefacto_bool }
      {
        \tag_mc_end_push:
        \tag_mc_begin:n { artifact }
        #1
        \tag_mc_end:
        \tag_mc_begin_pop:n { }
      }
      { #1 }
  }
\tl_new:N \l__eps_icono_texto_tl
\cs_new_protected:Npn \__eps_icono_texto:nn #1 #2
  {
    \tag_if_active:TF
      {
        \group_begin:
        \bool_set_false:N \l__eps_icono_artefacto_bool
        \tag_mc_end_push:
        \tl_set:Ne \l__eps_icono_texto_tl { \text_expand:n {#1} }
        \exp_args:Ne \tag_mc_begin:n
          { actualtext = { \exp_not:V \l__eps_icono_texto_tl } }
        #2
        \tag_mc_end:
        \tag_mc_begin_pop:n { }
        \group_end:
      }
      { #2 }
  }
\NewDocumentCommand \EPSiconoTexto { m m } { \__eps_icono_texto:nn {#1} {#2} }
\cs_new_protected:Npn \__eps_fa_parche:
  {
    \cs_if_exist:NT \fontawesome_use_icon:nn
      {
        \cs_new_eq:NN \__eps_fa_icono_original:nn \fontawesome_use_icon:nn
        \cs_set_protected:Npn \fontawesome_use_icon:nn ##1 ##2
          { \__eps_icono_artefacto:n { \__eps_fa_icono_original:nn {##1} {##2} } }
      }
  }
\AddToHook { package / fontawesome5 / after } { \__eps_fa_parche: }

%% (2) Idioma de los fragmentos en otro idioma (p. ej. el Abstract dentro de
%%     otherlanguage{english}): polyglossia no lo indica en el PDF, así que
%%     se pasa a tagpdf para que esas estructuras lleven /Lang. Se comprueba
%%     al empezar cada capítulo y cada párrafo; el ajuste es local y termina
%%     con el entorno.
\tl_new:N \l__eps_tag_idioma_tl
\cs_new_protected:Npn \__eps_tag_idioma:
  {
    \bool_lazy_and:nnT
      { \tag_if_active_p: }
      { ! \str_if_eq_p:ee { \languagename } { \g__eps_idioma_polyglossia_tl } }
      {
        \str_case_e:nnT { \languagename }
          {
            { spanish } { \tl_set:Nn \l__eps_tag_idioma_tl { es-ES } }
            { english } { \tl_set:Nn \l__eps_tag_idioma_tl { en-GB } }
            { catalan } { \tl_set:Nn \l__eps_tag_idioma_tl { ca-ES } }
          }
          { \exp_args:Ne \tagpdfsetup { text / lang = \l__eps_tag_idioma_tl } }
      }
  }
\AddToHook { cmd / chapter / before } { \__eps_tag_idioma: }
\AddToHook { para / begin } { \__eps_tag_idioma: }

%% (3) Cabecera de las tablas de datos: \EPScabeceraTabla[<filas>] (por
%%     defecto 1), justo antes del tabular, marca esas filas como cabecera
%%     (TH) para que el lector de pantalla asocie cada dato con su columna.
%%     Sin el módulo de tablas de LaTeX (versiones anteriores a 2025-11) no
%%     hace nada. En longtable no hace falta: \endhead ya marca la cabecera.
\NewDocumentCommand \EPScabeceraTabla { O{1} }
  {
    \keys_if_exist:nnT { __tag / setup } { table/header-rows }
      { \tagpdfsetup { table/header-rows = {#1} } }
  }

%% (4) Texto alternativo en dibujos TikZ y pgfplots:
%%     \begin{tikzpicture}[alt={...}] (o 'artifact' si es decorativo). LaTeX
%%     2025-11 o posterior define esas claves; en versiones anteriores se
%%     definen aquí sin efecto, para que el mismo documento compile en ambas.
\AddToHook { begindocument / before }
  {
    \cs_if_exist:NT \tikzset
      {
        \pgfkeysifdefined { /tikz/alt/.@cmd } { }
          {
            \tikzset
              {
                alt/.code = { } ,
                actualtext/.code = { } ,
                artifact/.code = { }
              }
          }
      }
  }

%% (5) Ajustes que dependen de los módulos de etiquetado de LaTeX 2025-11 o
%%     posterior (en versiones anteriores esos módulos no existen).
\IfFormatAtLeastT { 2025-11-01 }
  {
    % tcolorbox reasigna el rol «Caption» al título de sus cajas y, a partir
    % de la primera caja con título, todas las leyendas de figuras y tablas
    % dejan de ser Caption. Con 'noop' el título de la caja es un párrafo
    % normal y las leyendas no cambian.
    \AddToHook { begindocument / before }
      {
        \bool_lazy_and:nnT
          { \tag_if_active_p: }
          { \socket_if_exist_p:n { tagsupport / tcb / box / title } }
          { \AssignTaggingSocketPlug { tcb / box / title } { noop } }
      }
    % Las figuras y tablas etiquetadas se agrupan en un contenedor que LaTeX
    % coloca al final del documento; así se coloca al final de cada
    % capítulo, más cerca del texto que las cita.
    \AddToHook { cmd / chapter / before }
      { \tag_if_active:T { \tagtool { flush-floats = 0 } } }
  }
% Leyendas: con el etiquetado, LaTeX redefine \@makecaption con su formato
% estándar («Figura 1: texto») y se perdían las fuentes de \captionsetup
% (etiqueta en negrita, texto en tamaño pequeño). Se aplican las del paquete
% caption: \captionfont y \captiontextfont a toda la leyenda y
% \captionlabelfont a la etiqueta.
\cs_new_protected:Npn \__eps_leyendas_con_formato:
  {
    \bool_lazy_and:nnT
      { \cs_if_exist_p:N \captionlabelfont }
      { \socket_if_exist_p:n { caption/label } }
      {
        \NewSocketPlug { caption/label } { eps-tfg }
          { { \captionlabelfont ##1: } ~ }
        \AssignSocketPlug { caption/label } { eps-tfg }
        \AddToHookWithArguments { cmd/@makecaption/before }
          {
            \cs_if_exist_use:N \captionfont
            \cs_if_exist_use:N \captionsize
            \cs_if_exist_use:N \captiontextfont
          }
      }
  }
\IfFormatAtLeastT { 2025-11-01 }
  { \AddToHook { begindocument / before } { \__eps_leyendas_con_formato: } }
% tcolorbox 6.10 (2026) con capture=hbox (\tcbox, cajas UML de [software]):
% el título y una 'varwidth upper' van en minipages. Cada minipage cierra
% la estructura en curso como si interrumpiera un párrafo y luego abre otro.
% Si la caja no está dentro de un párrafo (modo vertical), cerraba la
% sección y dejaba abierto un párrafo con el resto del documento. Con
% capture=minipage tcolorbox lo evita; con hbox, no. En ese caso se hace lo
% mismo que con capture=minipage: esas minipages no cierran ni abren nada.
\cs_new_protected:Npn \__eps_tcb_hbox_minipages:
  {
    \cs_if_exist:NT \tcbox@inner@hbox
      {
        \cs_new_eq:NN \__eps_tcb_inner_hbox:n \tcbox@inner@hbox
        \cs_set:Npn \tcbox@inner@hbox ##1
          {
            % (sin \DocumentMetadata esos sockets no existen)
            \bool_lazy_and:nnT
              { \mode_if_vertical_p: }
              { \socket_if_exist_p:n { tagsupport / minipage / before } }
              {
                \AssignTaggingSocketPlug { minipage / before } { noop }
                \AssignTaggingSocketPlug { minipage / after } { noop }
              }
            \__eps_tcb_inner_hbox:n {##1}
          }
      }
  }
% (los sockets de minipage no existen antes de LaTeX 2025-11)
\IfFormatAtLeastT { 2025-11-01 }
  { \AddToHook { package / tcolorbox / after } { \__eps_tcb_hbox_minipages: } }

%% (6) Títulos de sección como encabezados (H2...H6). KOMA-Script compone los
%%     títulos con su propio código y el etiquetado de LaTeX solo reconoce
%%     \chapter: \section, \subsection... salían como párrafos normales. Se
%%     enganchan los sockets de etiquetado de secciones del núcleo a los
%%     ganchos documentados de KOMA (heading/postinit, heading/begingroup y
%%     \sectionlinesformat). La composición de los títulos no cambia.
\cs_new:Npn \__eps_sec_nivel:n #1
  {
    \str_case:nnF {#1}
      {
        { part } { -1 } { chapter } { 0 } { section } { 1 }
        { subsection } { 2 } { subsubsection } { 3 }
        { paragraph } { 4 } { subparagraph } { 5 }
      }
      { 6 }
  }
% Cierra la sección anterior del mismo nivel (o inferior) y abre la nueva
\cs_new_protected:Npn \__eps_sec_abrir:nn #1 #2
  {
    \tag_if_active:T
      {
        \UseTaggingSocket { sec / end } { \__eps_sec_nivel:n {#1} }
        \UseTaggingSocket { sec / begin }
          {
            { \__eps_sec_nivel:n {#1} }
            { tag = \UseStructureName { sec / \__eps_sec_nivel:n {#1} } }
          }
        % Título en línea: el párrafo que sigue empieza con él
        \bool_lazy_and:nnT
          {
            \bool_lazy_or_p:nn
              { \str_if_eq_p:nn {#1} { paragraph } }
              { \str_if_eq_p:nn {#1} { subparagraph } }
          }
          { \legacy_if_p:n { @startsection@runin } }
          { \UseTaggingSocket { sec / title / init } { \__eps_sec_nivel:n {#1} } }
      }
  }
% El párrafo del título se etiqueta como encabezado del nivel (H2, H3...)
\cs_new_protected:Npn \__eps_sec_titulo:nn #1 #2
  {
    \tag_if_active:T
      { \UseTaggingSocket { sec / title / init } { \__eps_sec_nivel:n {#1} } }
  }
\bool_new:N \l__eps_sec_sin_numero_bool
% Títulos en línea (\paragraph, \subparagraph): el párrafo que empieza con
% el título se abre como encabezado (H5, H6) y, tras el título, se parte
% (sec/title/split) para que el texto siga en un párrafo normal. Es lo que
% hace LaTeX con la clase book; KOMA compone el título cuando el párrafo ya
% ha empezado, así que el encabezado se prepara al iniciar el título.
\cs_new_protected:Npn \__eps_sec_en_linea:nnnn #1 #2 #3 #4
  {
    \hskip #2
    \tl_if_blank:nTF {#3}
      { \bool_set_true:N \l__eps_sec_sin_numero_bool }
      { \bool_set_false:N \l__eps_sec_sin_numero_bool }
    \UseTaggingSocket { sec / title / runin / number }
      { { \__eps_sec_nivel:n {#1} } \l__eps_sec_sin_numero_bool } {#3}
    #4
    \UseTaggingSocket { sec / title / split }
  }
% \chapter con LaTeX 2026-06 o posterior (ver más abajo): mismos ganchos de
% KOMA que en \section, y el número dentro del encabezado (H1), como en
% \sectionlinesformat (con \@hangfrom quedaba delante, suelto)
\cs_new_protected:Npn \__eps_capitulos_etiquetados:
  {
    \AddtoDoHook { heading / postinit / chapter }
      { \__eps_sec_abrir:nn { chapter } }
    \AddtoDoHook { heading / begingroup / chapter }
      { \__eps_sec_titulo:nn { chapter } }
    \cs_set:Npn \chapterlinesformat ##1 ##2 ##3
      {
        \tl_if_blank:nTF {##2}
          { \bool_set_true:N \l__eps_sec_sin_numero_bool }
          { \bool_set_false:N \l__eps_sec_sin_numero_bool }
        \UseTaggingSocket { sec / title / hang }
          { {0} \l__eps_sec_sin_numero_bool {##2} {##3} }
          { \@hangfrom {##2} }
        ##3
      }
  }

%% (7) accesible = true en \EPSsetup (por defecto): declara el PDF conforme
%%     a PDF/UA-2 (metadatos XMP pdfuaid:part=2) y avisa de las
%%     construcciones que estropean el PDF accesible. Requiere LaTeX 2025-11
%%     o posterior y el etiquetado activo; si no, se avisa y no se declara.
\cs_new_protected:Npn \__eps_accesible_no_compatible:nn #1 #2
  { \msg_warning:nnnn { eps-tfg } { accesible-no-compatible } {#1} {#2} }
\cs_new_protected:Npn \__eps_accesible_activar:
  {
    \SetKeys [ document / metadata ] { pdfstandard = ua-2 }
    \AddToHook { cmd / diagbox / before }
      {
        \__eps_accesible_no_compatible:nn { \token_to_str:N \diagbox }
          { deja~la~tabla~abierta~y~el~texto~siguiente~queda~dentro~de~ella }
      }
    \AddToHook { env / tblr / begin }
      {
        \__eps_accesible_no_compatible:nn { tblr~(tabularray) }
          { la~tabla~no~se~etiqueta~como~tabla;~usa~tabular }
      }
  }
\AddToHook { begindocument / before }
  {
    \bool_if:NT \g__eps_accesible_bool
      {
        \IfFormatAtLeastTF { 2025-11-01 }
          {
            \tag_if_active:TF
              { \__eps_accesible_activar: }
              { \msg_warning:nn { eps-tfg } { accesible-sin-etiquetado } }
          }
          { \msg_warning:nn { eps-tfg } { accesible-sin-etiquetado } }
      }
  }

%% (8) Texto alternativo automático. Una imagen sin alt={...} recibía como
%%     texto alternativo el nombre del archivo. Ahora, si está en una figura
%%     con leyenda, recibe «Figura 3.2: <leyenda>» (la leyenda va después de
%%     la imagen: se toma del .aux de la compilación anterior) y, si no,
%%     «Imagen N». Se avisa, con el archivo y el texto usado, para que el
%%     autor escriba una descripción de verdad.
\int_new:N \g__eps_alt_flotante_int   % figuras y subfiguras abiertas
\int_new:N \l__eps_alt_flotante_int   % la figura en curso (0: ninguna)
\int_new:N \g__eps_alt_imagen_int     % imágenes sin alt ni leyenda
\tl_new:N \l__eps_alt_tl
\tl_new:N \g__eps_alt_tl
% Lo escribe en el .aux cada figura con leyenda
\cs_new_protected:Npn \eps@altflotante #1 #2
  { \tl_gclear_new:c { g__eps_alt_flotante_#1_tl } \tl_gset:cn { g__eps_alt_flotante_#1_tl } {#2} }
\cs_new_protected:Npn \__eps_alt_flotante_inicio:
  {
    \int_gincr:N \g__eps_alt_flotante_int
    \int_set_eq:NN \l__eps_alt_flotante_int \g__eps_alt_flotante_int
    \tl_clear:N \@currentlabelname
  }
\cs_new_protected:Npn \__eps_alt_flotante_fin:
  {
    \tl_if_empty:NF \@currentlabelname
      {
        % La leyenda que guarda hyperref empieza con un cambio de idioma de
        % polyglossia dentro de \texorpdfstring: se usa su versión para PDF
        \group_begin:
          \cs_set_eq:NN \texorpdfstring \use_ii:nn
          \tl_gset:Ne \g__eps_alt_tl
            { \text_purify:n { \figurename \c_space_tl \@currentlabel :~ \@currentlabelname } }
        \group_end:
        \tl_set_eq:NN \l__eps_alt_tl \g__eps_alt_tl
        \iow_now:Ne \@auxout
          {
            \token_to_str:N \eps@altflotante
            { \int_use:N \l__eps_alt_flotante_int } { \exp_not:V \l__eps_alt_tl }
          }
      }
  }
% #1: el archivo de la imagen
\cs_new_protected:Npn \__eps_alt_relleno:n #1
  {
    \tl_if_empty:NT \l__tag_graphic_alt_tl
      {
        \bool_lazy_and:nnTF
          { \int_compare_p:nNn { \l__eps_alt_flotante_int } > { 0 } }
          { \tl_if_exist_p:c { g__eps_alt_flotante_ \int_use:N \l__eps_alt_flotante_int _tl } }
          {
            \tl_set_eq:Nc \l__tag_graphic_alt_tl
              { g__eps_alt_flotante_ \int_use:N \l__eps_alt_flotante_int _tl }
          }
          {
            \int_gincr:N \g__eps_alt_imagen_int
            \tl_set:Ne \l__tag_graphic_alt_tl
              {
                \EPSsegunidioma { Imagen } { Imatge } { Image }
                \c_space_tl \int_use:N \g__eps_alt_imagen_int
              }
          }
        \msg_warning:nnee { eps-tfg } { alt-falta }
          {#1} { \l__tag_graphic_alt_tl }
      }
  }
\cs_new_protected:Npn \__eps_alt_automatico:
  {
    \cs_if_exist:cT { __socket_tagsupport/graphic/begin_plug_alt:w }
      {
        \cs_new_eq:Nc \__eps_alt_plug_original:w
          { __socket_tagsupport/graphic/begin_plug_alt:w }
        \cs_set_protected:cpn { __socket_tagsupport/graphic/begin_plug_alt:w } ##1
          { \__eps_alt_relleno:n {##1} \__eps_alt_plug_original:w {##1} }
        \clist_map_inline:nn { figure , figure* , subfigure }
          {
            \AddToHook { env / ##1 / begin } { \__eps_alt_flotante_inicio: }
            \AddToHook { env / ##1 / end } { \__eps_alt_flotante_fin: }
          }
      }
  }
\IfFormatAtLeastT { 2025-11-01 }
  {
    \AddToHook { begindocument / before }
      { \tag_if_active:T { \__eps_alt_automatico: } }
  }

%% (9) Índices etiquetados y con enlaces. Las entradas de los índices de KOMA
%%     (tocbasic) no llaman a los ganchos del etiquetado: el índice general y
%%     las listas de figuras, tablas y códigos salían como artefactos (el
%%     lector de pantalla no los leía) y sin enlaces. Se componen con las
%%     rutinas del núcleo, que sí los llaman, con las mismas medidas que KOMA.
% Como en KOMA, una entrada no queda sola al pie de la página separada de la
% primera de sus subentradas: no se corta antes de una entrada más profunda.
\int_new:N \g__eps_toc_nivel_int
\cs_new_protected:Npn \__eps_toc_entrada:nnn #1 #2 #3
  {
    \int_compare:nNnT {#1} > { \g__eps_toc_nivel_int } { \nobreak }
    \int_gset:Nn \g__eps_toc_nivel_int {#1}
    \@dottedtocline {#1} {#2} {#3}
  }
\cs_new_protected:Npn \__eps_indices_etiquetados:
  {
    \cs_set:Npn \l@section       { \__eps_toc_entrada:nnn {1} {1.5em} {2.3em} }
    \cs_set:Npn \l@subsection    { \__eps_toc_entrada:nnn {2} {3.8em} {3.2em} }
    \cs_set:Npn \l@subsubsection { \__eps_toc_entrada:nnn {3} {7.0em} {4.1em} }
    \cs_set:Npn \l@paragraph     { \__eps_toc_entrada:nnn {4} {10em} {5em} }
    \cs_set:Npn \l@subparagraph  { \__eps_toc_entrada:nnn {5} {12em} {6em} }
    \cs_set:Npn \l@figure        { \__eps_toc_entrada:nnn {1} {1.5em} {2.3em} }
    \cs_set:Npn \l@table         { \__eps_toc_entrada:nnn {1} {1.5em} {2.3em} }
    \cs_if_exist:NT \l@listing
      { \cs_set:Npn \l@listing { \__eps_toc_entrada:nnn {1} {1.5em} {2.3em} } }
    % Capítulo: como el de latex-lab para 'report', con la tipografía y el
    % espaciado de KOMA (sin línea de puntos)
    \cs_set:Npn \l@chapter ##1 ##2
      {
        \int_compare:nNnT { \c@tocdepth } > { -1 }
          {
            \addpenalty { -\@highpenalty }
            \int_gzero:N \g__eps_toc_nivel_int
            \addvspace { 1.0em \@plus \p@ }
            \setlength \@tempdima { 1.5em }
            \group_begin:
              \parindent \z@
              \rightskip \@tocrmarg
              \parfillskip -\rightskip
              \leavevmode
              \usekomafont { chapterentry }
              \advance \leftskip \@tempdima
              \hskip -\leftskip
              \UseHookWithArguments { contentsline/text/before } {4}
                { \toclevel@chapter } {##1} {##2} { \@contentsline@destination }
              \use:c { contentsline@text@0@format } {##1}
              \UseHookWithArguments { contentsline/text/after } {4}
                { \toclevel@chapter } {##1} {##2} { \@contentsline@destination }
              \nobreak \hfill \nobreak
              \hb@xt@ \@pnumwidth
                {
                  \hss
                  \usekomafont { chapterentrypagenumber }
                  \UseHookWithArguments { contentsline/page/before } {4}
                    { \toclevel@chapter } {##1} {##2} { \@contentsline@destination }
                  ##2
                  \UseHookWithArguments { contentsline/page/after } {4}
                    { \toclevel@chapter } {##1} {##2} { \@contentsline@destination }
                  \kern -\p@ \kern \p@
                }
              \par
              \penalty \@highpenalty
            \group_end:
          }
      }
  }
\IfFormatAtLeastT { 2025-11-01 }
  {
    \clist_map_inline:nn
      { section , subsection , subsubsection , paragraph , subparagraph }
      {
        \AddtoDoHook { heading / postinit / #1 } { \__eps_sec_abrir:nn {#1} }
        \AddtoDoHook { heading / begingroup / #1 } { \__eps_sec_titulo:nn {#1} }
      }
    % \chapter: hasta LaTeX 2025-11 el módulo de secciones de latex-lab lo
    % redefine y lo etiqueta él. Desde LaTeX 2026-06 ya no (lo hace la nueva
    % implementación con plantillas, que no se carga): el título del
    % capítulo quedaba como un párrafo abierto que contenía todo el capítulo.
    % Se usan entonces los mismos ganchos de KOMA que en \section.
    \AddToHook { begindocument / before }
      {
        \bool_lazy_and:nnT
          { \cs_if_exist_p:N \ltlabsecdate }
          { \str_compare_p:eNe { \ltlabsecdate } > { 2026-01-01 } }
          { \__eps_capitulos_etiquetados: }
      }
    % Igual que la definición de KOMA (\@hangfrom{\hskip #2#3}{#4}), pero el
    % número va en su propio elemento dentro del encabezado
    \cs_set:Npn \sectionlinesformat #1 #2 #3 #4
      {
        \IfUseNumber
          { \bool_set_false:N \l__eps_sec_sin_numero_bool }
          { \bool_set_true:N \l__eps_sec_sin_numero_bool }
        \UseTaggingSocket { sec / title / hang }
          {
            { \__eps_sec_nivel:n {#1} }
            \l__eps_sec_sin_numero_bool
            { \hskip #2 #3 }
            {#4}
          }
          { \@hangfrom { \hskip #2 #3 } }
        #4
      }
    % Igual que la definición de KOMA (\hskip #2#3#4), con el título en su
    % propio encabezado
    \cs_set:Npn \sectioncatchphraseformat #1 #2 #3 #4
      { \__eps_sec_en_linea:nnnn {#1} {#2} {#3} {#4} }
    \AddToHook { begindocument / end }
      {
        \bool_lazy_and:nnT { \tag_if_active_p: }
          { \cs_if_exist_p:N \ltlabtocdate }  % módulo de índices de latex-lab
          { \__eps_indices_etiquetados: }
      }
    % En \chapter el número dejaba de leerse (artefacto): ahora forma parte
    % del encabezado. Igual que la definición de KOMA (\@hangfrom{#2}{#3}).
    \cs_set:Npn \chapterlinesformat #1 #2 #3
      {
        \@hangfrom
          { \tl_if_blank:nF {#2} { \UseTaggingSocket { sec / title / number } {0} {#2} } }
          {#3}
      }
  }
\ExplSyntaxOff

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
%% CONFIGURACIÓN DE HYPERREF Y SELECCIÓN DE IDIOMA (al final)
%% ============================================================================

% Idioma principal según 'idioma' (configuracion.tex se lee después de cargar
% la clase). Tiene que ser \setmainlanguage antes de empezar el documento:
% polyglossia restablece el idioma principal al final de \begin{document},
% así que un \selectlanguage en \AtBeginDocument no tendría efecto.
\ExplSyntaxOn
\cs_new_protected:Nn \__eps_idioma_principal:
  {
    \use:e
      {
        \exp_not:N \setmainlanguage
          [ \exp_not:V \g__eps_idioma_variante_tl ]
          { \exp_not:V \g__eps_idioma_polyglossia_tl }
      }
    % El resumen en español se escribe con otherlanguage{spanish}
    \str_if_eq:VnF \g__eps_idioma_polyglossia_tl { spanish }
      { \setotherlanguage{spanish} }
  }
\AddToHook { begindocument / before } [ eps-tfg / idioma ]
  { \__eps_idioma_principal: }

% Cambia al idioma del documento dentro del texto (p. ej. tras un bloque en
% otro idioma). Se mantiene por compatibilidad con versiones anteriores.
\cs_new_protected:Nn \__eps_seleccionar_idioma:
  { \exp_args:NV \selectlanguage \g__eps_idioma_polyglossia_tl }
\NewDocumentCommand{\EPSseleccionarIdioma}{}{\__eps_seleccionar_idioma:}
\ExplSyntaxOff

\AtBeginDocument{%
  % --- Metadatos del PDF ---
  % pdflang fija el idioma del PDF (y de los metadatos XMP) según 'idioma',
  % con prioridad sobre el valor 'lang' de cls/eps-metadata.tex.
  \hypersetup{
    % --- Metadatos básicos ---
    pdfauthor = {\EPSautor},
    pdftitle = {\EPStitulo},
    pdfsubject = {\EPStipoTrabajo},
    pdfkeywords = {TFG, TFM, Universidad de Alicante, EPS, \EPStitulacion},
    pdflang = {\EPSidiomaCodigo},
    % --- Metadatos extendidos ---
    pdfcopyright = {Copyright © \the\year\space \EPSautor. \EPSsegunidioma{Todos los derechos reservados.}{Tots els drets reservats.}{All rights reserved.}},
    pdfcontactemail = {\EPSautorEmail},
    pdfpublisher = {Universidad de Alicante - Escuela Politécnica Superior},
    pdfcontactcountry = {\EPSsegunidioma{España}{Espanya}{Spain}},
    pdfcontactcity = {Alicante},
    % --- Información de la plantilla ---
    pdfcreator = {LuaLaTeX con plantilla TFG-TFM EPS UA},
    pdfsource = {https://github.com/jmrplens/TFG-TFM_EPS},
    % --- Marcadores/Bookmarks ---
    bookmarksnumbered = true,
    bookmarksopen = true,
    bookmarksopenlevel = 1,
    % --- Visualización inicial ---
    pdfpagemode = {UseOutlines},
    pdfdisplaydoctitle = true,
    % --- Apariencia de enlaces ---
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
