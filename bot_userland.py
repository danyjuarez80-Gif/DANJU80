import requests
import re
import os

ARCHIVO = "lista_danju80.m3u"
URL_OBJETIVO = "https://futbollibre.ec"

# Canales que vamos a intentar "hackear"
OBJETIVOS = ["espn", "fox", "tudn", "directv", "caliente", "telemundo", "univision"]

def hackear_futbol_libre():
    print("--- Iniciando Operación: Romper Seguridad ---")
    enlaces = []
    
    # Cabeceras de alto nivel para parecer un humano en México
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
        'Accept-Language': 'es-MX,es;q=0.9',
        'Referer': URL_OBJETIVO,
        'Origin': URL_OBJETIVO,
    }

    try:
        # 1. Entramos a la boca del lobo
        r_home = requests.get(URL_OBJETIVO, headers=headers, timeout=10).text
        # Buscamos las rutas de los reproductores
        canales_web = re.findall(r'href="(/embed/[^"]+)"', r_home)
        
        for path in canales_web:
            nombre = path.split('/')[-1].replace('-', ' ').lower()
            
            if any(p in nombre for p in OBJETIVOS):
                print(f"Intentando vulnerar: {nombre.upper()}...")
                
                # 2. SEGUNDO SALTO: Entramos al iframe donde esconden el m3u8
                r_embed = requests.get(URL_OBJETIVO + path, headers=headers, timeout=10).text
                
                # 3. EXTRACCIÓN: Buscamos el link m3u8 incluso si está "escapado" (https:\/\/...)
                # Usamos una regex que limpia las barras automáticamente
                link_sucio = re.search(r'source:\s*"([^"]+\.m3u8[^"]*)"', r_embed)
                
                if link_sucio:
                    # Limpiamos el link de las barras invertidas que ponen para engañar
                    link_real = link_sucio.group(1).replace('\\/', '/')
                    enlaces.append(f"#EXTINF:-1, [HACKED] {nombre.upper()}\n{link_real}|Referer={URL_OBJETIVO}/")
                    print(f"¡SISTEMA VULNERADO!: {nombre.upper()}")
                else:
                    print(f"Fallo en {nombre}: El token es dinámico.")
                    
    except Exception as e:
        print(f"Error en la operación: {e}")
        
    return enlaces

if __name__ == "__main__":
    lista_hacked = hackear_futbol_libre()
    if lista_hacked:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(lista_hacked))
        print(f"\nOperación exitosa. Se extrajeron {len(lista_hacked)} enlaces protegidos.")
    else:
        print("\nLa seguridad de la página bloqueó el rastreo automático.")
