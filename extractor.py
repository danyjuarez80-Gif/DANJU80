import requests
import os
import re
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    filtros = ["google", "ads", "analytics", "facebook", "mp4", "log"]
    return ".m3u8" in url and len(url) > 50 and not any(x in url.lower() for x in filtros)

def ejecutar():
    # 1. LEER ARCHIVO ACTUAL Y BUSCAR EL ÚLTIMO NÚMERO
    lineas_finales = []
    ultimo_num = 70 # Empezamos base si no hay nada
    canales_existentes = {} # Para rastrear nombres y no repetir

    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        content = r.text if r.status_code == 200 else ""
        if not content and os.path.exists("DANJU80"):
            with open("DANJU80", "r") as f: content = f.read()

        for linea in content.splitlines():
            if "noticia" in linea.lower():
                # Extraer el número de la línea "noticia 74"
                nums = re.findall(r'\d+', linea)
                if nums:
                    num_actual = int(nums[-1])
                    if num_actual > ultimo_num: ultimo_num = num_actual
            lineas_finales.append(linea)
    except: pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1)")
        page = context.new_page()

        links_vivos = []
        page.on("request", lambda req: links_vivos.append(req.url) if es_m3u8(req.url) else None)

        try:
            # Ejemplo: Rastreamos un canal nuevo
            nombre_canal = "noticia" 
            page.goto(f"{URL_BASE}tudn-en-vivo.html", timeout=30000)
            page.wait_for_timeout(12000)
            
            if links_vivos:
                nuevo_link = links_vivos[-1].split("'")[0].split('"')[0]
                
                # VERIFICAR SI EL CANAL YA EXISTE PARA ACTUALIZARLO
                encontrado = False
                for i, linea in enumerate(lineas_finales):
                    if f"{nombre_canal} {ultimo_num}" in linea:
                        # Si lo encuentra, actualiza la línea de abajo (el link)
                        if i + 1 < len(lineas_finales):
                            lineas_finales[i+1] = nuevo_link
                            encontrado = True
                            print(f"🔄 Actualizado: {nombre_canal} {ultimo_num}")
                            break
                
                # SI ES NUEVO, USA EL SIGUIENTE NÚMERO
                if not encontrado:
                    ultimo_num += 1
                    lineas_finales.append(f'#EXTINF:-1 group-title="TV",{nombre_canal} {ultimo_num}')
                    lineas_finales.append(nuevo_link)
                    print(f"➕ Agregado: {nombre_canal} {ultimo_num}")

        except Exception as e: print(f"❌ Error: {e}")
        browser.close()

    # 3. GUARDAR TODO LIMPIO
    # Evitamos que el header #EXTM3U se repita
    resultado = ["#EXTM3U"] + [l for l in lineas_finales if l.strip() and "#EXTM3U" not in l]
    
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))
