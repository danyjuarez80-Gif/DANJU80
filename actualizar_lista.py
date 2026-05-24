import os

def procesar_listas():
    # Definimos los archivos que vamos a procesar
    archivos = ["DANJU80", "DANJU_MOVIES", "DANJU_SERIES"]
    
    for nombre_archivo in archivos:
        if not os.path.exists(nombre_archivo):
            print(f"Saltando {nombre_archivo}: No existe.")
            continue
            
        with open(nombre_archivo, "r", encoding="utf-8", errors="ignore") as f:
            lineas = f.read().splitlines()

        # 1. Agrupar por categoría
        # Estructura: lista de dicts {'titulo': '---NOMBRE---', 'canales': [('inf', 'url'), ...]}
        bloques = []
        bloque_actual = None
        
        for i in range(len(lineas)):
            linea = lineas[i].strip()
            if not linea or linea.startswith("#EXTM3U"):
                continue
            
            # Detecta si es un título de categoría
            if "----------" in linea:
                if bloque_actual:
                    bloques.append(bloque_actual)
                bloque_actual = {'titulo': linea, 'canales': []}
            elif linea.startswith("#EXTINF") and bloque_actual:
                url = lineas[i+1].strip() if i+1 < len(lineas) else ""
                bloque_actual['canales'].append((linea, url))
        
        if bloque_actual:
            bloques.append(bloque_actual)

        # 2. Ordenar alfabéticamente los canales dentro de cada bloque
        for b in bloques:
            b['canales'].sort(key=lambda x: x[0])

        # 3. Ordenar alfabéticamente los bloques por su título
        bloques.sort(key=lambda x: x['titulo'])

        # 4. Reescribir el archivo
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for b in bloques:
                f.write(f"\n{b['titulo']}\n")
                for canal, url in b['canales']:
                    f.write(f"{canal}\n{url}\n")
                    
    print("Listas ordenadas: categorías y canales en orden alfanumérico.")

if __name__ == "__main__":
    procesar_listas()
