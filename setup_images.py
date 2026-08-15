import os
import django
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aurea.settings")
django.setup()

from core.models import Programme

images_map = {
    "Confiance": "illu-montagne.png",
    "Gestion du temps": "illu-horloge.png",
    "Discipline": "illu-discipline.png",
    "Entourage": "illu-entourage.png",
    "Construire sa vie": "illu-chemin-coeur.png"
}

for theme_part, img_name in images_map.items():
    prog = Programme.objects.filter(theme__icontains=theme_part).first()
    if prog:
        img_path = os.path.join('static', 'images', 'programme', img_name)
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                prog.illustration.save(img_name, File(f), save=True)
            print(f"Image {img_name} ajoutee au programme '{prog.theme}'")
        else:
            print(f"Erreur: Image {img_path} introuvable.")
    else:
        print(f"Erreur: Programme contenant '{theme_part}' introuvable.")
