import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import Semaine, DomaineSemaine, ActionProposee, DomaineUtilisateur, CATEGORIES_ACTION

def seed_domaines():
    semaine = Semaine.objects.filter(theme__icontains="Construire").first()
    if not semaine:
        semaine = Semaine.objects.first()
        
    if not semaine:
        print("Aucune semaine trouvée dans la base de données.")
        return

    print(f"Mise à jour des domaines pour la semaine : {semaine.theme}")
    
    # Nettoyage
    DomaineUtilisateur.objects.filter(domaine__semaine=semaine).delete()
    DomaineSemaine.objects.filter(semaine=semaine).delete()

    domaines_data = {
        'pro': {
            'titre': 'Vie professionnelle / Études',
            'pourquoi_ca_compte': 'Le travail et les études sont des piliers de ton indépendance et de ta confiance en toi.',
            'actions': [
                "Mettre à jour mon CV",
                "Consacrer 1h à mon projet professionnel",
                "Faire mes recherches sur une formation"
            ]
        },
        'argent': {
            'titre': 'Mon argent',
            'pourquoi_ca_compte': "L'indépendance financière te donne la liberté de faire tes propres choix sans dépendre de personne.",
            'actions': [
                "Noter toutes mes dépenses pendant 7 jours afin de comprendre où part réellement mon argent.",
                "Identifier au moins 3 dépenses inutiles ou évitables et décider laquelle je vais réduire.",
                "Consacrer 30 minutes à rechercher une idée réaliste de revenu, de business, de compétence rentable ou d'opportunité financière adaptée à ma situation."
            ]
        },
        'objectifs': {
            'titre': 'Mes objectifs',
            'pourquoi_ca_compte': 'Avoir des objectifs clairs te permet de rester focalisée sur ta propre évolution.',
            'actions': [
                "Reprendre un objectif abandonné",
                "Fixer un nouvel objectif clair pour le mois",
                "Faire avancer un objectif déjà en cours"
            ]
        },
        'moi': {
            'titre': 'Moi-même',
            'pourquoi_ca_compte': 'Prendre soin de toi et te connaître est la base de toute relation saine, avec toi-même et les autres.',
            'actions': [
                "Faire quelque chose que je repousse par peur du regard des autres",
                "Reprendre une activité physique ou que j'aime",
                "Passer moins de temps à scroller"
            ]
        },
        'reseaux': {
            'titre': 'Réseaux sociaux',
            'pourquoi_ca_compte': 'Ton environnement numérique influence tes pensées. Le maîtriser, c\'est protéger ton énergie.',
            'actions': [
                "Créer et publier un contenu pour mon business",
                "Nettoyer mes abonnements",
                "Remplacer le scroll par une action utile (30 min)"
            ]
        },
        'amour': {
            'titre': 'Relation amoureuse',
            'pourquoi_ca_compte': "L'amour que tu acceptes est le reflet de l'amour que tu te portes. Ne te brade pas.",
            'actions': [
                "Traverser une peine de cœur",
                "Arrêter de se laisser marcher dessus en amour",
                "Ne pas donner son corps juste pour plaire"
            ]
        },
        'spiritualite': {
            'titre': 'Spiritualité',
            'pourquoi_ca_compte': 'Te reconnecter à tes valeurs et à ton intériorité te donne force et clarté d\'esprit.',
            'actions': [
                "Le Bain de Libération",
                "L'Offrande de Semence",
                "La Prière d'Élévation"
            ]
        }
    }

    count_domaines = 0
    count_actions = 0
    for code, _ in CATEGORIES_ACTION:
        if code in domaines_data:
            data = domaines_data[code]
            domaine = DomaineSemaine.objects.create(
                semaine=semaine,
                categorie=code,
                titre=data['titre'],
                pourquoi_ca_compte=data['pourquoi_ca_compte']
            )
            count_domaines += 1
            
            for texte_action in data['actions']:
                ActionProposee.objects.create(
                    domaine=domaine,
                    texte=texte_action
                )
                count_actions += 1
            
    print(f"Succès ! {count_domaines} domaines et {count_actions} actions ont été insérés.")

if __name__ == '__main__':
    seed_domaines()
