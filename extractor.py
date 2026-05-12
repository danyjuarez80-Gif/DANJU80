import requests
import re
from playwright.sync_api import sync_playwright

# URL de tu lista base para evitar duplicados
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN Mexico", "slug": "espnmexico"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
    {"nombre": "Azteca 7", "slug": "azteca7"},
    {"nombre": "Canal 5", "slug": "canal5"},
]

def capturar_m3u8(page, url_inicial):
    enlaces_encontrados = []

    # Escuchamos TODO el tráfico de red, no solo los .m3u8
    def interceptar(request):
        url = request.url
        # Buscamos patrones de m3u8 incluso si vienen con tokens largos
        if ".m3u8" in url.lower():
            enlaces_encontrados.append(url)

    page.on("request", interceptar)
    
    try:
        # Forzamos un User Agent de una persona real
        page.goto(url_inicial, timeout=60000, wait_until="networkidle")
        
        # 1. Buscamos cualquier iframe y entramos
        iframes = page.query_selector_all("iframe")
        for i, frame in enumerate(iframes):
            src = frame.get_attribute("src")
            if src and ("php" in src or "embed" in src):
                target = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
                print(f"  -> Entrando a iframe {i+1}...")
                page.goto(target, timeout=30000, wait_until="domcontentloaded")
                page.wait_for_timeout(5000) # Espera a que el video intente cargar

        # 2. Si no capturó por red, buscamos el link "escrito" en el código
        if not enlaces_encontrados:
            html_completo = page.content()
            # Buscamos cualquier cosa que parezca un link .m3u8
            match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', html_completo)
            if match:
                enlaces_encontrados.append(match.group(1))

    except Exception as e:
        print(f"  Error en {url_inicial}: {e}")
    
    return enlaces_encontrados[0] if enlaces_encontrados else None

def generar_lista():
    # Descargamos lo que ya tienes para no repetir
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        lista_actual = r.text if r.status_code == 200 else ""
    except:
        lista_actual = ""

    canales_vistos = set(re.findall(r'https?://[^\s]+', lista_actual))
    nuevos = []

    with sync_playwright() as p:
        # Iniciamos el navegador ocultando que somos un bot
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
            print(f"📺 {canal['nombre']}...")
            url_target = f"{BASE_EMBED}/{canal['slug']}.php"
            m3u8 = capturar_m3u8(page, url_target)
            
            if m3u8:
                # Limpieza rápida del link
                m3u8 = m3u8.split("'")[0].split('"')[0].split("\\")[0]
                if m3u8 not in canales_vistos:
                    nuevos.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                    nuevos.append(m3u8)
                    canales_vistos.add(m3u8)
                    print(f"  ✅ ENCONTRADO")
                else:
                    print(f"  ⚠️ Ya estaba en la lista")
            else:
                print(f"  ❌ No se pudo extraer")

        browser.close()

    # Escribimos el archivo final (lista_dany.m3u)
    if nuevos or lista_actual:
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")
            # Primero ponemos lo viejo
            if lista_actual:
                f.write(lista_actual.replace("#EXTM3U", "").strip() + "\n\n")
            # Luego lo nuevo
            for linea in nuevos:
                f.write(linea + "\n")
        print(f"\n✅ Proceso completado. Revisa el archivo lista_dany.m3u")
    else:
        print("\n⚠️ No se generó ningún contenido nuevo.")

if __name__ == "__main__":
    generar_lista()
