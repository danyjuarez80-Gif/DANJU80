import os
import re

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print(f"ERROR: {archivo_origen} no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Listas para almacenar los canales como tuplas (nombre, url)
    tv, movies, series = [], [], []

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            linea_limpia = re.sub(r'(tvg-logo|tvg-image|logo)=".*?"', '', linea)
            linea_limpia = re.sub(r'\s+', ' ', linea_limpia).strip()
            url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
            inf_low = linea_limpia.lower()
            url_low = url.lower()
            
            # Clasificación
            if "/series" in url_low or "series" in inf_low:
                series.append((linea_limpia, url))
            elif "/movie" in url_low or "movie" in inf_low or "pelic" in inf_low:
                movies.append((linea_limpia, url))
            else:
                tv.append((linea_limpia, url))
            i += 2
        else:
            i += 1

    # Función para ordenar y guardar
    def guardar_ordenado(nombre_archivo, lista):
        # Ordenamos la lista de tuplas alfabéticamente por el nombre (x[0])
        lista_ordenada = sorted(lista, key=lambda x: x[0])
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for nombre, url in lista_ordenada:
                f.write(f"{nombre}\n{url}\n")

    guardar_ordenado("DANJU80", tv)
    guardar_ordenado("DANJU_MOVIES", movies)
    guardar_ordenado("DANJU_SERIES", series)
    print("Listas procesadas, separadas y ordenadas alfabéticamente.")

if __name__ == "__main__":
    procesar_listas()
