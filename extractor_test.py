import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Iniciamos el navegador simulando un celular Android para imitar a Web Video Caster
        browser = p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
        )
        page = await context.new_page()

        print("🚀 Iniciando simulación estilo Web Video Caster...")
        
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
            if "mpegurl" in res.headers.get("content-type", "").lower() or "video/mp2t" in res.headers.get("content-type", "").lower() else None
        )

        try:
            # 💥 AQUÍ CAMBIAMOS LA URL POR LA PÁGINA PERRA QUE QUIERAS PROBAR
            url_a_proBAR = "https://tvlibr3.com/" 
            
            await page.goto(url_a_proBAR, wait_until="domcontentloaded", timeout=60000)
            print(f"📡 Entrando a: {url_a_proBAR}")

            # Simular una espera y un clic en la pantalla por si el reproductor pide interacción
            await asyncio.sleep(5)
            print("👆 Simulando clic en el reproductor para activar el flujo...")
            await page.click("body") # Da un clic general en la página para activar videos auto-play

            # Le damos 15 segundos a la página para que reproduzca de fondo y el script pesque el tráfico
            await asyncio.sleep(15)

        except Exception as e:
            print(f"❌ Error al cargar la página: {e}")

        finally:
            await browser.close()

        # Guardar los resultados para revisarlos en GitHub
        print(f"\n📊 Resultados: Se encontraron {len(enlaces_encontrados)} enlaces potenciales.")
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if enlaces_encontrados:
                for enlace in set(enlaces_encontrados): # 'set' elimina duplicados
                    f.write(enlace + "\n")
                    print(enlace)
            else:
                f.write("No se detectó ningún flujo de video activo en esta ejecución.\n")

if __name__ == "__main__":
    asyncio.run(run())
