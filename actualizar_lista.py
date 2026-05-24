import os

def procesar_archivo(nombre_archivo):
    # Imprimir ruta absoluta para depurar
    print(f"Intentando procesar: {os.path.abspath(nombre_archivo)}")
    
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: {nombre_archivo} NO EXISTE en la ruta.")
        return

    with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    categorias = {}
    cat_actual = "---------- SIN CATEGORIA ----------"

    for i in range(len(lineas)):
        linea = lineas[i].strip()
        if not linea or linea.startswith("#EXTM3U"): continue
        if "----------" in linea:
            cat_actual = linea
            if cat_actual not in categorias: categorias[cat_actual] = []
        elif linea.startswith("#EXTINF"):
            url = lineas[i+1].strip() if i+1 < len(lineas) else ""
            categorias.setdefault(cat_actual, []).append((linea, url))

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in sorted(categorias.keys()):
            f.write(f"\n{cat}\n")
            for nombre, url in sorted(categorias[cat], key=lambda x: x[0]):
                f.write(f"{nombre}\n{url}\n")
    print(f"ÉXITO: {nombre_archivo} procesado.")

if __name__ == "__main__":
    procesar_archivo("DANJU80")
    procesar_archivo("DANJU_MOVIES")
    procesar_archivo("DANJU_SERIES")
