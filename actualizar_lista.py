import os

def procesar():
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Inicializar estructuras
    datos = {"DANJU80": ["#EXTM3U"], "DANJU_MOVIES": ["#EXTM3U"], "DANJU_SERIES": ["#EXTM3U"]}
    
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Procesar de 2 en 2 líneas
    for i in range(0, len(lineas) - 1, 2):
        l1, l2 = lineas[i].strip(), lineas[i+1].strip()
        if not l1.startswith("#EXTINF"): continue
        
        # Determinar categoría
        cat = "DANJU80" # Default
        texto = (l1 + l2).lower()
        if any(x in texto for x in ["series", "s0", "episodio"]): cat = "DANJU_SERIES"
        elif any(x in texto for x in ["movie", "pelicula"]): cat = "DANJU_MOVIES"
        
        # Guardar en su categoría correspondiente
        datos[cat].extend([l1, mascara, l2])

    # Escribir archivos
    for nombre, contenido in datos.items():
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))

if __name__ == "__main__":
    procesar()
