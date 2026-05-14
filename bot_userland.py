from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Configuración del navegador
chrome_options = Options()
chrome_options.add_argument("--headless") # Para que no veas la ventana abrirse
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

def extraer_con_clics():
    driver = webdriver.Chrome(options=chrome_options)
    canales_finales = []
    
    try:
        print("Entrando a Futbol Libre...")
        driver.get("https://futbollibre.ec/")
        time.sleep(5) # Esperamos a que cargue la lista

        # Buscamos los botones "Ver Canal"
        botones = driver.find_elements(By.XPATH, "//a[contains(@href, '/embed/')]")
        urls_canales = [b.get_attribute('href') for b in botones]

        for url in urls_canales:
            print(f"Abriendo canal: {url}")
            driver.get(url)
            time.sleep(8) # Simulamos el tiempo de los clics y comerciales
            
            # Buscamos el m3u8 en el código fuente después de que cargó el JS
            html = driver.page_source
            import re
            m3u8 = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', html)
            
            if m3u8:
                link = m3u8.group(1)
                print(f"¡Link capturado!: {link}")
                canales_finales.append(f"#EXTINF:-1, Canal\n{link}|Referer=https://futbollibre.ec/")

    finally:
        driver.quit()
    return canales_finales

# Guardar en tu archivo final
canales = extraer_con_clics()
with open("lista_userland.m3u", "w") as f:
    f.write("#EXTM3U\n" + "\n".join(canales))
print("Lista generada con éxito en lista_userland.m3u")
