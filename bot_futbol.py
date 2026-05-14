import requests
import re

# Configuración de archivos
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_FUENTE = "https://futbollibre.ec/"

def extraer_todo_tipo_links():
    enlaces_encontrados = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': URL_FUENTE
    }
    
    try:
        response = requests.get(URL_FUENTE, headers=headers, timeout=15)
        if response.status_code != 200:
            return []

        # BUSCADOR MULTI-FORMATO:
        # Busca .m3u8, .ts, archivos .m3u externos e incluso IPs con puertos (ej: http://192.168.1.1:8080)
        patrones = [
            r'https?://[\w\.\-/]+\.m3u8', # Enlaces M3U8
            r'https?://[\w\.\-/]+\.ts',   # Enlaces TS
            r'https?://[\w\.\-/]+\.m3u',  # Listas M3U externas
            r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+' # IPs directas con puerto
        ]
        
        for patron in patrones:
            encontrados = re.findall(patron, response.text)
            enlaces_encontrados.extend(encontrados)
        
        # Eliminar duplicados
        return list(set(enlaces_encontrados))
        
    except Exception as e:
        print(f"Error en la extracción: {e}")
        return []

def generar_lista():
    # 1. Cargar tus canales fijos (los que no se borran)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            contenido_fijo = f.read().strip()
    except FileNotFoundError:
        contenido_fijo = "#EXTM3U"

    # 2. Extraer todo lo que encuentre el bot
    links_bot = extraer_todo_tipo_links()

    # 3. Escribir el archivo final (Sobrescribe el final, pero mantiene tus fijos arriba)
    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(contenido_fijo + "\n\n")
        f.write("# --- CANALES EXTRAÍDOS (M3U8, TS, IPS) ---\n")
        
        for i, link in enumerate(links_bot):
            # Detectar tipo de archivo para el nombre
            tipo = "STREAM"
            if ".m3u8" in link: tipo = "M3U8"
            elif ".ts" in link: tipo = "TS"
            elif ".m3u" in link: tipo = "LISTA"
            
            f.write(f"#EXTINF:-1, [BOT] {tipo} - Canal {i+1}\n")
            # Agregamos Referer para saltar bloqueos en Android
            f.write(f"{link}|Referer={URL_FUENTE}\n")
            
    print(f"Proceso terminado. Se registraron {len(links_bot)} enlaces nuevos.")

if __name__ == "__main__":
    generar_lista()
