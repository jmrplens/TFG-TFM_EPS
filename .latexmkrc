# ============================================================================
# Configuración de latexmk para la plantilla TFG/TFM EPS UA
# ============================================================================
# 
# Uso:
#   latexmk main.tex          - Compilación completa
#   latexmk -pvc main.tex     - Compilación continua (watch mode)
#   latexmk -c                - Limpiar archivos auxiliares
#   latexmk -C                - Limpiar todo (incluido PDF)
#

# ============================================================================
# MOTOR DE COMPILACIÓN
# ============================================================================

# Usar LuaLaTeX para generar PDF
$pdf_mode = 4;  # 4 = lualatex

# Comando de LuaLaTeX con opciones necesarias
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -file-line-error -synctex=1 %O %S';

# Máximo número de iteraciones
$max_repeat = 5;

# ============================================================================
# BIBLIOGRAFÍA (Biber)
# ============================================================================

$bibtex_use = 2;  # 2 = usar biber cuando se detecte
$biber = 'biber --validate-datamodel %O %S';

# ============================================================================
# GLOSARIOS Y ACRÓNIMOS
# ============================================================================

# Dependencias personalizadas para makeglossaries
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');

sub run_makeglossaries {
    my ($base_name, $path) = fileparse( $_[0] );
    my @args = ( "-d", $path, $base_name );
    if ($silent) { unshift @args, "-q"; }
    return system "makeglossaries", @args;
}

# Extensiones de glosarios
push @generated_exts, 'glo', 'gls', 'glg', 'glsdefs';
push @generated_exts, 'acn', 'acr', 'alg';
push @generated_exts, 'ist';

# ============================================================================
# LIMPIEZA DE ARCHIVOS
# ============================================================================

# Extensiones adicionales a limpiar
push @generated_exts, 'aux', 'log', 'out', 'toc', 'lof', 'lot';
push @generated_exts, 'bbl', 'bcf', 'blg', 'run.xml';
push @generated_exts, 'fls', 'fdb_latexmk', 'synctex.gz', 'xdv';
push @generated_exts, 'nav', 'snm', 'vrb';  # Beamer
push @generated_exts, 'pyg', 'listing', 'lol';  # Minted/listings
push @generated_exts, 'idx', 'ilg', 'ind';  # Índices

# Directorios a limpiar
$clean_ext = 'synctex.gz synctex.gz(busy) run.xml %R-blx.bib';

# Limpiar directorio de minted con clean
$clean_full_ext = '_minted-%R/';

# ============================================================================
# VISOR DE PDF
# ============================================================================

# Detectar sistema operativo para el visor
if ($^O eq 'darwin') {
    # macOS
    $pdf_previewer = 'open -a Preview %S';
} elsif ($^O eq 'MSWin32') {
    # Windows
    $pdf_previewer = 'start %S';
} else {
    # Linux y otros
    $pdf_previewer = 'xdg-open %S';
}

# ============================================================================
# OTRAS OPCIONES
# ============================================================================

# Directorio de salida (raíz del proyecto)
$out_dir = '.';

# No mostrar advertencias menores
$silence_logfile_warnings = 1;

# Colorear salida si es posible
$color = 1;
