import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
django.setup()

from django.contrib.auth.models import User

# Pegando os dados de variáveis de ambiente para segurança
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@email.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'senha_dificil_123')

if not User.objects.filter(username=username).exists():
    print(f"Criando superusuário: {username}")
    User.objects.create_superuser(username, email, password)
else:
    print(f"Superusuário {username} já existe.")