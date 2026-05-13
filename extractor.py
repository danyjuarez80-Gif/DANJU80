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
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if l.strip() and "#EXTM3U" not in l:
                    lineas_viejas.append(l.strip())
                    if "noticia" in l.lower() or "cine" in l.lower():
                        nums = re.findall(r'\d+', l)
                        if nums:
                            n = int(nums[-1])
                            if n > ultimo_num: ultimo_num = n
    except: pass

    canales_nuevos = []

    with sync_playwright() as p:
        try:
            # LANZAMOS UN NAVEGADOR QUE PAREZCA MÁS HUMANO
            browser = p.chromium.launch(headless=True)
            # Usamos una configuración de iPhone para despistar al servidor
            context = browser.new_context(
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
                viewport={'width': 375, 'height': 667},
                device_scale_factor=2,
                is_mobile=True
            )
            page = context.new_page()

            # CANALES DE PELÍCULAS QUE SÍ O SÍ DEBEN FUNCIONAR
            tanda = [
                ["cine canal", "cinecanal-en-vivo.html"],
                ["fx movies", "fx-movies-en-vivo.html"],
                ["tnt series", "tnt-series-en-vivo.html"]
            ]

            for nombre, slug in tanda:
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if es_m3u8(r.url) else None)
                
                try:
                    print(f"🕵️ Intentando entrar a: {nombre}")
                    page.goto(f"{URL_BASE}{slug}", timeout=60000, wait_until="load")
                    
                    # Si detectamos el mensaje de error o bucle, refrescamos una vez
                    page.wait_for_timeout(10000)
                    if not vivos:
                        print("🔄 Detectado posible bloqueo. Reintentando...")
                        page.reload(wait_until="load")
                        page.wait_for_timeout(15000)

                    # Simular clics en el centro para despertar al reproductor
                    page.mouse.click(180, 300)
                    page.wait_for_timeout(5000)

                    if vivos:
                        ultimo_num += 1
                        # Limpieza profunda del link capturado
                        link_raw = vivos[-1].split('?')[0].split('"')[0].split("'")[0]
                        link_final = f"{link_raw}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        
                        canales_nuevos.append(f'#EXTINF:-1 group-title="CINE",{nombre} {ultimo_num}')
                        canales_nuevos.append(link_final)
                        print(f"✅ ¡Canal pescado!")
                except Exception as e:
                    print(f"❌ Falló {nombre}: {e}")
                
                page.remove_listener("request", lambda r: None)
            
            browser.close()
        except: pass

    # GUARDADO FINAL: LO QUE YA TENÍAS + LO NUEVO DE CINE
    resultado = ["#EXTM3U"] + lineas_viejas + canales_nuevos
    final_text = "\n".join(resultado)
    for f in ["DANJU80", "lista_dany.m3u"]:
        with open(f, "w", encoding="utf-8") as file:
            file.write(final_text)

if __name__ == "__main__":
    ejecutar()
