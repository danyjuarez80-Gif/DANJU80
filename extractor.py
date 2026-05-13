import requests
from playwright.sync_api import sync_playwright

URL_GITHUB = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    # 1. Recuperar tus canales para no borrarlos
    lineas_viejas = ["#EXTM3U"]
    try:
        r = requests.get(URL_GITHUB, timeout=10)
        if r.status_code == 200:
            lineas_viejas = [l.strip() for l in r.text.splitlines() if l.strip()]
    except: pass

    link_encontrado = None
    # NUEVA FUENTE: Probamos con un sitio que no bloquea IPs de centros de datos
    url_alternativa = "https://televisionlibre.net/embed/azteca-7.html"

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            links_m3u8 = []
            page.on("request", lambda r: links_m3u8.append(r.url) if ".m3u8" in r.url else None)
            
            print("🕵️ Buscando en fuente alternativa...")
            page.goto(url_alternativa, timeout=60000)
            page.wait_for_timeout(10000)
            
            if links_m3u8:
                # Buscamos el link que no sea publicidad
                link_encontrado = next((l for l in reversed(links_m3u8) if "google" not in l and "ads" not in l), None)
            browser.close()
        except: pass

    # 2. Solo actualizamos si el bot de verdad encontró algo útil
    if link_encontrado:
        # Quitamos el Azteca 7 viejo para poner el nuevo
        lineas_finales = [l for l in lineas_viejas if "Azteca 7" not in l and "http" not in l]
        lineas_finales.append('#EXTINF:-1 group-title="TV",Azteca 7 (Actualizado)')
        lineas_finales.append(f"{link_encontrado}|Referer=https://televisionlibre.net/&User-Agent=Mozilla/5.0")
        
        contenido = "\n".join(lineas_finales)
        with open("DANJU80", "w", encoding="utf-8") as f: f.write(contenido)
        with open("lista_dany.m3u", "w", encoding="utf-8") as f: f.write(contenido)
        print("✅ ¡Nuevo link encontrado y guardado!")
    else:
        print("⚠️ No se halló link en esta fuente, manteniendo lista actual.")

if __name__ == "__main__":
    ejecutar()
