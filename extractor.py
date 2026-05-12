import requests
import re
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

# Lista simplificada para asegurar que capture estos primero
CANALES = [
    {"nombre": "TUDN HD", "slug": "tudn"},
    {"nombre": "ESPN 2 HD", "slug": "espn2"},
    {"nombre": "FOX SPORTS PREMIUM", "slug": "foxsportspremium"},
    {"nombre": "AZTECA 7", "slug": "azteca7"},
    {"nombre": "CANAL 5", "slug": "canal5"},
]

def capturar_con_clic_agresivo(page, url_canal):
    enlaces = []
    # Sniffer de red para atrapar el m3u8 apenas se genere
    page.on("request", lambda req: enlaces.append(req.url) if ".m3u8" in req.url else None)

    try:
        # Cargamos el PHP
        page.goto(url_canal, timeout=60000, wait_until="networkidle")
        
        # Localizar iframe y navegar a él directamente
        iframe = page.query_selector("iframe")
        if iframe:
            src = iframe.get_attribute("src")
            target = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
            page.goto(target, timeout=60000, wait_until="domcontentloaded")
            
            # Espera para que aparezca el botón de play
            page.wait_for_timeout(7000)
            
            # Forzamos el clic en el centro del reproductor o botón play
            for selector in ["video", "button", ".play-button", ".vjs-big-play-button"]:
                if page.query_selector(selector):
                    page.click(selector, force=True)
                    break
            
            # Espera crucial: Web Video Caster tarda unos segundos en capturar, nosotros igual
            page.wait_for_timeout(15000)
    except:
        pass
    
    return enlaces[0] if enlaces else None

def generar_lista():
    # 1. Leer lo que tienes en DANJU80 actualmente
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        contenido_base = r.text if r.status_code == 200 else ""
    except:
        contenido_base = ""

    nuevos_capturados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # CONFIGURACIÓN MÓVIL: Imita un Android para saltar bloqueos
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
            viewport={'width': 360, 'height': 800},
            is_mobile=True
        )
        page = context.new_page()

        for canal in CANALES:
            print(f"📡 Intentando capturar: {canal['nombre']}...")
            url = f"{BASE_EMBED}/{canal['slug']}.php"
            m3u8 = capturar_con_clic_agresivo(page, url)
            
            if m3u8:
                # Limpiar el link de comillas o basura
                link_final = m3u8.split("'")[0].split('"')[0]
                nuevos_capturados.append(f'#EXTINF:-1 group-title="DEPORTES AUTO",{canal["nombre"]}')
                nuevos_capturados.append(link_final)
                print(f"  ✅ Capturado: {link_final[:50]}...")
            else:
                print(f"  ❌ El servidor no soltó el link")

        browser.close()

    # 2. ESCRIBIR EL ARCHIVO FINAL (lista_dany.m3u)
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        
        # Pegamos tus canales manuales de DANJU80 primero
        if contenido_base:
            f.write("### TUS CANALES (DANJU80) ###\n")
            f.write(contenido_base.replace("#EXTM3U", "").strip() + "\n\n")
        
        # Pegamos los canales que el bot encontró
        if nuevos_capturados:
            f.write("### ACTUALIZADOS POR EL BOT ###\n")
            for linea in nuevos_capturados:
                f.write(linea + "\n")
        else:
            f.write("### EL BOT NO ENCONTRÓ ENLACES NUEVOS EN ESTA VUELTA ###\n")

    print("\n✅ Archivo editado y guardado.")

if __name__ == "__main__":
    generar_lista()
