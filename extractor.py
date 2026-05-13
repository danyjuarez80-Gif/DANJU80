import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]

def ejecutar():
    # Usaremos un link de Telemundo que es muy estable en USA
    # Pero le agregamos el 'User-Agent' al final para que no lo bloqueen
    user_agent = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    
    canal_telemundo = "https://telemundo-usa-east-1-mx.samsung.wurl.com/manifest/playlist.m3u8"
    
    contenido = [
        "#EXTM3U",
        f'#EXTINF:-1 group-title="PRUEBA",Telemundo (Con Disfraz)',
        f'{canal_telemundo}{user_agent}'
    ]

    texto = "\n".join(contenido)

    # El bot guarda los cambios gracias a tus permisos
    for nombre in GITHUB_FILES:
        with open(nombre, "w", encoding="utf-8") as f:
            f.write(texto)
    
    print("✅ Bot actualizó la lista con inyección de User-Agent.")

if __name__ == "__main__":
    ejecutar()
