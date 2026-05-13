import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]

def ejecutar():
    # Links directos sin añadidos que rompan VLC
    canales = [
        {"nombre": "Telemundo", "url": "https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
        {"nombre": "Azteca 7", "url": "https://televisa-latam-azteca7-1-mx.samsung.wurl.com/manifest/playlist.m3u8"}
    ]

    lineas = ["#EXTM3U"]
    for c in canales:
        # Formato estándar de IPTV
        lineas.append(f'#EXTINF:-1, {c["nombre"]}')
        lineas.append(c["url"])

    texto = "\n".join(lineas)

    # El bot guarda los cambios en GitHub
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ Lista actualizada con links limpios para VLC.")

if __name__ == "__main__":
    ejecutar()
