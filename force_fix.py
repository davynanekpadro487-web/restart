import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import ActionBonusUtilisateur, DomaineUtilisateur
from core.utils import get_initial_action_data

def force_fix_objectifs():
    bonus_actions = ActionBonusUtilisateur.objects.filter(domaine__categorie='objectifs')
    for bonus in bonus_actions:
        old_data = bonus.donnees_action
        new_data = get_initial_action_data('objectifs', bonus.action_choisie.texte, is_bonus=True)
        
        if old_data and new_data:
            new_data['etape_courante'] = old_data.get('etape_courante', 0)
            for i, step in enumerate(new_data.get('etapes', [])):
                if i < len(old_data.get('etapes', [])):
                    old_reponse = old_data['etapes'][i].get('reponse')
                    if old_reponse is not None:
                        step['reponse'] = old_reponse
        bonus.donnees_action = new_data
        bonus.save()
        
    main_actions = DomaineUtilisateur.objects.filter(domaine__categorie='objectifs')
    for action in main_actions:
        if action.action_choisie:
            old_data = action.donnees_action
            new_data = get_initial_action_data('objectifs', action.action_choisie.texte, is_bonus=False)
            
            if old_data and new_data:
                new_data['etape_courante'] = old_data.get('etape_courante', 0)
                for i, step in enumerate(new_data.get('etapes', [])):
                    if i < len(old_data.get('etapes', [])):
                        old_reponse = old_data['etapes'][i].get('reponse')
                        if old_reponse is not None:
                            step['reponse'] = old_reponse
            action.donnees_action = new_data
            action.save()
            
    print("Fixed both bonus and main actions for objectifs!")

if __name__ == '__main__':
    force_fix_objectifs()
