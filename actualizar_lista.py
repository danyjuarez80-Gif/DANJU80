import os

def procesar():
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Mantenemos tus tres archivos de destino
    archivos = {"DANJU80": ["#EXTM3U"], "DANJU_MOVIES": ["#EXTM3U"], "DANJU_SERIES": ["#EXTM3U"]}
    
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    for i in range(0, len(lineas) - 1, 2):
        l1, l2 = lineas[i].strip(), lineas[i+1].strip()
        if not l1.startswith("#EXTINF"): continue
        
        # CATEGORIZACIÓN FIJA (No cambiar)
        cat = "DANJU80"
        l_check = (l1 + l2).lower()
        if "series" in l_check or "s0" in l_check: cat = "DANJU_SERIES"
        elif "movie" in l_check or "pelicula" in l_check: cat = "DANJU_MOVIES"
        
        archivos[cat].extend([l1, mascara, l2])

    for nombre, contenido in archivos.items():
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))

if __name__ == "__main__":
    procesar()
