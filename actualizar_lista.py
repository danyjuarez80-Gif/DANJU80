name: Dividir y Actualizar Listas Separadas Cada 15 Minutos

on:
  schedule:
    - cron: '*/15 * * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Descargar el Repositorio
        uses: actions/checkout@v4
        with:
          persist-credentials: true

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Segmentar M3U en Tres Enlaces Limpios
        run: |
          python -c '
          import os

          archivo_origen = "dan88.m3u"
          if not os.path.exists(archivo_origen):
              print("ERROR: No se encontro dan88.m3u")
              exit(1)

          with open(archivo_origen, "r", encoding="utf-8", errors="ignore") as f:
              lineas = f.read().splitlines()

          cabecera = lineas[0] if lineas and lineas[0].startswith("#EXTM3U") else "#EXTM3U"

          listado_tv = [cabecera]
          listado_movies = [cabecera]
          listado_series = [cabecera]

          i = 1
          while i < len(lineas):
              linea = lineas[i].strip()
              if linea.startswith("#EXTINF"):
                  linea_inf = linea
                  linea_url = ""
                  if i + 1 < len(lineas):
                      linea_url = lineas[i + 1].strip()
                  
                  linea_inf_lower = linea_inf.lower()
                  linea_url_lower = linea_url.lower()

                  # Clasificación estricta por contenedor
                  es_pelicula = "/movie/" in linea_url_lower or 'group-title="películas"' in linea_inf_lower or ".mp4" in linea_url_lower or ".mkv" in linea_url_lower
                  es_serie = "/series/" in linea_url_lower or 'group-title="series"' in linea_inf_lower

                  if es_pelicula:
                      listado_movies.append(linea_inf)
                      if linea_url: listado_movies.append(linea_url)
                  elif es_serie:
                      listado_series.append(linea_inf)
                      if linea_url: listado_series.append(linea_url)
                  else:
                      listado_tv.append(linea_inf)
                      if linea_url: listado_tv.append(linea_url)
                  i += 2
              else:
                  i += 1

          # Guardar los 3 archivos independientes
          with open("DANJU80", "w", encoding="utf-8") as f:
              f.write("\n".join(listado_tv))
          with open("DANJU_MOVIES", "w", encoding="utf-8") as f:
              f.write("\n".join(listado_movies))
          with open("DANJU_SERIES", "w", encoding="utf-8") as f:
              f.write("\n".join(listado_series))

          # Tu archivo txt de sincronización para Render
          with open("lista_canales_render.txt", "w", encoding="utf-8") as f:
              f.write("https://raw.githubusercontent.com/danyjuarez80-Gif/DANJU80/main/DANJU80")
          '

      - name: Enviar los 3 archivos a GitHub
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          
          # Añadimos los tres archivos destino
          git add DANJU80 DANJU_MOVIES DANJU_SERIES lista_canales_render.txt
          
          if ! git diff --cached --quiet; then
            git commit -m "Automatización: Listas segmentadas (LiveTV, Pelis, Series)"
            git pull origin main --rebase
            git push origin main
          else
            echo "Sin cambios en los listados."
          fi
