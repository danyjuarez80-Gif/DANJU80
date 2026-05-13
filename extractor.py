import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]

def ejecutar():
    # Este 'disfraz' es el mismo que usa Web Video Caster (Chrome en Android)
    disfraz = "|User-Agent=Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    
    # Canales directos de Samsung (Wurl) que funcionan en Mexico
    canales = [
        {"n": "Azteca 7 HD", "u": "https://televisa-latam-azteca7-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
        {"n": "Telemundo", "u": "https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8"},
        {"n": "NASA TV (Prueba)", "u": "https://ntv1.akamaized.net/hls/live/2014049/NASA-NTV1/master.m3u8"}
    ]

    lineas = ["#EXTM3U"]
    for c in canales:
        lineas.append(f'#EXTINF:-1 group-title="CANALES", {c["n"]}')
        # Pegamos el link con el disfraz al final
        lineas.append(f'{c["u"]}{disfraz}')

    texto = "\n".join(lineas)

    # El bot guarda los cambios (esto ya sabemos que funciona)
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ Bot configurado con disfraz de Web Video Caster")

if __name__ == "__main__":
    ejecutar()
