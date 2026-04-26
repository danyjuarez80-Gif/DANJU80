import requests
import re

URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

def generar_lista():
    try:
        # 1. Obtenemos el token o contenido de la fuente
        r = requests.get(URL_FUENTE, timeout=15)
        r.raise_for_status()
        token_fresco = r.text.strip()
        
        # 2. Tu lista de canales (Basada en tus capturas 54243 y 54244)
        canales = [
            {"n": "noticias 1 (Telemundo)", "u": "https://plts3.envivoslatam.org/telemundousa/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"},
            {"n": "noticias 14 (TyC)", "u": "https://qzv4jmsc.fubohd.com/tycsports/mono.m3u8?token=TOKEN_AQUI"},
            {"n": "noticias 80 (ESPN)", "u": "https://wp9xqedt.fubohd.com/espn/mono.m3u8?token=TOKEN_AQUI"},
            # Agrega aquí los demás de tu lista estática (54244.jpg)
            {"n": "Canal Estandar", "u": "http://181.176.155.7:8090/play/a1qh/index.m3u8"}
        ]

        # 3. Escribimos el archivo final
        with open("lista_dany.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for c in canales:
                # Si el canal usa token, lo reemplazamos
                url_final = c['u'].replace("TOKEN_AQUI", token_fresco)
                f.write(f'#EXTINF:-1 group-title="Dany TV",{c["n"]}\n')
                f.write(f"{url_final}\n")
        
        print(f"✅ Lista generada con token: {token_fresco[:10]}...")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generar_lista()
