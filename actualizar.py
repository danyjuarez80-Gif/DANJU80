import asyncio
import requests
from scraper_tvplus import scrape_tvplus

ARCHIVOS_SALIDA = ["DANJU80", "lista_dany.m3u"]

FUENTES = [
    "https://iptv-org.github.io/iptv/countries/mx.m3u",
    "https://iptv-org.github.io/iptv/countries/us.m3u",
    "https://iptv-org.github.io/iptv/countries/ar.m3u",
    "https://iptv-org.github.io/iptv/countries/co.m3u",
    "https://iptv-org.github.io/iptv/countries/es.m3u",
    "https://iptv-org.github.io/iptv/categories/sports.m3u",
]

CANALES_DESEADOS = [
    "ESPN", "Fox One", "Fox Deportes", "Fox Sports",
    "Univision", "TUDN", "UniMas", "Unimas",
    "Telemundo", "beIN", "bein",
    "Champions", "Claro Sports", "Caliente",
    "TyC Sports", "DirecTV Sports", "Win Sports",
    "DAZN", "Sky Sports", "NBC Sports", "Eurosport",
    "NFL Network", "NBA TV", "MLB Network",
    "Star Sports", "One Sports", "Deportes",
    "Las Estrellas", "Canal 5", "Azteca",
    "Imagen", "Multimedios", "Galavision",
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


def limpiar_url(url):
    # Quita parámetros, agente y referer — solo el link m3u8 limpio
    return url.split("?")[0]


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
                    url = limpiar_url(lineas[i + 1].strip())
                    if url not in urls_existentes:
                        resultado.append((nombre_canal, url))
                        urls_existentes.add(url)
        i += 1
    return resultado


def ejecutar():
    contenido_actual, urls_existentes = leer_lista_existente(ARCHIVOS_SALIDA[0])
    print(f"📋 Lista actual: {len(urls_existentes)} canales existentes\n")

    canales_nuevos = []

    # 1. Scrapear tvplusgratis2.com
    print("🌐 Scrapeando tvplusgratis2.com...")
    try:
        canales_scrapeados = asyncio.run(scrape_tvplus())
        for nombre, url in canales_scrapeados:
            if url not in urls_existentes:
                canales_nuevos.append((nombre, url))
                urls_existentes.add(url)
        print(f"✅ {len(canales_scrapeados)} canales obtenidos de tvplusgratis2\n")
    except Exception as e:
        print(f"⚠️ Error en scraper: {e}\n")

    # 2. Buscar en fuentes iptv-org
    print("📡 Buscando en fuentes iptv-org...")
    for fuente in FUENTES:
        try:
            r = requests.get(fuente, timeout=15)
            r.raise_for_status()
            encontrados = extraer_canales(r.text, CANALES_DESEADOS, urls_existentes)
            canales_nuevos += encontrados
            print(f"  {fuente.split('/')[-1]}: {len(encontrados)} canales nuevos")
        except Exception as e:
            print(f"  ⚠️ Error en {fuente}: {e}")

    if not canales_nuevos:
        print("\n✅ No hay canales nuevos que agregar.")
        return

    # 3. Guardar — formato limpio sin agente ni referer
    nuevas_lineas = []
    for nombre, url in canales_nuevos:
        nuevas_lineas.append(f"#EXTINF:-1,{nombre}")
        nuevas_lineas.append(url)  # Solo el link, nada más

    contenido_final = contenido_actual + "\n" + "\n".join(nuevas_lineas)

    for archivo in ARCHIVOS_SALIDA:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido_final)

    print(f"\n✅ {len(canales_nuevos)} canales nuevos en: {', '.join(ARCHIVOS_SALIDA)}")


if __name__ == "__main__":
    ejecutar()
