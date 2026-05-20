import os

def procesar():
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Estructura maestra
    listas = {"DANJU80": ["#EXTM3U"], "DANJU_MOVIES": ["#EXTM3U"], "DANJU_SERIES": ["#EXTM3U"]}
    
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Procesar bloque de 2 líneas
    for i in range(0, len(lineas) - 1, 2):
        l1, l2 = lineas[i].strip(), lineas[i+1].strip()
        if not l1.startswith("#EXTINF"): continue
        
        # Clasificar por group-title presente en la línea
        l1_low = l1.lower()
        if "series" in l1_low or "series" in l2.lower():
            cat = "DANJU_SERIES"
        elif "pelicula" in l1_low or "movie" in l1_low:
            cat = "DANJU_MOVIES"
        else:
            cat = "DANJU80"
        
        listas[cat].extend([l1, mascara, l2])

    # Guardar
    for nombre, contenido in listas.items():
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))

if __name__ == "__main__":
    procesar()
