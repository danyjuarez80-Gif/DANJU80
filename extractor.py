import requests
import re
from playwright.sync_api import sync_playwright

# URL de tu archivo base
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN 2 HD", "slug": "espn2"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
    {"nombre": "Azteca 7", "slug": "azteca7"},
    {"nombre": "Canal 5", "slug": "canal5"},
]

def capturar_con_interaccion(page, url_canal):
    enlaces = []
    page.on("request", lambda req: enlaces.append(req.url) if ".m3u8" in req.url else None)
    try:
        page.goto(url_canal, timeout=60000, wait_until="networkidle")
        iframe = page.query_selector("iframe")
        if iframe:
            src = iframe.get_attribute("src")
            target = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
            page.goto(target, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            # Clic forzado para activar el m3u8
            for selector in ["video", "button.vjs-big-play-button", ".play-button", "#player"]:
                if page.query_selector(selector):
                    page.click(selector, force=True)
                    break
            page.wait_for_timeout(10000)
    except:
        pass
    return enlaces[0] if enlaces else None

def generar_lista():
    # 1. Obtener el contenido actual de DANJU80
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        contenido_actual = r.text if r.status_code == 200 else ""
    except:
        contenido_actual = ""

    # Separamos el contenido por líneas y quitamos la cabecera #EXTM3U para no repetirla
    lineas_viejas = [l for l in contenido_actual.splitlines() if l.strip() and not l.startswith("#EXTM3U")]
    
    nuevos_enlaces = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Mobile Safari/537.36")
        page = context.new_page()

        for canal in CANALES:
            print(f"📺 Extrayendo: {canal['nombre']}...")
            m3u8 = capturar_con_interaccion(page, f"{BASE_EMBED}/{canal['slug']}.php")
            if m3u8:
                link = m3u8.split("'")[0].split('"')[0]
                nuevos_enlaces.append(f'#EXTINF:-1 group-title="Auto-Update",{canal["nombre"]}')
                nuevos_enlaces.append(link)
                print(f"  ✅ Encontrado")
            else:
                print(f"  ❌ No capturado")
        browser.close()

    # 2. ESCRIBIR EL ARCHIVO (Aquí es donde estaba el problema)
    # Combinamos: Cabecera + Contenido de DANJU80 + Enlaces nuevos
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        
        # Escribimos lo que ya tenías en DANJU80 tal cual
        if lineas_viejas:
            f.write("### CANALES MANUALES (DANJU80) ###\n")
            for linea in lineas_viejas:
                f.write(linea + "\n")
            f.write("\n")
            
        # Añadimos lo que el bot acaba de encontrar
        if nuevos_enlaces:
            f.write("### CANALES AUTOMATICOS ###\n")
            for linea in nuevos_enlaces:
                f.write(linea + "\n")

    print("\n✅ Archivo lista_dany.m3u generado correctamente.")

if __name__ == "__main__":
    generar_lista()
