import requests
import os
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def ejecutar_rastreo_inteligente():
    # 1. Leer progreso anterior
    if os.path.exists("progreso.txt"):
        with open("progreso.txt", "r") as f:
            ultimo_indice = int(f.read().strip())
    else:
        ultimo_indice = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 11)", is_mobile=True)
        page = context.new_page()

        # PASO 1: Cosechar TODOS los canales de la web
        page.goto(URL_BASE, timeout=30000, wait_until="domcontentloaded")
        links = page.query_selector_all("a")
        todos_los_canales = []
        for link in links:
            href = link.get_attribute("href")
            texto = link.inner_text().strip()
            if href and ".html" in href and URL_BASE in href and len(texto) > 3:
                todos_los_canales.append({"n": texto, "u": href})
        
        # Quitar duplicados
        lista_total = list({v['u']: v for v in todos_los_canales}.values())
        total = len(lista_total)

        # PASO 2: Seleccionar los siguientes 15 canales
        inicio = ultimo_indice if ultimo_indice < total else 0
        fin = inicio + 15
        canales_de_esta_vuelta = lista_total[inicio:fin]

        print(f"🚀 Iniciando en el canal {inicio}. Analizando hasta el {min(fin, total)} de {total}.")

        bloque_auto = ""
        for c in canales_de_esta_vuelta:
            # Aquí va tu lógica de escanear_servidores (mismo código de antes)
            # ... (asumamos que extrae los links m3u8)
            pass

        # PASO 3: Guardar el nuevo progreso para la próxima vez
        nuevo_indice = fin if fin < total else 0
        with open("progreso.txt", "w") as f:
            f.write(str(nuevo_indice))

        browser.close()

    # Guardar archivos (DANJU80 y lista_dany.m3u) como siempre
    # ...
