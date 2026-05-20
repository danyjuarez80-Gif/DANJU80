import os

def procesar_listas():
    archivo_origen = "dan88.txt"
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Listas inicializadas con la cabecera M3U
    listas = {"DANJU80": ["#EXTM3U"], "DANJU_MOVIES": ["#EXTM3U"], "DANJU_SERIES": ["#EXTM3U"]}

    if not os.path.exists(archivo_origen):
        return

    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Procesamiento por bloques de 2 líneas
    for i in range(0, len(lineas) - 1, 2):
        l1 = lineas[i].strip()
        l2 = lineas[i+1].strip()
        
        if l1.startswith("#EXTINF"):
            # Determinar destino
            destino = "DANJU80"
            if "series" in l2.lower() or "s0" in l1.lower():
                destino = "DANJU_SERIES"
            elif "movie" in l2.lower() or "movie" in l1.lower():
                destino = "DANJU_MOVIES"
            
            # Agregar el bloque formateado correctamente
            listas[destino].append(l1)
            listas[destino].append(mascara)
            listas[destino].append(l2)

    # Escritura forzada de los 3 archivos
    for nombre, contenido in listas.items():
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))
        print(f"Archivo {nombre} generado con {len(contenido)} lineas.")

if __name__ == "__main__":
    procesar_listas()
