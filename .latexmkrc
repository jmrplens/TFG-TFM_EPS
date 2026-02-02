# Configuración de latexmk para la plantilla TFG/TFM EPS UA
# 
# Uso: latexmk main.tex
#

# Motor de compilación: LuaLaTeX
$pdf_mode = 4;  # 4 = lualatex
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -file-line-error %O %S';

# Biber para bibliografía
$biber = 'biber %O %S';
$bibtex_use = 2;

# Makeglossaries para glosarios y acrónimos
$makeglossaries = 'makeglossaries %O %S';
push @generated_exts, 'glo', 'gls', 'glg';
push @generated_exts, 'acn', 'acr', 'alg';

add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');

sub run_makeglossaries {
    my ($base_name, $path) = fileparse( $_[0] );
    my @args = ( "-d", $path, $base_name );
    if ($silent) { unshift @args, "-q"; }
    return system "makeglossaries", @args;
}

# Limpieza de archivos auxiliares
$clean_ext = 'synctex.gz synctex.gz(busy) run.xml tex.bak bbl bcf fdb_latexmk run tdo %R-blx.bib';

# Directorio de salida
$out_dir = 'build';

# Vista previa
$pdf_previewer = 'start';

# Extensiones a limpiar con -c
push @generated_exts, 'nav', 'snm', 'vrb';
push @generated_exts, 'fls', 'xdv';
