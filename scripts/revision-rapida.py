#!/usr/bin/env python3
"""
revision-rapida.py — Análisis estático del documento TFG/TFM EPS UA

Analiza los archivos .tex del proyecto y genera un informe de revisión
en informe-revision.md. No requiere IA ni conexión a internet.

Opcionalmente, si existe un archivo .env con COPYLEAKS_API_KEY o
TURNITIN_API_KEY, realiza una verificación de plagio contra la API
correspondiente.

Uso:
    python3 scripts/revision-rapida.py
    python3 scripts/revision-rapida.py --solo-errores
    python3 scripts/revision-rapida.py --capitulo contenido/capitulos/introduccion.tex
"""

from __future__ import annotations

import os
import re
import sys
import glob
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import ClassVar

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

RAIZ = Path(__file__).parent.parent
CONTENIDO_DIR = RAIZ / "contenido"
REFERENCIAS_BIB = RAIZ / "referencias.bib"
INFORME_SALIDA = RAIZ / "informe-revision.md"

# Comandos prohibidos por la plantilla
COMANDOS_PROHIBIDOS = [
    (r"\\hline", "Usar `\\toprule`, `\\midrule`, `\\bottomrule` (booktabs)"),
    (r"\\begin\{verbatim\}", "Usar entornos `*code` de minted"),
    (r"\\begin\{lstlisting\}", "Usar entornos `*code` de minted"),
    (r"\\usepackage\[utf8\]\{inputenc\}", "LuaLaTeX maneja UTF-8 nativamente"),
    (r"\\usepackage\{subfigure\}", "Usar `subcaption`"),
    (r"\\usepackage\{subfig\}", "Usar `subcaption`"),
    (r"\\bibliographystyle\{", "Usar BibLaTeX con `\\printbibliography`"),
    (r"\\bibliography\{", "Usar BibLaTeX con `\\printbibliography`"),
    (r"\\cite(?![a-zA-Z])", "Usar `\\parencite{}` o `\\textcite{}`"),
    (r"\\include\{", "Usar `\\input{}` para evitar saltos de página forzados"),
]

# Capítulos esperados en un TFG/TFM estándar (al menos algunos de estos)
CAPITULOS_ESPERADOS = [
    "introduccion", "objetivos", "marco", "teorico", "metodologia",
    "desarrollo", "resultados", "conclusiones"
]

# Palabras que indican registro informal
REGISTRO_INFORMAL = [
    r"\byo\b", r"\bmi\b(?!\s+trabajo|\s+tesis|\s+tfg|\s+tfm)",
    r"\bcreo\s+que\b", r"\bpienso\s+que\b", r"\bopino\s+que\b",
    r"\bbueno\b", r"\bpues\b", r"\bvale\b", r"\bgenial\b",
    r"\bchulo\b", r"\bguay\b",
]

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def cargar_env():
    """Carga variables de .env si existe."""
    env_path = RAIZ / ".env"
    env = {}
    if env_path.exists():
        for linea in env_path.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                clave, _, valor = linea.partition("=")
                env[clave.strip()] = valor.strip().strip('"').strip("'")
    return env


def leer_tex(ruta: Path) -> str:
    """Lee un archivo .tex ignorando líneas de comentario."""
    try:
        return ruta.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""
    except PermissionError as e:
        print(f"Error de permisos al leer {ruta}: {e}", file=sys.stderr)
        return ""
    except UnicodeDecodeError as e:
        print(f"Error de codificación en {ruta}: {e}", file=sys.stderr)
        return ""


def eliminar_comentarios(texto: str) -> str:
    """Elimina comentarios LaTeX (líneas que empiezan con %)."""
    lineas = []
    for linea in texto.splitlines():
        # Eliminar comentarios inline: % precedido de número par de backslashes
        # (?<!\\)   → no precedido por un \ solitario (evita \%)
        # (?:\\\\)* → permite cero o más pares \\  (p.ej. \\ seguido de %)
        linea_limpia = re.sub(r"((?<!\\)(?:\\\\)*)%.*$", r"\1", linea)
        lineas.append(linea_limpia)
    return "\n".join(lineas)


