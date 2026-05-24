import os
import re

def procesar_archivo(archivo):
    if not os.path.exists(archivo): return
    with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()
    
    grupos = {}
    cat_actual = "SIN CATEGORIA"
    
    # Agrupar por group-title
    for i in range(len(lineas)):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            match = re.search(r'group-title="([^"]+)"', linea)
            cat_actual = match.group(1) if match else "SIN CATEGORIA"
            if cat_actual not in grupos: grupos[cat_actual] = []
            grupos[cat_actual].append((linea, lineas[i+1].strip() if i+1 < len(lineas) else ""))
            i += 1
            
    # Escribir ordenado
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in sorted(grupos.keys()):
            for nombre, url in sorted(grupos[cat], key=lambda x: x[0]):
                f.write(f"{nombre}\n{url}\n")

if __name__ == "__main__":
    procesar_archivo("DANJU80")
    procesar_archivo("DANJU_MOVIES")
    procesar_archivo("DANJU_SERIES")
