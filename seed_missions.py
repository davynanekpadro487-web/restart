import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import Semaine, MissionSemaine, MissionUtilisateur, CATEGORIES_ACTION

def seed_missions_v2():
    semaine = Semaine.objects.filter(theme__icontains="Construire").first()
    if not semaine:
        semaine = Semaine.objects.first()
        
    if not semaine:
        print("Aucune semaine trouvée dans la base de données.")
        return

    print(f"Mise à jour des missions pour la semaine : {semaine.theme}")
    
    # Nettoyage
    MissionUtilisateur.objects.filter(mission__semaine=semaine).delete()
    MissionSemaine.objects.filter(semaine=semaine).delete()

    missions = {
        'pro': [
            "Terminer une tâche scolaire ou professionnelle que tu repousses depuis plusieurs jours.",
            "Consacrer au moins 1 heure à apprendre une compétence utile à ton avenir.",
            "Consacrer au moins 1 heure à avancer sur ton projet professionnel, ton business ou ton orientation."
        ],
        'argent': [
            "Noter toutes mes dépenses pendant 7 jours afin de comprendre où part réellement mon argent.",
            "Identifier au moins 3 dépenses inutiles ou évitables et décider laquelle je vais réduire.",
            "Consacrer 30 minutes à rechercher une idée réaliste de revenu, de business, de compétence rentable ou d'opportunité financière adaptée à ma situation."
        ],
        'objectifs': [
            "Reprendre un objectif que j'ai commencé puis abandonné et réaliser sa prochaine étape.",
            "Consacrer 30 minutes sans interruption à un objectif important que je repousse.",
            "Terminer une petite tâche que j'ai commencée mais jamais terminée."
        ],
        'moi': [
            "Faire quelque chose que je repousse par peur du regard des autres.",
            "Prendre au moins 30 minutes cette semaine pour prendre soin de moi et de mon bien-être.",
            "Faire quelque chose seule ou prendre une décision seule afin de développer mon autonomie et ma confiance."
        ],
        'reseaux': [
            "Créer et publier un contenu dans ma niche ou autour de mon activité.",
            "Utiliser les réseaux sociaux pour rechercher une opportunité : client, collaboration, business, emploi, partenariat, visibilité ou autre opportunité pertinente.",
            "Consacrer du temps à apprendre quelque chose d'utile grâce aux réseaux sociaux : formation, compétence, contenu éducatif ou information liée à mon domaine."
        ],
        'spiritualite': [
            "**BAIN DE LIBÉRATION** : Rituel spirituel de libération et de recentrage.",
            "**OFFRANDE / GESTE DE GÉNÉROSITÉ** : Préparer, selon ses moyens, quelque chose destiné à une personne dans le besoin.",
            "**PRIÈRE DE LIBÉRATION** : Moment calme de prière pour déposer ce qui pèse et remettre ses projets à Dieu ou selon ses convictions."
        ]
    }

    count = 0
    for categorie_code, liste_missions in missions.items():
        for texte_mission in liste_missions:
            MissionSemaine.objects.create(
                semaine=semaine,
                categorie=categorie_code,
                texte=texte_mission
            )
            count += 1
            
    print(f"Succès ! {count} missions exactes ont été insérées (3 par catégorie, 6 catégories).")

if __name__ == '__main__':
    seed_missions_v2()
