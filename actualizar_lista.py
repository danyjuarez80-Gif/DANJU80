import os

def procesar_listas():
    # MÁSCARA VLC CONSTANTE
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Abrir archivo fuente
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Estructura de archivos
    resultados = {"DANJU80": ["#EXTM3U"], "DANJU_MOVIES": ["#EXTM3U"], "DANJU_SERIES": ["#EXTM3U"]}

    # Procesar bloques
    for i in range(0, len(lineas) - 1, 2):
        l1, l2 = lineas[i].strip(), lineas[i+1].strip()
        if l1.startswith("#EXTINF"):
            dest = "DANJU_SERIES" if any(x in l2.lower() or x in l1.lower() for x in ["series", "s0", "episodio"]) else \
                   "DANJU_MOVIES" if "movie" in l2.lower() or "movie" in l1.lower() else "DANJU80"
            resultados[dest].extend([l1, mascara, l2])

    # Sobreescribir archivos siempre (esto fuerza la actualización)
    for nombre, contenido in resultados.items():
        with open(nombre, "w", encoding="utf-8") as f:
            f.write("\n".join(contenido))

if __name__ == "__main__":
    procesar_listas()
