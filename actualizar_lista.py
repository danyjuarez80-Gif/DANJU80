name: Filtrar y Actualizar Canales IPTV

on:
  workflow_dispatch: # Esto te permite ejecutarlo manualmente con un boton

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Clonar el repositorio
      uses: actions/checkout@v3

    - name: Configurar Python
      uses: actions/setup-python@v4
      with:
        python-python: '3.x'

    - name: Ejecutar script de filtrado
      run: python actualizar_lista.py

    - name: Guardar los cambios en el repositorio
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add lista_canales_render.txt
        git commit -m "Lista de canales actualizada automaticamente" || echo "No hay cambios para guardar"
        git push
