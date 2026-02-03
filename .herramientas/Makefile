# Makefile para herramientas de desarrollo
# Ejecutar desde la raíz del proyecto: make -f .herramientas/Makefile [target]

PYTHON := python3
HERRAMIENTAS := .herramientas
GENERAR := $(HERRAMIENTAS)/generar_previews.py
INSERTAR := $(HERRAMIENTAS)/insertar_previews.py

.PHONY: help previews previews-png previews-forzar listar insertar limpiar

help:
	@echo "Herramientas de desarrollo - Plantilla TFG/TFM EPS UA"
	@echo ""
	@echo "Uso: make -f .herramientas/Makefile [target]"
	@echo ""
	@echo "Targets disponibles:"
	@echo "  previews        - Generar previews PDF (solo cambios)"
	@echo "  previews-png    - Generar previews PDF + PNG"
	@echo "  previews-forzar - Regenerar todos los previews"
	@echo "  listar          - Listar snippets en la documentación"
	@echo "  insertar        - Insertar enlaces de preview en docs"
	@echo "  limpiar         - Eliminar previews huérfanos"
	@echo "  todo            - Generar previews + insertar enlaces"

previews:
	@$(PYTHON) $(GENERAR)

previews-png:
	@$(PYTHON) $(GENERAR) --png

previews-forzar:
	@$(PYTHON) $(GENERAR) --forzar --png

listar:
	@$(PYTHON) $(GENERAR) --listar

insertar:
	@$(PYTHON) $(INSERTAR)

insertar-dry:
	@$(PYTHON) $(INSERTAR) --dry-run

limpiar:
	@$(PYTHON) $(GENERAR) --limpiar

todo: previews-png insertar
	@echo "✅ Previews generados y enlaces insertados"
