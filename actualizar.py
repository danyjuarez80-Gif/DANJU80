import requests

ARCHIVOS_SALIDA = ["DANJU80", "lista_dany.m3u"]

# Fuentes públicas y gratuitas
FUENTES = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/ar.m3u",
    "https://iptv-org.github.io/iptv/countries/co.m3u",
    "https://iptv-org.github.io/iptv/countries/es.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
]

# Canales que pediste con URLs conocidas y estables (Tubi es legal y gratis)
CANALES_FIJOS = [
    {
        "nombre": "ESPN Deportes",
        "url": "https://e3.thetvapp.to/hls/espn-deportes/index.m3u8"
    },
    {
        "nombre": "Fox Deportes",
        "url": "https://live-news-manifest.tubi.video/live-news-manifest/csm/extlive/tubiprd01,Fox-Sports-Espanol2.m3u8"
    },
    {
        "nombre": "Fox Sports (Tubi)",
        "url": "https://aegis-cloudfront-1.tubi.video/63c84a5d-300a-4b9d-b1e8-40edbefb1ef6/index_1.m3u8"
    },
    {
        "nombre": "Caliente TV",
        "url": "https://live-news-manifest.tubi.video/live-news-manifest/csm/extlive/tubiprd01,Fox-Sports-Espanol2.m3u8"
    },
    {
        "nombre": "Canela Deportes",
        "url": "https://amg00658-amg00658c28-canelatv-international-5109.playouts.now.amagi.tv/playlist/amg00658-canelamediafast-deportesltta-canelatvinternational/playlist.m3u8"
    },
]

CANALES_DESEADOS = [
    # Los que pediste
    "ESPN", "Fox One", "Fox Deportes", "Fox Sports",
    "Univision", "TUDN", "UniMas", "Unimas",
    "Telemundo", "beIN", "bein",
    "Champions", "Claro Sports", "Caliente",
    # Extras deportivos
    "TyC Sports", "DirecTV Sports", "Win Sports",
    "DAZN", "Sky Sports", "NBC Sports", "Eurosport",
    "NFL Network", "NBA TV", "MLB Network",
    "Star Sports", "One Sports", "Deportes",
    # Generales
    "Las Estrellas", "Canal 5", "Azteca 7",
]


def leer_lista_existente(archivo):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        urls_existentes = set()
        for linea in contenido.splitlines():
            linea = linea.strip()
            if linea.startswith("http"):
                urls_existentes.add(linea)
        return contenido.rstrip(), urls_existentes
    except FileNotFoundError:
        return "#EXTM3U", set()


def extraer_canales(m3u_texto, nombres_deseados, urls_existentes):
    lineas = m3u_texto.splitlines()
    resultado = []
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if linea.startswith("#EXTINF"):
            nombre_canal = linea.split(",")[-1].strip()
            if any(d.lower() in nombre_canal.lower() for d in nombres_deseados):
                if i + 1 < len(lineas):
                    url = lineas[i + 1].strip()
                    if url not in urls_existentes:
                        resultado.append((nombre_canal, url))
                        urls_existentes.add(url)
        i += 1
    return resultado


def ejecutar():
    contenido_actual, urls_existentes = leer_lista_existente(ARCHIVOS_SALIDA[0])
    print(f"📋 Lista actual: {len(urls_existentes)} canales existentes")

    canales_nuevos = []

    # 1. Primero agregar canales fijos conocidos
    for c in CANALES_FIJOS:
        if c["url"] not in urls_existentes:
            canales_nuevos.append((c["nombre"], c["url"]))
            urls_existentes.add(c["url"])
            print(f"✅ Canal fijo agregado: {c['nombre']}")

    # 2. Luego buscar en fuentes iptv-org
    for fuente in FUENTES:
        try:
            r = requests.get(fuente, timeout=15)
            r.raise_for_status()
            encontrados = extraer_canales(r.text, CANALES_DESEADOS, urls_existentes)
            canales_nuevos += encontrados
            print(f"📡 {fuente.split('/')[-1]}: {len(encontrados)} canales nuevos")
        except Exception as e:
            print(f"⚠️ Error en {fuente}: {e}")

    if not canales_nuevos:
        print("✅ No hay canales nuevos que agregar.")
        return

    nuevas_lineas = []
    for nombre, url in canales_nuevos:
        nuevas_lineas.append(f"#EXTINF:-1,{nombre}")
        nuevas_lineas.append(url)

    contenido_final = contenido_actual + "\n" + "\n".join(nuevas_lineas)

    for archivo in ARCHIVOS_SALIDA:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_final)

    print(f"\n✅ {len(canales_nuevos)} canales nuevos en: {', '.join(ARCHIVOS_SALIDA)}")


if __name__ == "__main__":
    ejecutar()
