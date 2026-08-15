import os
import django
import sys

# Initialisation de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aurea.settings")
django.setup()

from core.models import Programme, Semaine, DomaineSemaine, ActionProposee

def populate():
    # 1. Récupérer le programme "Confiance en soi"
    try:
        prog = Programme.objects.get(theme="Confiance en soi")
    except Programme.DoesNotExist:
        print("Erreur: Le programme 'Confiance en soi' n'existe pas.")
        sys.exit(1)
        
    print(f"Programme '{prog.theme}' (ID: {prog.id}) trouvé.")
    
    # S'assurer de la présence d'une semaine 1
    semaine, created = Semaine.objects.get_or_create(
        programme=prog,
        ordre=1,
        defaults={
            "theme": "Semaine 1",
            "objectif": "Objectif par défaut",
            # On mettra à jour date_rendez_vous via un autre mécanisme si besoin, ou on garde ce qui est là
        }
    )
    
    # Mettre à jour les questions de réflexion
    semaine.questions = (
        "1. Dans quels moments te sens-tu le moins sûre de toi ?\n"
        "2. Qu’est-ce que tu te dis à toi-même quand tu doutes ?\n"
        "3. À quoi ressemblerait ta vie si tu avais une confiance inébranlable dès aujourd’hui ?"
    )
    semaine.save()
    
    # 2. Vider les domaines existants pour cette semaine
    DomaineSemaine.objects.filter(semaine=semaine).delete()
    
    # 3. Ajouter les 7 domaines
    
    domaines_data = [
        {
            "categorie": "pro",
            "titre": "VIE PRO / ÉTUDES",
            "pourquoi_ca_compte": "",
            "actions": [
                "Prendre la parole sans avoir peur du jugement",
                "Se reconnaître un vrai talent",
                "Mettre à jour son CV avec fierté"
            ]
        },
        {
            "categorie": "argent",
            "titre": "MON ARGENT",
            "pourquoi_ca_compte": "",
            "actions": [
                "Demander ce que tu mérites",
                "Suivre ses dépenses sans culpabilité",
                "Se fixer un petit objectif d’épargne symbolique"
            ]
        },
        {
            "categorie": "objectifs",
            "titre": "MES OBJECTIFS",
            "pourquoi_ca_compte": "",
            "actions": [
                "Reprendre un projet abandonné par peur de rater",
                "Se fixer un micro-objectif et le tenir jusqu’au bout",
                "S’inspirer au lieu de se comparer"
            ]
        },
        {
            "categorie": "moi",
            "titre": "MOI-MÊME",
            "pourquoi_ca_compte": "",
            "actions": [
                "Arrêter de se cacher à cause de son physique",
                "Se dire des mots qui construisent, pas qui détruisent",
                "Reprendre une activité qui te fait du bien"
            ]
        },
        {
            "categorie": "reseaux",
            "titre": "RÉSEAUX SOCIAUX",
            "pourquoi_ca_compte": "",
            "actions": [
                "Publier quelque chose de vrai, sans filtre de perfection",
                "Répondre à un message qu’on évitait par peur du jugement",
                "Suivre des comptes qui font grandir, pas douter"
            ]
        },
        {
            "categorie": "amour",
            "titre": "RELATION AMOUREUSE",
            "pourquoi_ca_compte": "Astuce finale : Pour plus de conseils sur les relations amoureuses, suis Coach Amondchic, Tasha Leblanc et Coach Yoman sur TikTok et Facebook.",
            "actions": [
                "Ne plus douter de sa valeur en couple",
                "Ne plus avoir peur d’être seule",
                "Oser être toi-même, sans te transformer pour plaire"
            ]
        },
        {
            "categorie": "spiritualite",
            "titre": "SPIRITUALITÉ (optionnel)",
            "pourquoi_ca_compte": "Astuce finale : Pour plus de conseils de déblocage spirituel, suis Coach Farah sur Facebook et TikTok.",
            "actions": [
                "L’Acte d’Offrande et de Partage",
                "Le Bain Spirituel de Libération",
                "L’Acte de Foi"
            ]
        }
    ]
    
    for d_data in domaines_data:
        dom = DomaineSemaine.objects.create(
            semaine=semaine,
            categorie=d_data["categorie"],
            titre=d_data["titre"],
            pourquoi_ca_compte=d_data["pourquoi_ca_compte"]
        )
        for act_texte in d_data["actions"]:
            ActionProposee.objects.create(
                domaine=dom,
                texte=act_texte
            )
            
    print("Mise à jour de la base de données terminée avec succès !")

if __name__ == '__main__':
    populate()
