import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import Programme

programmes_data = [
    {"theme": "Construire sa vie avant l'amour", "ordre": 1, "publie": True},
    {"theme": "Confiance en soi", "ordre": 2, "publie": True},
    {"theme": "Entourage", "ordre": 3, "publie": True},
    {"theme": "Discipline", "ordre": 4, "publie": False},
    {"theme": "Gestion du temps", "ordre": 5, "publie": False},
]

for data in programmes_data:
    prog = Programme.objects.filter(theme__icontains=data["theme"]).first()
    if prog:
        prog.ordre = data["ordre"]
        prog.publie = data["publie"]
        prog.save()
        print(f"Updated: {prog.theme} -> ordre={prog.ordre}, publie={prog.publie}")
    else:
        print(f"NOT FOUND: {data['theme']}")

print("Data migration complete.")
