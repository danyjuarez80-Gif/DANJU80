import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print(f"ERROR: {archivo_origen} no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Estructura: listas de diccionarios para TV, MOVIES, SERIES
    # Cada uno tendrá categorías, y cada categoría tendrá sus canales
    data = {"TV": {}, "MOVIES": {}, "SERIES": {}}
    categoria_actual = "GENERAL"
    tipo_actual = "TV"

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        # 1. Detectar Categoría
        if "----------" in linea:
            categoria_actual = linea.upper()
            # Asignar tipo automáticamente según el nombre de la categoría
            if "SERIE" in categoria_actual: tipo_actual = "SERIES"
            elif "MOVIE" in categoria_actual or "PELIC" in categoria_actual: tipo_actual = "MOVIES"
            else: tipo_actual = "TV"
            
            if categoria_actual not in data[tipo_actual]:
                data[tipo_actual][categoria_actual] = []
            i += 1
            continue

        # 2. Procesar Canales
        if linea.startswith("#EXTINF"):
            linea_limpia = re.sub(r'(tvg-logo|tvg-image|logo)=".*?"', '', linea)
            linea_limpia = re.sub(r'\s+', ' ', linea_limpia).strip()
            url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
            data[tipo_actual].setdefault(categoria_actual, []).append((linea_limpia, url))
            i += 2
        else:
            i += 1

    # 3. Ordenar y Guardar
    def guardar(nombre_archivo, tipo):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Ordenar categorías alfabéticamente
            categorias_ordenadas = sorted(data[tipo].keys())
            for cat in categorias_ordenadas:
                f.write(f"\n{cat}\n")
                # Ordenar canales alfabéticamente
                canales_ordenados = sorted(data[tipo][cat], key=lambda x: x[0])
                for nombre, url in canales_ordenados:
                    f.write(f"{nombre}\n{url}\n")

    guardar("DANJU80", "TV")
    guardar("DANJU_MOVIES", "MOVIES")
    guardar("DANJU_SERIES", "SERIES")
    print("Listas procesadas, clasificadas y ordenadas alfabéticamente.")

if __name__ == "__main__":
    procesar_listas()
