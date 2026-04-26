import re
import requests

# 1. Fuente del token fresco
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

# 2. Lista de canales (He resumido los nombres para evitar errores de caracteres)
mis_canales = [
    {"n": "Telemundo USA", "u": "https://plts3.envivoslatam.org/telemundousa/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"},
    {"n": "ESPN MX", "u": "https://qbk4f.envivoslatam.org/espnmx/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"},
    {"n": "TyC Sports", "u": "https://qzv4jmsc.fubohd.com/tycsports/mono.m3u8?token=TOKEN_AQUI"},
    {"n": "TNT Sports", "u": "https://8c51.streameasthd.net/global/tntsports/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"n": "DSports", "u": "https://agvyby.fubohd.com/dsports/mono.m3u8?token=TOKEN_AQUI"},
    {"n": "DSports 2", "u": "https://bgfuzq.fubohd.com/dsports2/mono.m3u8?token=TOKEN_AQUI"},
    {"n": "DSports Plus", "u": "https://24a1.streameasthd.net/global/dsportsplus/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"n": "Fox Sports 1 AR", "u": "https://pecdl1.streameasthd.net/global/fox1ar/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"n": "Win Sports", "u": "https://8c51.streameasthd.net/global/winsports/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"n": "TUDN USA", "u": "https://14c51.streameasthd.net/tudn_usa/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"},
    {"n": "Canal 5", "u": "https://qzv4jmsc.fubohd.com/canal5/mono.m3u8?token=TOKEN_AQUI"},
    {"n": "Telemundo News", "u": "https://d368vp0qqzvkid.cloudfront.net/11603/88889703/hls/master.m3u8?ads.vip=45.191.53.2"}
]

# Canales Estáticos (Links directos sin token variable)
estaticos = [
    "http://181.176.155.7:8090/play/a1qh/index.m3u8",
    "http://181.176.155.7:8090/play/a1wl/index.m3u8",
    "https://linear-893.frequency.stream/dist/xumo/893/hls/master/playlist_1920x1080.m3u8",
    "https://bein-esp-xumo.amagi.tv/playlistR720P.m3u8"
]

def automatizar():
    try:
        r = requests.get(URL_FUENTE, timeout=15)
        match = re.search(r'token=([a-zA-Z0-9\-_]+)', r.text)
        
        if match:
            token = match.group(1)
            print(f"Token encontrado: {token}")
            
            with open("lista_dany.m3u", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                # Escribir canales con token
                for c in mis_canales:
                    url = c['u'].replace("TOKEN_AQUI", token)
                    f.write(f"#EXTINF:-1 group-title=\"TV\", {c['n']}\n{url}\n")
                
                # Escribir canales estáticos
                for i, url in enumerate(estaticos):
                    f.write(f"#EXTINF:-1 group-title=\"Estaticos\", Canal Extra {i+1}\n{url}\n")
            
            print("Archivo M3U creado exitosamente.")
        else:
            print("No se pudo extraer el token de la fuente.")
    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    automatizar()
