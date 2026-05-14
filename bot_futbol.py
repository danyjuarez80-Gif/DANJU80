import requests
import re

# Configuración
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
# Probamos con la URL que pasaste
URL_FUENTE = "https://futbollibre.ec/"

def extraer_links_reales():
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://google.com'
    }
    
    try:
        # 1. Entrar a la página principal
        r = requests.get(URL_FUENTE, headers=headers, timeout=15)
        
        # 2. Buscar enlaces de transmisiones (m3u8, ts, o reproductores embed)
        # Buscamos patrones de video y de las páginas internas de partidos
        patrones = [
            r'https?://[\w\.\-/]+\.m3u8',
            r'https?://[\w\.\-/]+\.ts',
            r'href="(https?://futbollibre.ec/embed/[^"]+)"',
            r'src="(https?://[\w\.\-/]+embed[^"]+)"'
        ]
        
        for p in patrones:
            encontrados = re.findall(p, r.text)
            for link in encontrados:
                if link not in enlaces:
                    enlaces.append(link)
        
        return enlaces
    except Exception as e:
        print(f"Error de conexión: {e}")
        return []

def generar_lista():
    # Cargar tus canales fijos (los que DANJU80 ya tiene)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            contenido_fijo = f.read().strip()
    except FileNotFoundError:
        contenido_fijo = "#EXTM3U"

    links_encontrados = extraer_links_reales()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(contenido_fijo + "\n\n")
        f.write("# --- CANALES DE FUTBOL LIBRE ---\n")
        
        if not links_encontrados:
            f.write("# El bot no encontró links activos en este momento.\n")
        else:
            for i, link in enumerate(links_encontrados):
                f.write(f"#EXTINF:-1, [BOT] Canal {i+1}\n")
                f.write(f"{link}|Referer={URL_FUENTE}\n")
                
    print(f"Lista actualizada con {len(links_encontrados)} enlaces.")

if __name__ == "__main__":
    generar_lista()
