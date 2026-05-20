import os

# Nombre de los archivos de salida
archivos = ["DANJU80", "DANJU_MOVIES", "DANJU_SERIES"]

def aplicar_mascara():
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Leer el original
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Procesar y escribir
    with open("DANJU80", "w", encoding="utf-8") as f:
        for linea in lineas:
            f.write(linea)
            if linea.strip().startswith("http"):
                f.write(mascara + "\n")
    
    # Si necesitas separar en archivos, copiamos el mismo contenido para recuperar los otros
    for archivo in ["DANJU_MOVIES", "DANJU_SERIES"]:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(open("DANJU80", "r").read())

if __name__ == "__main__":
    aplicar_mascara()
