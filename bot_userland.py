import requests
import re
import time
import os

# 1. CONSTANTES
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
ARCHIVO_PROGRESO = "progreso.txt"

# 2. FUNCIONES DE APOYO PARA LA MEMORIA
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

# 3. RASTREADOR
def cazar_futbol_libre():
    print("--- Escaneando Fútbol Libre ---")
    enlaces = []
    url_base = "https://futbollibre.ec"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        r = requests.get(url_base, headers=headers, timeout=15).text
        bloques = sorted(list(set(re.findall(r'href="(/embed/[^"]+)"', r))))
        
        inicio = leer_progreso()
        fin = inicio + 10  # Bloque de 10 en 10
        seleccionados = bloques[inicio:fin]

        if not seleccionados:
            print("Lista completada, reiniciando...")
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
            except: continue

        guardar_progreso(fin if fin < len(bloques) else 0)
    except: pass
    return enlaces

# 4. LOGICA PRINCIPAL (LA QUE ACABAMOS DE EDITAR)
def principal():
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            base = f.read().strip()
    except:
        base = "#EXTM3U"

    try:
        with open(ARCHIVO_FINAL, "r", encoding="utf-8") as f:
            contenido_actual = f.read()
    except:
        contenido_actual = ""

    nuevos = cazar_futbol_libre()
    lista_final_nuevos = []
    for item in nuevos:
        lineas = item.split("\n")
        if len(lineas) > 1:
            url_nueva = lineas[1].split("|")[0]
            if url_nueva not in contenido_actual:
                lista_final_nuevos.append(item)

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        if not contenido_actual.startswith("#EXTM3U"):
            f.write(base + "\n")
        else:
            f.write(contenido_actual.strip() + "\n")
        
        if lista_final_nuevos:
            f.write("\n" + "\n".join(lista_final_nuevos) + "\n")
            print(f"Éxito: Se añadieron {len(lista_final_nuevos)} canales.")
        else:
            print("No se encontraron links nuevos en este bloque.")

if __name__ == "__main__":
    principal()
