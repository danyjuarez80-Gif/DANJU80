import requests
import random
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    # 1. RECUPERACIÓN: No dejamos que el archivo muera
    lineas_seguras = ["#EXTM3U"]
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            lineas_seguras = [l.strip() for l in r.text.splitlines() if l.strip() and "#EXTM3U" not in l]
    except: pass

    # 2. CONFIGURACIÓN DE RASTREO
    url_fuente = "https://www.tvplusgratis2.com/azteca-7-en-vivo.html"
    
    # Lista de proxies (IP:PUERTO) - Estos cambian seguido, el bot probará suerte
    proxies_mexico = [
        "187.189.143.109:8080",
        "201.144.152.138:80",
        "189.206.185.114:8080"
    ]
    
    link_final = None

    with sync_playwright() as p:
        # Intentamos con proxy o sin él
        for proxy_addr in [None] + proxies_mexico:
            if link_final: break
            try:
                print(f"🕵️ Probando con proxy: {proxy_addr}")
                launch_args = {}
                if proxy_addr:
                    launch_args['proxy'] = {"server": f"http://{proxy_addr}"}
                
                browser = p.chromium.launch(headless=True, **launch_args)
                context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)")
                page = context.new_page()
                
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if "34_.m3u8?token=" in r.url else None)
                
                page.goto(url_fuente, timeout=40000)
                page.wait_for_timeout(15000)
                
                # Buscamos el patrón 34_.m3u8 que sí reproduce
                if vivos:
                    link_final = next((l for l in reversed(vivos) if "34_.m3u8" in l), vivos[-1])
                    print("✅ ¡Código de Azteca 7 rastreado!")
                
                browser.close()
            except:
                print("❌ Falló el intento, saltando al siguiente...")

    # 3. GUARDADO: Estructura manual exacta
    if link_final:
        # Limpiamos duplicados viejos de Azteca 7 antes de añadir el nuevo
        lineas_limpias = [l for l in lineas_seguras if "Azteca 7" not in l and "34_.m3u8" not in l]
        lineas_finales = ["#EXTM3U"] + lineas_limpias + [
            '#EXTINF:-1 group-title="TV",Azteca 7',
            f"{link_final}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0"
        ]
        
        contenido = "\n".join(lineas_finales)
        with open("DANJU80", "w", encoding="utf-8") as f: f.write(contenido)
        with open("lista_dany.m3u", "w", encoding="utf-8") as f: f.write(contenido)
        print("📁 Archivo actualizado con el link rastreado.")
    else:
        print("⚠️ No se encontró nada, archivo intacto para evitar borrado.")

if __name__ == "__main__":
    ejecutar()
