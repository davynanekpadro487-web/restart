import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import Semaine, DomaineSemaine, ActionProposee
from django.utils import timezone

def add_amour():
    aujourdhui = timezone.now().date()
    semaine = Semaine.objects.filter(date_rendez_vous__lte=aujourdhui).order_by('-date_rendez_vous').first()
    
    if not semaine:
        print("Aucune semaine en cours trouvée.")
        return
        
    # Check if amour already exists for this week
    if DomaineSemaine.objects.filter(semaine=semaine, categorie='amour').exists():
        print("Le domaine 'amour' existe déjà pour cette semaine.")
        return
        
    domaine = DomaineSemaine.objects.create(
        semaine=semaine,
        categorie='amour',
        titre='Relation amoureuse',
        pourquoi_ca_compte="L'amour que tu acceptes est le reflet de l'amour que tu te portes. Ne te brade pas."
    )
    
    actions = [
        "Traverser une peine de cœur",
        "Arrêter de se laisser marcher dessus en amour",
        "Ne pas donner son corps juste pour plaire"
    ]
    
    for texte in actions:
        ActionProposee.objects.create(domaine=domaine, texte=texte)
        
    print("Le domaine 'Relation amoureuse' a été ajouté avec succès.")

if __name__ == '__main__':
    add_amour()
