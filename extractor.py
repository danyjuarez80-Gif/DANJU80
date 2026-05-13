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
    lineas_preservadas = []
    ultimo_num = 70

    # 1. LEER LISTA ACTUAL PARA NO BORRAR NADA
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if l.strip() and "#EXTM3U" not in l:
                    lineas_preservadas.append(l.strip())
                    # Seguir el conteo de tus noticias/canales
                    nums = re.findall(r'\d+', l)
                    if nums and int(nums[-1]) > ultimo_num: ultimo_num = int(nums[-1])
    except: pass

    canales_nuevos = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Linux; Android 10)")
            
            # 2. BUSCAR CANALES EN LA WEB
            page.goto(URL_BASE, timeout=60000, wait_until="load")
            links_web = page.query_selector_all("a")
            tanda = []
            for l in links_web:
                h, t = l.get_attribute("href"), l.inner_text().strip()
                if h and ".html" in h and URL_BASE in h and len(t) > 3:
                    if h not in [x[1] for x in tanda]: tanda.append([t, h])
            
            # 3. CAPTURAR ENLACES (Tanda de 6 para no saturar)
            for nombre, url in tanda[:6]:
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if es_m3u8(r.url) else None)
                try:
                    page.goto(url, timeout=45000)
                    page.wait_for_timeout(15000) # Paciencia de 15 segundos
                    page.mouse.click(300, 300)
                    
                    if vivos:
                        ultimo_num += 1
                        link_final = f"{vivos[-1].split('?')[0]}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        # Guardamos el par: Etiqueta correcta + Link
                        canales_nuevos.append(f'#EXTINF:-1 group-title="TV",{nombre} {ultimo_num}')
                        canales_nuevos.append(link_final)
                except: pass
                page.remove_listener("request", lambda r: None)
            browser.close()
        except: pass

    # 4. RECONSTRUCCIÓN: Mantener lo viejo + Añadir lo nuevo
    resultado = ["#EXTM3U"] + lineas_preservadas + canales_nuevos

    # Guardar sin errores de formato
    final_str = "\n".join(resultado)
    for f in ["DANJU80", "lista_dany.m3u"]:
        with open(f, "w", encoding="utf-8") as file:
            file.write(final_str)

if __name__ == "__main__":
    ejecutar()
