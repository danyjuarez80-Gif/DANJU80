import os
import re
from collections import defaultdict

def procesar_listas():
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print(f"ERROR: {archivo_origen} no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Usamos diccionarios para agrupar por categoría
    # Estructura: categorias[nombre_categoria] = [(nombre_canal, url), ...]
    data = {
        "TV": [],
        "MOVIES": [],
        "SERIES": []
    }

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            linea_limpia = re.sub(r'(tvg-logo|tvg-image|logo)=".*?"', '', linea)
            linea_limpia = re.sub(r'\s+', ' ', linea_limpia).strip()
            url = lineas[i+1].strip() if i + 1 < len(lineas) else ""
            
            inf_low = linea_limpia.lower()
            url_low = url.lower()

            # Clasificación (Categoría)
            if "/series" in url_low or "series" in inf_low:
                data["SERIES"].append((linea_limpia, url))
            elif "/movie" in url_low or "movie" in inf_low or "pelic" in inf_low:
                data["MOVIES"].append((linea_limpia, url))
            else:
                data["TV"].append((linea_limpia, url))
            i += 2
        else:
            i += 1

    # Ordenar solo los canales DENTRO de su categoría
    for cat in data:
        data[cat].sort(key=lambda x: x[0])

    # Guardado: Aquí escribimos los archivos manteniendo la integridad
    def guardar(archivo, lista):
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in lista:
                f.write(f"{item[0]}\n{item[1]}\n")

    guardar("DANJU80", data["TV"])
    guardar("DANJU_MOVIES", data["MOVIES"])
    guardar("DANJU_SERIES", data["SERIES"])

if __name__ == "__main__":
    procesar_listas()
