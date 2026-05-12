import requests
import re
from playwright.sync_api import sync_playwright

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
BASE_EMBED = "https://embed.ksdjugfsddeports.com"

CANALES = [
    {"nombre": "TUDN", "slug": "tudn"},
    {"nombre": "ESPN 2 HD", "slug": "espn2"},
    {"nombre": "Fox Sports Mexico", "slug": "foxsportsmexico"},
]

def extraccion_con_interaccion(page, url_target):
    enlaces = []
    
    # Interceptamos el tráfico de red
    page.on("request", lambda req: enlaces.append(req.url) if ".m3u8" in req.url else None)

    try:
        # 1. Cargar el PHP inicial
        page.goto(url_target, timeout=60000, wait_until="networkidle")
        
        # 2. Localizar el iframe y entrar en él
        iframe_element = page.query_selector("iframe")
        if iframe_element:
            frame_url = iframe_element.get_attribute("src")
            target_url = frame_url if frame_url.startswith("http") else f"{BASE_EMBED}/{frame_url.lstrip('/')}"
            
            print(f"  -> Entrando al reproductor: {target_url}")
            page.goto(target_url, timeout=60000, wait_until="domcontentloaded")
            
            # --- PARTE CLAVE: SIMULAR EL CLIC ---
            # Esperamos un poco a que aparezca el botón de play
            page.wait_for_timeout(3000)
            
            # Intentamos hacer clic en selectores comunes de reproductores
            botones_play = [
                "button.vjs-big-play-button", # VideoJS
                ".play-button", 
                "video", # A veces clicar el video mismo inicia la carga
                "#player",
                ".jw-display-icon-container" # JWPlayer
            ]
            
            for selector in botones_play:
                if page.query_selector(selector):
                    print(f"  -> Simulando clic en el canal...")
                    page.click(selector, force=True)
                    break
            
            # Esperamos a que el clic genere el tráfico m3u8
            page.wait_for_timeout(10000)

    except Exception as e:
        print(f"  Error durante la interacción: {e}")
    
    return enlaces[0] if enlaces else None

def generar_lista():
    # Obtener base actual de tu GitHub
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        base_raw = r.text if r.status_code == 200 else ""
    except:
        base_raw = ""

    vistos = set(re.findall(r'https?://[^\s]+', base_raw))
    nuevos = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for canal in CANALES:
            print(f"🔍 Activando {canal['nombre']}...")
            url_target = f"{BASE_EMBED}/{canal['slug']}.php"
            link = extraccion_con_interaccion(page, url_target)
            
            if link:
                link_clean = link.split("'")[0].split('"')[0]
                if link_clean not in vistos:
                    nuevos.append(f'#EXTINF:-1 group-title="Deportes",{canal["nombre"]}')
                    nuevos.append(link_clean)
                    vistos.add(link_clean)
                    print(f"  ✅ Enlace capturado tras clic")
                else:
                    print(f"  ✅ Ya estaba actualizado")
            else:
                print(f"  ❌ El clic no generó m3u8")

        browser.close()

    # Guardar cambios
    if nuevos:
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n\n")
            if base_raw:
                f.write(base_raw.replace("#EXTM3U", "").strip() + "\n\n")
            for n in nuevos:
                f.write(n + "\n")
        print("\n✅ Lista actualizada con éxito.")
    else:
        print("\nNo hubo enlaces nuevos.")

if __name__ == "__main__":
    generar_lista()
