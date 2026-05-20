import os

def procesar():
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Inicializamos listas con la cabecera M3U
    listas = {"DANJU80": ["#EXTM3U"], "DANJU_MOVIES": ["#EXTM3U"], "DANJU_SERIES": ["#EXTM3U"]}
    
    if not os.path.exists("dan88.txt"):
        print("Archivo dan88.txt no encontrado")
        return

    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Procesamos bloques de 2 líneas
    for i in range(0, len(lineas) - 1, 2):
        l1, l2 = lineas[i].strip(), lineas[i+1].strip()
        if not l1.startswith("#EXTINF"): continue
        
        # Clasificación robusta
        linea_completa = (l1 + l2).lower()
        if "series" in linea_completa or "capitulo" in linea_completa:
            cat = "DANJU_SERIES"
        elif "movie" in linea_completa or "pelicula" in linea_completa:
            cat = "DANJU_MOVIES"
        else:
            cat = "DANJU80" # Todo lo demás va aquí
        
        listas[cat].extend([l1, mascara, l2])

    # Guardamos los archivos
    for nombre, contenido in listas.items():
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))

if __name__ == "__main__":
    procesar()
