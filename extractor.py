import requests
import re
from playwright.sync_api import sync_playwright

# URL base del m3u existente en GitHub
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

# Paginas de cada canal — el script extrae el PHP link real automaticamente
CANALES = [
    {"nombre": "ESPN",                   "pagina": "https://www.tvplusgratis2.com/espn-en-vivo.html"},
    {"nombre": "ESPN 2",                 "pagina": "https://www.tvplusgratis2.com/espn-2-en-vivo.html"},
    {"nombre": "ESPN 3",                 "pagina": "https://www.tvplusgratis2.com/espn-3-en-vivo.html"},
    {"nombre": "ESPN 4",                 "pagina": "https://www.tvplusgratis2.com/espn-4-en-vivo.html"},
    {"nombre": "ESPN Premium",           "pagina": "https://www.tvplusgratis2.com/espn-premium-en-vivo.html"},
    {"nombre": "ESPN Mexico",            "pagina": "https://www.tvplusgratis2.com/espn-mexico-en-vivo.html"},
    {"nombre": "ESPN 2 Mexico",          "pagina": "https://www.tvplusgratis2.com/espn-2-mexico-en-vivo.html"},
    {"nombre": "ESPN 3 Mexico",          "pagina": "https://www.tvplusgratis2.com/espn-3-mexico-en-vivo.html"},
    {"nombre": "Fox Sports",             "pagina": "https://www.tvplusgratis2.com/fox-sports-en-vivo.html"},
    {"nombre": "Fox Sports 2",           "pagina": "https://www.tvplusgratis2.com/fox-sports-2-en-vivo.html"},
    {"nombre": "Fox Sports 3",           "pagina": "https://www.tvplusgratis2.com/fox-sports-3-en-vivo.html"},
    {"nombre": "Fox Sports Mexico",      "pagina": "https://www.tvplusgratis2.com/fox-sports-mexico-en-vivo.html"},
    {"nombre": "Fox Sports 2 Mexico",    "pagina": "https://www.tvplusgratis2.com/fox-sports-2-mexico-en-vivo.html"},
    {"nombre": "Fox Sports 3 Mexico",    "pagina": "https://www.tvplusgratis2.com/fox-sports-3-mexico-en-vivo.html"},
    {"nombre": "Fox Sports Premium",     "pagina": "https://www.tvplusgratis2.com/fox-sports-premium-en-vivo.html"},
    {"nombre": "DirecTV Sports",         "pagina": "https://www.tvplusgratis2.com/directv-sports-en-vivo.html"},
    {"nombre": "DirecTV Sports 2",       "pagina": "https://www.tvplusgratis2.com/directv-sports-2-en-vivo.html"},
    {"nombre": "DirecTV Sports Plus",    "pagina": "https://www.tvplusgratis2.com/directv-sports-plus-en-vivo.html"},
    {"nombre": "TNT Sports",             "pagina": "https://www.tvplusgratis2.com/tnt-sports-en-vivo.html"},
    {"nombre": "TNT Sports Chile",       "pagina": "https://www.tvplusgratis2.com/tnt-sports-chile-en-vivo.html"},
    {"nombre": "TUDN",                   "pagina": "https://www.tvplusgratis2.com/tudn-en-vivo.html"},
    {"nombre": "Liga 1",                 "pagina": "https://www.tvplusgratis2.com/liga-1-en-vivo.html"},
    {"nombre": "Liga 1 Max",             "pagina": "https://www.tvplusgratis2.com/liga-1-max-en-vivo.html"},
    {"nombre": "TyC Sports",             "pagina": "https://www.tvplusgratis2.com/tyc-sports-en-vivo.html"},
    {"nombre": "DAZN F1",                "pagina": "https://www.tvplusgratis2.com/dazn-f1-en-vivo.html"},
    {"nombre": "DAZN La Liga",           "pagina": "https://www.tvplusgratis2.com/dazn-la-liga-en-vivo.html"},
    {"nombre": "Sky Sports La Liga",     "pagina": "https://www.tvplusgratis2.com/sky-sports-la-liga-en-vivo.html"},
    {"nombre": "Telemundo 51",           "pagina": "https://www.tvplusgratis2.com/telemundo-51-en-vivo.html"},
    {"nombre": "Telemundo Puerto Rico",  "pagina": "https://www.tvplusgratis2.com/telemundo-puerto-rico-en-vivo.html"},
    {"nombre": "Telemundo Internacional","pagina": "https://www.tvplusgratis2.com/telemundo-internacional-en-vivo.html"},
    {"nombre": "Azteca 7",               "pagina": "https://www.tvplusgratis2.com/azteca-7-en-vivo.html"},
    {"nombre": "Canal 5 Mexico",         "pagina": "https://www.tvplusgratis2.com/canal-5-mexico-en-vivo.html"},
    {"nombre": "America TV",             "pagina": "https://www.tvplusgratis2.com/america-tv-en-vivo.html"},
    {"nombre": "Latina",                 "pagina": "https://www.tvplusgratis2.com/latina-en-vivo.html"},
    {"nombre": "Antena 3",               "pagina": "https://www.tvplusgratis2.com/antena-3-en-vivo.html"},
]


