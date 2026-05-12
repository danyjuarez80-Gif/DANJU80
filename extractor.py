import requests
import re
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN 2 HD", "slug": "espn2"}, # Basado en tu captura
    {"nombre": "ESPN Mexico", "slug": "espnmexico"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
]

def capturar_como_caster(page, url_inicial):
    enlaces = []

    # Interceptor de red idéntico al de Web Video Caster
    def on_request(request):
        u = request.url
        if ".m3u8" in u and ("token=" in u or "index" in u):
            enlaces.append(u)

    page.on("request", on_request)
    
    try:
        # Navegamos a la web principal
        page.goto(url_inicial, timeout=60000, wait_until="domcontentloaded")
        
        # Buscamos el iframe y lo cargamos
        iframe = page.query_selector("iframe")
        if iframe:
            src = iframe.get_attribute("src")
            target = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
            print(f"  -> Imitando navegador en: {target}")
            
            # Entramos al iframe y ESPERAMOS a que el reproductor se active
            page.goto(target, timeout=60000, wait_until="networkidle")
            
            # Simulamos un "clic" o espera para que el stream arranque (clave en Web Video Caster)
            page.wait_for_timeout(8000) 
            
    except Exception as e:
        print(f"  Error: {e}")
    
    return enlaces[0] if enlaces else None

def generar_lista():
    # Obtener lista actual para no repetir enlaces que ya funcionan
    try:
        r = requests.get(URL_FUENTE, timeout=10)
        base_txt = r.text if r.status_code == 200 else ""
    except:
        base_txt = ""

    vistos = set(re.findall(r'https?://[^\s]+', base_txt))
    nuevos = []

    with sync_playwright() as p:
        # Usamos opciones de "sigilo" para que no nos detecten como bot
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
            print(f"📺 Analizando {canal['nombre']}...")
            url_php = f"{BASE_EMBED}/{canal['slug']}.php"
            m3u8 = capturar_como_caster(page, url_php)
            
            if m3u8:
                m3u8_limpio = m3u8.split("'")[0].split('"')[0]
                if m3u8_limpio not in vistos:
                    nuevos.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                    nuevos.append(m3u8_limpio)
                    vistos.add(m3u8_limpio)
                    print(f"  ✅ Enlace capturado")
                else:
                    print(f"  ⚠️ Ya existe")
            else:
                print(f"  ❌ No detectado")

        browser.close()

    # Guardar el resultado
    if nuevos:
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")
            if base_txt:
                f.write(base_txt.replace("#EXTM3U", "").strip() + "\n\n")
            for n in nuevos:
                f.write(n + "\n")
        print("\n✅ Lista actualizada con nuevos enlaces.")
    else:
        print("\nNo se encontraron enlaces nuevos esta vez.")

if __name__ == "__main__":
    generar_lista()
