import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]

def ejecutar():
    # Link de NASA TV (Cero bloqueos, funciona en todo el mundo)
    canal_prueba = [
        "#EXTM3U",
        '#EXTINF:-1 group-title="PRUEBA",NASA TV (Si este abre, el bot es inocente)',
        'https://ntv1.akamaized.net/hls/live/2014049/NASA-NTV1/master.m3u8'
    ]

    texto = "\n".join(canal_prueba)

    # El bot escribe los archivos con los permisos que ya activaste
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ Archivo de prueba técnica actualizado.")

if __name__ == "__main__":
    ejecutar()
