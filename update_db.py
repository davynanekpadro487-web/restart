import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()
from core.models import DomaineUtilisateur

dus = DomaineUtilisateur.objects.filter(
    action_choisie__texte__icontains='fiert'
)
for du in dus:
    if du.donnees_action and 'etapes' in du.donnees_action:
        etapes = du.donnees_action['etapes']
        if len(etapes) > 2:
            etapes[1] = {
                'is_checklist_etape': True,
                'question': 'Étape 2 — Choisir un modèle de CV',
                'contexte': 'Choisis un modèle simple et professionnel.',
                'items': [
                    {'label': 'Choisir un modèle sur <a href="https://canva.com" target="_blank" class="text-aurea-purple hover:underline">Canva</a>', 'done': False},
                    {'label': 'Vérifier qu’il est simple et facile à lire', 'done': False},
                    {'label': 'Éviter les tableaux et les designs trop chargés', 'done': False},
                    {'label': 'Vérifier qu’il est compatible avec les ATS avec <a href="https://jobscan.co" target="_blank" class="text-aurea-purple hover:underline">Jobscan</a>', 'done': False}
                ],
                'bouton': 'Suivant'
            }
            etapes[2] = {
                'is_checklist_etape': True,
                'question': 'Étape 3',
                'contexte': '',
                'items': [
                    {'label': 'Ajouter cette réussite oubliée', 'done': False},
                    {'label': 'Relire le CV en se disant : ‘je mérite ce que j’ai accompli’', 'done': False}
                ],
                'bouton': 'Oui, je l’ai fait pour moi'
            }
            du.donnees_action['etapes'] = etapes
            du.save()
            print('Updated DomaineUtilisateur', du.id)
print('Done!')
