import requests
import re
import json
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

# Canales principales para probar el desbloqueo
CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN 2 HD", "slug": "espn2"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
]

def extraccion_forzada(page, url_target):
    enlaces = []
    
    # Escucha de red (Método Caster)
    page.on("request", lambda req: enlaces.append(req.url) if ".m3u8" in req.url else None)

    try:
        # Navegación con evasión de detección
        page.goto(url_target, timeout=60000, wait_until="commit")
        
        # Buscamos en el código fuente sin esperar a que cargue el video
        content = page.content()
        
        # BUSQUEDA 1: Enlaces directos en el HTML
        regex_links = re.findall(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', content)
        if regex_links:
            return regex_links[0]

        # BUSQUEDA 2: Dentro de iframes (recursivo)
        iframes = page.query_selector_all("iframe")
        for frame in iframes:
            src = frame.get_attribute("src")
            if src:
                full_src = src if src.startswith("http") else f"{BASE_EMBED}/{src.lstrip('/')}"
                print(f"  -> Escaneando nivel interno: {full_src}")
                page.goto(full_src, timeout=30000)
                page.wait_for_timeout(5000)
                
                # Re-escaneamos el contenido del iframe
                inner_content = page.content()
                inner_match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', inner_content)
                if inner_match:
                    return inner_match.group(1)

    except Exception as e:
        print(f"  Aviso: {e}")
    
    return enlaces[0] if enlaces else None

def generar_lista():
    # 1. Obtener base actual
    try:
        r = requests.get(URL_FUENTE, timeout=10)
        base_raw = r.text if r.status_code == 200 else ""
    except:
        base_raw = ""

    vistos = set(re.findall(r'https?://[^\s]+', base_raw))
    nuevos = []

    with sync_playwright() as p:
        # Modo sigilo extremo
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()

        for canal in CANALES:
            print(f"🔍 Buscando {canal['nombre']}...")
            target = f"{BASE_EMBED}/{canal['slug']}.php"
            link = extraccion_forzada(page, target)
            
            if link:
                # Limpiar caracteres de escape de JS
                link_clean = link.replace('\\/', '/').replace('\\', '').split('"')[0].split("'")[0]
                if link_clean not in vistos:
                    nuevos.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                    nuevos.append(link_clean)
                    vistos.add(link_clean)
                    print(f"  ⭐ Encontrado!")
                else:
                    print(f"  ✅ Ya está al día")
            else:
                print(f"  ❌ No se detectó rastro del m3u8")

        browser.close()

    # 2. Guardar si hay novedades
    if nuevos:
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")
            if base_raw:
                f.write(base_raw.replace("#EXTM3U", "").strip() + "\n\n")
            for n in nuevos:
                f.write(n + "\n")
        print("\n✅ Archivo actualizado.")
    else:
        print("\nNo hubo cambios en los enlaces.")

if __name__ == "__main__":
    generar_lista()
