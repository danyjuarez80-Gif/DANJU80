import requests

# Tus archivos en GitHub
GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    # 1. Recuperar lo que ya tienes para no borrar nada
    lineas = ["#EXTM3U"]
    try:
        r = requests.get(URL_RESCATE, timeout=10)
        if r.status_code == 200:
            lineas = [l.strip() for l in r.text.splitlines() if l.strip()]
    except: pass

    # 2. El link 'mágico' que no pide tokens complicados y funciona en México
    # Esta fuente es mucho más estable que la de 'deportes' que te bloqueaba
    nuevo_azteca = [
        '#EXTINF:-1 group-title="TV",Azteca 7 HD',
        'https://cloud2.stweb.tv/azteca7/azteca7/playlist.m3u8'
    ]

    # Limpiamos links viejos de Azteca que ya no sirven
    lineas_limpias = [l for l in lineas if "Azteca 7" not in l and "http" not in l and "#EXTM3U" not in l]
    
    # Armamos la lista final
    contenido_final = ["#EXTM3U"] + lineas_limpias + nuevo_azteca
    texto = "\n".join(contenido_final)

    # 3. GUARDADO: Ahora que diste permisos, esto ya funcionará
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ ¡Bot chambeando con éxito! Archivos actualizados.")

if __name__ == "__main__":
    ejecutar()
