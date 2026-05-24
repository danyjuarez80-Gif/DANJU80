import os

def procesar_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return

    with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
        lineas = f.read().splitlines()

    # Estructura: categorias[nombre_categoria] = [lista de (inf, url)]
    categorias = {}
    cat_actual = "---------- SIN CATEGORIA ----------"

    i = 0
    while i < len(lineas):
        linea = lineas[i].strip()
        
        # Saltamos la cabecera #EXTM3U para volver a escribirla al inicio
        if linea.startswith("#EXTM3U"):
            i += 1
            continue
        
        # Detectar inicio de categoría (tu formato ----------NOMBRE---------)
        if "----------" in linea:
            cat_actual = linea
            if cat_actual not in categorias:
                categorias[cat_actual] = []
            i += 1
        elif linea.startswith("#EXTINF"):
            url = lineas[i+1].strip() if i+1 < len(lineas) else ""
            categorias.setdefault(cat_actual, []).append((linea, url))
            i += 2
        else:
            i += 1

    # Reescribir el archivo ordenado
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        # 1. Ordenamos las categorías de la A a la Z
        for cat in sorted(categorias.keys()):
            f.write(f"\n{cat}\n")
            # 2. Ordenamos los canales de esa categoría de la A a la Z
            for nombre, url in sorted(categorias[cat], key=lambda x: x[0]):
                f.write(f"{nombre}\n{url}\n")

if __name__ == "__main__":
    procesar_archivo("DANJU80")
    procesar_archivo("DANJU_MOVIES")
    procesar_archivo("DANJU_SERIES")
    print("Ordenamiento completado sin mezclar categorías.")
