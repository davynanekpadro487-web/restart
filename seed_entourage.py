import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import Semaine, DomaineSemaine, ActionProposee, DomaineUtilisateur, CATEGORIES_ACTION

def seed_entourage():
    semaine = Semaine.objects.filter(programme__theme__icontains="Entourage").first()
        
    if not semaine:
        print("Le programme 'Entourage' n'a pas été trouvé dans la base de données.")
        return

    print(f"Mise à jour des domaines pour la semaine : {semaine.theme}")
    
    # Nettoyage
    DomaineUtilisateur.objects.filter(domaine__semaine=semaine).delete()
    DomaineSemaine.objects.filter(semaine=semaine).delete()

    domaines_data = {
        'pro': {
            'titre': 'Vie professionnelle / Études',
            'pourquoi_ca_compte': 'Ton entourage professionnel détermine ta motivation et tes opportunités. T\'entourer des bonnes personnes te tire vers le haut.',
            'actions': [
                "Proposer un déjeuner ou un café à un(e) collègue ou camarade inspirant(e) pour échanger (renforce ton réseau).",
                "Identifier 2 personnes toxiques ou plaintives au travail/école et réduire volontairement mes interactions avec elles.",
                "Envoyer un message de remerciement ou de reconnaissance à quelqu'un qui m'a aidé professionnellement récemment."
            ]
        },
        'argent': {
            'titre': 'Mon argent',
            'pourquoi_ca_compte': 'L\'argent est souvent tabou, mais s\'entourer de personnes ayant une saine éducation financière aide à faire les bons choix.',
            'actions': [
                "Parler d'un de mes objectifs financiers avec une personne de confiance qui gère bien son argent (obtenir un bon conseil).",
                "Arrêter de suivre les personnes sur les réseaux sociaux qui me poussent à la surconsommation.",
                "Proposer une sortie gratuite ou peu coûteuse à mes amis cette semaine au lieu d'une dépense habituelle."
            ]
        },
        'objectifs': {
            'titre': 'Mes objectifs',
            'pourquoi_ca_compte': 'Partager ses objectifs avec les bonnes personnes crée une saine pression positive et un soutien précieux.',
            'actions': [
                "Partager mon objectif principal du mois avec un(e) ami(e) en lui demandant de prendre de mes nouvelles à ce sujet (crée de l'accountability).",
                "Lister 3 personnes de mon entourage et écrire à côté d'elles comment elles m'inspirent à m'améliorer.",
                "Mettre fin poliment à une conversation où quelqu'un essaie de me décourager d'un de mes projets."
            ]
        },
        'moi': {
            'titre': 'Moi-même',
            'pourquoi_ca_compte': 'Tu es la moyenne des 5 personnes que tu côtoies le plus. Savoir dire non est essentiel pour préserver ton énergie.',
            'actions': [
                "Dire non à une sollicitation ou une sortie dont je n'ai pas vraiment envie, sans me justifier (protège mon énergie).",
                "Faire le tri dans mes contacts téléphoniques : supprimer ou bloquer les personnes qui ne m'apportent que du négatif.",
                "Prendre un moment seul(e) pour évaluer comment je me sens après avoir vu telle ou telle personne."
            ]
        },
        'reseaux': {
            'titre': 'Réseaux sociaux',
            'pourquoi_ca_compte': 'Ton cercle social inclut aussi le monde numérique. Filtre impitoyablement ce qui entre dans ton cerveau.',
            'actions': [
                "Me désabonner d'au moins 5 comptes qui me font me sentir inférieur(e) ou qui polluent mon fil d'actualité.",
                "S'abonner à 3 nouveaux comptes qui m'inspirent, m'éduquent ou me motivent (enrichit mon entourage numérique).",
                "Laisser un commentaire positif et sincère sur la publication d'un de mes amis pour renforcer notre lien."
            ]
        },
        'amour': {
            'titre': 'Relation amoureuse',
            'pourquoi_ca_compte': 'Tes amis ont un impact majeur sur ta vision de l\'amour. Ne laisse pas leurs échecs ou cynisme dicter ta vie sentimentale.',
            'actions': [
                "Identifier une croyance négative sur l'amour que mon entourage m'a transmise, et décider de ne plus y croire (reprendre mon pouvoir).",
                "Faire un compliment sincère à mon partenaire (ou à moi-même si je suis célibataire) sur ses qualités humaines.",
                "Ne pas participer à une conversation où l'on dénigre les hommes/femmes de manière généralisée."
            ]
        },
        'spiritualite': {
            'titre': 'Spiritualité',
            'pourquoi_ca_compte': 'Ta paix intérieure ne doit pas être perturbée par le chaos extérieur. Un bon entourage respecte tes valeurs.',
            'actions': [
                "La bulle de protection : visualiser une lumière protectrice autour de soi avant de retrouver un environnement ou une personne drainante.",
                "Le rituel du pardon silencieux : pardonner intérieurement à quelqu'un qui m'a déçu, non pour lui, mais pour me libérer.",
                "Le cercle de gratitude : prendre 5 minutes pour écrire ce que les personnes que j'aime apportent de beau dans ma vie."
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
            
    print(f"Succès ! {count_domaines} domaines et {count_actions} actions ont été insérés pour le programme Entourage.")

if __name__ == '__main__':
    seed_entourage()
