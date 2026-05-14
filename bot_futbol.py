import requests
import re

# Configuración
ARCHIVO_FIJOS = "fijos.m3u"
ARCHIVO_FINAL = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec/"

def extraer_con_iframes():
    enlaces_finales = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Referer': URL_BASE
    }

    try:
        # 1. Obtener la página principal
        sesion = requests.Session()
        r = sesion.get(URL_BASE, headers=headers, timeout=15)
        
        # 2. Buscar las URLs de los "Embeds" (donde están los clics)
        embeds = re.findall(r'href="(https?://futbollibre.ec/embed/[^"]+)"', r.text)
        
        for url_embed in embeds:
            # El bot "entra" al reproductor simulando el primer clic
            r_embed = sesion.get(url_embed, headers=headers, timeout=10)
            
            # 3. Buscar dentro del reproductor el archivo .m3u8 real
            # Aquí es donde se oculta el link tras los "3 clics"
            match = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_embed.text)
            if not match:
                match = re.search(r'file:\s*"([^"]+\.m3u8[^"]*)"', r_embed.text)
                
            if match:
                link_directo = match.group(1)
                enlaces_finales.append(link_directo)

        return list(set(enlaces_finales))
    except Exception as e:
        print(f"Error: {e}")
        return []

def generar_lista():
    # Mantener tus avances y archivos fijos (DANJU80)
    try:
        with open(ARCHIVO_FIJOS, "r", encoding="utf-8") as f:
            contenido_fijo = f.read().strip()
    except FileNotFoundError:
        contenido_fijo = "#EXTM3U"

    links = extraer_con_iframes()

    with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
        f.write(contenido_fijo + "\n\n")
        f.write("# --- CANALES DETECTADOS TRAS SIMULAR CLICS ---\n")
        
        if links:
            for i, l in enumerate(links):
                f.write(f"#EXTINF:-1, [BOT] Canal Activo {i+1}\n")
                f.write(f"{l}|User-Agent={headers['User-Agent']}&Referer={URL_BASE}\n")
        else:
            f.write("# No hubo eventos en vivo detectados.\n")

if __name__ == "__main__":
    generar_lista()
