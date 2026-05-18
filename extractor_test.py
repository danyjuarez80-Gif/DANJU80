import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🚀 Iniciando simulación estilo Web Video Caster...")
        
        # 🛠️ AQUÍ ESTÁ EL PARCHE: Agregamos 'await' antes de p.chromium.launch
        browser = await p.chromium.launch(headless=True)
        
        # También le metemos await al contexto
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        page = await context.new_page()
        
        # Aquí guardaremos los enlaces sospechosos que encontremos
        enlaces_encontrados = []

        # 1. ESCUCHAR PETICIONES DE RED (Filtro por texto de URL)
        page.on("request", lambda req: 
            enlaces_encontrados.append(f"[URL] {req.url}") 
            if any(ext in req.url for ext in [".m3u8", ".ts", "master", "playlist", "live"]) else None
        )

        # 2. ESCUCHAR RESPUESTAS DE RED (Filtro avanzado por tipo de contenido, como los Blobs ocultos)
        page.on("response", lambda res: 
            enlaces_encontrados.append(f"[MIME: {res.headers.get('content-type')}] -> {res.url}")
            if res.headers.get('content-type') and ("mpegurl" in res.headers.get('content-type').lower() or "video/mp2t" in res.headers.get('content-type').lower()) else None
        )

        try:
            # 💥 RECUERDA CAMBIAR ESTA URL POR LA PÁGINA QUE QUIERAS TRASTEAR
            url_a_probar = "https://TU-PAGINA-DE-STREAMING-AQUI.com" 
            
            await page.goto(url_a_probar, wait_until="domcontentloaded", timeout=60000)
            print(f"📡 Entrando a: {url_a_probar}")

            # Esperar un momento a que carguen anuncios iniciales
            await asyncio.sleep(5)
            print("👆 Simulando clic en la pantalla para activar reproductor...")
            await page.click("body") 

            # Dejamos que el video corra en el fondo 15 segundos para pescar el tráfico
            await asyncio.sleep(15)

        except Exception as e:
            print(f"❌ Error al cargar la página: {e}")

        finally:
            await browser.close()

        # Guardar los resultados para revisarlos en GitHub
        print(f"\n📊 Resultados: Se encontraron {len(enlaces_encontrados)} enlaces potenciales.")
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if enlaces_encontrados:
                for enlace in set(enlaces_encontrados): # Elimina duplicados
                    f.write(enlace + "\n")
                    print(enlace)
            else:
                f.write("No se detectó ningún flujo de video activo en esta ejecución.\n")

if __name__ == "__main__":
    asyncio.run(run())
