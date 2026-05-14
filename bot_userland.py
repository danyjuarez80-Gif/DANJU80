import requests
import re
import time
import os

# Configuración de archivos (Basado en imagen 83517.jpg)
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
ARCHIVO_PROGRESO = "progreso.txt" # Para recordar dónde nos quedamos

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
    print("--- Escaneando Fútbol Libre ---")
    enlaces = []
    url_base = "https://futbollibre.ec"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        r = requests.get(url_base, headers=headers, timeout=15).text
        bloques = sorted(list(set(re.findall(r'href="(/embed/[^"]+)"', r))))
        
        inicio = leer_progreso()
        fin = inicio + 10
        seleccionados = bloques[inicio:fin]

        # Si ya terminamos la lista, reiniciamos desde el principio
        if not seleccionados:
            print("Lista completada, reiniciando al canal 1...")
            inicio = 0
            fin = 10
            seleccionados = bloques[inicio:fin]

        for path in seleccionados:
            try:
                time.sleep(1.5)
                r_canal = requests.get(url_base + path, headers=headers, timeout=10).text
                match = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_canal)
                if match:
                    link = match.group(1)
                    nombre = path.replace("/embed/", "").replace("-", " ").upper()
                    enlaces.append(f"#EXTINF:-1, [FUTBOL] {nombre}\n{link}|Referer={url_base}/")
                    print(f"Cazado: {nombre}")
            except Exception as e:
                print(f"Error en {path}: {e}")

        # Guardar el siguiente punto de inicio
        guardar_progreso(fin if fin < len(bloques) else 0)
        
    except Exception as e:
        print(f"Error general: {e}")
    return enlaces

def principal():
    # 1. Leer canales actuales para no duplicar
    existentes = ""
    try:
        with open(ARCHIVO_FINAL, "r", encoding="utf-8") as f:
            existentes = f.read()
    except: pass

    # 2. Cargar base de fijos
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except: base = "#EXTM3U"

    # 3. Cazar nuevos
    nuevos = cazar_futbol_libre()
    
    # 4. Filtrar: solo agregar si el link no está ya en el archivo
    lista_para_escribir = []
    for item in nuevos:
        link_solo = item.split("\n")[1]
        if link_solo not in existentes:
            lista_para_escribir.append(item)

    # 5. Guardar (Modo 'a' para agregar al final o 'w' para refrescar)
    # Aquí lo puse para que refresque la sección dinámica pero mantenga los fijos
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(base + "\n\n")
        f.write("# --- CANALES ACTUALIZADOS ---\n")
        f.write(existentes.split("# --- CANALES ACTUALIZADOS ---")[-1] if "# --- CANALES ACTUALIZADOS ---" in existentes else "")
        if lista_para_escribir:
            f.write("\n".join(lista_para_escribir) + "\n")
    
    print(f"Se agregaron {len(lista_para_escribir)} canales nuevos.")

if __name__ == "__main__":
    principal()
