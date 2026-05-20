import os

def actualizar():
    # Solo procesamos si el archivo origen tiene contenido
    if not os.path.exists("dan88.txt") or os.path.getsize("dan88.txt") == 0:
        print("Error: dan88.txt vacío o no encontrado.")
        return

    mascara = "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    
    with open("dan88.txt", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nueva_lista = []
    for linea in lineas:
        linea = linea.strip()
        if not linea: continue
        nueva_lista.append(linea)
        # Inyectar máscara solo después de enlaces http
        if linea.startswith("http"):
            nueva_lista.append(mascara)

    # Solo guardamos si la lista tiene más de 1 línea (evitamos vaciar archivos)
    if len(nueva_lista) > 1:
        with open("DANJU80", "w", encoding="utf-8") as f:
            f.write("\n".join(nueva_lista))
        print("DANJU80 actualizado con éxito.")

if __name__ == "__main__":
    actualizar()