def contar_palabras(texto: str) -> int:
    """Cuenta palabras aproximadas en texto LaTeX."""
    # Reemplazar comandos preservando su contenido de forma iterativa para
    # manejar llaves anidadas (p.ej. \caption{texto \ref{fig:x}}).
    # Se usa r"\1" para conservar las palabras dentro de \textit{}, \textbf{},
    # \caption{}, etc. y obtener un conteo más preciso.
    prev = None
    while prev != texto:
        prev = texto
        texto = re.sub(r"\\[a-zA-Z]+\*?\{([^{}]*)\}", r"\1", texto)
    texto = re.sub(r"\\[a-zA-Z]+\*?", " ", texto)
    texto = re.sub(r"[{}]", " ", texto)
    texto = re.sub(r"\$[^$]*\$", " ", texto)
    return len(texto.split())


def extraer_texto_plano(archivos_tex: list) -> str:
    """Extrae texto sin markup LaTeX para envío a APIs externas de plagio."""
    fragmentos = []
    for ruta in archivos_tex:
        texto = leer_tex(ruta)
        if not texto.strip():
            continue
        texto = eliminar_comentarios(texto)
        prev = None
        while prev != texto:
            prev = texto
            texto = re.sub(r"\\[a-zA-Z]+\*?\{([^{}]*)\}", r"\1", texto)
        texto = re.sub(r"\\[a-zA-Z]+\*?", " ", texto)
        texto = re.sub(r"[{}]", " ", texto)
        texto = re.sub(r"\$[^$]*\$", " ", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        if texto:
            fragmentos.append(texto)
    return "\n\n".join(fragmentos)


# ---------------------------------------------------------------------------
# Análisis
# ---------------------------------------------------------------------------

class Problema:
    SEVERIDAD: ClassVar[dict[str, str]] = {"error": "❌", "advertencia": "⚠️", "info": "ℹ️"}

    def __init__(self, archivo, linea, severidad, categoria, mensaje, sugerencia=""):
        self.archivo = archivo
        self.linea = linea
        self.severidad = severidad
        self.categoria = categoria
        self.mensaje = mensaje
        self.sugerencia = sugerencia

    def __str__(self):
        icono = self.SEVERIDAD.get(self.severidad, "•")
        loc = f"`{self.archivo}`" + (f" línea {self.linea}" if self.linea else "")
        base = f"{icono} **{self.categoria}** — {loc}: {self.mensaje}"
        if self.sugerencia:
            base += f"\n  > {self.sugerencia}"
        return base


def analizar_comandos_prohibidos(ruta: Path, texto: str) -> list:
    """Detecta uso de comandos prohibidos por la plantilla."""
    problemas = []
    texto_sin_comentarios = eliminar_comentarios(texto)
    for patron, sugerencia in COMANDOS_PROHIBIDOS:
        for m in re.finditer(patron, texto_sin_comentarios):
            linea = texto_sin_comentarios[:m.start()].count("\n") + 1
            problemas.append(Problema(
                archivo=str(ruta.relative_to(RAIZ)),
                linea=linea,
                severidad="error",
                categoria="Formato LaTeX",
                mensaje=f"Comando prohibido: `{m.group().strip()}`",
                sugerencia=sugerencia,
            ))
    return problemas


def analizar_etiquetas(ruta: Path, texto: str) -> list:
    r"""Detecta figuras, tablas y ecuaciones sin \label{}."""
    problemas = []
    texto_sin_comentarios = eliminar_comentarios(texto)

    # Entornos que deben tener \label
    entornos_con_label = ["figure", "table", "equation", "align", "lstlisting"]
    for entorno in entornos_con_label:
        patron = rf"\\begin\{{{entorno}\*?\}}(.*?)\\end\{{{entorno}\*?\}}"
        for m in re.finditer(patron, texto_sin_comentarios, re.DOTALL):
            bloque = m.group(0)
            if r"\label{" not in bloque:
                linea = texto_sin_comentarios[:m.start()].count("\n") + 1
                problemas.append(Problema(
                    archivo=str(ruta.relative_to(RAIZ)),
                    linea=linea,
                    severidad="advertencia",
                    categoria="Referencias",
                    mensaje=f"Entorno `{entorno}` sin `\\label{{}}` — no se podrá referenciar",
                    sugerencia=f"Añadir `\\label{{{entorno[:3]}:nombre}}` dentro del entorno",
                ))

    return problemas


def analizar_captions(ruta: Path, texto: str) -> list:
    r"""Detecta figuras y tablas sin \caption{}."""
    problemas = []
    texto_sin_comentarios = eliminar_comentarios(texto)

    for entorno in ["figure", "table"]:
        patron = rf"\\begin\{{{entorno}\*?\}}(.*?)\\end\{{{entorno}\*?\}}"
        for m in re.finditer(patron, texto_sin_comentarios, re.DOTALL):
            bloque = m.group(0)
            if r"\caption{" not in bloque:
                linea = texto_sin_comentarios[:m.start()].count("\n") + 1
                problemas.append(Problema(
                    archivo=str(ruta.relative_to(RAIZ)),
                    linea=linea,
                    severidad="error",
                    categoria="Figuras/Tablas",
                    mensaje=f"Entorno `{entorno}` sin `\\caption{{}}` — obligatorio",
                    sugerencia=f"Añadir `\\caption{{Descripción de la {entorno}}}` antes de `\\label`",
                ))

    return problemas


def analizar_referencias_cruzadas(archivos_tex: list) -> list:
    r"""Detecta \ref{} sin \label{} correspondiente."""
    problemas = []
    labels_definidos = set()
    refs_usadas = []  # (archivo, linea, clave)

    for ruta in archivos_tex:
        texto = eliminar_comentarios(leer_tex(ruta))
        for m in re.finditer(r"\\label\{([^}]+)\}", texto):
            labels_definidos.add(m.group(1))
        for m in re.finditer(r"\\(?:ref|pageref|cref|Cref)\{([^}]+)\}", texto):
            linea = texto[:m.start()].count("\n") + 1
            refs_usadas.append((str(ruta.relative_to(RAIZ)), linea, m.group(1)))

    for archivo, linea, clave in refs_usadas:
        if clave not in labels_definidos:
            problemas.append(Problema(
                archivo=archivo,
                linea=linea,
                severidad="error",
                categoria="Referencias",
                mensaje=f"Referencia `\\ref{{{clave}}}` sin `\\label{{{clave}}}` definido",
                sugerencia="Añadir `\\label{" + clave + "}` en el elemento referenciado",
            ))

    return problemas


def analizar_bibliografia(archivos_tex: list) -> list:
    """Detecta citas sin entrada en .bib y entradas .bib no citadas."""
    problemas = []

    if not REFERENCIAS_BIB.exists():
        problemas.append(Problema(
            archivo="referencias.bib",
            linea=None,
            severidad="error",
            categoria="Bibliografía",
            mensaje="No se encontró el archivo `referencias.bib`",
        ))
        return problemas

    # Claves definidas en .bib
    texto_bib = REFERENCIAS_BIB.read_text(encoding="utf-8")
    claves_bib = set(re.findall(r"@\w+\{([^,\s]+),", texto_bib))

    # Claves citadas en los .tex
    claves_citadas = set()
    citas_por_archivo = []
    for ruta in archivos_tex:
        texto = eliminar_comentarios(leer_tex(ruta))
        for m in re.finditer(
            r"\\(?:parencite|textcite|cite|citeauthor|citeyear|citetitle)"
            r"(?:\[[^\]]*\]){0,2}\{([^}]+)\}",
            texto
        ):
            for clave in m.group(1).split(","):
                clave = clave.strip()
                claves_citadas.add(clave)
                linea = texto[:m.start()].count("\n") + 1
                citas_por_archivo.append((str(ruta.relative_to(RAIZ)), linea, clave))

    # Citas sin entrada en .bib
    for archivo, linea, clave in citas_por_archivo:
        if clave and clave not in claves_bib:
            problemas.append(Problema(
                archivo=archivo,
                linea=linea,
                severidad="error",
                categoria="Bibliografía",
                mensaje=f"Cita `{clave}` no encontrada en `referencias.bib`",
                sugerencia=f"Añadir la entrada `@...{{{clave}, ...}}` a `referencias.bib`",
            ))

    # Entradas .bib no citadas
    no_citadas = claves_bib - claves_citadas
    for clave in sorted(no_citadas):
        problemas.append(Problema(
            archivo="referencias.bib",
            linea=None,
            severidad="info",
            categoria="Bibliografía",
            mensaje=f"Entrada `{clave}` definida en `.bib` pero no citada en el texto",
            sugerencia="Citar con `\\parencite{" + clave + "}` o eliminar la entrada si no se usa",
        ))

    return problemas


def analizar_secciones_vacias(ruta: Path, texto: str) -> list:
    """Detecta secciones con muy poco contenido."""
    problemas = []
    texto_sin_comentarios = eliminar_comentarios(texto)

    # Dividir por secciones
    patron_seccion = r"(\\(?:chapter|section|subsection)\{[^}]+\})"
    partes = re.split(patron_seccion, texto_sin_comentarios)
    # Localizar posiciones reales de cada sección en el texto
    coincidencias_seccion = list(re.finditer(patron_seccion, texto_sin_comentarios))

    for i in range(1, len(partes) - 1, 2):
        titulo = partes[i]
        contenido = partes[i + 1] if i + 1 < len(partes) else ""
        palabras = contar_palabras(contenido)

        if palabras < 50:
            # Usar la posición real del match para calcular la línea
            indice_seccion = (i - 1) // 2
            if 0 <= indice_seccion < len(coincidencias_seccion):
                inicio_seccion = coincidencias_seccion[indice_seccion].start()
                linea = texto_sin_comentarios.count("\n", 0, inicio_seccion) + 1
            else:
                linea = 1
            nivel = "capítulo" if "chapter" in titulo else "sección"
            problemas.append(Problema(
                archivo=str(ruta.relative_to(RAIZ)),
                linea=linea,
                severidad="advertencia",
                categoria="Estructura",
                mensaje=f"{nivel.capitalize()} `{titulo.strip()}` con muy poco contenido ({palabras} palabras)",
                sugerencia=f"Un {nivel} debería tener al menos 150-200 palabras de contenido",
            ))

    return problemas


def analizar_registro_informal(ruta: Path, texto: str) -> list:
    """Detecta posible registro informal."""
    problemas = []
    texto_sin_comentarios = eliminar_comentarios(texto)

    for patron in REGISTRO_INFORMAL:
        for m in re.finditer(patron, texto_sin_comentarios, re.IGNORECASE):
            linea = texto_sin_comentarios[:m.start()].count("\n") + 1
            problemas.append(Problema(
                archivo=str(ruta.relative_to(RAIZ)),
                linea=linea,
                severidad="advertencia",
                categoria="Lenguaje",
                mensaje=f"Posible registro informal: `{m.group().strip()}`",
                sugerencia="Usar voz impersonal: 'se ha desarrollado', 'en este trabajo se propone'",
            ))

    return problemas


def analizar_estructura_global(archivos_tex: list) -> list:
    """Verifica que el documento tiene los capítulos esperados."""
    problemas = []
    nombres_archivos = [p.stem.lower() for p in archivos_tex]
    texto_total = " ".join(nombres_archivos)

    capitulos_encontrados = []
    for cap in CAPITULOS_ESPERADOS:
        if any(cap in nombre for nombre in nombres_archivos):
            capitulos_encontrados.append(cap)

    if "introduccion" not in texto_total and "introduction" not in texto_total:
        problemas.append(Problema(
            archivo="main.tex",
            linea=None,
            severidad="advertencia",
            categoria="Estructura",
            mensaje="No se detecta capítulo de introducción",
            sugerencia="Crear `contenido/capitulos/introduccion.tex` e incluirlo en `main.tex`",
        ))

    if "conclusiones" not in texto_total and "conclusions" not in texto_total:
        problemas.append(Problema(
            archivo="main.tex",
            linea=None,
            severidad="advertencia",
            categoria="Estructura",
            mensaje="No se detecta capítulo de conclusiones",
            sugerencia="Crear `contenido/capitulos/conclusiones.tex` e incluirlo en `main.tex`",
        ))

    return problemas


# ---------------------------------------------------------------------------
# API de plagio (opcional)
# ---------------------------------------------------------------------------

def verificar_plagio_copyleaks(texto: str, api_key: str) -> list:
    """
    Integración con Copyleaks API v3 (opt-in).

    Autentica con la cuenta Copyleaks y envía el documento para análisis.
    La API v3 es asíncrona (webhook): los resultados detallados llegan al
    endpoint configurado en el dashboard de Copyleaks o a COPYLEAKS_WEBHOOK_URL.

    Credencial en .env (formato email:clave-uuid):
        COPYLEAKS_API_KEY=email@dominio.com:00000000-0000-0000-0000-000000000000
    """
    import base64
    import json
    import uuid
    import urllib.request
    import urllib.error

    if ":" not in api_key:
        return [{
            "tipo": "error",
            "mensaje": "COPYLEAKS_API_KEY debe tener formato "
                       "'email@dominio.com:clave-uuid'",
        }]

    email, _, key = api_key.partition(":")

    try:
        # 1. Autenticación
        login_body = json.dumps({"email": email, "key": key}).encode()
        req = urllib.request.Request(
            "https://id.copyleaks.com/v3/account/login/api",
            data=login_body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            token = json.loads(resp.read().decode())["access_token"]

        # 2. Envío del documento
        scan_id = str(uuid.uuid4())
        text_b64 = base64.b64encode(texto.encode("utf-8")).decode()
        submit_body = json.dumps({
            "base64": text_b64,
            "filename": "tfg-tfm.txt",
            "properties": {
                "sandbox": False,
                "action": 0,
                "webhooks": {"status": "https://webhook.site/placeholder"},
            },
        }).encode()
        req = urllib.request.Request(
            f"https://api.copyleaks.com/v3/scans/submit/file/{scan_id}",
            data=submit_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            method="PUT",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            pass  # 200 OK

        return [{
            "tipo": "info",
            "mensaje": (
                f"Copyleaks: documento enviado (scan ID: {scan_id}). "
                "El análisis es asíncrono — ver resultados en "
                "https://app.copyleaks.com"
            ),
        }]

    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")[:200]
        return [{"tipo": "error", "mensaje": f"Copyleaks HTTP {e.code}: {detalle}"}]
    except Exception as e:
        return [{"tipo": "error", "mensaje": f"Error al conectar con Copyleaks: {e}"}]


def verificar_plagio_turnitin(texto: str, api_key: str, tenant_url: str) -> list:
    """
    Integración completa con Turnitin Core API v1 (opt-in).

    Crea la entrega, sube el contenido y obtiene el porcentaje de similitud
    mediante sondeo (polling). Requiere acceso institucional a Turnitin.

    Credenciales en .env:
        TURNITIN_API_KEY=tu-clave-de-api
        TURNITIN_TENANT_URL=https://tu-institucion.turnitin.com/api/v1
    """
    import json
    import time
    import urllib.request
    import urllib.error

    if not tenant_url:
        return [{
            "tipo": "error",
            "mensaje": (
                "Falta TURNITIN_TENANT_URL en .env "
                "(ej: https://tu-institucion.turnitin.com/api/v1)"
            ),
        }]

    base_url = tenant_url.rstrip("/")
    base_headers = {
        "Authorization": f"Bearer {api_key}",
        "X-Turnitin-Integration-Name": "TFG-TFM-EPS-UA",
        "X-Turnitin-Integration-Version": "2.1.0",
    }

    def _request(method: str, path: str, body=None, binary: bool = False) -> dict:
        url = f"{base_url}/{path.lstrip('/')}"
        headers = dict(base_headers)
        data = None
        if body is not None:
            if binary:
                headers["Content-Type"] = "binary/octet-stream"
                headers["Content-Disposition"] = 'inline; filename="tfg-tfm.txt"'
                data = body if isinstance(body, bytes) else body.encode("utf-8")
            else:
                headers["Content-Type"] = "application/json"
                data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}

    def _poll(method: str, path: str, campo: str, valor_ok: str,
              valor_error: str, intentos: int = 24, espera: int = 5) -> dict | None:
        for _ in range(intentos):
            time.sleep(espera)
            data = _request(method, path)
            if data.get(campo) == valor_ok:
                return data
            if data.get(campo) == valor_error:
                return None
        return None

    try:
        # 1. Crear entrega
        submission = _request("POST", "/submissions", {
            "owner": "student",
            "title": "TFG-TFM EPS UA",
            "submitter": "student",
            "owner_default_permission_set": "LEARNER",
            "submitter_default_permission_set": "INSTRUCTOR",
        })
        sid = submission["id"]

        # 2. Subir contenido
        _request("PUT", f"/submissions/{sid}/original", body=texto, binary=True)

        # 3. Esperar procesamiento de la entrega
        estado = _poll("GET", f"/submissions/{sid}", "status", "COMPLETE", "ERROR")
        if estado is None:
            return [{
                "tipo": "advertencia",
                "mensaje": (
                    f"Turnitin: tiempo de espera agotado (entrega ID: {sid}). "
                    "Consultar el panel de Turnitin para ver el resultado."
                ),
            }]

        # 4. Solicitar informe de similitud
        _request("PUT", f"/submissions/{sid}/similarity", {
            "generation_settings": {
                "search_repositories": ["SUBMITTED_WORK", "INTERNET", "PUBLICATION"],
                "auto_exclude_self_matching_scope": "ALL",
            }
        })

        # 5. Obtener informe de similitud
        sim = _poll("GET", f"/submissions/{sid}/similarity", "status", "COMPLETE", "ERROR")
        if sim is None:
            return [{
                "tipo": "advertencia",
                "mensaje": (
                    f"Turnitin: informe de similitud en curso (entrega ID: {sid}). "
                    "Consultar el panel de Turnitin."
                ),
            }]

        pct = sim.get("overall_match_percentage", 0)
        internet = sim.get("internet_match_percentage", "?")
        publicaciones = sim.get("publication_match_percentage", "?")
        trabajos = sim.get("submitted_works_match_percentage", "?")
        nivel = "error" if pct > 20 else "advertencia" if pct > 10 else "info"
        return [{
            "tipo": nivel,
            "mensaje": (
                f"Turnitin: similitud global {pct}% "
                f"(internet {internet}%, publicaciones {publicaciones}%, "
                f"trabajos previos {trabajos}%)"
            ),
        }]

    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")[:200]
        return [{"tipo": "error", "mensaje": f"Turnitin HTTP {e.code}: {detalle}"}]
    except Exception as e:
        return [{"tipo": "error", "mensaje": f"Error al conectar con Turnitin: {e}"}]


# ---------------------------------------------------------------------------
# Generación del informe
# ---------------------------------------------------------------------------

def generar_informe(problemas: list, env: dict, archivos_analizados: list, texto: str = "") -> str:
    """Genera el informe de revisión en formato Markdown."""
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    n_errores = sum(1 for p in problemas if p.severidad == "error")
    n_advertencias = sum(1 for p in problemas if p.severidad == "advertencia")
    n_info = sum(1 for p in problemas if p.severidad == "info")

    lineas = [
        "# Informe de revisión — TFG/TFM EPS UA",
        "",
        f"**Generado:** {ahora}  ",
        f"**Archivos analizados:** {len(archivos_analizados)}  ",
        f"**Problemas encontrados:** {n_errores} errores · {n_advertencias} advertencias · {n_info} informativo",
        "",
        "---",
        "",
    ]

    # Resumen ejecutivo
    if n_errores == 0 and n_advertencias == 0:
        lineas += [
            "## Resumen",
            "",
            "✅ No se encontraron errores ni advertencias en el análisis estático.",
            "",
        ]
    else:
        lineas += [
            "## Resumen",
            "",
            "| Severidad | Cantidad |",
            "|---|---|",
            f"| ❌ Errores | {n_errores} |",
            f"| ⚠️ Advertencias | {n_advertencias} |",
            f"| ℹ️ Informativos | {n_info} |",
            "",
        ]

    # Agrupar por categoría
    por_categoria = defaultdict(list)
    for p in problemas:
        por_categoria[p.categoria].append(p)

    orden_categorias = [
        "Estructura", "Formato LaTeX", "Referencias", "Figuras/Tablas",
        "Bibliografía", "Lenguaje", "Plagio (API)"
    ]
    categorias_ordenadas = orden_categorias + [
        c for c in por_categoria if c not in orden_categorias
    ]

    for categoria in categorias_ordenadas:
        if categoria not in por_categoria:
            continue
        items = por_categoria[categoria]
        n_err = sum(1 for p in items if p.severidad == "error")
        n_adv = sum(1 for p in items if p.severidad == "advertencia")
        resumen_cat = []
        if n_err:
            resumen_cat.append(f"{n_err} error{'es' if n_err > 1 else ''}")
        if n_adv:
            resumen_cat.append(f"{n_adv} advertencia{'s' if n_adv > 1 else ''}")
        sufijo = f" ({', '.join(resumen_cat)})" if resumen_cat else ""

        lineas += [
            f"## {categoria}{sufijo}",
            "",
        ]
        for p in items:
            lineas.append(str(p))
            lineas.append("")

    # Plagio por API
    copyleaks_key = env.get("COPYLEAKS_API_KEY")
    turnitin_key = env.get("TURNITIN_API_KEY")
    turnitin_tenant = env.get("TURNITIN_TENANT_URL", "")

    if copyleaks_key or turnitin_key:
        lineas += ["## Plagio (API)", ""]
        if copyleaks_key:
            resultados = verificar_plagio_copyleaks(texto, copyleaks_key)
            for r in resultados:
                icono = "ℹ️" if r["tipo"] == "info" else "❌"
                lineas.append(f"{icono} {r['mensaje']}")
                lineas.append("")
        if turnitin_key:
            resultados = verificar_plagio_turnitin(texto, turnitin_key, turnitin_tenant)
            for r in resultados:
                icono = "ℹ️" if r["tipo"] == "info" else "❌"
                lineas.append(f"{icono} {r['mensaje']}")
                lineas.append("")
    else:
        lineas += [
            "## Plagio (API)",
            "",
            "ℹ️ No se ha configurado ninguna API de detección de plagio.",
            "",
            "Para activar la verificación externa, crear un archivo `.env` en la raíz del proyecto con:",
            "```text",
            "# Copyleaks — formato email:clave-uuid",
            "COPYLEAKS_API_KEY=email@dominio.com:00000000-0000-0000-0000-000000000000",
            "",
            "# Turnitin — requiere acceso institucional",
            "TURNITIN_API_KEY=tu-clave-de-api",
            "TURNITIN_TENANT_URL=https://tu-institucion.turnitin.com/api/v1",
            "```",
            "",
            "El archivo `.env` ya está en `.gitignore` y no se subirá al repositorio.",
            "",
        ]

    # Archivos analizados
    lineas += [
        "---",
        "",
        "## Archivos analizados",
        "",
    ]
    for ruta in sorted(archivos_analizados):
        lineas.append(f"- `{ruta}`")
    lineas.append("")
    lineas += [
        "---",
        "",
        "*Generado por `scripts/revision-rapida.py`. "
        "Para una revisión semántica completa (coherencia, lenguaje, plagio por IA), "
        "usar el agente revisor en GitHub Copilot Chat o Claude.*",
    ]

    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Revisión estática del documento TFG/TFM EPS UA"
    )
    parser.add_argument(
        "--solo-errores",
        action="store_true",
        help="Mostrar solo errores, omitir advertencias e informativos",
    )
    parser.add_argument(
        "--capitulo",
        type=str,
        default=None,
        help="Analizar solo un archivo .tex específico",
    )
    parser.add_argument(
        "--salida",
        type=str,
        default=str(INFORME_SALIDA),
        help=f"Ruta del informe de salida (por defecto: {INFORME_SALIDA})",
    )
    args = parser.parse_args()

    # Cargar variables de entorno
    env = cargar_env()

    # Determinar archivos a analizar
    if args.capitulo:
        archivos_tex = [Path(args.capitulo)]
        if not archivos_tex[0].exists():
            print(f"Error: no se encontró el archivo {args.capitulo}", file=sys.stderr)
            sys.exit(1)
    else:
        archivos_tex = sorted(
            list(CONTENIDO_DIR.rglob("*.tex"))
        )
        # Añadir main.tex para análisis de estructura
        main_tex = RAIZ / "main.tex"
        if main_tex.exists():
            archivos_tex.insert(0, main_tex)

    if not archivos_tex:
        print("No se encontraron archivos .tex para analizar.", file=sys.stderr)
        sys.exit(1)

    print(f"Analizando {len(archivos_tex)} archivo(s)...")

    todos_los_problemas = []

    # Análisis global (requiere todos los archivos)
    todos_los_problemas += analizar_estructura_global(archivos_tex)
    todos_los_problemas += analizar_referencias_cruzadas(archivos_tex)
    todos_los_problemas += analizar_bibliografia(archivos_tex)

    # Análisis por archivo
    for ruta in archivos_tex:
        if not ruta.exists():
            continue
        texto = leer_tex(ruta)
        if not texto.strip():
            continue

        todos_los_problemas += analizar_comandos_prohibidos(ruta, texto)
        todos_los_problemas += analizar_etiquetas(ruta, texto)
        todos_los_problemas += analizar_captions(ruta, texto)
        todos_los_problemas += analizar_secciones_vacias(ruta, texto)
        todos_los_problemas += analizar_registro_informal(ruta, texto)

    # Filtrar si --solo-errores
    if args.solo_errores:
        todos_los_problemas = [p for p in todos_los_problemas if p.severidad == "error"]

    # Extraer texto plano para APIs externas de plagio
    texto_plano = extraer_texto_plano(archivos_tex)

    # Generar informe
    archivos_rel = [str(r.relative_to(RAIZ)) for r in archivos_tex if r.exists()]
    informe = generar_informe(todos_los_problemas, env, archivos_rel, texto_plano)

    # Guardar informe
    salida = Path(args.salida)
    salida.write_text(informe, encoding="utf-8")
    print(f"Informe guardado en: {salida}")

    # Resumen en consola
    n_err = sum(1 for p in todos_los_problemas if p.severidad == "error")
    n_adv = sum(1 for p in todos_los_problemas if p.severidad == "advertencia")
    n_inf = sum(1 for p in todos_los_problemas if p.severidad == "info")
    print(f"Resultado: {n_err} errores · {n_adv} advertencias · {n_inf} informativos")

    # Salir con código de error si hay errores
    sys.exit(1 if n_err > 0 else 0)


if __name__ == "__main__":
    main()
