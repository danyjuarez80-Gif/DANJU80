import requests
from playwright.sync_api import sync_playwright

# URL base del m3u existente en GitHub
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

# Todos los canales - solo Opcion 1 (live/slug.php)
CANALES = [
    {"nombre": "ESPN",                   "php": "https://www.tvplusgratis2.com/live/espn.php"},
    {"nombre": "ESPN 2",                 "php": "https://www.tvplusgratis2.com/live/espn2.php"},
    {"nombre": "ESPN 3",                 "php": "https://www.tvplusgratis2.com/live/espn3.php"},
    {"nombre": "ESPN 4",                 "php": "https://www.tvplusgratis2.com/live/espn4.php"},
    {"nombre": "ESPN Premium",           "php": "https://www.tvplusgratis2.com/live/espnpremium.php"},
    {"nombre": "ESPN Mexico",            "php": "https://www.tvplusgratis2.com/live/espnmexico.php"},
    {"nombre": "ESPN 2 Mexico",          "php": "https://www.tvplusgratis2.com/live/espn2mexico.php"},
    {"nombre": "ESPN 3 Mexico",          "php": "https://www.tvplusgratis2.com/live/espn3mexico.php"},
    {"nombre": "Fox Sports",             "php": "https://www.tvplusgratis2.com/live/foxsports.php"},
    {"nombre": "Fox Sports 2",           "php": "https://www.tvplusgratis2.com/live/foxsports2.php"},
    {"nombre": "Fox Sports 3",           "php": "https://www.tvplusgratis2.com/live/foxsports3.php"},
    {"nombre": "Fox Sports Mexico",      "php": "https://www.tvplusgratis2.com/live/foxsportsmx.php"},
    {"nombre": "Fox Sports 2 Mexico",    "php": "https://www.tvplusgratis2.com/live/foxsports2mx.php"},
    {"nombre": "Fox Sports 3 Mexico",    "php": "https://www.tvplusgratis2.com/live/foxsports3mx.php"},
    {"nombre": "Fox Sports Premium",     "php": "https://www.tvplusgratis2.com/live/foxsportspremium.php"},
    {"nombre": "DirecTV Sports",         "php": "https://www.tvplusgratis2.com/live/directvsports.php"},
    {"nombre": "DirecTV Sports 2",       "php": "https://www.tvplusgratis2.com/live/directvsports2.php"},
    {"nombre": "DirecTV Sports Plus",    "php": "https://www.tvplusgratis2.com/live/directvsportsplus.php"},
    {"nombre": "TNT Sports",             "php": "https://www.tvplusgratis2.com/live/tntsports.php"},
    {"nombre": "TNT Sports Chile",       "php": "https://www.tvplusgratis2.com/live/tntsportschile.php"},
    {"nombre": "TUDN",                   "php": "https://www.tvplusgratis2.com/live/tudn.php"},
    {"nombre": "Liga 1",                 "php": "https://www.tvplusgratis2.com/live/liga1.php"},
    {"nombre": "Liga 1 Max",             "php": "https://www.tvplusgratis2.com/live/liga1max.php"},
    {"nombre": "TyC Sports",             "php": "https://www.tvplusgratis2.com/live/tycsports.php"},
    {"nombre": "DAZN F1",                "php": "https://www.tvplusgratis2.com/live/daznf1.php"},
    {"nombre": "DAZN La Liga",           "php": "https://www.tvplusgratis2.com/live/daznlaliga.php"},
    {"nombre": "Sky Sports La Liga",     "php": "https://www.tvplusgratis2.com/live/skysportslaliga.php"},
    {"nombre": "Telemundo 51",           "php": "https://www.tvplusgratis2.com/live/telemundo51.php"},
    {"nombre": "Telemundo Puerto Rico",  "php": "https://www.tvplusgratis2.com/live/telemundopr.php"},
    {"nombre": "Telemundo Internacional","php": "https://www.tvplusgratis2.com/live/telemundoint.php"},
    {"nombre": "Azteca 7",               "php": "https://www.tvplusgratis2.com/live/azteca7.php"},
    {"nombre": "Canal 5 Mexico",         "php": "https://www.tvplusgratis2.com/live/canal5mexico.php"},
    {"nombre": "America TV",             "php": "https://www.tvplusgratis2.com/live/americatv.php"},
    {"nombre": "Latina",                 "php": "https://www.tvplusgratis2.com/live/latina.php"},
    {"nombre": "Antena 3",               "php": "https://www.tvplusgratis2.com/live/antena3.php"},
]


def capturar_m3u8(page, url_php):
    """Abre el PHP e intercepta el m3u8."""
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

    # Scrapear solo Opcion 1 de cada canal
    nuevos_canales = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
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
