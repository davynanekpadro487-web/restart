import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import DomaineUtilisateur, ActionBonusUtilisateur
from core.utils import get_initial_action_data

def update_amour_data():
    # Update main actions
    main_actions = DomaineUtilisateur.objects.filter(domaine__categorie='amour')
    count = 0
    for action in main_actions:
        if action.action_choisie:
            old_data = action.donnees_action
            new_data = get_initial_action_data('amour', action.action_choisie.texte, is_bonus=False)
            
            # Restore state if it exists
            if old_data and new_data:
                new_data['etape_courante'] = old_data.get('etape_courante', 0)
                # copy responses safely
                for i, step in enumerate(new_data.get('etapes', [])):
                    if i < len(old_data.get('etapes', [])):
                        step['reponse'] = old_data['etapes'][i].get('reponse', step['reponse'])
            
            action.donnees_action = new_data
            action.save()
            count += 1
            
    # Update bonus actions
    bonus_actions = ActionBonusUtilisateur.objects.filter(domaine__categorie='amour')
    bonus_count = 0
    for bonus in bonus_actions:
        old_data = bonus.donnees_action
        new_data = get_initial_action_data('amour', bonus.action_choisie.texte, is_bonus=True)
        
        # Restore state if it exists
        if old_data and new_data:
            new_data['etape_courante'] = old_data.get('etape_courante', 0)
            # copy responses safely
            for i, step in enumerate(new_data.get('etapes', [])):
                if i < len(old_data.get('etapes', [])):
                    step['reponse'] = old_data['etapes'][i].get('reponse', step['reponse'])
                    
        bonus.donnees_action = new_data
        bonus.save()
        bonus_count += 1
        
    print(f"Mis à jour : {count} actions principales, {bonus_count} actions bonus.")

if __name__ == '__main__':
    update_amour_data()
