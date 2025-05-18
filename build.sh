#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate

git update-index --chmod=+x build.sh 

git init
git add .
git commit -m "Initial commit for deployment" 

git remote add origin https://github.com/TU_USUARIO/hackplanograma.git
git branch -M main
git push -u origin main 

git add build.sh render.yaml
git commit -m "Fix build script and render configuration"
git push 