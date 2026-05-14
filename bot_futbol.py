import requests
import re

# Configuración de archivos
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_FUENTE = "https://futbollibre.ec/"

def extraer_canales():
    canales_encontrados = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': URL_FUENTE
    }
    
    try:
        # 1. El bot visita la página principal
        response = requests.get(URL_FUENTE, headers=headers, timeout=15)
        if response.status_status != 200:
            return canales_encontrados

        # 2. Buscamos enlaces a los partidos/canales (suelen estar en etiquetas <a>)
        # Este regex busca patrones comunes de canales en esa web
        patrones = re.findall(r'href="(https?://futbollibre.ec/embed/[^"]+)"', response.text)
        
        # Eliminamos duplicados
        enlaces_unicos = list(set(patrones))
        
        for i, link in enumerate(enlaces_unicos):
            # Formateamos para M3U
            # Nota: Algunos reproductores necesitan el User-Agent y Referer para abrir estos links
            nombre = f"Futbol Libre Canal {i+1}"
            canales_encontrados.append({
                "nombre": nombre,
                "url": link
            })
            
        return canales_encontrados
    except Exception as e:
        print(f"Error al extraer: {e}")
        return []

def generar_lista():
    # Leer tus canales fijos que creaste en el paso anterior
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            contenido_fijo = f.read()
    except FileNotFoundError:
        contenido_fijo = "#EXTM3U\n"

    # Obtener los nuevos canales del bot
    nuevos_canales = extraer_canales()

    # Escribir la lista final combinada
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        # Escribimos tus canales fijos primero (para no borrarlos)
        f.write(contenido_fijo.strip() + "\n")
        
        # Agregamos los que encontró el bot
        if nuevos_canales:
            f.write("\n# --- CANALES AGREGADOS POR EL BOT ---\n")
            for canal in nuevos_canales:
                f.write(f"#EXTINF:-1, [LIVE] {canal['nombre']}\n")
                # Agregamos parámetros de red para que funcionen mejor
                f.write(f"{canal['url']}|User-Agent=Mozilla/5.0&Referer={URL_FUENTE}\n")
            print(f"Se agregaron {len(nuevos_canales)} canales.")
        else:
            print("No se encontraron canales nuevos en esta vuelta.")

if __name__ == "__main__":
    generar_lista()
