import requests
import re
from playwright.sync_api import sync_playwright

# URL de tu archivo base en GitHub
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

# Canales para extraer (puedes añadir más siguiendo este formato)
CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN 2 HD", "slug": "espn2"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
    {"nombre": "Azteca 7", "slug": "azteca7"},
    {"nombre": "Canal 5", "slug": "canal5"},
]

def capturar_con_clic(page, url_canal):
    enlaces = []
    # Escuchamos el tráfico de red para atrapar el m3u8 tras el clic
    page.on("request", lambda req: enlaces.append(req.url) if ".m3u8" in req.url else None)

    try:
        page.goto(url_canal, timeout=60000, wait_until="networkidle")
        
        # Localizamos el iframe del reproductor
        iframe = page.query_selector("iframe")
        if iframe:
            src = iframe.get_attribute("src")
            target = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
            print(f"  -> Accediendo al reproductor: {target}")
            page.goto(target, timeout=60000, wait_until="domcontentloaded")
            
            # Esperamos a que cargue el botón de Play
            page.wait_for_timeout(5000)
            
            # Intentamos hacer clic en el video o botones de inicio
            for selector in ["video", "button.vjs-big-play-button", ".play-button", "#player"]:
                if page.query_selector(selector):
                    print(f"  -> Haciendo clic para activar stream...")
                    page.click(selector, force=True)
                    break
            
            # Tiempo para que el servidor suelte el enlace tras el clic
            page.wait_for_timeout(10000)

    except Exception as e:
        print(f"  Error: {e}")
    
    return enlaces[0] if enlaces else None

def generar_lista():
    # Leemos tu archivo DANJU80 para saber qué canales ya tienes
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        base_raw = r.text if r.status_code == 200 else ""
    except:
        base_raw = ""

    vistos = set(re.findall(r'https?://[^\s]+', base_raw))
    nuevos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
            print(f"📺 Procesando {canal['nombre']}...")
            m3u8 = capturar_con_clic(page, f"{BASE_EMBED}/{canal['slug']}.php")
            
            if m3u8:
                link_limpio = m3u8.split("'")[0].split('"')[0]
                if link_limpio not in vistos:
                    nuevos.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                    nuevos.append(link_limpio)
                    vistos.add(link_limpio)
                    print(f"  ✅ Enlace capturado")
                else:
                    print(f"  ✅ Ya actualizado")
            else:
                print(f"  ❌ No se detectó enlace")

        browser.close()

    # Guardamos el resultado en lista_dany.m3u
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        if base_raw:
            f.write(base_raw.replace("#EXTM3U", "").strip() + "\n\n")
        for n in nuevos:
            f.write(n + "\n")
    print("\n✅ Archivo lista_dany.m3u actualizado.")

if __name__ == "__main__":
    generar_lista()
