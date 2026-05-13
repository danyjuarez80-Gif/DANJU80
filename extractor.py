import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]

def ejecutar():
    # El disfraz para que el servidor crea que somos un navegador
    ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    canales = [
        {"n": "Azteca 7 HD", "u": "https://televisa-latam-azteca7-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
        {"n": "Telemundo", "u": "https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8"}
    ]

    lineas = ["#EXTM3U"]
    for c in canales:
        lineas.append(f'#EXTINF:-1 group-title="MEXICO", {c["n"]}')
        # Esta es la instrucción especial que solo VLC y reproductores avanzados entienden
        lineas.append(f'#EXTVLCOPT:http-user-agent={ua}')
        lineas.append(c["u"])

    texto = "\n".join(lineas)

    # El bot guarda los cambios con tus permisos de escritura
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ Lista optimizada específicamente para VLC")

if __name__ == "__main__":
    ejecutar()
