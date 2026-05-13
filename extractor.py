import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]
# Tu link de rescate para no perder nada
URL_RESCATE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    lineas = ["#EXTM3U"]
    try:
        r = requests.get(URL_RESCATE, timeout=10)
        if r.status_code == 200:
            lineas = [l.strip() for l in r.text.splitlines() if l.strip()]
    except: pass

    # --- NUEVA FUENTE DE AZTECA 7 ---
    # Este link es directo y suele saltarse los bloqueos de IP
    nuevo_canal = [
        '#EXTINF:-1 group-title="TV",Azteca 7 (Directo)',
        'https://televisa-latam-azteca7-1-mx.samsung.wurl.com/manifest/playlist.m3u8'
    ]

    # Limpiamos los links que fallaron antes
    lineas_limpias = [l for l in lineas if "Azteca 7" not in l and "http" not in l and "#EXTM3U" not in l]
    
    contenido_final = ["#EXTM3U"] + lineas_limpias + nuevo_canal
    texto = "\n".join(contenido_final)

    # Guardamos (ahora que el bot ya tiene permiso)
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ ¡Bot actualizó con el link directo!")

if __name__ == "__main__":
    ejecutar()
