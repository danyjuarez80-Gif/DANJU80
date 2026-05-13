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
    lineas_finales = []
    ultimo_num = 70
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        content = r.text if r.status_code == 200 else ""
        if not content and os.path.exists("DANJU80"):
            with open("DANJU80", "r") as f: content = f.read()

        for linea in content.splitlines():
            if "noticia" in linea.lower():
                nums = re.findall(r'\d+', linea)
                if nums:
                    n = int(nums[-1])
                    if n > ultimo_num: ultimo_num = n
            lineas_finales.append(linea)
    except: pass

    with sync_playwright() as p:
        # LUNCH MÁS LENTO: Para que el servidor no sospeche
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            extra_http_headers={"Referer": URL_BASE}
        )
        page = context.new_page()

        links_vivos = []
        page.on("request", lambda req: links_vivos.append(req.url) if es_m3u8(req.url) else None)

        try:
            nombre_canal = "noticia" 
            print(f"📡 Entrando a buscar el link para {nombre_canal}...")
            # Entramos a la página del canal (puedes cambiar esto por el que quieras rastrear)
            page.goto(f"{URL_BASE}tudn-en-vivo.html", timeout=45000, wait_until="networkidle")
            
            # ESPERA CRÍTICA: Le damos 15 segundos reales para que cargue el video
            # tal como lo haces tú cuando esperas en Web Video Caster
            page.wait_for_timeout(15000) 
            
            # Intentamos forzar el clic en el centro para que suelte el m3u8
            page.mouse.click(400, 300)
            page.wait_for_timeout(5000)

            if links_vivos:
                nuevo_link = links_vivos[-1].split("'")[0].split('"')[0]
                print(f"✅ ¡Link atrapado!: {nuevo_link[:50]}...")
                
                encontrado = False
                for i, linea in enumerate(lineas_finales):
                    if f"{nombre_canal} {ultimo_num}" in linea:
                        if i + 1 < len(lineas_finales):
                            lineas_finales[i+1] = nuevo_link
                            encontrado = True
                            break
                
                if not encontrado:
                    ultimo_num += 1
                    lineas_finales.append(f'#EXTINF:-1 group-title="TV",{nombre_canal} {ultimo_num}')
                    lineas_finales.append(nuevo_link)
            else:
                print("❌ No se detectó ningún flujo m3u8 en esta vuelta.")

        except Exception as e:
            print(f"⚠️ Error durante el rastreo: {e}")
        
        browser.close()

    # GUARDADO FINAL (Asegurando que no se repita el header)
    resultado = ["#EXTM3U"] + [l for l in lineas_finales if l.strip() and "#EXTM3U" not in l]
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))
    
    # También actualizamos el archivo .m3u para tu app
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))

if __name__ == "__main__":
    ejecutar()
