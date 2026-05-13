import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    lineas = ["#EXTM3U"]
    try:
        r = requests.get(URL_RESCATE, timeout=10)
        if r.status_code == 200:
            # Recuperamos todo lo que no sea el Azteca que falló
            lineas = [l.strip() for l in r.text.splitlines() if l.strip() and "Azteca 7" not in l and "samsung" not in l]
    except: pass

    # --- LINK DE ALTA DISPONIBILIDAD ---
    # Este link es un espejo estable que no suele pedir tokens de IP
    nuevo_azteca = [
        '#EXTINF:-1 group-title="MEXICO",Azteca 7 (Respaldo)',
        'https://stream.tvazteca.com/live/azteca7/playlist.m3u8'
    ]

    # Armamos la lista asegurando que #EXTM3U esté al inicio
    if not lineas or "#EXTM3U" not in lineas[0]:
        lineas.insert(0, "#EXTM3U")
    
    resultado = lineas + nuevo_azteca
    texto = "\n".join(resultado)

    # Guardamos ahora que ya tenemos permisos
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ ¡Bot actualizó con el link de respaldo estable!")

if __name__ == "__main__":
    ejecutar()
