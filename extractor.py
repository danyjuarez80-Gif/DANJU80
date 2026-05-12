import requests
import re
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

# Vamos a probar solo con Azteca Deportes para asegurar que pegue uno que sirva
URL_TEST = "https://www.tvplusgratis2.com/azteca-deportes-en-vivo.html"

def capturar_link_real(page):
    enlaces_buenos = []
    
    # Esta función atrapa el tráfico pero filtra solo lo que tiene peso de video real
    def interceptar(request):
        u = request.url
        if ".m3u8" in u and "chunklist" not in u: # El chunklist suele fallar, queremos el master
            if not any(x in u.lower() for x in ["ads", "pixel", "analytics"]):
                enlaces_buenos.append(u)

    page.on("request", interceptar)

    try:
        print("📡 Entrando a la página como si fuera un celular...")
        page.goto(URL_TEST, timeout=60000, wait_until="networkidle")
        page.wait_for_timeout(5000)
        
        # Buscamos el reproductor y le damos Play forzado
        # Si no hay play, el link que sale es basura
        play_btn = page.query_selector("button.vjs-big-play-button")
        if play_btn:
            play_btn.click()
            print("  ▶️ Play presionado")
        
        page.wait_for_timeout(10000)
    except:
        pass
    
    return enlaces_buenos

def sincronizar_todo():
    # 1. Obtener tus links que sí sirven (noticias 100)
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        manual = r.text if r.status_code == 200 else ""
    except:
        manual = ""

    lineas_manuales = [l for l in manual.splitlines() if l.strip() and not l.startswith("#EXTM3U")]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Usamos identidad de Chrome en Android (muy importante para el servidor)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            is_mobile=True
        )
        page = context.new_page()
        
        links_capturados = capturar_link_real(page)
        browser.close()

    # 3. Armar el archivo final
    final = "#EXTM3U\n\n"
    if lineas_manuales:
        final += "### TUS LINKS (LOS QUE SIRVEN) ###\n" + "\n".join(lineas_manuales) + "\n\n"
    
    if links_capturados:
        final += "### PRUEBA BOT (SI FALLAN AVISA) ###\n"
        for i, l in enumerate(links_capturados[:2]):
            final += f'#EXTINF:-1 group-title="Test", Azteca Bot Opcion {i+1}\n{l}\n'
    
    # Guardamos en ambos
    for f_name in ["DANJU80", "lista_dany.m3u"]:
        with open(f_name, "w", encoding="utf-8") as f:
            f.write(final)

sincronizar_todo()
