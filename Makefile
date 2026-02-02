# Makefile para TFG/TFM EPS Universidad de Alicante
# ================================================
#
# Comandos disponibles:
#   make         - Compilación completa (lualatex + biber + 2x lualatex)
#   make quick   - Compilación rápida (solo lualatex)
#   make clean   - Eliminar archivos auxiliares
#   make distclean - Eliminar todo lo generado (incluido PDF)
#   make view    - Abrir el PDF generado
#   make watch   - Compilación continua (requiere latexmk)
#   make help    - Mostrar ayuda

# Configuración
MAIN = main
LATEX = lualatex
LATEX_FLAGS = -shell-escape -interaction=nonstopmode -halt-on-error
BIBER = biber
VIEWER = xdg-open

# Archivos a limpiar
AUX_FILES = *.aux *.log *.out *.toc *.lof *.lot *.bbl *.bcf *.blg \
            *.run.xml *.fls *.fdb_latexmk *.synctex.gz *.nav *.snm \
            *.vrb *.pyg *.pytxcode *.acn *.acr *.alg *.glg *.glo *.gls \
            *.ist *.glsdefs *-blx.bib contenido/**/*.aux

.PHONY: all quick clean distclean view watch help

# Compilación completa por defecto
all: $(MAIN).pdf

# Compilación completa con bibliografía
$(MAIN).pdf: $(MAIN).tex configuracion.tex $(wildcard contenido/**/*.tex) referencias.bib
	@echo "══════════════════════════════════════════════════════════════"
	@echo "  Compilando $(MAIN).tex (paso 1/4)..."
	@echo "══════════════════════════════════════════════════════════════"
	$(LATEX) $(LATEX_FLAGS) $(MAIN)
	@echo ""
	@echo "══════════════════════════════════════════════════════════════"
	@echo "  Procesando bibliografía con Biber (paso 2/4)..."
	@echo "══════════════════════════════════════════════════════════════"
	$(BIBER) $(MAIN)
	@echo ""
	@echo "══════════════════════════════════════════════════════════════"
	@echo "  Compilando $(MAIN).tex (paso 3/4)..."
	@echo "══════════════════════════════════════════════════════════════"
	$(LATEX) $(LATEX_FLAGS) $(MAIN)
	@echo ""
	@echo "══════════════════════════════════════════════════════════════"
	@echo "  Compilando $(MAIN).tex (paso 4/4)..."
	@echo "══════════════════════════════════════════════════════════════"
	$(LATEX) $(LATEX_FLAGS) $(MAIN)
	@echo ""
	@echo "══════════════════════════════════════════════════════════════"
	@echo "  ✓ Compilación completada: $(MAIN).pdf"
	@echo "══════════════════════════════════════════════════════════════"

# Compilación rápida (solo un paso de lualatex)
quick:
	@echo "Compilación rápida..."
	$(LATEX) $(LATEX_FLAGS) $(MAIN)

# Limpiar archivos auxiliares
clean:
	@echo "Limpiando archivos auxiliares..."
	-rm -f $(AUX_FILES)
	-rm -rf _minted-$(MAIN)
	@echo "✓ Limpieza completada"

# Limpieza profunda (incluye el PDF)
distclean: clean
	@echo "Eliminando PDF generado..."
	-rm -f $(MAIN).pdf
	@echo "✓ Limpieza profunda completada"

# Abrir el PDF
view: $(MAIN).pdf
	@echo "Abriendo $(MAIN).pdf..."
	$(VIEWER) $(MAIN).pdf &

# Compilación continua con latexmk
watch:
	@echo "Iniciando compilación continua (Ctrl+C para detener)..."
	latexmk -lualatex -shell-escape -pvc -interaction=nonstopmode $(MAIN)

# Ayuda
help:
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════╗"
	@echo "║      Makefile para TFG/TFM EPS Universidad de Alicante      ║"
	@echo "╠══════════════════════════════════════════════════════════════╣"
	@echo "║                                                              ║"
	@echo "║  Comandos disponibles:                                       ║"
	@echo "║                                                              ║"
	@echo "║    make          Compilación completa                        ║"
	@echo "║                  (lualatex + biber + 2x lualatex)            ║"
	@echo "║                                                              ║"
	@echo "║    make quick    Compilación rápida (solo lualatex)          ║"
	@echo "║                                                              ║"
	@echo "║    make clean    Eliminar archivos auxiliares                ║"
	@echo "║                                                              ║"
	@echo "║    make distclean  Eliminar todo (incluido PDF)              ║"
	@echo "║                                                              ║"
	@echo "║    make view     Abrir el PDF generado                       ║"
	@echo "║                                                              ║"
	@echo "║    make watch    Compilación continua (requiere latexmk)     ║"
	@echo "║                                                              ║"
	@echo "║    make help     Mostrar esta ayuda                          ║"
	@echo "║                                                              ║"
	@echo "╚══════════════════════════════════════════════════════════════╝"
	@echo ""
