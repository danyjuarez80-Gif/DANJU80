import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print("ERROR: Archivo origen no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Estructura: lista de secciones. Cada sección tiene un título y sus canales
    secciones = []
    seccion_actual = {"titulo": "SIN_CATEGORIA", "canales": []}
    
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        # Detectar si la línea es un separador de categoría (ej: ----------NOMBRE---------)
        # O si es una línea vacía/basura, la saltamos
        if not linea or linea.startswith("#EXTM3U"):
            i += 1
            continue
            
        if "----------" in linea:
            # Guardamos la sección anterior y abrimos una nueva
            secciones.append(seccion_actual)
            seccion_actual = {"titulo": linea, "canales": []}
            i += 1
        elif linea.startswith("#EXTINF"):
            canal = linea
            url = lineas[i+1].strip() if i+1 < len(lineas) else ""
            seccion_actual["canales"].append((canal, url))
            i += 2
        else:
            i += 1
    secciones.append(seccion_actual)

    # Ordenar solo los canales DENTRO de cada sección
    for s in secciones:
        s["canales"].sort(key=lambda x: x[0])

    # Guardar los archivos separados como los tenías (TV, MOVIES, SERIES)
    # Creamos un diccionario para mapear qué sección va a qué archivo
    def guardar_por_tipo(nombre_archivo, lista_secciones):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for s in lista_secciones:
                if s["titulo"] != "SIN_CATEGORIA":
                    f.write(f"\n{s['titulo']}\n")
                for canal, url in s["canales"]:
                    f.write(f"{canal}\n{url}\n")

    # Aquí clasificamos las secciones según su contenido para tus 3 archivos
    tv_secciones, mov_secciones, ser_secciones = [], [], []
    
    for s in secciones:
        titulo = s["titulo"].lower()
        if "serie" in titulo:
            ser_secciones.append(s)
        elif "movie" in titulo or "pelic" in titulo:
            mov_secciones.append(s)
        else:
            tv_secciones.append(s)

    guardar_por_tipo("DANJU80", tv_secciones)
    guardar_por_tipo("DANJU_MOVIES", mov_secciones)
    guardar_por_tipo("DANJU_SERIES", ser_secciones)

    print("Listas ordenadas por categoría y alfabéticamente dentro de cada una.")

if __name__ == "__main__":
    procesar_listas()
