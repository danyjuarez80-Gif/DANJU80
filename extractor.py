import re
import requests

# 1. Fuente del token fresco
URL_FUENTE = "https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/refs/heads/main/DANJU80"

# 2. Tu lista completa de canales (86 canales)
# Nota: He puesto "TOKEN_AQUI" en los que usan el formato de tu fuente.
mis_canales = [
    {"nombre": "noticias 1", "url": "https://plts3.envivoslatam.org/telemundousa/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"},
    {"nombre": "noticias 1 - Proxy", "url": "https://chevy.soyspace.cyou/proxy/dokko1/premium845/mono.css"},
    {"nombre": "noticias 1 - ESPN", "url": "https://qbk4f.envivoslatam.org/espnmx/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"},
    {"nombre": "noticias 1 - Play", "url": "http://181.176.155.7:8090/play/a1qh/index.m3u8"},
    {"nombre": "noticias 2", "url": "http://181.176.155.7:8090/play/a1wl/index.m3u8"},
    {"nombre": "noticias 3", "url": "http://181.176.155.7:8090/play/a1nv/index.m3u8"},
    {"nombre": "noticias 4", "url": "http://181.176.155.7:8090/play/a1vv/index.m3u8"},
    {"nombre": "noticias 5", "url": "http://181.176.155.7:8090/play/a1kd/index.m3u8"},
    {"nombre": "noticias 6", "url": "http://181.176.155.7:8090/play/a1e8/index.m3u8"},
    {"nombre": "noticias 7", "url": "http://181.176.155.7:8090/play/a1kh/index.m3u8"},
    {"nombre": "noticias 8", "url": "https://linear-893.frequency.stream/dist/xumo/893/hls/master/playlist_1920x1080.m3u8"},
    {"nombre": "noticias 9", "url": "https://bein-esp-xumo.amagi.tv/playlistR720P.m3u8"},
    {"nombre": "noticias 10", "url": "https://channel01-onlymex.akamaized.net/hls/live/2022749/event01/index_6.m3u8"},
    {"nombre": "noticias 11", "url": "https://azt-mun.otteravision.com/azt/mun/mun_360p.m3u8"},
    {"nombre": "noticias 12", "url": "https://regionales.saohgdasregions.fun:9092/NDUuMTkxLjUzLjI=/1_.m3u8?token=F6ND1pDapW91m8yWy1Frqw&expires=1775450685"},
    {"nombre": "noticias 13", "url": "https://deportes.ksdjugfsddeports.com:9092/NDUuMTkxLjUzLjI=/1_.m3u8?token=n6LjzkJvXSymagor_BHYGQ&expires=1775451183"},
    {"nombre": "noticias 14", "url": "https://qzv4jmsc.fubohd.com/tycsports/mono.m3u8?token=TOKEN_AQUI"},
    {"nombre": "noticias 15", "url": "https://8c51.streameasthd.net/global/tntsports/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"nombre": "noticias 16", "url": "https://agvyby.fubohd.com/dsports/mono.m3u8?token=TOKEN_AQUI"},
    {"nombre": "noticias 17", "url": "https://bgfuzq.fubohd.com/dsports2/mono.m3u8?token=TOKEN_AQUI"},
    {"nombre": "noticias 18", "url": "https://24a1.streameasthd.net/global/dsportsplus/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"nombre": "noticias 19", "url": "https://pecdl1.streameasthd.net/global/fox1ar/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"nombre": "noticias 20", "url": "https://8c51.streameasthd.net/global/winsports/index.m3u8?token=TOKEN_AQUI&ip=45.191.53.2"},
    {"nombre": "noticias 21", "url": "https://dai.google.com/linear/hls/event/yINISWAPQ0CPhPixe-40wQ/master.m3u8"},
    {"nombre": "noticias 22", "url": "https://d368vp0qqzvkid.cloudfront.net/11603/88889703/hls/master.m3u8?ads.vip=45.191.53.2"},
    {"nombre": "noticias 23", "url": "https://d368vp0qqzvkid.cloudfront.net/manifest/3fec3e5cac39a52b2132f9c66c83dae043dc17d4/prod_default_nbc-direct/1e4f5edc-8930-4101-a07b-856fc39cf821/5.m3u8"},
    {"nombre": "noticias 24", "url": "https://dw5pdgvk.fubohd.com/dsports/mono.m3u8?token=TOKEN_AQUI"},
    {"nombre": "noticias 25", "url": "https://14c51.streameasthd.net/tudn_usa/tracks-v1a1/mono.m3u8?ip=45.191.55.32&token=TOKEN_AQUI"},
    {"nombre": "noticias 26", "url": "https://14c51.streameasthd.net:443/tudn_usa/index.m3u8?token=TOKEN_AQUI&ip=45.191.55.32"},
    {"nombre": "noticias 27", "url": "https://deportes.ksdjugfsddeports.com:9092/NDUuMTkxLjU1LjMy/1_.m3u8?token=3dzfL3OS1hHR4ceGV7opyA&expires=1776270998"},
    {"nombre": "noticias 28", "url": "https://deportes.ksdjugfsddeports.com:9092/NDUuMTkxLjU1LjMy/1_.m3u8?token=rcrc-o6OIRVWJ1rbnChLqA&expires=1776271233"},
    {"nombre": "noticias 29", "url": "https://ym9yzq.fubohd.com/tudn/mono.m3u8?token=TOKEN_AQUI"},
    {"nombre": "noticias 30", "url": "https://d35j504z
