import requests
import re
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN 2 HD", "slug": "espn2"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
    {"nombre": "Azteca 7", "slug": "azteca7"},
    {"nombre": "Canal 5", "slug": "canal5"},
]

def capturar_flujo_dinamico(page, url_canal):
    enlaces_detectados = []
    
    # Escucha de red tipo "sniffer" (como hace Web Video Caster)
    def detectar(request):
        u = request.url
        if ".m3u8" in u and ("token=" in u or "index" in u or "/hls/" in u):
            enlaces_detectados.append(u)

    page.on("request", detectar)

    try:
        # Entramos con identidad de Android
        page.goto(url_canal, timeout=60000, wait_until="networkidle")
        
        iframe = page.query_selector("iframe")
        if iframe:
            src = iframe.get_attribute("src")
            target = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
            print(f"  -> Abriendo reproductor: {target}")
            
            page.goto(target, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            
            # Forzamos el inicio del video para que suelte el m3u8
            for s in ["video", ".vjs-big-play-button", "button", "#player"]:
                if page.query_selector(s):
                    page.click(s, force=True)
                    break
            
            # Espera activa para capturar el tráfico
            page.wait_for_timeout(12000)
    except Exception as e:
        print(f"  Aviso: {e}")
    
    return enlaces_detectados[0] if enlaces_detectados else None

def generar_lista():
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        base_raw = r.text if r.status_code == 200 else ""
    except:
        base_raw = ""

    vistos = set(re.findall(r'https?://[^\s]+', base_raw))
    nuevos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # CONFIGURACIÓN MÓVIL (Clave para que funcione como Web Video Caster)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 12; SM-S906B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36",
            viewport={'width': 360, 'height': 800},
            is_mobile=True
        )
        page = context.new_page()

        for canal in CANALES:
            print(f"📺 Extrayendo {canal['nombre']}...")
            url = f"{BASE_EMBED}/{canal['slug']}.php"
            m3u8 = capturar_flujo_dinamico(page, url)
            
            if m3u8:
                limpio = m3u8.split("'")[0].split('"')[0]
                if limpio not in vistos:
                    nuevos.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                    nuevos.append(limpio)
                    vistos.add(limpio)
                    print(f"  ✅ Enlace obtenido")
                else:
                    print(f"  ⚠️ Ya estaba en DANJU80")
            else:
                print(f"  ❌ No se pudo extraer automáticamente")

        browser.close()

    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        if base_raw:
            f.write(base_raw.replace("#EXTM3U", "").strip() + "\n\n")
        for n in nuevos:
            f.write(n + "\n")
    print("\n✅ Proceso terminado.")

if __name__ == "__main__":
    generar_lista()
