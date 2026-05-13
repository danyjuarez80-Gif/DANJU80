import requests

ARCHIVO_SALIDA = "DANJU80"

FUENTES = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/ar.m3u",
    "https://iptv-org.github.io/iptv/countries/co.m3u",
    "https://iptv-org.github.io/iptv/countries/es.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",  # ⭐ Todos los deportes
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
    "Multicanal", "Canal Sur Deportes", "Real Madrid TV",
    "Barcelona TV", "Antena 3 Deportes"
]

CANALES_DESEADOS = CANALES_GENERALES + CANALES_DEPORTES

def extraer_canales(m3u_texto, nombres_deseados):
    lineas = m3u_texto.splitlines()
    resultado = []
    vistos = set()
    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if linea.startswith("#EXTINF"):
            nombre_canal = linea.split(",")[-1].strip()
            if any(d.lower() in nombre_canal.lower() for d in nombres_deseados):
                if i + 1 < len(lineas):
                    url = lineas[i + 1].strip()
                    clave = nombre_canal.lower()
                    if clave not in vistos:  # Evita duplicados
                        vistos.add(clave)
                        resultado.append((nombre_canal, url))
        i += 1
    return resultado

def ejecutar():
    canales = []
    for fuente in FUENTES:
        try:
            r = requests.get(fuente, timeout=15)
            r.raise_for_status()
            encontrados = extraer_canales(r.text, CANALES_DESEADOS)
            canales += encontrados
            print(f"📡 {fuente.split('/')[-1]}: {len(encontrados)} canales")
        except Exception as e:
            print(f"⚠️ Error en {fuente}: {e}")

    if not canales:
        print("❌ No se encontraron canales.")
        return

    # Ordenar: primero generales, luego deportes
    lineas = ["#EXTM3U"]
    for nombre, url in canales:
        lineas.append(f"#EXTINF:-1,{nombre}")
        lineas.append(url)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

    print(f"\n✅ {len(canales)} canales guardados en {ARCHIVO_SALIDA}")

if __name__ == "__main__":
    ejecutar()
