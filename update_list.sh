#!/bin/bash
git pull origin main --rebase
echo "Iniciando rastreo real..."
python3 bot_userland.py
echo "Subiendo cambios a GitHub..."
git add .
git commit -m "Update desde celular"
git push origin main
