import requests
import os
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    filtros = ["google", "ads", "analytics", "pixel", "facebook", "mp4", "log"]
    # Filtramos también links muy cortos que suelen ser basura
    return ".m3u8" in url and len(url) > 50 and not any(x in url.lower() for x in filtros)

def escanear_servidores(page, canal):
    links_found = []
    # Escuchamos el tráfico de red
    page.on("request", lambda req: links_found.append(req.url) if es_m3u8(req.url) else None)
    try:
        print(f"📡 Analizando: {canal['n']}...")
        page.goto(canal['u'], timeout=25000, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)
        
        # Intentamos interactuar con el reproductor para que suelte los links
        for selector in ["video", "iframe", "button.vjs-big-play-button"]:
            try:
                el = page.query_selector(selector)
                if el: el.click(force=True)
            except: continue
            
        page.wait_for_timeout(8000)
    except: pass
    return list(dict.fromkeys(links_found))

def ejecutar():
    # 1. Memoria de rastreo
    if os.path.exists("progreso.txt"):
        with open("progreso.txt", "r") as f:
            try: ultimo_indice = int(f.read().strip())
            except: ultimo_indice = 0
    else: ultimo_indice = 0

    # 2. Cargar tus manuales
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        manual = r.text if r.status_code == 200 else ""
    except: manual = ""
    lineas_m = [l for l in manual.splitlines() if l.strip() and not l.startswith("#EXTM3U")]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Usamos un User-Agent de Android moderno para mejor compatibilidad
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            is_mobile=True
        )
        page = context.new_page()

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
            
            # Cargar 10 canales
            inicio = ultimo_indice if ultimo_indice < len(lista_total) else 0
            canales_vuelta = lista_total[inicio:inicio+10]

            bloque_auto = ""
            for c in canales_vuelta:
                opciones = escanear_servidores(page, c)
                # AQUÍ ESTÁ EL FILTRO: Solo opciones de la 3 en adelante
                # opciones[2:] significa: salta el índice 0 y 1 (opción 1 y 2)
                opciones_validas = opciones[2:5] 

                if opciones_validas:
                    bloque_auto += f"### {c['n'].upper()} ###\n"
                    for i, link in enumerate(opciones_validas):
                        # Limpiamos el link de posibles comillas
                        clean = link.split("'")[0].split('"')[0]
                        # Agregamos el User-Agent al final del link para que el reproductor lo use
                        # Esto ayuda a que "agarre" en apps como OTT Navigator o VLC
                        link_final = f"{clean}|User-Agent=Mozilla/5.0"
                        bloque_auto += f'#EXTINF:-1 group-title="Auto-Opt", {c["n"]} (Opcion {i+3})\n{link_final}\n'

            with open("progreso.txt", "w") as f:
                f.write(str(inicio + 10 if inicio + 10 < len(lista_total) else 0))

        except Exception as e:
            print(f"❌ Error: {e}")

        browser.close()

    # Guardar archivos
    contenido = "#EXTM3U\n\n"
    if lineas_m:
        contenido += "### MANUALES ###\n" + "\n".join(lineas_m) + "\n\n"
    contenido += bloque_auto

    for archivo in ["DANJU80", "lista_dany.m3u"]:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

if __name__ == "__main__":
    ejecutar()
