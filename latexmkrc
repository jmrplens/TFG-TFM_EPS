# Configuración de latexmk para TFG/TFM EPS UA
# ==============================================
#
# Usar con: latexmk main.tex
# Compilación continua: latexmk -pvc main.tex

# Motor de compilación: LuaLaTeX
$pdf_mode = 4;  # 4 = lualatex

# Comando de LuaLaTeX
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -halt-on-error %O %S';

# Procesador de bibliografía: Biber
$bibtex_use = 2;  # 2 = usar biber cuando se detecte
$biber = 'biber --validate-datamodel %O %S';

# Visor de PDF (Linux)
$pdf_previewer = 'xdg-open %S';

# Extensiones adicionales a limpiar
@generated_exts = qw(aux log out toc lof lot bbl bcf blg run.xml fls fdb_latexmk 
                     synctex.gz nav snm vrb pyg pytxcode acn acr alg glg glo gls 
                     ist glsdefs);

# Limpiar directorio de minted
$clean_ext .= ' %R.ist %R.glsdefs';

push @generated_exts, 'run.xml';

# Personalización del proceso de compilación
$max_repeat = 5;  # Máximo número de repeticiones

# Silenciar advertencias comunes
$silence_logfile_warnings = 1;

# Mostrar errores de forma clara
$warnings_as_errors = 0;

# Archivo de salida
$out_dir = '.';

# Hook para limpiar directorio minted después de distclean
END {
    if (-d "_minted-main") {
        # No eliminar automáticamente, solo si se usa clean
    }
}
