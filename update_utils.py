import os

new_code = '''
    # --- CONFIANCE EN SOI (Nouveau Programme) ---
    
    # PRO
    if categorie == 'pro' and 'parole' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à une fois où tu n’as pas osé parler ou donner ton avis. Qu’est-ce qui t’a retenue ?', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Entraîne-toi avant de parler : répète ce que tu veux dire à voix haute devant un miroir, ou enregistre-toi et réécoute-toi.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Cette semaine, prends la parole une fois — même pour une petite chose.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'pro' and 'talent' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Note une compétence que tu maîtrises vraiment. Si tu as du mal à voir clair, demande à une IA comme Claude ou ChatGPT de t’aider.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Demande à 2-3 personnes qui te connaissent bien ce qu’elles pensent que tu fais mieux que la moyenne.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Utilise ce talent activement cette semaine.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'pro' and 'cv' in texte_lower and 'fierté' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Relis ton CV actuel. Qu’est-ce qui manque ?', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Utilise un modèle gratuit sur Canva (canva.com). Vérifie qu’il est compatible ATS avec Jobscan (jobscan.co) : évite tableaux et designs trop chargés.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Ajoute cette réussite oubliée, et relis-le en te disant : ‘je mérite ce que j’ai accompli’.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
        
    # ARGENT
    elif categorie == 'argent' and 'mérites' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à une augmentation, un tarif ou un paiement que tu n’as jamais osé demander.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Prépare ce que tu vas dire — écris 2-3 phrases claires. Entraîne-toi à voix haute avant.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Fixe un moment cette semaine pour le demander.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'argent' and 'dépenses' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Note toutes tes dépenses pendant 7 jours.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Utilise l’appli Wallet (budgetbakers.com, gratuite) pour tout noter au fur et à mesure.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'À la fin de la semaine, regarde ce que tu as noté sans te juger.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'argent' and 'épargne' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Choisis un petit montant réaliste à mettre de côté cette semaine.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Mets-le physiquement de côté dès réception — enveloppe, tirelire, ou compte séparé.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Tiens ton engagement jusqu’à la fin de la semaine, sans y toucher, et plus tard cherche un business rentable pour commencer.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }

    # OBJECTIFS
    elif categorie == 'objectifs' and 'abandonné' in texte_lower and 'rater' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à un projet abandonné par peur de rater.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Utilise Notion (notion.so) ou Trello (trello.com) pour le découper en tâches simples. Cherche aussi des témoignages sur YouTube ou les réseaux sociaux.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Fais cette première étape cette semaine, même imparfaitement.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'objectifs' and 'micro-objectif' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Choisis un petit objectif réalisable en 7 jours maximum.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Découpe-le en 2-3 actions simples avec des dates précises, sur Google Agenda (calendar.google.com).', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Tiens ton engagement jusqu’au bout, sans repousser.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'objectifs' and 'comparer' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Note 3 choses que TOI tu as accomplies à ton rythme.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Choisis une personne que tu admires — comme Stanislas Zézé, Fabrice Sawegnon ou Maurine Ayité.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Mets une limite de temps d’écran sur les comptes qui te donnent un sentiment de comparaison.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }

    # MOI-MÊME
    elif categorie == 'moi' and 'physique' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Y a-t-il une partie de toi qui te pousse à te cacher ou à avoir honte ?', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Cherche une routine skincare sur YouTube. Cherche des tenues selon ta morphologie sur TikTok/Instagram/Facebook. Si tu te maquilles, regarde aussi des tutoriels adaptés.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Cette semaine, va vers une personne ou une situation que tu évitais à cause de ça.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'moi' and 'détruisent' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repère une phrase négative que tu te dis souvent sur toi-même.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Transforme-la en affirmation positive. Répète-la à voix haute devant le miroir chaque matin — écris-la sur un post-it.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Note comment tu te sens à la fin de la semaine en la répétant.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'moi' and 'activité' in texte_lower and 'bien' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à une activité que tu aimais et que tu as abandonnée.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Trouve un tutoriel gratuit sur YouTube pour t’y remettre en douceur, ou rejoins un groupe près de chez toi.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Consacre au moins une session cette semaine, rien que pour toi.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }

    # RÉSEAUX SOCIAUX
    elif categorie == 'reseaux' and 'perfection' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à un post jamais publié par peur du jugement.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Publie-le cette semaine, tel quel. Utilise CapCut (capcut.com, gratuit) si tu veux un montage simple.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Regarde les réactions sans les juger.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'reseaux' and 'répondre' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à un message que tu évites par peur de mal faire.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Rédige ta réponse, même imparfaite.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Envoie-la cette semaine.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'reseaux' and 'grandir' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repère 3-5 comptes qui te font douter de toi ou te comparer.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Désabonne-toi ou mets-les en sourdine, sans culpabilité.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Suis des comptes qui t’aident vraiment à progresser — comme William Angora, Naomi Davinci ou Mymy sur TikTok, Instagram ou Facebook.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }

    # RELATION AMOUREUSE
    elif categorie == 'amour' and 'valeur en couple' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à un moment où tu as douté d’être ‘assez bien’ pour une relation.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Note 3 qualités qui font de toi une personne qui mérite d’être aimée pleinement, sans conditions.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Cette semaine, affirme un besoin ou une envie dans ta relation sans t’excuser.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'amour' and 'peur d’être seule' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Es-tu restée dans une relation ou une situation par peur d’être seule plutôt que par envie réelle ?', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Fais une activité seule cette semaine que tu apprécies vraiment — sortie, repas, cinéma.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Note ce que cette expérience t’a appris sur ta propre valeur.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }
    elif categorie == 'amour' and 'transformer' in texte_lower:
        return {
            'type': 'questionnaire',
            'etapes': [
                {'question': 'Repense à une fois où tu as caché une partie de toi pour plaire à quelqu’un.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Cette semaine, montre-toi telle que tu es vraiment dans une interaction où tu aurais habituellement filtré.', 'reponse': '', 'bouton': 'Suivant'},
                {'question': 'Observe comment tu te sens après.', 'reponse': None, 'bouton': 'Oui, je l’ai fait pour moi'}
            ],
            'etape_courante': 0
        }

    # SPIRITUALITÉ
    elif categorie == 'spiritualite' and 'offrande' in texte_lower and 'partage' in texte_lower:
        return {
            'type': 'checklist',
            'intro': 'Ce don de nourriture symbolise l’abondance et le soutien. En nourrissant ton prochain, tu montres à l’Univers que tu es un canal d’abondance — ça consolide l’estime de soi et chasse le sentiment de manque.',
            'etapes': [
                {'label': 'Prépare une offrande de vivres (riz, sucre, lait, ou denrées de première nécessité).', 'done': False},
                {'label': 'Offre-la à une personne dans le besoin ou une personne âgée — si possible un jour lié à ton chiffre de naissance.', 'done': False}
            ]
        }
    elif categorie == 'spiritualite' and 'libération' in texte_lower:
        return {
            'type': 'checklist',
            'intro': 'Ce bain nettoie l’aura des énergies de doute, du regard des autres et de la peur de l’échec.',
            'etapes': [
                {'label': 'Prépare ton bain : eau claire tempérée, gros sel de mer, fleurs jaunes ou écorces d’agrumes, quelques gouttes de fleur d’oranger.', 'done': False},
                {'label': 'Après ta douche, verse cette eau des épaules aux pieds en disant : « Je me libère du poids du jugement, des peurs héritées et de l’ombre du doute. Je reprends ma place et mon rayonnement naturel. »', 'done': False},
                {'label': 'Laisse sécher à l’air libre, sans frotter.', 'done': False}
            ]
        }
    elif categorie == 'spiritualite' and 'foi' in texte_lower:
        return {
            'type': 'checklist',
            'intro': 'L’aube (5h-5h30) ou le coucher du soleil sont des moments de transition intense — parfaits pour sceller un engagement fort avec toi-même.',
            'etapes': [
                {'label': 'Installe-toi pieds nus, allume une bougie jaune ou dorée.', 'done': False},
                {'label': 'Écris sur un papier une situation bloquée par le manque d’assurance.', 'done': False},
                {'label': 'Prononce ta prière d’abandon et de puissance, puis brûle ou enterre le papier — engage-toi à une action immédiate dans la journée.', 'done': False}
            ]
        }
'''

with open('core/utils_backup.py', 'r', encoding='utf-8') as f:
    content = f.read()

insertion_point = "texte_lower = texte.lower()"
if insertion_point in content:
    modified = content.replace(insertion_point, insertion_point + "\n" + new_code)
    with open('core/utils.py', 'w', encoding='utf-8') as f2:
        f2.write(modified)
    print("utils.py mis à jour !")
else:
    print("Point d'insertion non trouvé.")
