import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import Programme

programmes = Programme.objects.all()
mapping = {
    'construire': 'illu-chemin-coeur.png',
    'amour': 'illu-chemin-coeur.png',
    'confiance': 'illu-montagne.png',
    'entourage': 'illu-entourage.png',
    'discipline': 'illu-discipline.png',
    'temps': 'illu-horloge.png',
    'gestion': 'illu-horloge.png'
}

print("=== Mise à jour des images de programmes ===")

for prog in programmes:
    theme_lower = prog.theme.lower()
    image_name = 'illu-laptop-nuit.png'
    for key, filename in mapping.items():
        if key in theme_lower:
            image_name = filename
            break

    # Remplir le champ si l'image est manquante physiquement ou si le champ est vide
    path = os.path.join('static', 'images', 'programme', image_name)
    
    if os.path.exists(path):
        with open(path, 'rb') as f:
            prog.illustration.save(image_name, File(f), save=True)
        print(f"[{prog.theme}] -> mis à jour avec {image_name}")
    else:
        print(f"[{prog.theme}] -> Erreur : {path} introuvable.")

print("=== Terminé ===")
