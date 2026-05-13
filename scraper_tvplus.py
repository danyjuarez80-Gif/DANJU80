import asyncio
from playwright.async_api import async_playwright

CANALES_TVPLUS = [
    # ESPN
    {"nombre": "ESPN",              "url": "https://www.tvplusgratis2.com/espn-en-vivo.html"},
    {"nombre": "ESPN 2",            "url": "https://www.tvplusgratis2.com/espn-2-en-vivo.html"},
    {"nombre": "ESPN 3",            "url": "https://www.tvplusgratis2.com/espn-3-en-vivo.html"},
    {"nombre": "ESPN 4",            "url": "https://www.tvplusgratis2.com/espn-4-en-vivo.html"},
    {"nombre": "ESPN Extra",        "url": "https://www.tvplusgratis2.com/espn-extra-en-vivo.html"},
    {"nombre": "ESPN Mexico",       "url": "https://www.tvplusgratis2.com/espn-mexico-en-vivo.html"},
    {"nombre": "ESPN 2 Mexico",     "url": "https://www.tvplusgratis2.com/espn-2-mexico-en-vivo.html"},
    {"nombre": "ESPN Deportes",     "url": "https://www.tvplusgratis2.com/espn-deportes-en-vivo.html"},
    # Fox
    {"nombre": "Fox Deportes",      "url": "https://www.tvplusgratis2.com/fox-deportes-en-vivo.html"},
    {"nombre": "Fox Sports",        "url": "https://www.tvplusgratis2.com/fox-sports-en-vivo.html"},
    {"nombre": "Fox Sports 2",      "url": "https://www.tvplusgratis2.com/fox-sports-2-en-vivo.html"},
    {"nombre": "Fox Sports 3",      "url": "https://www.tvplusgratis2.com/fox-sports-3-en-vivo.html"},
    {"nombre": "Fox One",           "url": "https://www.tvplusgratis2.com/fox-one-en-vivo.html"},
    {"nombre": "Fox Premium",       "url": "https://www.tvplusgratis2.com/fox-premium-en-vivo.html"},
    # Univision / Telemundo
    {"nombre": "TUDN",              "url": "https://www.tvplusgratis2.com/tudn-en-vivo.html"},
    {"nombre": "Univision",         "url": "https://www.tvplusgratis2.com/univision-en-vivo.html"},
    {"nombre": "UniMas",            "url": "https://www.tvplusgratis2.com/unimas-en-vivo.html"},
    {"nombre": "Telemundo",         "url": "https://www.tvplusgratis2.com/telemundo-en-vivo.html"},
    {"nombre": "Galavision",        "url": "https://www.tvplusgratis2.com/galavision-en-vivo.html"},
    # Deportes
    {"nombre": "beIN Sports",       "url": "https://www.tvplusgratis2.com/bein-sports-en-vivo.html"},
    {"nombre": "beIN Sports 2",     "url": "https://www.tvplusgratis2.com/bein-sports-2-en-vivo.html"},
    {"nombre": "beIN Sports 3",     "url": "https://www.tvplusgratis2.com/bein-sports-3-en-vivo.html"},
    {"nombre": "Claro Sports",      "url": "https://www.tvplusgratis2.com/claro-sports-en-vivo.html"},
    {"nombre": "Caliente TV",       "url": "https://www.tvplusgratis2.com/caliente-tv-en-vivo.html"},
    {"nombre": "TyC Sports",        "url": "https://www.tvplusgratis2.com/tyc-sports-en-vivo.html"},
    {"nombre": "Win Sports",        "url": "https://www.tvplusgratis2.com/win-sports-en-vivo.html"},
    {"nombre": "DirecTV Sports",    "url": "https://www.tvplusgratis2.com/directv-sports-en-vivo.html"},
    {"nombre": "Sky Sports",        "url": "https://www.tvplusgratis2.com/sky-sports-en-vivo.html"},
    {"nombre": "NBA TV",            "url": "https://www.tvplusgratis2.com/nba-tv-en-vivo.html"},
    {"nombre": "NFL Network",       "url": "https://www.tvplusgratis2.com/nfl-network-en-vivo.html"},
    {"nombre": "MLB Network",       "url": "https://www.tvplusgratis2.com/mlb-network-en-vivo.html"},
    {"nombre": "Golf Channel",      "url": "https://www.tvplusgratis2.com/golf-channel-en-vivo.html"},
    # Mexico
    {"nombre": "Las Estrellas",     "url": "https://www.tvplusgratis2.com/las-estrellas-en-vivo.html"},
    {"nombre": "Canal 5",           "url": "https://www.tvplusgratis2.com/canal-5-en-vivo.html"},
    {"nombre": "Azteca 7",          "url": "https://www.tvplusgratis2.com/azteca-7-en-vivo.html"},
    {"nombre": "Azteca Deportes",   "url": "https://www.tvplusgratis2.com/azteca-deportes-en-vivo.html"},
    {"nombre": "Imagen TV",         "url": "https://www.tvplusgratis2.com/imagen-tv-en-vivo.html"},
    {"nombre": "Multimedios",       "url": "https://www.tvplusgratis2.com/multimedios-en-vivo.html"},
]


async def capturar_m3u8(page, canal):
    m3u8_url = None

    def interceptar(request):
        nonlocal m3u8_url
        url = request.url
        if ".m3u8" in url and m3u8_url is None:
            m3u8_url = url

    page.on("request", interceptar)

    try:
        await page.goto(canal["url"], timeout=25000, wait_until="domcontentloaded")
        await asyncio.sleep(6)
    except Exception as e:
        print(f"  ⚠️ Error: {e}")
    finally:
        page.remove_listener("request", interceptar)

    return m3u8_url


async def scrape_tvplus():
    resultados = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        page = await context.new_page()

        for canal in CANALES_TVPLUS:
            print(f"🔍 Buscando: {canal['nombre']}...")
            url = await capturar_m3u8(page, canal)
            if url:
                # URL limpia sin parámetros extra
                url_limpia = url.split("?")[0]
                print(f"  ✅ {canal['nombre']}: {url_limpia}")
                resultados.append((canal["nombre"], url_limpia))
            else:
                print(f"  ❌ {canal['nombre']}: no encontrado")

        await browser.close()

    return resultados


if __name__ == "__main__":
    resultados = asyncio.run(scrape_tvplus())
    print(f"\n📋 Total encontrados: {len(resultados)}")
    for nombre, url in resultados:
        print(f"  {nombre} -> {url}")