def obtener_php_opcion1(page, url_pagina):
    """Visita la pagina del canal con requests simple y extrae la Opcion 1 PHP."""
    try:
        r = requests.get(url_pagina, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        })
        # Buscar primer link live/*.php
        match = re.search(r'https://www\.tvplusgratis2\.com/live/[^"\']+\.php', r.text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"  Error obteniendo PHP: {e}")
    return None


def capturar_m3u8(page, url_php):
    """Abre el PHP con Playwright e intercepta el m3u8."""
    capturados = []

    def on_request(request):
        if ".m3u8" in request.url and "token=" in request.url:
            capturados.append(request.url)

    page.on("request", on_request)
    try:
        page.goto(url_php, timeout=20000, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
    except Exception as e:
        print(f"  Error: {e}")
    page.remove_listener("request", on_request)
    return capturados[0] if capturados else None


def obtener_lista_base():
    try:
        r = requests.get(URL_FUENTE, timeout=20)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"Error descargando lista base: {e}")
    return ""


def generar_lista():
    lista_base = obtener_lista_base()
    canales_vistos = set()
    lineas_base = []

    # Procesar lista base eliminando duplicados
    lineas = lista_base.splitlines()
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            if i + 1 < len(lineas):
                url = lineas[i + 1].strip()
                if url not in canales_vistos:
                    lineas_base.append(linea)
                    lineas_base.append(url)
                    canales_vistos.add(url)
            i += 2
        else:
            i += 1

    # Primero obtener todos los PHP links con requests (rapido, sin Playwright)
    print("Obteniendo links PHP...")
    canales_con_php = []
    for canal in CANALES:
        php = obtener_php_opcion1(None, canal["pagina"])
        if php:
            canales_con_php.append({"nombre": canal["nombre"], "php": php})
            print(f"  ✅ {canal['nombre']}: {php}")
        else:
            print(f"  ❌ {canal['nombre']}: no encontrado")

    # Luego capturar m3u8 con Playwright solo para los que tienen PHP
    nuevos_canales = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
        page = context.new_page()

        for canal in canales_con_php:
            print(f"📺 {canal['nombre']}...")
            m3u8 = capturar_m3u8(page, canal["php"])
            if m3u8 and m3u8 not in canales_vistos:
                nuevos_canales.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                nuevos_canales.append(m3u8)
                canales_vistos.add(m3u8)
                print(f"  ✅ OK")
            elif m3u8:
                print(f"  ⚠️ Duplicado")
            else:
                print(f"  ❌ Sin m3u8")

        browser.close()

    # Escribir lista final
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for linea in lineas_base:
            f.write(linea + "\n")
        if nuevos_canales:
            f.write("\n")
            for linea in nuevos_canales:
                f.write(linea + "\n")

    print(f"\n✅ Lista generada. Total canales unicos: {len(canales_vistos)}")


if __name__ == "__main__":
    generar_lista()
