import requests
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    lineas_finales = ["#EXTM3U"]
    
    # 1. Recuperar tus canales manuales
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            for l in r.text.splitlines():
                if "###" in l: lineas_finales.append(l.strip())
    except: pass

    # URL real del canal que sí queremos (Azteca 7)
    url_fuente = "https://www.tvplusgratis2.com/azteca-7-en-vivo.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Disfraz de iPhone para evitar bloqueos
        context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)")
        page = context.new_page()
        
        links_vivos = []
        # Captura links .m3u8 pero IGNORA los que digan "latam" o sean basura
        page.on("request", lambda r: links_vivos.append(r.url) 
                if ".m3u8?token=" in r.url and "latam" not in r.url.lower() else None)
        
        try:
            print("🚀 Saltando trampas y buscando canal real...")
            page.goto(url_fuente, timeout=60000)
            page.wait_for_timeout(15000)
            
            if links_vivos:
                # ESTRUCTURA MANUAL PERFECTA
                link_limpio = links_vivos[-1]
                lineas_finales.append('#EXTINF:-1 group-title="TV",Azteca 7')
                lineas_finales.append(f"{link_limpio}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0")
                print("✅ Azteca 7 capturado sin caer en la trampa.")
            else:
                print("❌ No se encontró el link real (posible bloqueo de IP en GitHub).")
        except: pass
        browser.close()

    # Guardar archivos limpios
    contenido = "\n".join(lineas_finales)
    with open("DANJU80", "w", encoding="utf-8") as f: f.write(contenido)
    with open("lista_dany.m3u", "w", encoding="utf-8") as f: f.write(contenido)

if __name__ == "__main__":
    ejecutar()
