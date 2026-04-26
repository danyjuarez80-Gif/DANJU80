import re
import requests

# 1. De dónde sacamos el token fresco
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

# 2. Tu lista de canales (aquí puedes añadir todos los que quieras)
# Importante: Deja la palabra TOKEN_AQUI para que el script la reemplace
mis_canales = [
    {
        "nombre": "Telemundo", 
        "url": "https://plts3.envivoslatam.org/telemundousa/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"
    },
    {
        "nombre": "Canal 2", 
        "url": "https://ejemplo.com/stream.m3u8?token=TOKEN_AQUI"
    }
]

def automatizar():
    try:
        # Descargamos la fuente
        r = requests.get(URL_FUENTE, timeout=10)
        # El REGEX: busca 'token=' seguido de letras y números
        match = re.search(r'token=([a-zA-Z0-9]+)', r.text)
        
        if match:
            token_fresco = match.group(1)
            print(f"Token encontrado: {token_fresco}")
            
            # Creamos el archivo final M3U
            with open("lista_dany.m3u", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for canal in mis_canales:
                    url_final = canal['url'].replace("TOKEN_AQUI", token_fresco)
                    f.write(f"#EXTINF:-1, {canal['nombre']}\n")
                    f.write(f"{url_final}\n")
            
            print("✅ Lista 'lista_dany.m3u' actualizada con éxito.")
        else:
            print("❌ No se encontró el token en la fuente.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    automatizar()
