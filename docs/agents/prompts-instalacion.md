# Prompts de instalación — Plantilla TFG/TFM EPS UA

Prompts listos para copiar y pegar en GitHub Copilot Chat o Claude
cuando necesitas ayuda para instalar el entorno de trabajo.

Sustituir los valores entre `[corchetes]` por los datos reales.

---

## Cómo usar estos prompts

**En GitHub Copilot Chat:**
1. Abrir Copilot Chat (`Ctrl+Alt+I` en VS Code)
2. Escribir `@workspace` al inicio
3. Pegar el prompt

**En Claude:**
1. Adjuntar la salida del script de instalación (si ya lo has ejecutado)
2. Pegar el prompt

**Alternativa automática (sin IA):**
```bash
# Linux / macOS
python3 scripts/instalar.py
# Windows
python scripts/instalar.py
```
El script comprueba las dependencias e instala lo que puede automáticamente.
Para no-desarrolladores: simplemente ejecútalo y sigue las instrucciones.

---

## I01 — Primera instalación (entorno desde cero)

```text
@workspace Necesito instalar todo lo necesario para usar la plantilla
TFG/TFM EPS UA. Soy estudiante y no tengo experiencia con LaTeX ni con
la terminal.

Mi sistema operativo es: [Windows 11 / macOS 14 / Ubuntu 22.04 / otro]

Por favor, guíame paso a paso para instalar:
1. Python (si hace falta)
2. LaTeX (LuaLaTeX + Biber + latexmk)
3. El paquete latexminted
4. Las herramientas de compilación (make o equivalente)

Al final, quiero poder compilar y obtener un PDF
(`make quick` en Linux/macOS, o compilación manual si no tengo `make` en Windows).
```

---

## I02 — Diagnóstico tras ejecutar el script

```text
@workspace He ejecutado el script de instalación de la plantilla TFG/TFM EPS UA:

    python3 scripts/instalar.py

Este es el resultado que he obtenido:

[pegar aquí la salida completa del script]

¿Qué tengo que instalar? Guíame paso a paso para resolver lo que falta.
Mi sistema es: [Windows / macOS / Ubuntu / otro]
```

---

## I03 — Error al compilar con make

```text
@workspace Al intentar compilar mi TFG/TFM con 'make' obtengo un error.
Estas son las últimas líneas del archivo main.log:

[pegar aquí las últimas 30-50 líneas de main.log]

¿Cuál es el problema y cómo lo soluciono?
```

---

## I04 — Error específico de latexminted / minted

```text
@workspace Al compilar mi TFG/TFM aparece un error relacionado con minted
o el resaltado de código. El error es:

[pegar el mensaje de error]

Mi sistema es: [Windows / macOS / Linux]
¿Tengo instalado latexminted?: [Sí / No / No sé]

¿Qué tengo que hacer para solucionarlo?
```

---

## I05 — Instalar en Windows sin experiencia

```text
@workspace Soy estudiante de [titulación] y necesito instalar LaTeX
en Windows [10 / 11] para usar la plantilla TFG/TFM EPS UA.

Nunca he instalado LaTeX antes y no tengo experiencia con la terminal.

Por favor, explícame:
1. Qué programas tengo que descargar (con los enlaces exactos)
2. Cómo instalarlos paso a paso
3. Cómo verificar que todo funciona correctamente
4. Cómo compilar el documento por primera vez
```

---

## I06 — Configurar la verificación de plagio

```text
@workspace Quiero activar la verificación de plagio en la plantilla
TFG/TFM EPS UA usando [Copyleaks / Turnitin].

Guíame para:
1. Crear y configurar el archivo .env a partir de .env.example
2. Obtener las credenciales necesarias
3. Verificar que la integración funciona ejecutando:
       python3 scripts/revision-rapida.py   (Linux/macOS)
       python  scripts/revision-rapida.py   (Windows)
```

---

## I07 — El PDF no se genera (compilación silenciosa)

```text
@workspace Ejecuto 'make' en mi proyecto TFG/TFM EPS UA pero no se
genera ningún PDF y no veo errores claros.

Contenido del directorio raíz: [listar los archivos del directorio]
Sistema operativo: [Windows / macOS / Linux]

¿Qué puede estar pasando? ¿Qué pasos debo seguir para diagnosticarlo?
```

---

## I08 — Actualizar la plantilla a una nueva versión

```text
@workspace Tengo la plantilla TFG/TFM EPS UA instalada y quiero
actualizarla a la última versión sin perder mi contenido.

Mi estructura actual:
- contenido/ con mis capítulos escritos
- referencias.bib con mis referencias
- configuracion.tex con mis datos

¿Cómo actualizo los archivos de la plantilla (cls/, sty/, Makefile, scripts/)
sin sobreescribir mi contenido?
```

---

## Consejos de uso

- **Siempre ejecuta primero el script:** `python3 scripts/instalar.py` antes
  de pedir ayuda a la IA. La salida del script es la información más útil
  para diagnosticar el problema.
- **Copia el error completo:** no resumas el mensaje de error; pégalo entero.
  Los detalles importan para el diagnóstico.
- **Un paso a la vez:** no intentes resolver varios problemas a la vez.
  Instala una cosa, comprueba que funciona y sigue al siguiente.
- **Si algo falla después de instalarlo:** cierra y abre de nuevo el terminal.
  Muchos problemas se resuelven así porque el PATH se actualiza al abrir
  una nueva sesión.
