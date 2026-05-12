import requests
import os
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE = "https://www.tvplusgratis2.com/"

def es_m3u8(url):
    filtros = ["google", "ads", "analytics", "pixel", "facebook", "mp4", "log"]
    return ".m3u8" in url and not any(x in url.lower() for x in filtros)

def escanear_servidores(page, canal):
    links_found = []
    page.on("request", lambda req: links_found.append(req.url) if es_m3u8(req.url) else None)
    try:
        print(f"📡 Analizando: {canal['n']}...")
        page.goto(canal['u'], timeout=25000, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        play = page.query_selector("video, iframe, button")
        if play: play.click(force=True)
        page.wait_for_timeout(6000)
    except:
        pass
    return list(dict.fromkeys(links_found))

def ejecutar():
    # 1. Leer progreso anterior
    if os.path.exists("progreso.txt"):
        with open("progreso.txt", "r") as f:
            try: ultimo_indice = int(f.read().strip())
            except: ultimo_indice = 0
    else:
        ultimo_indice = 0

    # 2. Obtener tus manuales
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=10)
        manual = r.text if r.status_code == 200 else ""
    except: manual = ""
    lineas_m = [l for l in manual.splitlines() if l.strip() and not l.startswith("#EXTM3U")]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Linux; Android 11)", is_mobile=True)
        page = context.new_page()

        # PASO 1: Cosechar todos los canales de la portada
        try:
            page.goto(URL_BASE, timeout=30000, wait_until="domcontentloaded")
            links = page.query_selector_all("a")
            canales_web = []
            for link in links:
                href = link.get_attribute("href")
                texto = link.inner_text().strip()
                if href and ".html" in href and URL_BASE in href and len(texto) > 3:
                    canales_web.append({"n": texto, "u": href})
            
            lista_total = list({v['u']: v for v in canales_web}.values())
            total = len(lista_total)

            # PASO 2: Seleccionar los 15 que siguen
            inicio = ultimo_indice if ultimo_indice < total else 0
            fin = inicio + 15
            canales_vuelta = lista_total[inicio:fin]

            print(f"🚀 Vuelta inteligente: Canales {inicio} al {min(fin, total)} de {total}")

            bloque_auto = ""
            for c in canales_vuelta:
                opciones = escanear_servidores(page, c)
                if opciones:
                    bloque_auto += f"### {c['n'].upper()} ###\n"
                    for i, link in enumerate(opciones[:2]):
                        clean = link.split("'")[0].split('"')[0]
                        bloque_auto += f'#EXTINF:-1 group-title="Auto-Total", {c["n"]} (Opcion {i+1})\n{clean}\n'

            # PASO 3: Actualizar progreso.txt
            nuevo_indice = fin if fin < total else 0
            with open("progreso.txt", "w") as f:
                f.write(str(nuevo_indice))

        except Exception as e:
            print(f"❌ Error general: {e}")
            bloque_auto = "### ERROR EN EL ESCANEO ###\n"

        browser.close()

    # 4. Guardado final
    final = "#EXTM3U\n\n"
    if lineas_m:
        final += "### TUS CANALES MANUALES ###\n" + "\n".join(lineas_m) + "\n\n"
    final += f"### RASTREO AUTOMATICO (Indice: {inicio}) ###\n" + bloque_auto

    for archivo in ["DANJU80", "lista_dany.m3u"]:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(final)
    print("✅ Proceso terminado y progreso guardado.")

if __name__ == "__main__":
    ejecutar()
