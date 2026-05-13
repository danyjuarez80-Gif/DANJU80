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
    # 1. LEER LO QUE YA TIENES (PARA NO PERDER TUS CANALES)
    lineas_manuales = []
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if l.strip() and "#EXTM3U" not in l:
                    # Guardamos solo líneas que no sean basura del bot anterior
                    if "|" not in l and not l.startswith("http") and "#EXTINF" not in l:
                        continue # Saltamos basura
                    lineas_manuales.append(l.strip())
    except: pass

    canales_capturados = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            # Simulamos iPhone para evitar el bloqueo "Latam - Reintentando"
            context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1")
            page = context.new_page()

            # Tanda de canales de CINE (Más estables para probar)
            tanda = [
                ["CINE CANAL", "cinecanal-en-vivo.html"],
                ["FX MOVIES", "fx-movies-en-vivo.html"],
                ["TNT SERIES", "tnt-series-en-vivo.html"]
            ]

            for nombre, slug in tanda:
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if es_m3u8(r.url) else None)
                try:
                    page.goto(f"{URL_BASE}{slug}", timeout=60000, wait_until="load")
                    page.wait_for_timeout(15000)
                    page.mouse.click(200, 300) # Clic para activar video
                    
                    if vivos:
                        link_final = f"{vivos[-1].split('?')[0]}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        # ESTRUCTURA CRITICA: Etiqueta y link pegados
                        canales_capturados.append(f'#EXTINF:-1 group-title="CINE",{nombre}')
                        canales_capturados.append(link_final)
                except: pass
                page.remove_listener("request", lambda r: None)
            browser.close()
        except: pass

    # 2. ARMADO FINAL (LIMPIO)
    final_m3u = ["#EXTM3U"]
    
    # Agregamos tus canales que ya tenías
    for l in lineas_manuales:
        if l not in final_m3u:
            final_m3u.append(l)
            
    # Agregamos los nuevos con la estructura que pediste
    final_m3u.extend(canales_capturados)

    # 3. GUARDAR ARCHIVOS
    output = "\n".join(final_m3u)
    for f_name in ["DANJU80", "lista_dany.m3u"]:
        with open(f_name, "w", encoding="utf-8") as f:
            f.write(output)

if __name__ == "__main__":
    ejecutar()
