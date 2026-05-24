import os
import re

def procesar_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return

    with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # grupos[nombre_del_grupo] = lista de (linea_extinf, url)
    grupos = {}
    
    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            # Extraer el group-title usando una expresión regular
            match = re.search(r'group-title="([^"]+)"', linea)
            nombre_grupo = match.group(1) if match else "SIN CATEGORIA"
            
            url = lineas[i+1].strip() if i+1 < len(lineas) else ""
            
            if nombre_grupo not in grupos:
                grupos[nombre_grupo] = []
            grupos[nombre_grupo].append((linea, url))
            i += 2
        else:
            i += 1

    # Reescribir el archivo ordenado
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        # 1. Ordenamos grupos alfabéticamente
        for nombre_grupo in sorted(grupos.keys()):
            # 2. Ordenamos canales dentro de cada grupo
            for extinf, url in sorted(grupos[nombre_grupo], key=lambda x: x[0]):
                f.write(f"{extinf}\n{url}\n")

if __name__ == "__main__":
    procesar_archivo("DANJU80")
    procesar_archivo("DANJU_MOVIES")
    procesar_archivo("DANJU_SERIES")
