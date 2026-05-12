import requests
import re
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

# Lista simplificada para pruebas (luego añade los demás)
CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN Mexico", "slug": "espnmexico"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
]

def capturar_m3u8(page, url_inicial):
    capturados = []

    def on_request(request):
        url = request.url
        if ".m3u8" in url and ("token=" in url or "index" in url or "playlist" in url):
            capturados.append(url)

    page.on("request", on_request)
    
    try:
        # Navegación con tiempo de espera extendido
        page.goto(url_inicial, timeout=60000, wait_until="domcontentloaded")
        
        # BUSQUEDA DE IFRAME DINÁMICA
        # Intentamos encontrar cualquier iframe que parezca contener el video
        iframes = page.query_selector_all("iframe")
        for frame in iframes:
            src = frame.get_attribute("src")
            if src and ("embed" in src or "php" in src):
                target_url = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
                print(f"  -> Entrando a: {target_url}")
                page.goto(target_url, timeout=60000, wait_until="networkidle")
                break
        
        # Espera agresiva para que cargue el reproductor
        page.wait_for_timeout(10000)
        
        # TRUCO EXTRA: Si no capturó por red, buscamos en el HTML
        if not capturados:
            content = page.content()
            match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', content)
            if match:
                capturados.append(match.group(1))

    except Exception as e:
        print(f"  Error: {e}")
    
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
        # Lanzamos con argumentos para evitar detecciones de bots
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
            url_php = f"{BASE_EMBED}/{canal['slug']}.php"
            print(f"📺 {canal['nombre']}...")
            m3u8 = capturar_m3u8(page, url_php)
            
            if m3u8:
                # Limpiar el m3u8 de posibles caracteres extra
                m3u8 = m3u8.split("'")[0].split('"')[0]
                if m3u8 not in canales_vistos:
                    nuevos_canales.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                    nuevos_canales.append(m3u8)
                    canales_vistos.add(m3u8)
                    print(f"  ✅ CAPTURADO")
                else: print(f"  ⚠️ Ya lo tengo")
            else: print(f"  ❌ Fallo total")

        browser.close()

    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for linea in lineas_base: f.write(linea + "\n")
        if nuevos_canales:
            f.write("\n")
            for linea in nuevos_canales: f.write(linea + "\n")

if __name__ == "__main__":
    generar_lista()
