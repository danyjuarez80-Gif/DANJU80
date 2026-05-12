import requests
from playwright.sync_api import sync_playwright

# URL de tu lista en GitHub
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

# Lista de canales (puedes seguir agregando según necesites)
CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "TNT Sports", "slug": "tntsports"},
    {"nombre": "ESPN Mexico", "slug": "espnmexico"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
    {"nombre": "Azteca 7", "slug": "azteca7"},
    {"nombre": "Canal 5", "slug": "canal5"},
]

def capturar_m3u8(page, url_inicial):
    """Navega al PHP, detecta el iframe y captura el tráfico m3u8."""
    capturados = []

    def on_request(request):
        url = request.url
        # Filtramos por extension m3u8 y que contenga tokens comunes
        if ".m3u8" in url and ("token=" in url or "index" in url):
            capturados.append(url)

    page.on("request", on_request)
    
    try:
        # 1. Cargar la página principal del canal
        page.goto(url_inicial, timeout=30000, wait_until="networkidle")
        
        # 2. Intentar saltar al iframe (donde Claude decía que estaba el m3u8)
        iframe_element = page.query_selector("iframe")
        if iframe_element:
            iframe_url = iframe_element.get_attribute("src")
            if iframe_url:
                if iframe_url.startswith("/"):
                    iframe_url = f"{BASE_EMBED}{iframe_url}"
                elif not iframe_url.startswith("http"):
                    iframe_url = f"{BASE_EMBED}/{iframe_url}"
                
                print(f"  -> Navegando al iframe interno: {iframe_url}")
                page.goto(iframe_url, timeout=30000, wait_until="networkidle")
        
        # Tiempo de espera para que el reproductor inicie y genere el tráfico
        page.wait_for_timeout(7000)
        
    except Exception as e:
        print(f"  Error en navegación: {e}")
    
    page.remove_listener("request", on_request)
    return capturados[0] if capturados else None

def obtener_lista_base():
    try:
        r = requests.get(URL_FUENTE, timeout=20)
        if r.status_code == 200: return r.text
    except: pass
    return ""

def generar_lista():
    lista_base = obtener_lista_base()
    canales_vistos = set()
    lineas_base = []

    # Procesar lista actual para no duplicar
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
        else: i += 1

    nuevos_canales = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
            url_php = f"{BASE_EMBED}/{canal['slug']}.php"
            print(f"📺 Buscando: {canal['nombre']}...")
            m3u8 = capturar_m3u8(page, url_php)
            
            if m3u8 and m3u8 not in canales_vistos:
                nuevos_canales.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                nuevos_canales.append(m3u8)
                canales_vistos.add(m3u8)
                print(f"  ✅ OK")
            else:
                print(f"  ❌ No capturado / Duplicado")

        browser.close()

    # Guardar archivo m3u
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for linea in lineas_base: f.write(linea + "\n")
        if nuevos_canales:
            f.write("\n")
            for linea in nuevos_canales: f.write(linea + "\n")

    print(f"\nFinalizado. Total canales: {len(canales_vistos)}")

if __name__ == "__main__":
    generar_lista()
