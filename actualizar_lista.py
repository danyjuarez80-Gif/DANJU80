import os

# Nombre del archivo donde se guardará el resultado final
ARCHIVO_SALIDA = "DANJU80"

def aplicar_mascara():
    # Leer el archivo origen original
    with open("dan88.txt", "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    # Escribir el archivo manteniendo la estructura original
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        for linea in lineas:
            f.write(linea) # Escribir la línea original tal cual
            if linea.strip().startswith("http"):
                f.write(mascara + "\n") # Inyectar máscara

if __name__ == "__main__":
    aplicar_mascara()
