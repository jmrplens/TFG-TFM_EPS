# Makefile para herramientas de desarrollo
# Ejecutar desde la raíz del proyecto: make -f .herramientas/Makefile [target]

PYTHON := python3
HERRAMIENTAS := .herramientas
ACTUALIZAR_PREVIEWS := $(HERRAMIENTAS)/actualizar_previews.py
GENERAR_PORTADAS := $(HERRAMIENTAS)/generar_portadas.py

.PHONY: help previews previews-forzar listar limpiar portadas todo

help:
	@echo "Herramientas de desarrollo - Plantilla TFG/TFM EPS UA"
	@echo ""
	@echo "Uso: make -f .herramientas/Makefile [target]"
	@echo ""
	@echo "Targets disponibles:"
	@echo "  previews        - Generar e insertar previews (solo cambios)"
	@echo "  previews-forzar - Regenerar todos los previews"
	@echo "  listar          - Listar snippets marcados en documentación"
	@echo "  limpiar         - Eliminar previews huérfanos"
	@echo "  portadas        - Generar portadas para README"
	@echo "  todo            - Generar previews + portadas"

previews:
	@$(PYTHON) $(ACTUALIZAR_PREVIEWS)

previews-forzar:
	@$(PYTHON) $(ACTUALIZAR_PREVIEWS) --forzar

listar:
	@$(PYTHON) $(ACTUALIZAR_PREVIEWS) --listar

limpiar:
	@$(PYTHON) $(ACTUALIZAR_PREVIEWS) --limpiar

portadas:
	@$(PYTHON) $(GENERAR_PORTADAS)

todo: previews portadas
	@echo "✅ Previews y portadas generados"
