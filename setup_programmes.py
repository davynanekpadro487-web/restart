import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurea.settings')
django.setup()

from core.models import Programme, Semaine, DomaineSemaine, ActionProposee

def setup():
    # 1. Fetch old Semaines
    semaine_construire = Semaine.objects.filter(theme="Construire sa vie avant l'amour").first()
    semaine_confiance = Semaine.objects.filter(theme="Confiance en soi").first()
    semaine_entourage = Semaine.objects.filter(theme="Entourage").first()
    semaine_discipline = Semaine.objects.filter(theme="Discipline").first()

    # 2. Create the new Programmes
    prog_construire, _ = Programme.objects.get_or_create(
        theme="Construire sa vie avant l'amour",
        defaults={
            'statut': 'archive',
            'date_debut': date(2026, 8, 5),
            'date_fin': date(2026, 8, 26),
            'description': 'Un programme pour poser des bases saines avant de construire une relation.',
        }
    )
    # Ensure it's archive if it already existed
    prog_construire.statut = 'archive'
    prog_construire.save()

    prog_confiance, _ = Programme.objects.get_or_create(
        theme="Confiance en soi",
        defaults={
            'statut': 'en_cours',
            'date_debut': date(2026, 8, 12),
            'date_fin': date(2026, 9, 2),
            'description': 'Reprends le contrôle de ta vie et développe une confiance inébranlable.',
        }
    )
    prog_confiance.statut = 'en_cours'
    prog_confiance.save()

    prog_entourage, _ = Programme.objects.get_or_create(
        theme="Entourage",
        defaults={'statut': 'a_venir', 'description': 'Savoir s\'entourer des bonnes personnes.'}
    )
    prog_entourage.statut = 'a_venir'
    prog_entourage.save()

    prog_discipline, _ = Programme.objects.get_or_create(
        theme="Discipline",
        defaults={'statut': 'a_venir', 'description': 'Construire une routine solide pour atteindre tes objectifs.'}
    )
    prog_discipline.statut = 'a_venir'
    prog_discipline.save()

    # 3. Move old Semaines to these new Programmes and rename them
    if semaine_construire:
        semaine_construire.programme = prog_construire
        semaine_construire.theme = "Semaine 1"
        semaine_construire.save()

    if semaine_confiance:
        semaine_confiance.programme = prog_confiance
        semaine_confiance.theme = "Semaine 1"
        semaine_confiance.save()
        
        # Populate Confiance en soi with 6 dummy domains if empty
        if not semaine_confiance.domaines.exists():
            categories = [
                ('pro', 'Vie pro & études', 'Faire un bilan de tes compétences.'),
                ('argent', 'Mon argent', 'Comprendre ton rapport à l\'argent.'),
                ('objectifs', 'Mes objectifs', 'Définir un cap clair.'),
                ('moi', 'Moi-même', 'Prendre soin de son corps et son esprit.'),
                ('reseaux', 'Réseaux sociaux', 'Savoir couper les notifications.'),
                ('amour', 'Relation amoureuse', 'Apprendre à s\'aimer soi-même d\'abord.'),
                ('spiritualite', 'Spiritualité (Optionnel)', 'Se reconnecter à son intuition.')
            ]
            for cat_code, cat_titre, cat_pourquoi in categories:
                dom = DomaineSemaine.objects.create(
                    semaine=semaine_confiance,
                    categorie=cat_code,
                    titre=cat_titre,
                    pourquoi_ca_compte=cat_pourquoi
                )
                ActionProposee.objects.create(domaine=dom, texte="Action fictive (à modifier)")
                ActionProposee.objects.create(domaine=dom, texte="Autre action fictive")
                ActionProposee.objects.create(domaine=dom, texte="Troisième action fictive")

    if semaine_entourage:
        semaine_entourage.programme = prog_entourage
        semaine_entourage.theme = "Semaine 1"
        semaine_entourage.save()

    if semaine_discipline:
        semaine_discipline.programme = prog_discipline
        semaine_discipline.theme = "Semaine 1"
        semaine_discipline.save()

    # 4. Clean up old "Le Nouveau Départ" if it has no weeks left
    old_prog = Programme.objects.filter(theme="Le Nouveau Départ").first()
    if old_prog and old_prog.semaines.count() == 0:
        old_prog.delete()
        
    print("Migration terminée.")

if __name__ == '__main__':
    setup()
