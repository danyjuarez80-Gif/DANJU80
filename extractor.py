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
    
    # 1. Cargar lista actual para mantener orden y manuales
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        content = r.text if r.status_code == 200 else ""
        if not content and os.path.exists("DANJU80"):
            with open("DANJU80", "r", encoding="utf-8") as f: content = f.read()
        for l in content.splitlines():
            if "#EXTM3U" not in l: lineas_finales.append(l)
            nums = re.findall(r'\d+', l)
            if nums and "noticia" in l.lower():
                n = int(nums[-1])
                if n > ultimo_num: ultimo_num = n
    except: pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 10)")
        page = context.new_page()

        # 2. AUTO-DESCUBRIMIENTO: El bot busca qué canales hay hoy
        print("🕵️ Buscando canales disponibles en la web...")
        page.goto(URL_BASE, timeout=60000, wait_until="networkidle")
        links_elementos = page.query_selector_all("a")
        
        canales_encontrados = []
        for el in links_elementos:
            href = el.get_attribute("href")
            texto = el.inner_text().strip().lower()
            # Filtramos solo links de canales reales
            if href and ".html" in href and URL_BASE in href and len(texto) > 3:
                if href not in [c[1] for c in canales_encontrados]:
                    canales_encontrados.append([texto, href])

        # Tomamos una tanda (ejemplo: los primeros 8 canales que encuentre)
        tanda_hoy = canales_encontrados[:8]
        print(f"✅ Se encontraron {len(canales_encontrados)} canales. Procesando los primeros {len(tanda_hoy)}...")

        # 3. RASTREO AUTOMÁTICO DE LA TANDA
        for nombre_web, url_canal in tanda_hoy:
            links_vivos = []
            def capturar(request):
                if es_m3u8(request.url): links_vivos.append(request.url)
            page.on("request", capturar)

            try:
                print(f"📡 Extrayendo: {nombre_web}...")
                page.goto(url_canal, timeout=60000, wait_until="networkidle")
                page.wait_for_timeout(15000) # Tiempo para que suelte el m3u8
                page.mouse.click(300, 300)
                page.wait_for_timeout(5000)

                if links_vivos:
                    # Inyección de Referer para que funcione en tu app
                    nuevo_link = f"{links_vivos[-1].split('?')[0]}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                    
                    # Si el nombre ya existe, lo actualiza. Si no, lo crea con número nuevo.
                    encontrado = False
                    for i, linea in enumerate(lineas_finales):
                        if nombre_web in linea.lower():
                            if i + 1 < len(lineas_finales):
                                lineas_finales[i+1] = nuevo_link
                                encontrado = True
                                break
                    
                    if not encontrado:
                        ultimo_num += 1
                        lineas_finales.append(f'#EXTINF:-1 group-title="TV",{nombre_web} {ultimo_num}')
                        lineas_finales.append(nuevo_link)
            except: pass
            page.remove_listener("request", capturar)

        browser.close()

    # 4. GUARDAR CAMBIOS
    resultado = ["#EXTM3U"] + [l for l in lineas_finales if l.strip()]
    for archivo in ["DANJU80", "lista_dany.m3u"]:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("\n".join(resultado))
    print("🚀 ¡Bot completado sin que muevas un dedo!")

if __name__ == "__main__":
    ejecutar()
