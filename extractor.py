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
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if l.strip() and "#EXTM3U" not in l:
                    lineas_preservadas.append(l.strip())
                    nums = re.findall(r'\d+', l)
                    if nums and "noticia" in l.lower():
                        n = int(nums[-1])
                        if n > ultimo_num: ultimo_num = n
    except: pass

    canales_nuevos = []

    with sync_playwright() as p:
        try:
            # LANZAMOS NAVEGADOR CON MÁS RECURSOS
            browser = p.chromium.launch(headless=True)
            # Simulamos un usuario real de Chrome en Windows para evitar el "Reintentando"
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()

            # Tanda de canales de películas (CineCanal, etc)
            tanda = [
                ["cine canal", "cinecanal-en-vivo.html"],
                ["azteca 7", "azteca-7-en-vivo.html"],
                ["canal 5", "canal-5-en-vivo.html"]
            ]

            for nombre, slug in tanda:
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if es_m3u8(r.url) else None)
                try:
                    print(f"📡 Entrando a {nombre}...")
                    page.goto(f"{URL_BASE}{slug}", timeout=60000, wait_until="load")
                    
                    # ESPERA ACTIVA: Esperamos a que el video cargue o falle
                    page.wait_for_timeout(20000) 
                    
                    # Intentamos dar clic en las diferentes "Opciones" para forzar el link
                    for i in range(1, 4):
                        opcion = page.get_by_text(f"Opción {i}")
                        if opcion.is_visible():
                            opcion.click()
                            page.wait_for_timeout(5000)
                            if vivos: break

                    if vivos:
                        ultimo_num += 1
                        # CAPTURA PURA DEL ENLACE
                        link_raw = vivos[-1].split('?')[0].split('"')[0]
                        link_final = f"{link_raw}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        canales_nuevos.append(f'#EXTINF:-1 group-title="TV",{nombre} {ultimo_num}')
                        canales_nuevos.append(link_final)
                        print(f"✅ ¡Capturado!")
                    else:
                        print(f"⚠️ {nombre} sigue en bucle de reintento.")
                except: pass
                page.remove_listener("request", lambda r: None)
            browser.close()
        except: pass

    resultado = ["#EXTM3U"] + lineas_preservadas + canales_nuevos
    final_str = "\n".join(resultado)
    for f in ["DANJU80", "lista_dany.m3u"]:
        with open(f, "w", encoding="utf-8") as file:
            file.write(final_str)

if __name__ == "__main__":
    ejecutar()
