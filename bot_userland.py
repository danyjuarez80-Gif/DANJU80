import requests
import re
import time
import os

# CONFIGURACIÓN
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
ARCHIVO_PROGRESO = "progreso.txt"
# Múltiples fuentes para mayor éxito
URLS = ["https://futbollibre.ec", "https://librefutboltv.com", "https://futbollibretv.me"]
# Canales prioritarios que pediste
PRIORIDAD = ["espn", "fox", "tudn", "directv", "caliente", "telemundo", "univision"]

def leer_progreso():
    if os.path.exists(ARCHIVO_PROGRESO):
        try:
            with open(ARCHIVO_PROGRESO, "r") as f:
                return int(f.read().strip())
        except: return 0
    return 0

def guardar_progreso(n):
    with open(ARCHIVO_PROGRESO, "w") as f:
        f.write(str(n))

def cazar_canales():
    print("--- Iniciando rastreo prioritario (Multi-fuente) ---")
    enlaces = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for url_base in URLS:
        try:
            print(f"Buscando en: {url_base}")
            r = requests.get(url_base, headers=headers, timeout=10).text
            bloques = list(set(re.findall(r'href="(/embed/[^"]+)"', r)))
            
            for path in bloques:
                nombre_raw = path.replace("/embed/", "").replace("-", " ").lower()
                
                # FILTRO DE PRIORIDAD
                if any(p in nombre_raw for p in PRIORIDAD):
                    try:
                        time.sleep(0.5)
                        r_canal = requests.get(url_base + path, headers=headers, timeout=8).text
                        match = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
                        if match:
                            link = match.group(1)
                            nombre_final = nombre_raw.upper()
                            formato = f"#EXTINF:-1, [IPTV] {nombre_final}\n{link}|Referer={url_base}/"
                            if formato not in enlaces:
                                enlaces.append(formato)
                                print(f"¡Cazado!: {nombre_final}")
                    except: continue
        except: continue
    return enlaces

def principal():
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except: base = "#EXTM3U"

    try:
        with open(ARCHIVO_FINAL, "r", encoding="utf-8") as f:
            contenido_actual = f.read()
    except: contenido_actual = ""

    nuevos = cazar_canales()
    lista_final_nuevos = []
    
    for item in nuevos:
        url_nueva = item.split("\n")[1].split("|")[0]
        if url_nueva not in contenido_actual:
            lista_final_nuevos.append(item)

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n" + contenido_actual.split(base)[-1].strip() + "\n")
        if lista_final_nuevos:
            f.write("\n" + "\n".join(lista_final_nuevos) + "\n")
            print(f"Éxito: Se añadieron {len(lista_final_nuevos)} canales.")
        else:
            print("No se encontraron canales nuevos que no estuvieran ya en la lista.")

if __name__ == "__main__":
    principal()
