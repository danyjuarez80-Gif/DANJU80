import requests
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    # 1. Recuperamos tus manuales para no perder nada
    lineas_seguras = ["#EXTM3U"]
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            lineas_seguras = [l.strip() for l in r.text.splitlines() if l.strip()]
    except: pass

    # 2. LISTA DE FUENTES (Si una falla, el bot intenta la siguiente)
    fuentes = [
        "https://www.tvplusgratis2.com/azteca-7-en-vivo.html",
        "https://rvep.org/azteca-7.html" # Ejemplo de fuente alterna
    ]

    link_encontrado = None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()

        for url in fuentes:
            if link_encontrado: break
            try:
                print(f"🔎 Probando fuente: {url}")
                vivos = []
                page.on("request", lambda r: vivos.append(r.url) if "34_.m3u8?token=" in r.url else None)
                
                page.goto(url, timeout=45000)
                page.wait_for_timeout(15000)
                
                if vivos:
                    link_encontrado = vivos[-1]
                    print(f"✅ ¡Éxito en {url}!")
            except:
                print(f"❌ Falló la fuente {url}")
        
        browser.close()

    # 3. GUARDADO: Solo si encontramos algo nuevo actualizamos
    if link_encontrado:
        # Formato manual estricto
        nueva_lista = lineas_seguras + [
            '#EXTINF:-1 group-title="TV",Azteca 7 (Auto)',
            f"{link_encontrado}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0"
        ]
    else:
        nueva_lista = lineas_seguras # No borramos nada

    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(nueva_lista))

if __name__ == "__main__":
    ejecutar()
