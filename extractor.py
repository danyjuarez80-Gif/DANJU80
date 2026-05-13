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
    lineas_manuales = []
    canales_auto = {} # Diccionario para evitar duplicados
    ultimo_num = 70

    # 1. LEER Y SEPARAR: Guardamos tus manuales y limpiamos lo viejo del bot
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        content = r.text if r.status_code == 200 else ""
        lines = content.splitlines()
        
        for i, l in enumerate(lines):
            l = l.strip()
            if not l or "#EXTM3U" in l: continue
            
            # Si es manual (no tiene números largos de bot), lo guardamos
            if "###" in l or ("noticia" in l.lower() and len(re.findall(r'\d+', l)) == 1):
                lineas_manuales.append(l)
                # Mantener el conteo de noticias
                nums = re.findall(r'\d+', l)
                if nums and int(nums[-1]) > ultimo_num: ultimo_num = int(nums[-1])
    except: pass

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Linux; Android 10)")
            
            # 2. BUSCAR CANALES
            page.goto(URL_BASE, timeout=60000, wait_until="load")
            links = page.query_selector_all("a")
            tanda = []
            for l in links:
                h, t = l.get_attribute("href"), l.inner_text().strip().lower()
                if h and ".html" in h and URL_BASE in h and len(t) > 3:
                    if h not in [x[1] for x in tanda]: tanda.append([t, h])
            
            # 3. EXTRAER LINKS (Tanda de 8)
            for nombre, url in tanda[:8]:
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if es_m3u8(r.url) else None)
                try:
                    page.goto(url, timeout=45000)
                    page.wait_for_timeout(15000)
                    page.mouse.click(300, 300)
                    if vivos:
                        ultimo_num += 1
                        # Formato limpio: Referer inyectado sin basura
                        link_final = f"{vivos[-1].split('?')[0]}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        canales_auto[f'#EXTINF:-1 group-title="TV",{nombre} {ultimo_num}'] = link_final
                except: pass
            browser.close()
        except: pass

    # 4. RECONSTRUCCIÓN TOTAL: Primero manuales, luego lo nuevo del bot
    final = ["#EXTM3U"]
    final.extend(lineas_manuales)
    
    for etiqueta, link in canales_auto.items():
        final.append(etiqueta)
        final.append(link)

    # Escribir archivos
    content_str = "\n".join(final)
    for f in ["DANJU80", "lista_dany.m3u"]:
        with open(f, "w", encoding="utf-8") as file:
            file.write(content_str)

if __name__ == "__main__":
    ejecutar()
