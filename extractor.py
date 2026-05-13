import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    lineas = ["#EXTM3U"]
    try:
        # Rescatamos lo que ya tienes para no perder canales anteriores
        r = requests.get(URL_RESCATE, timeout=10)
        if r.status_code == 200:
            lineas = [l.strip() for l in r.text.splitlines() if l.strip() and "Azteca" not in l]
    except: pass

    # --- CANAL DE PRUEBA: TELEMUNDO (USA) ---
    # Este link debería abrir sin problemas desde la IP de GitHub y en tu red
    nuevo_canal = [
        '#EXTINF:-1 group-title="PRUEBA USA",Telemundo',
        'https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8'
    ]

    # Armamos la lista asegurando el formato correcto
    if not lineas or "#EXTM3U" not in lineas[0]:
        lineas.insert(0, "#EXTM3U")
    
    resultado = lineas + nuevo_canal
    texto = "\n".join(resultado)

    # Guardamos los archivos
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ ¡Prueba de Telemundo lista! Archivos actualizados.")

if __name__ == "__main__":
    ejecutar()
