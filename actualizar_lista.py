import os

def aplicar_mascara():
    # Leer el archivo original intacto
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Escribir el resultado manteniendo la estructura original
    with open("DANJU80", "w", encoding="utf-8") as f:
        for linea in lineas:
            f.write(linea)
            if linea.strip().startswith("http"):
                f.write(mascara + "\n")

if __name__ == "__main__":
    aplicar_mascara()
