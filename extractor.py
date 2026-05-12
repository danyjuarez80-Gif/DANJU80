import requests
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "TNT Sports", "slug": "tntsports"},
    # ... (mantén el resto de tu lista de canales igual)
]

def capturar_m3u8(page, url_inicial):
    """Navega al PHP, busca el iframe y captura el m3u8 generado por JS."""
    capturados = []

    def on_request(request):
        url = request.url
        if ".m3u8" in url and ("token=" in url or "index" in url):
            capturados.append(url)

    page.on("request", on_request)
    
    try:
        # 1. Ir a la página principal del canal
        page.goto(url_inicial, timeout=20000, wait_until="networkidle")
        
        # 2. Buscar el iframe (según la captura, el m3u8 está ahí dentro)
        iframe_element = page.query_selector("iframe")
        if iframe_element:
            iframe_url = iframe_element.get_attribute("src")
            if iframe_url:
                # Si la URL es relativa, la completamos
                if iframe_url.startswith("/"):
                    iframe_url = f"{BASE_EMBED}{iframe_url}"
                elif not iframe_url.startswith("http"):
                    iframe_url = f"{BASE_EMBED}/{iframe_url}"
                
                print(f"  -> Entrando al iframe: {iframe_url}")
                page.goto(iframe_url, timeout=20000, wait_until="networkidle")
        
        # Espera extra para que el JS del iframe cargue el m3u8
        page.wait_for_timeout(5000)
        
    except Exception as e:
        print(f"  Error de navegación: {e}")
    
    page.remove_listener("request", on_request)
    return capturados[0] if capturados else None

def obtener_lista_base():
    try:
        r = requests.get(URL_FUENTE, timeout=20)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"Error descargando lista base: {e}")
    return ""

def generar_lista():
    lista_base = obtener_lista_base()
    canales_vistos = set()
    lineas_base = []

    # Limpieza de duplicados en la base
    lineas = lista_base.splitlines()
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            if i + 1 < len(lineas):
                url = lineas[i + 1].strip()
                if url not in canales_vistos:
                    lineas_base.append(linea)
                    lineas_base.append(url)
                    canales_vistos.add(url)
            i += 2
        else:
            i += 1

    nuevos_canales = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Usamos un perfil más "humano" para evitar bloqueos
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()

        for canal in CANALES:
            url_php = f"{BASE_EMBED}/{canal['slug']}.php"
            print(f"📺 Procesando: {canal['nombre']}...")
            
            m3u8 = capturar_m3u8(page, url_php)
            
            if m3u8 and m3u8 not in canales_vistos:
                nuevos_canales.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                nuevos_canales.append(m3u8)
                canales_vistos.add(m3u8)
                print(f"  ✅ Enlace capturado con éxito")
            elif m3u8:
                print(f"  ⚠️ Enlace ya existente (duplicado)")
            else:
                print(f"  ❌ No se detectó flujo .m3u8 en esta ruta")

        browser.close()

    # Escritura del archivo final
    with open("lista_dany.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for linea in lineas_base:
            f.write(linea + "\n")
        if nuevos_canales:
            f.write("\n")
            for linea in nuevos_canales:
                f.write(linea + "\n")

    print(f"\n✅ Proceso terminado. Canales totales: {len(canales_vistos)}")

if __name__ == "__main__":
    generar_lista()
