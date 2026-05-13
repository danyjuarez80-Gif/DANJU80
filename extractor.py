import requests

ARCHIVO_SALIDA = "DANJU80"

FUENTES = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/ar.m3u",
    "https://iptv-org.github.io/iptv/countries/co.m3u",
    "https://iptv-org.github.io/iptv/countries/es.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
]

CANALES_GENERALES = [
    "Telemundo", "Azteca 7", "Canal 5", "Las Estrellas", "Univision"
]

CANALES_DEPORTES = [
    "ESPN", "Fox Sports", "TUDN", "Claro Sports", "Win Sports",
    "Marca", "Gol", "DAZN", "Teledeporte", "TyC Sports",
    "DirecTV Sports", "Star Sports", "One Sports", "Sky Sports",
    "beIN Sports", "Sport TV", "Eurosport", "NBC Sports",
    "NFL Network", "NBA TV", "MLB Network", "Golf Channel",
    "Tennis Channel", "Motorsport", "Sport", "Deportes",
    "Canal Sur Deportes", "Real Madrid TV", "Antena 3 Deportes"
]

CANALES_DESEADOS = CANALES_GENERALES + CANALES_DEPORTES


def leer_lista_existente(archivo):
    """Lee tu lista actual y extrae las URLs ya guardadas para no duplicar."""
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        urls_existentes = set()
        lineas = contenido.splitlines()
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith("http"):
                urls_existentes.add(linea)
        return contenido.rstrip(), urls_existentes
    except FileNotFoundError:
        return "#EXTM3U", set()


def extraer_canales(m3u_texto, nombres_deseados, urls_existentes):
    """Extrae canales que NO están ya en tu lista."""
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
                    if url not in urls_existentes:  # Solo si es nuevo
                        resultado.append((nombre_canal, url))
                        urls_existentes.add(url)  # Marca como visto
        i += 1
    return resultado


def ejecutar():
    # 1. Leer tu lista actual
    contenido_actual, urls_existentes = leer_lista_existente(ARCHIVO_SALIDA)
    print(f"📋 Lista actual: {len(urls_existentes)} canales existentes")

    # 2. Buscar canales nuevos en las fuentes
    canales_nuevos = []
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

    # 3. Agregar al FINAL de tu lista sin tocar nada
    nuevas_lineas = []
    for nombre, url in canales_nuevos:
        nuevas_lineas.append(f"#EXTINF:-1,{nombre}")
        nuevas_lineas.append(url)

    contenido_final = contenido_actual + "\n" + "\n".join(nuevas_lineas)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write(contenido_final)

    print(f"\n✅ {len(canales_nuevos)} canales nuevos agregados al final de {ARCHIVO_SALIDA}")


if __nam
