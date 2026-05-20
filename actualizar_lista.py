import os

def aplicar_mascara():
    archivo_origen = "dan88.txt"
    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.readlines()

    # Procesamos el archivo línea a línea
    resultado = []
    for linea in lineas:
        linea = linea.strip()
        resultado.append(linea)
        # Si la línea es una URL, inyectamos la máscara inmediatamente después
        if linea.startswith("http"):
            resultado.append(mascara)
            
    # Guardamos el archivo final (mantiene el nombre original o lo sobrescribes)
    with open("DANJU80", "w", encoding="utf-8") as f:
        f.write("\n".join(resultado))

if __name__ == "__main__":
    aplicar_mascara()
