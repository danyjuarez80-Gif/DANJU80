import requests
import re
import os

ARCHIVO = "lista_danju80.m3u"
URL_BASE = "https://futbollibre.ec"

# Canales que vamos a "atacar"
PRIORIDAD = ["espn", "fox", "tudn", "directv", "caliente", "telemundo", "univision", "azteca"]

def operacion_infiltrado():
    print("--- INICIANDO EXTRACCIÓN DINÁMICA ---")
    enlaces = []
    
    # Headers para engañar al servidor (suplantamos tu Tecno Pova 6 en México)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6) AppleWebKit/537.36',
        'Referer': URL_BASE,
        'Accept-Language': 'es-MX,es;q=0.9'
    }

    try:
        # 1. Escaneamos la portada para buscar los IDs de los canales
        r_home = requests.get(URL_BASE, headers=headers, timeout=10).text
        canales_encontrados = re.findall(r'href="(/embed/[^"]+)"', r_home)
        
        for path in list(set(canales_encontrados)):
            nombre_canal = path.split("/")[-1].replace("-", " ").lower()
            
            if any(p in nombre_canal for p in PRIORIDAD):
                print(f"Vulnerando seguridad de: {nombre_canal.upper()}...")
                
                # 2. SEGUNDO SALTO: Entramos al reproductor profundo
                # Aquí es donde ocurre la magia: buscamos el m3u8 oculto
                r_embed = requests.get(URL_BASE + path, headers=headers, timeout=10).text
                
                # Buscamos enlaces m3u8 que estén "escapados" o escondidos en variables JS
                # Esta regex limpia las barras inclinadas que usan para engañar bots
                match = re.search(r'(https?://[^\s"\'<>]+?\.m3u8[^\s"\'<>]*)', r_embed.replace('\\/', '/'))
                
                if match:
                    link_real = match.group(1).split('"')[0].split("'")[0]
                    # Agregamos el Referer para que el link no muera al usarlo
                    enlaces.append(f"#EXTINF:-1, [HACKED] {nombre_canal.upper()}\n{link_real}|Referer={URL_BASE}/")
                    print(f"¡SISTEMA VULNERADO! Link extraído.")
                else:
                    print(f"Escudo detectado en {nombre_canal}. Requiere bypass de JS.")
                    
    except Exception as e:
        print(f"Error en la operación: {e}")
        
    return enlaces

if __name__ == "__main__":
    lista_final = operacion_infiltrado()
    if lista_final:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(lista_final))
        print(f"\nOperación exitosa: {len(lista_final)} canales extraídos.")
    else:
        print("\nNo se pudieron romper las defensas de la página en esta pasada.")
