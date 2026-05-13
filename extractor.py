import requests
import os
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    filtros = ["google", "ads", "analytics", "facebook", "mp4", "log"]
    # Al igual que Web Video Caster, buscamos específicamente el archivo maestro
    return ".m3u8" in url and not any(x in url.lower() for x in filtros)

def ejecutar():
    # 1. Recuperar tus manuales (como noticias 100)
    lineas_m = []
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            lineas_m = [l for l in r.text.splitlines() if l.strip() and not l.startswith("#EXTM3U") and "Auto" not in l]
    except: pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Usamos el User-Agent que capturamos de Web Video Caster
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
            extra_http_headers={"Referer": URL_BASE}
        )
        page = context.new_page()

        # AQUÍ ESTÁ EL TRUCO: Escuchamos TODO el tráfico como la app
        links_vivos = []
        page.on("request", lambda req: links_vivos.append(req.url) if es_m3u8(req.url) else None)

        try:
            # Seleccionamos un canal (ejemplo TUDN como en tu captura)
            page.goto(f"{URL_BASE}tudn-en-vivo.html", timeout=30000)
            page.wait_for_timeout(10000) # Tiempo para que carguen los anuncios y el video
            
            # Forzamos el play para que el link aparezca en el tráfico
            play = page.query_selector("video, iframe")
            if play: play.click(force=True)
            page.wait_for_timeout(5000)

        except: pass
        browser.close()

    # 2. Construcción final con los links "cazados"
    contenido = "#EXTM3U\n\n"
    if lineas_m:
        contenido += "### TUS CANALES MANUALES ###\n" + "\n".join(lineas_m) + "\n\n"
    
    if links_vivos:
        # Usamos solo el último link detectado (suele ser el más fresco)
        clean = list(dict.fromkeys(links_vivos))[-1]
        # Añadimos los parámetros de reproducción para que "agarre"
        link_final = f"{clean}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
        contenido += f'#EXTINF:-1 group-title="Auto", TUDN HD\n{link_final}\n'

    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write(contenido)
