import requests
import os

# Tu link directo de GitHub para no perder lo que ya tienes
URL_RAW = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def ejecutar():
    lineas_viejas = ["#EXTM3U"]
    try:
        # Recuperamos tus canales actuales para no dejar la lista vacía
        r = requests.get(URL_RAW, timeout=10)
        if r.status_code == 200:
            lineas_viejas = [l.strip() for l in r.text.splitlines() if l.strip()]
    except: pass

    # FUENTE NUEVA: Azteca 7 sin tantos bloqueos
    # El bot ahora aprende a usar links que no mueren en 5 minutos
    nuevo_canal = [
        '#EXTINF:-1 group-title="TV",Azteca 7 (Estable)',
        'https://cloud2.stweb.tv/azteca7/azteca7/playlist.m3u8'
    ]

    # Quitamos versiones viejas de Azteca 7 para que no se repitan
    lineas_limpias = [l for l in lineas_viejas if "Azteca 7" not in l and "34_.m3u8" not in l and "#EXTM3U" not in l]
    resultado = ["#EXTM3U"] + lineas_limpias + nuevo_canal

    # Guardamos forzosamente en ambos archivos
    contenido = "\n".join(resultado)
    with open("DANJU80", "w", encoding="utf-8") as f: f.write(contenido)
    with open("lista_dany.m3u", "w", encoding="utf-8") as f: f.write(contenido)
    print("✅ ¡Bot chambeando! Lista actualizada con éxito.")

if __name__ == "__main__":
    ejecutar()
