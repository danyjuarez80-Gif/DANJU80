import requests
import re
import os

ARCHIVO_FINAL = "lista_danju80.m3u"
# Agregamos la fuente exacta de tu video
FUENTES = ["https://tvplusgratis2.com", "https://futbollibre.ec", "https://librefutboltv.com"]
PRIORIDAD = ["espn", "fox", "tudn", "directv", "caliente", "telemundo", "univision", "azteca"]

def cazar_dinamico():
    print("--- Iniciando Rastreo de Tráfico Dinámico ---")
    enlaces_encontrados = []
    sesion = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    }

    for url in FUENTES:
        try:
            print(f"Entrando a: {url}")
            # Paso 1: Obtener la página principal
            home = sesion.get(url, headers=headers, timeout=10).text
            # Paso 2: Buscar los IFRAMES o archivos JS que cargan el video
            # Esta regex busca cualquier cosa que parezca un servidor de video
            scripts = re.findall(r'src="([^"]+?\.js[^"]*)"', home)
            iframes = re.findall(r'src="([^"]+?embed[^"]*)"', home)
            
            # Combinamos todo para revisar
            objetivos = list(set(iframes + scripts))
            
            for obj in objetivos:
                # Si el enlace es relativo, le ponemos el dominio
                target_url = obj if obj.startswith('http') else url + obj
                
                # Buscamos nombres clave en la URL
                if any(p in target_url.lower() for p in PRIORIDAD):
                    print(f"Cazando señal en: {target_url}")
                    # Paso 3: "Simulamos" la entrada al reproductor
                    r_final = sesion.get(target_url, headers=headers, timeout=10).text
                    
                    # Buscamos el m3u8 incluso si está oculto o escapado con barras ( \/ )
                    m3u8_matches = re.findall(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', r_final.replace('\\/', '/'))
                    
                    for m in m3u8_matches:
                        # Limpiamos el link de posibles residuos de código
                        clean_link = m.split('"')[0].split("'")[0]
                        nombre_canal = target_url.split('/')[-1].split('.')[0].replace('-', ' ').upper()
                        
                        formato = f"#EXTINF:-1, [TV] {nombre_canal}\n{clean_link}|Referer={url}/"
                        if formato not in enlaces_encontrados:
                            enlaces_encontrados.append(formato)
                            print(f"¡LOGRADO!: {nombre_canal}")
        except Exception as e:
            print(f"Error en fuente: {e}")
            
    return enlaces_encontrados

if __name__ == "__main__":
    resultado = cazar_dinamico()
    if resultado:
        with open(ARCHIVO_FINAL, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(resultado))
        print(f"--- Éxito: {len(resultado)} canales nuevos capturados ---")
    else:
        print("--- No se pudo extraer el m3u8. La web requiere clic manual o JS ---")
