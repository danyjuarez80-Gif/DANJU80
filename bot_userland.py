import requests
import re

ARCHIVO = "lista_danju80.m3u"
# Las páginas que mencionó Jhon Doe
FUENTES = ["https://www.rojadirectatv.tv", "https://jeinzmacias.net", "https://futbollibre.ec"]

def scraping_trafico_interno():
    print("--- INICIANDO RASTREO DE COMPONENTES DE VIDEO ---")
    enlaces = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Tecno Pova 6)',
        'Referer': 'https://google.com'
    }

    for url in FUENTES:
        try:
            print(f"Analizando tráfico de: {url}")
            # 1. Entramos a la página base
            response = requests.get(url, headers=headers, timeout=15).text
            
            # 2. Buscamos el 'componente de video' (normalmente un iframe o un script de stream)
            componentes = re.findall(r'src="([^"]+)"', response)
            
            for comp in componentes:
                # El truco de Jhon Doe: buscar la comunicación interna
                if "m3u8" in comp or "stream" in comp or "embed" in comp:
                    print(f"Componente detectado: {comp[:50]}...")
                    
                    # 3. Interceptamos el flujo interno
                    try:
                        r_interna = requests.get(comp if comp.startswith('http') else url+comp, headers=headers, timeout=5).text
                        # Buscamos el flujo de datos real (el que no tiene tokens vencidos)
                        match = re.search(r'["\'](http[^"\']+\.m3u8[^"\']*)["\']', r_interna.replace('\\/', '/'))
                        
                        if match:
                            link_final = match.group(1)
                            nombre = url.split('.')[1].upper()
                            enlaces.append(f"#EXTINF:-1, [TRAFFIC-SCAN] {nombre}\n{link_final}")
                            print(f"✅ ¡FLUJO INTERNO CAPTURADO!")
                    except: continue
        except: continue
    return enlaces

if __name__ == "__main__":
    resultado = scraping_trafico_interno()
    if resultado:
        with open(ARCHIVO, "w") as f:
            f.write("#EXTM3U\n" + "\n".join(resultado))
        print(f"\nSe capturaron {len(resultado)} flujos internos exitosamente.")
    else:
        print("\nNo se detectó tráfico de video abierto. Los componentes están encriptados.")
