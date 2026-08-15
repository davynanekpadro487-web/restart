from django.core.management.base import BaseCommand
from datetime import date
from core.models import Programme, Semaine, DomaineSemaine, ActionProposee


class Command(BaseCommand):
    help = "Seed complet : crée les 5 programmes + semaines + domaines + actions en base."

    def handle(self, *args, **kwargs):
        self.stdout.write("=== SEED COMPLET — Restart by Auréa ===")
        self._seed_programmes()
        self.stdout.write(self.style.SUCCESS("Seed terminé avec succès !"))

    # ────────────────────────────────────────────────────────────
    # PROGRAMMES
    # ────────────────────────────────────────────────────────────
    def _seed_programmes(self):
        programmes = [
            {
                "theme": "Construire sa vie avant l'amour",
                "ordre": 1, "publie": True,
                "description": "Un programme pour poser des bases saines avant de construire une relation.",
                "semaines": [self._semaine_construire()],
            },
            {
                "theme": "Confiance en soi",
                "ordre": 2, "publie": True,
                "description": "Reprends le contrôle de ta vie et développe une confiance inébranlable.",
                "semaines": [self._semaine_confiance()],
            },
            {
                "theme": "Entourage",
                "ordre": 3, "publie": True,
                "description": "Savoir s'entourer des bonnes personnes.",
                "semaines": [self._semaine_entourage()],
            },
            {
                "theme": "Discipline",
                "ordre": 4, "publie": False,
                "description": "Construire une routine solide pour atteindre tes objectifs.",
                "semaines": [],
            },
            {
                "theme": "Gestion du temps",
                "ordre": 5, "publie": False,
                "description": "Apprendre à prioriser et à utiliser son temps intelligemment.",
                "semaines": [],
            },
        ]

        for data in programmes:
            semaines_data = data.pop("semaines")
            prog, created = Programme.objects.get_or_create(
                theme=data["theme"],
                defaults={
                    "ordre": data["ordre"],
                    "publie": data["publie"],
                    "description": data["description"],
                    "statut": "en_cours" if data["publie"] else "a_venir",
                }
            )
            if not created:
                prog.ordre = data["ordre"]
                prog.publie = data["publie"]
                prog.description = data["description"]
                prog.save()
                action = "mis à jour"
            else:
                action = "créé"

            self.stdout.write(f"  Programme '{prog.theme}' {action} (ordre={prog.ordre}, publié={prog.publie})")

            for sem_data in semaines_data:
                self._create_semaine(prog, sem_data)

    # ────────────────────────────────────────────────────────────
    # HELPER : create semaine + domaines
    # ────────────────────────────────────────────────────────────
    def _create_semaine(self, programme, sem_data):
        sem, created = Semaine.objects.get_or_create(
            programme=programme,
            ordre=sem_data["ordre"],
            defaults={
                "theme": sem_data["theme"],
                "objectif": sem_data["objectif"],
                "questions": sem_data["questions"],
                "date_rendez_vous": sem_data["date_rendez_vous"],
            }
        )
        if not created:
            sem.theme = sem_data["theme"]
            sem.objectif = sem_data["objectif"]
            sem.questions = sem_data["questions"]
            sem.save()

        action = "créée" if created else "mise à jour"
        self.stdout.write(f"    Semaine '{sem.theme}' {action}")

        # Re-seed domaines uniquement si absents
        if not DomaineSemaine.objects.filter(semaine=sem).exists():
            for dom_data in sem_data["domaines"]:
                dom = DomaineSemaine.objects.create(
                    semaine=sem,
                    categorie=dom_data["categorie"],
                    titre=dom_data["titre"],
                    pourquoi_ca_compte=dom_data.get("pourquoi_ca_compte", ""),
                )
                for texte in dom_data["actions"]:
                    ActionProposee.objects.create(domaine=dom, texte=texte)
            self.stdout.write(f"      {len(sem_data['domaines'])} domaines insérés")
        else:
            self.stdout.write(f"      Domaines déjà présents — ignorés")

    # ────────────────────────────────────────────────────────────
    # CONTENU — Construire sa vie avant l'amour
    # ────────────────────────────────────────────────────────────
    def _semaine_construire(self):
        return {
            "ordre": 1,
            "theme": "Semaine 1",
            "objectif": "Poser les premières bases solides",
            "questions": (
                "1. Qu'est-ce que tu veux vraiment construire pour toi-même ?\n"
                "2. Quelles habitudes te rapprochent de la femme que tu veux être ?\n"
                "3. Qu'est-ce qui te freine encore aujourd'hui ?"
            ),
            "date_rendez_vous": date(2026, 8, 13),
            "domaines": [
                {
                    "categorie": "pro",
                    "titre": "Vie professionnelle / Études",
                    "pourquoi_ca_compte": "Le travail et les études sont des piliers de ton indépendance et de ta confiance en toi.",
                    "actions": [
                        "Mettre à jour mon CV",
                        "Consacrer 1h à mon projet professionnel",
                        "Faire mes recherches sur une formation"
                    ]
                },
                {
                    "categorie": "argent",
                    "titre": "Mon argent",
                    "pourquoi_ca_compte": "L'indépendance financière te donne la liberté de faire tes propres choix sans dépendre de personne.",
                    "actions": [
                        "Noter toutes mes dépenses pendant 7 jours afin de comprendre où part réellement mon argent.",
                        "Identifier au moins 3 dépenses inutiles ou évitables et décider laquelle je vais réduire.",
                        "Consacrer 30 minutes à rechercher une idée réaliste de revenu, de business, de compétence rentable ou d'opportunité financière adaptée à ma situation."
                    ]
                },
                {
                    "categorie": "objectifs",
                    "titre": "Mes objectifs",
                    "pourquoi_ca_compte": "Avoir des objectifs clairs te permet de rester focalisée sur ta propre évolution.",
                    "actions": [
                        "Reprendre un objectif abandonné",
                        "Fixer un nouvel objectif clair pour le mois",
                        "Faire avancer un objectif déjà en cours"
                    ]
                },
                {
                    "categorie": "moi",
                    "titre": "Moi-même",
                    "pourquoi_ca_compte": "Prendre soin de toi et te connaître est la base de toute relation saine, avec toi-même et les autres.",
                    "actions": [
                        "Faire quelque chose que je repousse par peur du regard des autres",
                        "Reprendre une activité physique ou que j'aime",
                        "Passer moins de temps à scroller"
                    ]
                },
                {
                    "categorie": "reseaux",
                    "titre": "Réseaux sociaux",
                    "pourquoi_ca_compte": "Ton environnement numérique influence tes pensées. Le maîtriser, c'est protéger ton énergie.",
                    "actions": [
                        "Créer et publier un contenu pour mon business",
                        "Nettoyer mes abonnements",
                        "Remplacer le scroll par une action utile (30 min)"
                    ]
                },
                {
                    "categorie": "amour",
                    "titre": "Relation amoureuse",
                    "pourquoi_ca_compte": "L'amour que tu acceptes est le reflet de l'amour que tu te portes. Ne te brade pas.",
                    "actions": [
                        "Traverser une peine de cœur",
                        "Arrêter de se laisser marcher dessus en amour",
                        "Ne pas donner son corps juste pour plaire"
                    ]
                },
                {
                    "categorie": "spiritualite",
                    "titre": "Spiritualité (Optionnel)",
                    "pourquoi_ca_compte": "Te reconnecter à tes valeurs et à ton intériorité te donne force et clarté d'esprit.",
                    "actions": [
                        "Le Bain de Libération",
                        "L'Offrande de Semence",
                        "La Prière d'Élévation"
                    ]
                },
            ]
        }

    # ────────────────────────────────────────────────────────────
    # CONTENU — Confiance en soi
    # ────────────────────────────────────────────────────────────
    def _semaine_confiance(self):
        return {
            "ordre": 1,
            "theme": "Semaine 1",
            "objectif": "Reprendre confiance en toi et en ta valeur",
            "questions": (
                "1. Dans quels moments te sens-tu le moins sûre de toi ?\n"
                "2. Qu'est-ce que tu te dis à toi-même quand tu doutes ?\n"
                "3. À quoi ressemblerait ta vie si tu avais une confiance inébranlable dès aujourd'hui ?"
            ),
            "date_rendez_vous": date(2026, 8, 20),
            "domaines": [
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
                        "Se fixer un petit objectif d'épargne symbolique"
                    ]
                },
                {
                    "categorie": "objectifs",
                    "titre": "MES OBJECTIFS",
                    "pourquoi_ca_compte": "",
                    "actions": [
                        "Reprendre un projet abandonné par peur de rater",
                        "Se fixer un micro-objectif et le tenir jusqu'au bout",
                        "S'inspirer au lieu de se comparer"
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
                        "Répondre à un message qu'on évitait par peur du jugement",
                        "Suivre des comptes qui font grandir, pas douter"
                    ]
                },
                {
                    "categorie": "amour",
                    "titre": "RELATION AMOUREUSE",
                    "pourquoi_ca_compte": "Astuce finale : Pour plus de conseils sur les relations amoureuses, suis Coach Amondchic, Tasha Leblanc et Coach Yoman sur TikTok et Facebook.",
                    "actions": [
                        "Ne plus douter de sa valeur en couple",
                        "Ne plus avoir peur d'être seule",
                        "Oser être toi-même, sans te transformer pour plaire"
                    ]
                },
                {
                    "categorie": "spiritualite",
                    "titre": "SPIRITUALITÉ (optionnel)",
                    "pourquoi_ca_compte": "Astuce finale : Pour plus de conseils de déblocage spirituel, suis Coach Farah sur Facebook et TikTok.",
                    "actions": [
                        "L'Acte d'Offrande et de Partage",
                        "Le Bain Spirituel de Libération",
                        "L'Acte de Foi"
                    ]
                },
            ]
        }

    # ────────────────────────────────────────────────────────────
    # CONTENU — Entourage
    # ────────────────────────────────────────────────────────────
    def _semaine_entourage(self):
        return {
            "ordre": 1,
            "theme": "Semaine 1",
            "objectif": "Évaluer et améliorer ton cercle",
            "questions": (
                "1. Qui dans ton entourage te tire vers le haut ?\n"
                "2. Qui te draine de ton énergie sans que tu t'en rendes compte ?\n"
                "3. Comment peux-tu renforcer les relations qui te font vraiment du bien ?"
            ),
            "date_rendez_vous": date(2026, 8, 27),
            "domaines": [
                {
                    "categorie": "pro",
                    "titre": "Vie professionnelle / Études",
                    "pourquoi_ca_compte": "Ton entourage professionnel détermine ta motivation et tes opportunités. T'entourer des bonnes personnes te tire vers le haut.",
                    "actions": [
                        "Proposer un déjeuner ou un café à un(e) collègue ou camarade inspirant(e) pour échanger (renforce ton réseau).",
                        "Identifier 2 personnes toxiques ou plaintives au travail/école et réduire volontairement mes interactions avec elles.",
                        "Envoyer un message de remerciement ou de reconnaissance à quelqu'un qui m'a aidé professionnellement récemment."
                    ]
                },
                {
                    "categorie": "argent",
                    "titre": "Mon argent",
                    "pourquoi_ca_compte": "L'argent est souvent tabou, mais s'entourer de personnes ayant une saine éducation financière aide à faire les bons choix.",
                    "actions": [
                        "Parler d'un de mes objectifs financiers avec une personne de confiance qui gère bien son argent (obtenir un bon conseil).",
                        "Arrêter de suivre les personnes sur les réseaux sociaux qui me poussent à la surconsommation.",
                        "Proposer une sortie gratuite ou peu coûteuse à mes amis cette semaine au lieu d'une dépense habituelle."
                    ]
                },
                {
                    "categorie": "objectifs",
                    "titre": "Mes objectifs",
                    "pourquoi_ca_compte": "Partager ses objectifs avec les bonnes personnes crée une saine pression positive et un soutien précieux.",
                    "actions": [
                        "Partager mon objectif principal du mois avec un(e) ami(e) en lui demandant de prendre de mes nouvelles à ce sujet (crée de l'accountability).",
                        "Lister 3 personnes de mon entourage et écrire à côté d'elles comment elles m'inspirent à m'améliorer.",
                        "Mettre fin poliment à une conversation où quelqu'un essaie de me décourager d'un de mes projets."
                    ]
                },
                {
                    "categorie": "moi",
                    "titre": "Moi-même",
                    "pourquoi_ca_compte": "Tu es la moyenne des 5 personnes que tu côtoies le plus. Savoir dire non est essentiel pour préserver ton énergie.",
                    "actions": [
                        "Dire non à une sollicitation ou une sortie dont je n'ai pas vraiment envie, sans me justifier (protège mon énergie).",
                        "Faire le tri dans mes contacts téléphoniques : supprimer ou bloquer les personnes qui ne m'apportent que du négatif.",
                        "Prendre un moment seul(e) pour évaluer comment je me sens après avoir vu telle ou telle personne."
                    ]
                },
                {
                    "categorie": "reseaux",
                    "titre": "Réseaux sociaux",
                    "pourquoi_ca_compte": "Ton cercle social inclut aussi le monde numérique. Filtre impitoyablement ce qui entre dans ton cerveau.",
                    "actions": [
                        "Me désabonner d'au moins 5 comptes qui me font me sentir inférieur(e) ou qui polluent mon fil d'actualité.",
                        "S'abonner à 3 nouveaux comptes qui m'inspirent, m'éduquent ou me motivent (enrichit mon entourage numérique).",
                        "Laisser un commentaire positif et sincère sur la publication d'un de mes amis pour renforcer notre lien."
                    ]
                },
                {
                    "categorie": "amour",
                    "titre": "Relation amoureuse",
                    "pourquoi_ca_compte": "Tes amis ont un impact majeur sur ta vision de l'amour. Ne laisse pas leurs échecs ou cynisme dicter ta vie sentimentale.",
                    "actions": [
                        "Identifier une croyance négative sur l'amour que mon entourage m'a transmise, et décider de ne plus y croire (reprendre mon pouvoir).",
                        "Faire un compliment sincère à mon partenaire (ou à moi-même si je suis célibataire) sur ses qualités humaines.",
                        "Ne pas participer à une conversation où l'on dénigre les hommes/femmes de manière généralisée."
                    ]
                },
                {
                    "categorie": "spiritualite",
                    "titre": "Spiritualité",
                    "pourquoi_ca_compte": "Ta paix intérieure ne doit pas être perturbée par le chaos extérieur. Un bon entourage respecte tes valeurs.",
                    "actions": [
                        "La bulle de protection : visualiser une lumière protectrice autour de soi avant de retrouver un environnement ou une personne drainante.",
                        "Le rituel du pardon silencieux : pardonner intérieurement à quelqu'un qui m'a déçu, non pour lui, mais pour me libérer.",
                        "Le cercle de gratitude : prendre 5 minutes pour écrire ce que les personnes que j'aime apportent de beau dans ma vie."
                    ]
                },
            ]
        }
