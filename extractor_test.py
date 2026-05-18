import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🔥 Iniciando Modo Agresivo en tvlibr3.com...")
        
        # Lanzamos el navegador simulando un cel
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            viewport={"width": 360, "height": 740}
        )
        page = await context.new_page()
        
        todo_el_trafico = []

        # Capturar absolutamente todo el tráfico de red
        page.on("request", lambda req: todo_el_trafico.append(f"[REQ] -> {req.url}"))
        page.on("response", lambda res: todo_el_trafico.append(f"[RES ({res.status})] -> {res.url} | MIME: {res.headers.get('content-type')}"))

        try:
            # 🛠️ ¡YA TIENE LA URL DE TVLIBR3 PUESTA, PERRITO!
            url_a_probar = "https://tvlibr3.com/" 
            
            print(f"📡 Navegando en la boca del lobo: {url_a_probar}")
            await page.goto(url_a_probar, wait_until="load", timeout=60000)
            await asyncio.sleep(5)

            # Tirar clics en el centro para intentar saltar el primer anuncio flotante
            print("👇 Tirando clics en el centro para activar el reproductor...")
            await page.mouse.click(180, 370) 
            await asyncio.sleep(4)
            
            # Segundo clic por si el primero abrió una pestaña basura
            await page.mouse.click(180, 370) 
            await asyncio.sleep(15)

            # Tomar la foto para ver si nos quedamos atorados en publicidad
            await page.screenshot(path="pantalla_final.png")
            print("📸 Foto de la página guardada con éxito.")

        except Exception as e:
            print(f"❌ Tronó el proceso: {e}")
        finally:
            await browser.close()

        # Guardar todo el reporte de tráfico bruto
        with open("resultados_trafico.txt", "w", encoding="utf-8") as f:
            if todo_el_trafico:
                f.write(f"Tráfico total detectado en tvlibr3: {len(todo_el_trafico)} peticiones.\n\n")
                for linea in todo_el_trafico:
                    f.write(linea + "\n")
            else:
                f.write("La página bloqueó por completo la salida de red del bot.\n")

if __name__ == "__main__":
    asyncio.run(run())
