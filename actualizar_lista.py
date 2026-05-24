import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print(f"ERROR: {archivo_origen} no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Estructura: diccionarios que guardarán {nombre_categoria: [(linea, url), ...]}
    tv, movies, series = {}, {}, {}

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            # Lógica de limpieza original
            linea_limpia = re.sub(r'tvg-logo=".*?"', '', linea)
            linea_limpia = re.sub(r'tvg-image=".*?"', '', linea_limpia)
            linea_limpia = re.sub(r'logo=".*?"', '', linea_limpia)
            linea_limpia = re.sub(r'\s+', ' ', linea_limpia).strip()
            url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
            # Extraer categoría (group-title) para ordenar
            match = re.search(r'group-title="([^"]+)"', linea_limpia)
            categoria = match.group(1) if match else "SIN CATEGORIA"
            
            inf_low = linea_limpia.lower()
            url_low = url.lower()
            
            # Clasificación básica original
            if "/series" in url_low or "series" in inf_low:
                if categoria not in series: series[categoria] = []
                series[categoria].append((linea_limpia, url))
            elif "/movie" in url_low or "movie" in inf_low or "pelic" in inf_low:
                if categoria not in movies: movies[categoria] = []
                movies[categoria].append((linea_limpia, url))
            else:
                if categoria not in tv: tv[categoria] = []
                tv[categoria].append((linea_limpia, url))
            i += 2
        else:
            i += 1

    # Función para escribir los archivos ordenados
    def escribir_ordenado(nombre_archivo, datos):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # 1. Ordenar categorías alfabéticamente
            for cat in sorted(datos.keys()):
                # 2. Ordenar canales dentro de la categoría alfabéticamente
                for nombre, url in sorted(datos[cat], key=lambda x: x[0]):
                    f.write(f"{nombre}\n{url}\n")

    escribir_ordenado("DANJU80", tv)
    escribir_ordenado("DANJU_MOVIES", movies)
    escribir_ordenado("DANJU_SERIES", series)
    
    print("Listas procesadas, limpias y ordenadas alfabéticamente exitosamente.")

if __name__ == "__main__":
    procesar_listas()
