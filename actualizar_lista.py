import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print(f"ERROR: {archivo_origen} no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Estructura para almacenar bloques: {archivo: {categoria: [(nombre, url), ...]}}
    # Usamos esto para mantener las categorías ordenadas
    datos = {
        "DANJU80": {},      # Canales (TV)
        "DANJU_MOVIES": {}, # MP4 (Pelis)
        "DANJU_SERIES": {}  # MKV (Series)
    }
    
    archivo_actual = "DANJU80"
    cat_actual = "GENERAL"

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        # 1. Detectar Categoría
        if "----------" in linea:
            cat_actual = linea
            i += 1
            continue
            
        # 2. Detectar Canales
        if linea.startswith("#EXTINF"):
            url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
            # Clasificación por extensión
            url_low = url.lower()
            if url_low.endswith(".mp4"):
                target = "DANJU_MOVIES"
            elif url_low.endswith(".mkv"):
                target = "DANJU_SERIES"
            else:
                target = "DANJU80"
            
            datos[target].setdefault(cat_actual, []).append((linea, url))
            i += 2
        else:
            i += 1

    # 3. Guardar ordenado
    for archivo, categorias in datos.items():
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Ordenar categorías alfabéticamente
            for cat in sorted(categorias.keys()):
                f.write(f"\n{cat}\n")
                # Ordenar canales alfabéticamente dentro de la categoría
                for nombre, url in sorted(categorias[cat], key=lambda x: x[0]):
                    f.write(f"{nombre}\n{url}\n")

    print("Listas separadas por extensión y ordenadas exitosamente.")

if __name__ == "__main__":
    procesar_listas()
