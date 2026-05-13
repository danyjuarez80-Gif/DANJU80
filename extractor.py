import requests
from playwright.sync_api import sync_playwright

# Tu lista principal en GitHub
URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    lineas_finales = ["#EXTM3U"]
    
    # 1. Conservamos tus canales manuales (los de ###)
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if "###" in l: lineas_finales.append(l.strip())
    except: pass

    # 2. RASTREO DINÁMICO: Vamos a la fuente de Azteca 7
    url_fuente = "https://www.tvplusgratis2.com/azteca-7-en-vivo.html"

    with sync_playwright() as p:
        # Usamos un navegador con disfraz de celular para que nos dé el token
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15"
        )
        page = context.new_page()
        
        links_capturados = []
        # El bot aprende a buscar el patrón '34_.m3u8' que me pasaste
        page.on("request", lambda r: links_capturados.append(r.url) 
                if "34_.m3u8?token=" in r.url else None)
        
        try:
            print("🕵️ El bot está rastreando el código de Azteca 7...")
            page.goto(url_fuente, timeout=60000)
            
            # Esperamos a que el reproductor cargue el token fresco
            page.wait_for_timeout(20000) 
            
            if links_capturados:
                # Tomamos el link más reciente con el token nuevo
                link_nuevo = links_capturados[-1]
                
                # Estructura manual limpia
                lineas_finales.append('#EXTINF:-1 group-title="TV",Azteca 7')
                lineas_finales.append(f"{link_nuevo}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0")
                print("✅ ¡Código rastreado y actualizado!")
            else:
                print("❌ No se detectó el código 34_.m3u8 en la página.")
        except Exception as e:
            print(f"❌ Error en el rastreo: {e}")
        
        browser.close()

    # 3. Guardar el archivo DANJU80 con el nuevo link
    contenido = "\n".join(lineas_finales)
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write(contenido)
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write(contenido)

if __name__ == "__main__":
    ejecutar()
