import os

def procesar():
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Inicializar con cabecera
    archivos = {"DANJU80": ["#EXTM3U"], "DANJU_MOVIES": ["#EXTM3U"], "DANJU_SERIES": ["#EXTM3U"]}
    
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Procesar bloques de dos líneas (#EXTINF + URL)
    for i in range(0, len(lineas) - 1, 2):
        l1, l2 = lineas[i].strip(), lineas[i+1].strip()
        if not l1.startswith("#EXTINF"): continue
        
        # Clasificar según contenido
        cat = "DANJU80" # Default
        texto = (l1 + l2).lower()
        if any(x in texto for x in ["series", "s0", "episodio", "capitulo"]): cat = "DANJU_SERIES"
        elif any(x in texto for x in ["movie", "pelicula"]): cat = "DANJU_MOVIES"
        
        archivos[cat].extend([l1, mascara, l2])

    # Guardar
    for nombre, contenido in archivos.items():
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))

if __name__ == "__main__":
    procesar()
