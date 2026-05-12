import requests
from playwright.sync_api import sync_playwright

# URL base del m3u existente en GitHub
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

BASE_EMBED = "https://embed.ksdjugfsddeports.com"

# Canales con slugs reales de embed.ksdjugfsddeports.com
CANALES = [
    # DEPORTES
    {"nombre": "TUDN",                  "slug": "tudn"},
    {"nombre": "TNT Sports",            "slug": "tntsports"},
    {"nombre": "TNT Sports Chile",      "slug": "tntsportschile"},
    {"nombre": "ESPN Premium",          "slug": "espnpremium"},
    {"nombre": "TyC Sports",            "slug": "tycsports"},
    {"nombre": "Fox Sports",            "slug": "foxsports"},
    {"nombre": "Fox Sports 2",          "slug": "foxsports2"},
    {"nombre": "Fox Sports 3",          "slug": "foxsports3"},
    {"nombre": "Fox Sports Premium",    "slug": "foxsportspremium"},
    {"nombre": "Fox Sports Mexico",     "slug": "foxsportsmexico"},
    {"nombre": "Fox Sports 2 Mexico",   "slug": "foxsports2mexico"},
    {"nombre": "Fox Sports 3 Mexico",   "slug": "foxsports3mexico"},
    {"nombre": "ESPN",                  "slug": "espn"},
    {"nombre": "ESPN 2",                "slug": "espn2"},
    {"nombre": "ESPN 3",                "slug": "espn3"},
    {"nombre": "ESPN 4",                "slug": "espn4"},
    {"nombre": "ESPN Mexico",           "slug": "espnmexico"},
    {"nombre": "ESPN 2 Mexico",         "slug": "espn2mexico"},
    {"nombre": "ESPN 3 Mexico",         "slug": "espn3mexico"},
    {"nombre": "DirecTV Sports",        "slug": "directvsports"},
    {"nombre": "DirecTV Sports 2",      "slug": "directvsports2"},
    {"nombre": "DirecTV Sports Plus",   "slug": "directvsportsplus"},
    {"nombre": "Liga 1",                "slug": "liga1"},
    {"nombre": "Liga 1 Max",            "slug": "liga1max"},
    {"nombre": "DAZN F1",               "slug": "daznf1"},
    {"nombre": "DAZN La Liga",          "slug": "daznlaliga"},
    {"nombre": "Sky Sports Mexico",     "slug": "skysportsmexico"},
    {"nombre": "Azteca Deportes",       "slug": "aztecadeportes"},
    # REGIONALES
    {"nombre": "Azteca 7",              "slug": "azteca7"},
    {"nombre": "Canal 5",               "slug": "canal5"},
    {"nombre": "Latina",                "slug": "latina"},
    {"nombre": "America TV",            "slug": "americatv"},
    {"nombre": "Telemundo Miami",       "slug": "telemundo51"},
    {"nombre": "Telemundo Puerto Rico", "slug": "telemundopuertorico"},
    {"nombre": "Antena 3",              "slug": "antena3"},
    {"nombre": "Univision",             "slug": "univision"},
    {"nombre": "Galavision",            "slug": "galavision"},
    {"nombre": "Las Estrellas",         "slug": "lasestrellas"},
    {"nombre": "Azteca Uno",            "slug": "aztecauno"},
    {"nombre": "Unicable",              "slug": "unicable"},
    {"nombre": "RCN",                   "slug": "rcn"},
    {"nombre": "Caracol",               "slug": "caracol"},
]


def capturar_m3u8(page, url_php):
    """Abre el PHP con Playwright e intercepta el m3u8."""
    capturados = []

    def on_request(request):
        url = request.url
        if ".m3u8" in url and ("token=" in url or "index" in url):
            capturados.append(url)

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

    # Scrapear con Playwright desde embed directo
    nuevos_canales = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
            url_php = f"{BASE_EMBED}/{canal['slug']}.php"
            print(f"📺 {canal['nombre']}...")
            m3u8 = capturar_m3u8(page, url_php)
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
