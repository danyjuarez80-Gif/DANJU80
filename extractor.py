import requests
import re
from playwright.sync_api import sync_playwright

# Configuración de URLs
URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_AZTECA = "https://www.tvplusgratis2.com/azteca-deportes-en-vivo.html"

def capturar_m3u8(page):
    enlaces = []
    page.on("request", lambda req: enlaces.append(req.url) if ".m3u8" in req.url else None)
    try:
        print("📡 Navegando a la fuente de deportes...")
        page.goto(URL_AZTECA, timeout=60000, wait_until="networkidle")
        page.wait_for_timeout(8000)
        
        # Simular interacción para activar el stream
        for selector in ["video", "iframe", ".play-button", "button"]:
            if page.query_selector(selector):
                page.click(selector, force=True)
                break
        page.wait_for_timeout(15000)
    except:
        pass
    return enlaces[0] if enlaces else None

def generar_archivos():
    # 1. Obtener tus canales manuales actuales
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        contenido_actual = r.text if r.status_code == 200 else ""
    except:
        contenido_actual = ""

    # Limpiar el contenido previo para evitar duplicar cabeceras
    lineas_limpias = [l for l in contenido_actual.splitlines() if l.strip() and not l.startswith("#EXTM3U")]

    # 2. Capturar el nuevo enlace
    nuevo_link = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Mobile Safari/537.36",
            is_mobile=True
        )
        page = context.new_page()
        nuevo_link = capturar_m3u8(page)
        browser.close()

    # 3. Preparar el bloque de texto final
    cabecera = "#EXTM3U\n\n"
    bloque_manual = "### MIS CANALES MANUALES ###\n" + "\n".join(lineas_limpias) + "\n\n"
    
    if nuevo_link:
        link_clean = nuevo_link.split("'")[0].split('"')[0]
        bloque_auto = "### ACTUALIZADO POR EL BOT ###\n"
        bloque_auto += '#EXTINF:-1 group-title="Deportes Auto",Azteca Deportes\n'
        bloque_auto += f"{link_clean}\n"
    else:
        bloque_auto = "### EL BOT NO ENCONTRÓ ENLACES NUEVOS ###\n"

    contenido_final = cabecera + bloque_manual + bloque_auto

    # 4. EDITAR AMBOS ARCHIVOS A LA VEZ
    # Actualizamos el archivo de base
    with open("DANJU80", "w", encoding="utf-8") as f1:
        f1.write(contenido_final)
    
    # Actualizamos la lista m3u
    with open("lista_dany.m3u", "w", encoding="utf-8") as f2:
        f2.write(contenido_final)

    print("✅ DANJU80 y lista_dany.m3u actualizados correctamente.")

if __name__ == "__main__":
    generar_archivos()
