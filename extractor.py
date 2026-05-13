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
    lineas_finales = []
    ultimo_num = 70
    
    # 1. Recuperar base actual
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        content = r.text if r.status_code == 200 else ""
        if not content and os.path.exists("DANJU80"):
            with open("DANJU80", "r", encoding="utf-8") as f: content = f.read()
        
        for l in content.splitlines():
            if "#EXTM3U" not in l and l.strip():
                lineas_finales.append(l.strip())
                if "noticia" in l.lower():
                    nums = re.findall(r'\d+', l)
                    if nums:
                        n = int(nums[-1])
                        if n > ultimo_num: ultimo_num = n
    except: pass

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 10)")
            page = context.new_page()

            # 2. Descubrimiento con protección
            page.goto(URL_BASE, timeout=60000, wait_until="load")
            elementos = page.query_selector_all("a")
            canales_encontrados = []
            for el in elementos:
                href = el.get_attribute("href")
                texto = el.inner_text().strip().lower()
                if href and ".html" in href and URL_BASE in href and len(texto) > 3:
                    if href not in [c[1] for c in canales_encontrados]:
                        canales_encontrados.append([texto, href])
            
            tanda = canales_encontrados[:8]

            # 3. Rastreo individual
            for nombre, url in tanda:
                links_vivos = []
                def capturar(req):
                    if es_m3u8(req.url): links_vivos.append(req.url)
                page.on("request", capturar)

                try:
                    page.goto(url, timeout=45000)
                    page.wait_for_timeout(15000)
                    page.mouse.click(300, 300)
                    page.wait_for_timeout(5000)

                    if links_vivos:
                        enlace = f"{links_vivos[-1].split('?')[0]}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        encontrado = False
                        for i, l in enumerate(lineas_finales):
                            if nombre in l.lower():
                                if i + 1 < len(lineas_finales):
                                    lineas_finales[i+1] = enlace
                                    encontrado = True
                                    break
                        if not encontrado:
                            ultimo_num += 1
                            lineas_finales.append(f'#EXTINF:-1 group-title="TV",{nombre} {ultimo_num}')
                            lineas_finales.append(enlace)
                except: pass
                page.remove_listener("request", capturar)

            browser.close()
        except Exception as e:
            print(f"Error en navegador: {e}")

    # 4. Guardado con formato estricto
    res = ["#EXTM3U"]
    vistos = []
    for i, l in enumerate(lineas_finales):
        if l.startswith("#EXTINF") and l not in vistos:
            res.append(l)
            vistos.append(l)
            if i + 1 < len(lineas_finales) and lineas_finales[i+1].startswith("http"):
                res.append(lineas_finales[i+1])
        elif l.startswith("###"):
            res.append(l)

    final = "\n".join(res)
    for f_name in ["DANJU80", "lista_dany.m3u"]:
        with open(f_name, "w", encoding="utf-8") as f:
            f.write(final)

if __name__ == "__main__":
    ejecutar()
