import requests
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    # 1. RECUPERACIÓN: Intentamos leer lo que tenías antes del error
    lineas_seguras = ["#EXTM3U"]
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            # Filtramos para no meter líneas vacías o basura
            lineas_seguras = [l.strip() for l in r.text.splitlines() if l.strip()]
            if not lineas_seguras: lineas_seguras = ["#EXTM3U"]
    except:
        print("⚠️ No se pudo leer GitHub, usando base limpia.")

    # 2. RASTREO: Buscamos el patrón que me pasaste (34_.m3u8)
    url_fuente = "https://www.tvplusgratis2.com/azteca-7-en-vivo.html"
    canal_nuevo = []

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)")
            page = context.new_page()
            
            links = []
            # Atrapamos cualquier cosa que termine en .m3u8 y tenga token
            page.on("request", lambda r: links.append(r.url) if ".m3u8?token=" in r.url else None)
            
            page.goto(url_fuente, timeout=60000)
            page.wait_for_timeout(20000) 
            
            if links:
                # Buscamos específicamente el que tú identificaste como bueno
                link_real = next((l for l in reversed(links) if "34_.m3u8" in l), links[-1])
                canal_nuevo.append('#EXTINF:-1 group-title="TV",Azteca 7')
                canal_nuevo.append(f"{link_real}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0")
            browser.close()
        except Exception as e:
            print(f"❌ Error rastreando: {e}")

    # 3. GUARDADO INTELIGENTE: Si falló el rastreo, NO borramos lo anterior
    if len(canal_nuevo) > 0:
        # Si encontramos el canal, lo agregamos (o actualizamos si ya estaba)
        # Para esta prueba, simplemente lo añadimos al final
        resultado = lineas_seguras + canal_nuevo
    else:
        # Si no encontró nada, dejamos el archivo como estaba para no dejarlo en blanco
        resultado = lineas_seguras

    contenido = "\n".join(resultado)
    with open("DANJU80", "w", encoding="utf-8") as f: f.write(contenido)
    with open("lista_dany.m3u", "w", encoding="utf-8") as f: f.write(contenido)

if __name__ == "__main__":
    ejecutar()
