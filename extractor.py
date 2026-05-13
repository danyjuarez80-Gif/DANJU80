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

    # 2. FILTRAR MANUALES (Solo lo que NO es automático)
    lineas_m = []
    try:
        # Intentamos descargar el archivo actual de GitHub
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            raw_text = r.text
        else:
            # Si falla GitHub, leemos el archivo local
            with open("DANJU80", "r", encoding="utf-8") as f:
                raw_text = f.read()
        
        # AQUÍ ESTÁ EL TRUCO: Solo guardamos líneas que NO tengan "Auto-Total" o "ACTUALIZACIÓN"
        # Así limpiamos los canales automáticos viejos en cada corrida
        for linea in raw_text.splitlines():
            if linea.strip() and not linea.startswith("#EXTM3U") and "Auto-Total" not in linea and "###" not in linea:
                lineas_m.append(linea)
    except: pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-G960F) AppleWebKit/537.36",
            is_mobile=True,
            extra_http_headers={"Referer": URL_BASE}
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
            
            # Seleccionamos los 10 siguientes según el progreso
            inicio = ultimo_indice if ultimo_indice < len(lista_total) else 0
            canales_vuelta = lista_total[inicio:inicio+10]
            print(f"🚀 Procesando canales nuevos del {inicio} al {inicio+10}")

            for c in canales_vuelta:
                opciones = escanear_servidores(page, c)
                # Seleccionamos opción 3 si existe, si no, la 1
                finales = opciones[2:5] if len(opciones) >= 3 else opciones[:2]
                base_idx = 3 if len(opciones) >= 3 else 1

                if finales:
                    bloque_auto += f"### {c['n'].upper()} ###\n"
                    for i, link in enumerate(finales):
                        clean = link.split("'")[0].split('"')[0]
                        link_final = f"{clean}|Referer={URL_BASE}&User-Agent=Mozilla/5.0"
                        bloque_auto += f'#EXTINF:-1 group-title="Auto-Total", {c["n"]} (Opcion {i+base_idx})\n{link_final}\n'

            # Guardar el nuevo índice para la siguiente ejecución
            with open("progreso.txt", "w") as f:
                f.write(str(inicio + 10 if inicio + 10 < len(lista_total) else 0))

        except Exception as e:
            print(f"❌ Error: {e}")
        browser.close()

    # 3. CONSTRUCCIÓN LIMPIA DEL ARCHIVO
    # Solo ponemos tus manuales (sin lo viejo automático) + lo nuevo que se
