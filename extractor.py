import requests
import os
import re
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    filtros = ["google", "ads", "analytics", "facebook", "mp4", "log", "pixel"]
    return ".m3u8" in url and len(url) > 50 and not any(x in url.lower() for x in filtros)

def ejecutar():
    lineas_viejas = []
    ultimo_num = 70

    # 1. Recuperamos tus canales actuales para que NO se borren
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if l.strip() and "#EXTM3U" not in l:
                    lineas_viejas.append(l.strip())
                    nums = re.findall(r'\d+', l)
                    if nums and "noticia" in l.lower():
                        n = int(nums[-1])
                        if n > ultimo_num: ultimo_num = n
    except: pass

    canales_nuevos = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            page = context.new_page()

            # 2. LISTA DE CANALES DE PELÍCULAS/VARIEDAD (Más fáciles de abrir)
            tanda_cine = [
                ["canal 5 mx", "canal-5-en-vivo.html"],
                ["azteca 7 mx", "azteca-7-en-vivo.html"],
                ["las estrellas", "las-estrellas-en-vivo.html"],
                ["cine canal", "cinecanal-en-vivo.html"],
                ["fox movies", "cine-premium-en-vivo.html"]
            ]

            for nombre, slug in tanda_cine:
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if es_m3u8(r.url) else None)
                try:
                    print(f"📡 Intentando capturar: {nombre}")
                    page.goto(f"{URL_BASE}{slug}", timeout=45000)
                    page.wait_for_timeout(15000) # Tiempo para que el video arranque
                    page.mouse.click(350, 350) # Clic al centro del video
                    
                    if vivos:
                        ultimo_num += 1
                        # Limpiamos el link de tokens basura y ponemos Referer
                        link_limpio = vivos[-1].split('?')[0].split('"')[0].split("'")[0]
                        link_final = f"{link_limpio}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        
                        canales_nuevos.append(f'#EXTINF:-1 group-title="CINE",{nombre} {ultimo_num}')
                        canales_nuevos.append(link_final)
                        print(f"✅ ¡Atrapado!")
                except: pass
                page.remove_listener("request", lambda r: None)

            browser.close()
        except: pass

    # 3. Armamos la lista: EXTM3U + LO VIEJO + LO NUEVO
    resultado = ["#EXTM3U"] + lineas_viejas + canales_nuevos

    # Escribimos los archivos para que los lea tu app
    final_m3u = "\n".join(resultado)
    for f_name in ["DANJU80", "lista_dany.m3u"]:
        with open(f_name, "w", encoding="utf-8") as f:
            f.write(final_m3u)

if __name__ == "__main__":
    ejecutar()
