import requests
import re
from playwright.sync_api import sync_playwright

URL_GITHUB_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"
URL_BASE_TV = "https://www.tvplusgratis2.com/"

CANALES_A_MONITOREAR = [
    {"n": "Azteca Deportes", "u": "https://www.tvplusgratis2.com/azteca-deportes-en-vivo.html"},
    {"n": "TUDN", "u": "https://www.tvplusgratis2.com/tudn-en-vivo.html"},
    {"n": "ESPN 2", "u": "https://www.tvplusgratis2.com/espn-2-en-vivo.html"},
    {"n": "Fox Sports 1", "u": "https://www.tvplusgratis2.com/fox-sports-en-vivo.html"},
    {"n": "Canal 5", "u": "https://www.tvplusgratis2.com/canal-5-en-vivo-mexico.html"}
]

def es_link_valido(url):
    bloqueados = ["google", "doubleclick", "ads", "analytics", "pixel", "facebook", "mp4", "log"]
    return ".m3u8" in url and not any(x in url.lower() for x in bloqueados)

def escanear_canal_completo(page, info_canal):
    enlaces_servidores = []
    page.on("request", lambda req: enlaces_servidores.append(req.url) if es_link_valido(req.url) else None)
    try:
        print(f"🔍 Escaneando: {info_canal['n']}...")
        page.goto(info_canal['u'], timeout=60000, wait_until="networkidle")
        page.wait_for_timeout(6000)
        elementos_clic = page.query_selector_all("video, iframe, .play-button, button")
        for el in elementos_clic[:3]: 
            try:
                el.click(force=True)
                page.wait_for_timeout(4000)
            except:
                continue
        page.wait_for_timeout(10000)
    except:
        pass
    return list(dict.fromkeys(enlaces_servidores))

def ejecucion_maestra():
    try:
        r = requests.get(URL_GITHUB_RAW, timeout=15)
        raw_manual = r.text if r.status_code == 200 else ""
    except:
        raw_manual = ""

    lineas_manuales = [l for l in raw_manual.splitlines() if l.strip() and not l.startswith("#EXTM3U")]
    bloque_auto = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-G960F) AppleWebKit/537.36 Mobile Safari/537.36",
            is_mobile=True
        )
        page = context.new_page()

        for canal in CANALES_A_MONITOREAR:
            opciones = escanear_canal_completo(page, canal)
            if opciones:
                bloque_auto += f"### {canal['n'].upper()} ###\n"
                for i, link in enumerate(opciones[:4]):
                    link_clean = link.split("'")[0].split('"')[0]
                    bloque_auto += f'#EXTINF:-1 group-title="Auto-Multi", {canal["n"]} (Opción {i+1})\n{link_clean}\n'
                print(f"  ✅ {len(opciones[:4])} opciones encontradas.")
            else:
                print(f"  ❌ Sin servidores activos.")
        browser.close()

    # Construcción final sin errores de comillas
    contenido_total = "#EXTM3U\n\n"
    if lineas_manuales:
        contenido_total += "### CANALES MANUALES ###\n" + "\n".join(lineas_manuales) + "\n\n"
    
    contenido_total += "### ACTUALIZACIÓN MULTI-SERVIDOR ###\n" + bloque_auto

    for nombre_archivo in ["DANJU80", "lista_dany.m3u"]:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido_total)
    print("\n🚀 Proceso completado exitosamente.")

if __name__ == "__main__":
    ejecucion_maestra()
