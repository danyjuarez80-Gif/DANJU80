import requests
import re
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
# Nueva URL base para el canal solicitado
URL_AZTECA = "https://www.tvplusgratis2.com/azteca-deportes-en-vivo.html"

def capturar_azteca_deportes(page):
    enlaces = []
    page.on("request", lambda req: enlaces.append(req.url) if ".m3u8" in req.url else None)

    try:
        print(f"📡 Navegando a Azteca Deportes...")
        page.goto(URL_AZTECA, timeout=60000, wait_until="networkidle")
        
        # Esperamos a que carguen los posibles reproductores o iframes
        page.wait_for_timeout(8000)
        
        # Intentamos interactuar con el reproductor para activar el stream
        # Buscamos botones de play o el área del video
        for selector in ["video", "iframe", ".play-button", "button"]:
            if page.query_selector(selector):
                print(f"  -> Interactuando con: {selector}")
                page.click(selector, force=True)
                break
        
        # Espera extendida para capturar el tráfico de red (como lo hace Web Video Caster)
        page.wait_for_timeout(15000)
    except Exception as e:
        print(f"  ❌ Error en la captura: {e}")
    
    return enlaces[0] if enlaces else None

def generar_lista():
    # 1. Obtener contenido actual de DANJU80
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        base_raw = r.text if r.status_code == 200 else ""
    except:
        base_raw = ""

    nuevo_link = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Usamos configuración de móvil para mayor compatibilidad
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
            is_mobile=True
        )
        page = context.new_page()
        
        nuevo_link = capturar_azteca_deportes(page)
        browser.close()

    # 2. Escribir el archivo final lista_dany.m3u
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        
        # Mantener tus canales previos
        if base_raw:
            f.write("### CANALES DANJU80 ###\n")
            f.write(base_raw.replace("#EXTM3U", "").strip() + "\n\n")
        
        # Pegar el nuevo canal si se capturó
        if nuevo_link:
            link_limpio = nuevo_link.split("'")[0].split('"')[0]
            f.write("### AUTO-CAPTURA NOCTURNA ###\n")
            f.write(f'#EXTINF:-1 group-title="Deportes",Azteca Deportes\n')
            f.write(f'{link_limpio}\n')
            print(f"✅ Canal pegado con éxito.")
        else:
            print("❌ No se pudo capturar el link esta vez.")

if __name__ == "__main__":
    generar_lista()
