import requests
import os
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    filtros = ["google", "ads", "analytics", "pixel", "facebook", "mp4", "log"]
    return ".m3u8" in url and len(url) > 50 and not any(x in url.lower() for x in filtros)

def escanear_servidores(page, canal):
    links_found = []
    page.on("request", lambda req: links_found.append(req.url) if es_m3u8(req.url) else None)
    try:
        print(f"📡 Analizando: {canal['n']}...")
        page.goto(canal['u'], timeout=25000, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        # Intentamos clics en varios elementos para activar el stream
        for selector in ["video", "iframe", "button"]:
            try:
                el = page.query_selector(selector)
                if el: el.click(force=True)
            except: continue
        page.wait_for_timeout(7000)
    except: pass
    return list(dict.fromkeys(links_found))

def ejecutar():
    # 1. MEMORIA DE RASTREO
    if os.path.exists("progreso.txt"):
        with open("progreso.txt", "r") as f:
            try: ultimo_indice = int(f.read().strip())
            except: ultimo_indice = 0
    else: ultimo_indice = 0

    # 2. CARGAR TUS MANUALES (IMPORTANTE: NO BORRAR)
    # Si falla la descarga, intentamos leer el archivo local para no perder nada
    lineas_m = []
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            lineas_m = [l for l in r.text.splitlines() if l.strip() and not l.startswith("#EXTM3U") and "Auto" not in l]
        else:
            with open("DANJU80", "r", encoding="utf-8") as f:
                lineas_m = [l for l in f.read().splitlines() if l.strip() and not l.startswith("#EXTM3U") and "Auto" not in l]
    except: pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Configuración de "Engaño" al servidor (Headers de México)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-G960F) AppleWebKit/537.36",
            is_mobile=True,
            extra_http_headers={
                "Referer": "https://www.tvplusgratis2.com/",
                "Origin": "https://www.tvplusgratis2.com/"
            }
        )
        page = context.new_page()

        bloque_auto = ""
        try:
            page.goto(URL_BASE, timeout=30000)
            links = page.query_selector_all("a")
            canales_web = []
            for link in links:
                href = link.get_attribute("href")
                texto = link.inner_text().strip()
                if href and ".html" in href and URL_BASE in href and len(texto) > 3:
                    canales_web.append({"n": texto, "u": href})
            
            lista_total = list({v['u']: v for v in canales_web}.values())
            
            inicio = ultimo_indice if ultimo_indice < len(lista_total) else 0
            canales_vuelta = lista_total[inicio:inicio+10]

            for c in canales_vuelta:
                opciones = escanear_servidores(page, c)
                
                # Si pediste saltar 1 y 2, pero el canal tiene pocos, 
                # regresamos a la opción 1 para que al menos salga algo.
                if len(opciones) >= 3:
                    finales = opciones[2:5]
                    base_idx = 3
                else:
                    finales = opciones[:2]
                    base_idx = 1

                if finales:
                    bloque_auto += f"### {c['n'].upper()} ###\n"
                    for i, link in enumerate(finales):
                        clean = link.split("'")[0].split('"')[0]
                        # El pipe con Referer ayuda a que las apps lo abran mejor
                        link_final = f"{clean}|Referer=https://www.tvplusgratis2.com/&User-Agent=Mozilla/5.0"
                        bloque_auto += f'#EXTINF:-1 group-title="Auto-Total", {c["n"]} (Opcion {i+base_idx})\n{link_final}\n'

            with open("progreso.txt", "w") as f:
                f.write(str(inicio + 10 if inicio + 10 < len(lista_total) else 0))

        except Exception as e:
            print(f"❌ Error: {e}")

        browser.close()

    # 3. CONSTRUCCIÓN DEL ARCHIVO FINAL
    contenido = "#EXTM3U\n\n"
    if lineas_m:
        contenido += "### TUS CANALES MANUALES ###\n" + "\n".join(lineas_m) + "\n\n"
    
    contenido
