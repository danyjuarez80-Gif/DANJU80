import requests
import os
from playwright.sync_api import sync_playwright

# Tu archivo en GitHub para mantener lo que ya tienes
URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    lineas_finales = ["#EXTM3U"]
    
    # 1. Mantenemos tus canales manuales (los de ###)
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if "###" in l: lineas_finales.append(l.strip())
    except: pass

    # 2. EL RETO: Vamos a la página que genera el link que me pasaste
    # (Ajusta esta URL si la del canal es distinta)
    url_pagina_canal = "https://www.tvplusgratis2.com/azteca-deportes-en-vivo.html" 
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Simulamos tu celular para que nos dé el mismo token que a ti
        context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 10; SM-G960F)")
        page = context.new_page()
        
        vivos = []
        # Solo atrapamos links que tengan el token de deportes
        page.on("request", lambda r: vivos.append(r.url) if ".m3u8?token=" in r.url else None)
        
        try:
            print("📡 Intentando entrar a la página del canal...")
            page.goto(url_pagina_canal, timeout=60000)
            page.wait_for_timeout(20000) # Esperamos 20 seg para que cargue el token
            
            if vivos:
                # ESTRUCTURA LIMPIA: Etiqueta arriba, Link abajo
                # Usamos el link completo con token y le pegamos el Referer
                link_con_token = vivos[-1]
                lineas_finales.append('#EXTINF:-1 group-title="DEPORTES",Azteca Deportes TEST')
                lineas_finales.append(f"{link_con_token}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0")
                print("✅ ¡Token capturado!")
            else:
                print("❌ El bot no vio ningún link con token. Posible bloqueo de IP.")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        browser.close()

    # 3. Guardar con estructura manual perfecta
    contenido = "\n".join(lineas_finales)
    with open("DANJU80", "w", encoding="utf-8") as f: f.write(contenido)
    with open("lista_dany.m3u", "w", encoding="utf-8") as f: f.write(contenido)

if __name__ == "__main__":
    ejecutar()
