import os
import re

def procesar_listas():
    # Leemos la lista original dan88.txt (donde está todo junto)
    archivo_origen = "dan88.txt"
    if not os.path.exists(archivo_origen):
        print(f"Error: {archivo_origen} no encontrado.")
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Clasificadores
    archivos = {"DANJU80": {}, "DANJU_MOVIES": {}, "DANJU_SERIES": {}}

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        if linea.startswith("#EXTINF"):
            url = lineas[i+1].strip() if i+1 < len(lineas) else ""
            
            # Detectar grupo
            match = re.search(r'group-title="([^"]+)"', linea)
            grupo = match.group(1) if match else "GENERAL"
            grupo_low = grupo.lower()
            
            # Clasificación estricta
            if "serie" in grupo_low:
                target = "DANJU_SERIES"
            elif "movie" in grupo_low or "pelic" in grupo_low:
                target = "DANJU_MOVIES"
            else:
                target = "DANJU80"
                
            archivos[target].setdefault(grupo, []).append((linea, url))
            i += 2
        else:
            i += 1

    # Escribir cada archivo
    for nombre_archivo, grupos in archivos.items():
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Ordenar grupos y canales
            for nombre_grupo in sorted(grupos.keys()):
                for extinf, url in sorted(grupos[nombre_grupo], key=lambda x: x[0]):
                    f.write(f"{extinf}\n{url}\n")
    print("Separación y ordenamiento estricto completado.")

if __name__ == "__main__":
    procesar_listas()
