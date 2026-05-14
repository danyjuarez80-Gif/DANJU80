import requests
import re

# Configuración
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_para_ver.m3u"
URL_FUTBOL = "https://futbollibre.ec/"

def extraer_m3u8():
    try:
        # El bot entra a la web
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL_FUTBOL, headers=headers, timeout=10)
        
        # BUSCADOR (Regex): Busca cualquier cosa que termine en .m3u8
        # Nota: Esto es un ejemplo, la web puede cambiar su estructura
        enlaces = re.findall(r'https?://[\w\.\-/]+\.m3u8', response.text)
        
        return enlaces[0] if enlaces else None
    except:
        return None

def generar_lista():
    # 1. Leer tus canales de siempre
    with open(ARCHIVO_FIJOS, "r") as f:
        contenido_fijo = f.read()

    # 2. Obtener el link nuevo del bot
    link_nuevo = extraer_m3u8()

    # 3. Crear el archivo final combinando ambos
    with open(ARCHIVO_FINAL, "w") as f:
        f.write(contenido_fijo) # Escribe lo viejo
        if link_nuevo:
            f.write(f"\n#EXTINF:-1, [BOT] Futbol Libre En Vivo\n")
            f.write(f"{link_nuevo}\n")
            print("¡Link de fútbol actualizado!")
        else:
            print("No se encontró link nuevo, se mantuvo la lista original.")

if __name__ == "__main__":
    generar_lista()
