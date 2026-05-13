import requests

GITHUB_FILES = ["DANJU80", "lista_dany.m3u"]

# Fuente pública mantenida y actualizada
FUENTE_MX = "https://iptv-org.github.io/iptv/countries/mx.m3u"
FUENTE_US = "https://iptv-org.github.io/iptv/countries/us.m3u"

CANALES_DESEADOS = ["Telemundo", "Azteca 7", "Canal 5", "Las Estrellas"]

def extraer_canales(m3u_texto, nombres_deseados):
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
                    resultado.append((nombre_canal, url))
        i += 1
    return resultado

def ejecutar():
    canales = []
    for fuente in [FUENTE_MX, FUENTE_US]:
        try:
            r = requests.get(fuente, timeout=10)
            r.raise_for_status()
            canales += extraer_canales(r.text, CANALES_DESEADOS)
        except Exception as e:
            print(f"⚠️ Error descargando fuente: {e}")

    if not canales:
        print("❌ No se encontraron canales.")
        return

    lineas = ["#EXTM3U"]
    for nombre, url in canales:
        lineas.append(f"#EXTINF:-1,{nombre}")
        lineas.append(url)

    texto = "\n".join(lineas)

    for nombre_archivo in GITHUB_FILES:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(texto)

    print(f"✅ Lista actualizada con {len(canales)} canales.")

if __name__ == "__main__":
    ejecutar()
