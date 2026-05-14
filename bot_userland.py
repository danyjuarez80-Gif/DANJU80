import requests
import re
import time
import os

# CONFIGURACIÓN
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
ARCHIVO_PROGRESO = "progreso.txt"

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

def cazar_futbol_libre():
    print("--- Escaneando Fútbol Libre (Bloque profundo) ---")
    enlaces = []
    url_base = "https://futbollibre.ec"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        r = requests.get(url_base, headers=headers, timeout=15).text
        # Buscamos todos los links de canales
        bloques = sorted(list(set(re.findall(r'href="(/embed/[^"]+)"', r))))
        
        inicio = leer_progreso()
        fin = inicio + 30  # Aumentado a 30 para buscar más contenido
        seleccionados = bloques[inicio:fin]

        if not seleccionados:
            print("Reiniciando búsqueda desde el canal 1...")
            inicio = 0
            fin = 30
            seleccionados = bloques[inicio:fin]

        for path in seleccionados:
            try:
                time.sleep(1) # Pausa reducida para ser más rápido
                r_canal = requests.get(url_base + path, headers=headers, timeout=10).text
                match = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
                if match:
                    link = match.group(1)
                    nombre = path.replace("/embed/", "").replace("-", " ").upper()
                    enlaces.append(f"#EXTINF:-1, [FUTBOL] {nombre}\n{link}|Referer={url_base}/")
                    print(f"¡Cazado!: {nombre}")
            except: continue

        guardar_progreso(fin if fin < len(bloques) else 0)
    except Exception as e:
        print(f"Error en rastreo: {e}")
    return enlaces

def principal():
    # Cargar fijos
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except: base = "#EXTM3U"

    # Cargar lista actual
    try:
        with open(ARCHIVO_FINAL, "r", encoding="utf-8") as f:
            contenido_actual = f.read()
    except: contenido_actual = ""

    # Cazar nuevos
    nuevos = cazar_futbol_libre()
    lista_final_nuevos = []
    
    # Filtrar duplicados reales (comparando URL)
    for item in nuevos:
        url_nueva = item.split("\n")[1].split("|")[0]
        if url_nueva not in contenido_actual:
            lista_final_nuevos.append(item)

    # Reescribir archivo manteniendo estructura
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n" + contenido_actual.split(base)[-1].strip() + "\n")
        if lista_final_nuevos:
            f.write("\n" + "\n".join(lista_final_nuevos) + "\n")
            print(f"Éxito: {len(lista_final_nuevos)} canales nuevos añadidos.")
        else:
            print("No se encontraron canales nuevos en este bloque.")

if __name__ == "__main__":
    principal()
