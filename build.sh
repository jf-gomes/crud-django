#!/usr/bin/env bash

# aqui ficam scripts que serão executados ao fazer o deploy (instalar dependências, migração do banco e criação do superadmin.)
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python create_admin.py