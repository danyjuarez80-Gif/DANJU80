import requests
from playwright.sync_api import sync_playwright

URL_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    # 1. Recuperar lo que ya tienes para no perderlo
    try:
        r = requests.get(URL_RAW, timeout=10)
        lineas = [l.strip() for l in r.text.splitlines() if l.strip()]
        if not lineas: lineas = ["#EXTM3U"]
    except:
        lineas = ["#EXTM3U"]

    # 2. Intentar rastrear el nuevo link de Azteca 7
    link_nuevo = None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)")
            
            links = []
            page.on("request", lambda r: links.append(r.url) if "34_.m3u8?token=" in r.url else None)
            
            page.goto("https://www.tvplusgratis2.com/azteca-7-en-vivo.html", timeout=60000)
            page.wait_for_timeout(15000)
            
            if links:
                link_nuevo = links[-1]
            browser.close()
    except Exception as e:
        print(f"Error rastreando: {e}")

    # 3. Actualizar solo si encontramos el link, si no, dejamos lo que estaba
    if link_nuevo:
        # Quitamos versiones viejas de Azteca 7 para no repetir
        lineas = [l for l in lineas if "Azteca 7" not in l and "34_.m3u8" not in l]
        lineas.append('#EXTINF:-1 group-title="TV",Azteca 7')
        lineas.append(f"{link_nuevo}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0")

    # 4. Guardar forzosamente
    contenido = "\n".join(lineas)
    for nombre in ["DANJU80", "lista_dany.m3u"]:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(contenido)

if __name__ == "__main__":
    ejecutar()
