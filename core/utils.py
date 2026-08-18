def get_initial_action_data(categorie, texte, is_bonus=False):
    """
    Retourne la structure JSON (dictionnaire) du flux interactif pour une action donnée.
    Chaque étape contient au moins une question et un contexte pour garantir la profondeur de l'accompagnement.
    """
    if not texte:
        return None
        
    texte_lower = texte.lower()

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

    
    # ------------------ PRO ------------------
    if categorie == 'pro' and "cv" in texte_lower:
        return {
            "type": "checklist",
            "intro": "Un bon CV ne liste pas juste tes expériences, il raconte ton parcours. Prends le temps de soigner ces points.",
            "etapes": [
                {"label": "Informations personnelles — Vérifie que ton numéro et ton adresse mail sont professionnels et à jour.", "done": False},
                {"label": "Expériences — Décris ta dernière expérience en utilisant des verbes d'action précis (ex: 'Piloté un projet' au lieu de 'En charge de').", "done": False},
                {"label": "Compétences — Mets en évidence les 3 compétences clés spécifiquement attendues pour le poste que tu vises.", "done": False},
                {"label": "Formation — Assure-toi que les dates et les intitulés de diplômes sont corrects et clairs.", "done": False},
                {"label": "Mise en page — Aère le document et choisis une police lisible pour faciliter la lecture en diagonale.", "done": False},
                {"label": "Relecture finale — Traque la moindre faute d'orthographe (fais-le relire par un proche si besoin).", "done": False}
            ]
        }
    elif categorie == 'pro' and "1h" in texte_lower:
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Sur quel projet professionnel vas-tu avancer aujourd'hui ?",
                    "contexte": "Il peut s'agir d'un projet de création d'entreprise, d'une reconversion, ou d'une promotion. Choisis une priorité unique.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Quelle est la tâche précise que tu vas accomplir pendant cette heure ?",
                    "contexte": "Ne sois pas vague ('travailler sur mon projet'). Sois précis : 'rédiger la page d'accueil', 'lister 10 entreprises', etc.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "C'est parti. Coupe tes notifications, lance un chrono de 60 minutes et au travail.",
                    "contexte": "L'engagement envers toi-même commence maintenant. Ne reviens cliquer sur 'Valider' que lorsque le chrono aura sonné.",
                    "reponse": None,
                    "bouton": "J'ai fait cette heure"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'pro' and "formation" in texte_lower:
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Quelle compétence ou métier souhaites-tu apprendre ou approfondir ?",
                    "contexte": "Identifie le domaine exact. Par exemple : la gestion de projet, le design graphique, la menuiserie, l'anglais.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Recherche 2 à 3 organismes qui proposent cette formation. Qu'as-tu trouvé concernant la durée et le prix ?",
                    "contexte": "Regarde s'il s'agit de formations en ligne, en présentiel, et comment elles peuvent être financées (CPF, Pôle Emploi, etc.).",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Quelle est ta prochaine action pour concrétiser ce projet de formation ?",
                    "contexte": "Exemples : 'Appeler le centre de formation', 'Vérifier mon solde CPF', 'M'inscrire à une réunion d'information'.",
                    "reponse": "",
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }
        
    # ------------------ ARGENT ------------------
    elif categorie == 'argent' and ("30 minutes" in texte_lower or "business" in texte_lower):
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Quel secteur ou quelle compétence t'intéresse le plus en ce moment ?",
                    "contexte": "Pense à ce que tu aimes faire naturellement, ou à une compétence que les autres te demandent souvent (conseil, création, organisation...).",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Note 1 à 3 idées de business ou de revenus possibles dans ce domaine.",
                    "contexte": "Pas besoin d'idées révolutionnaires. Vendre un service simple, créer un petit produit, donner des cours en ligne...",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Laquelle de ces idées te semble la plus réalisable tout de suite, et pourquoi ?",
                    "contexte": "Choisis celle qui demande le moins d'investissement de départ et que tu pourrais tester dès ce week-end.",
                    "reponse": "",
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }

    # ------------------ OBJECTIFS ------------------
    elif categorie == 'objectifs' and "abandonné" in texte_lower:
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Quel est cet objectif que tu avais mis de côté ?",
                    "contexte": "Il n'est jamais trop tard pour s'y remettre. Identifie clairement ce que tu voulais accomplir.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Pourquoi avais-tu abandonné, et pourquoi est-ce important de reprendre aujourd'hui ?",
                    "contexte": "Comprendre pourquoi tu as arrêté (manque de temps, démotivation) t'aidera à ne pas reproduire le même schéma.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Quelle est la plus petite action que tu peux faire aujourd'hui pour t'y remettre ?",
                    "contexte": "Fais-la maintenant, avant de valider. L'inertie est le plus grand obstacle au succès.",
                    "reponse": "",
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'objectifs' and ("nouvel objectif" in texte_lower or "fixer" in texte_lower):
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Quel est ce nouvel objectif ?",
                    "contexte": "Formule-le de manière positive et précise (ex: 'Courir 5km d'ici la fin du mois' au lieu de 'Faire du sport').",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Pourquoi cet objectif est-il si important pour toi en ce moment ?",
                    "contexte": "Trouve ton 'Pourquoi' profond. C'est ce qui te motivera quand l'enthousiasme des premiers jours retombera.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Quelle est ta première action concrète pour l'initier ?",
                    "contexte": "L'objectif est fixé, mais il faut le démarrer. Note ta première tâche et réalise-la aujourd'hui.",
                    "reponse": "",
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'objectifs' and "en cours" in texte_lower:
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Quel est l'objectif sur lequel tu travailles actuellement ?",
                    "contexte": "Rappelle-toi la vision globale de cet objectif pour te reconnecter à ton ambition.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Où en es-tu exactement, et qu'est-ce qui te bloque éventuellement ?",
                    "contexte": "Fais un point honnête sur ton avancée. Y a-t-il un obstacle à contourner, ou une procrastination à vaincre ?",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Concrètement, tu vas faire quoi pour que ça avance cette semaine ?",
                    "contexte": "Passe à l'action dès maintenant. Fais-le, puis valide ton défi.",
                    "reponse": "",
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }

    # ------------------ MOI-MÊME ------------------
    elif categorie == 'moi' and ("peur" in texte_lower or "regard des autres" in texte_lower):
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Quelle est cette chose que tu t'empêches de faire par peur du jugement ?",
                    "contexte": "S'habiller d'une certaine façon, publier un post, donner ton avis... Identifie cette peur.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Concrètement, que se passerait-il de pire si tu le faisais quand même ?",
                    "contexte": "Souvent, on réalise que les conséquences imaginées sont bien pires que la réalité. Les autres sont concentrés sur eux-mêmes.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Passe à l'action. Même si c'est imparfait ou effrayant.",
                    "contexte": "Fais-le pour toi. La confiance en soi se construit en agissant malgré la peur. Valide une fois que c'est fait !",
                    "reponse": None,
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'moi' and "activité" in texte_lower:
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Quelle activité as-tu choisi de reprendre cette semaine ?",
                    "contexte": "Un sport, de la lecture, de la peinture, du piano... Quelque chose qui te nourrit et te fait du bien.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Qu'est-ce qui t'empêchait de la faire jusqu'à maintenant ?",
                    "contexte": "Manque de temps ? Fatigue ? En l'identifiant, tu peux trouver comment l'intégrer plus facilement (ex: le faire 10 min au lieu d'1h).",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Prends au moins 30 minutes pour cette activité aujourd'hui. Fait ?",
                    "contexte": "Accorde-toi ce moment sans culpabiliser. C'est un rendez-vous avec toi-même.",
                    "reponse": None,
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'moi' and "scroller" in texte_lower:
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Combien de temps passes-tu en moyenne sur ton téléphone par jour ?",
                    "contexte": "Regarde ton temps d'écran dans les paramètres de ton téléphone. Sois honnête avec toi-même.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Définis une limite de temps stricte sur les applications qui te font perdre du temps.",
                    "contexte": "Va dans tes paramètres et active une limite (ex: 30 min max pour Instagram/TikTok). C'est fait ?",
                    "reponse": None,
                    "bouton": "C'est fait"
                },
                {
                    "question": "Qu'as-tu fait du temps libre que tu viens de regagner ?",
                    "contexte": "Le but n'est pas juste de couper les réseaux, mais de réinvestir ce temps dans quelque chose de positif (repos, lecture, échange).",
                    "reponse": "",
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }

    # ------------------ RÉSEAUX SOCIAUX ------------------
    elif categorie == 'reseaux' and "publier" in texte_lower:
        return {
            "type": "checklist",
            "intro": "Créer du contenu te permet de montrer ton expertise et de développer ton audience. Suis ces étapes :",
            "etapes": [
                {"label": "Choisis un sujet pertinent — Trouve un sujet qui te tient à cœur et qui apporte de la valeur à ta cible.", "done": False},
                {"label": "Prépare ton message — Rédige ou scripte ton contenu pour aller à l'essentiel et capter l'attention.", "done": False},
                {"label": "Passe à la création — Enregistre, écris ou designe. Fais-le simplement, sans chercher la perfection absolue.", "done": False},
                {"label": "Publie ton contenu — Appuie sur le bouton publier (et n'hésite pas à le partager ou le sponsoriser légèrement).", "done": False}
            ]
        }
    elif categorie == 'reseaux' and "nettoyer" in texte_lower:
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Identifie un type de compte qui déclenche chez toi de la comparaison, de la jalousie ou du stress.",
                    "contexte": "Cela peut être des influenceurs 'parfaits', des actualités anxiogènes, ou des gens qui te font te sentir insuffisant.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Désabonne-toi de 5 comptes de ce type dès maintenant.",
                    "contexte": "Ton fil d'actualité est ton espace personnel. Tu as le droit (et le devoir) de protéger ton énergie. C'est fait ?",
                    "reponse": None,
                    "bouton": "C'est fait"
                },
                {
                    "question": "Comment te sens-tu après avoir repris le contrôle de ton fil ?",
                    "contexte": "L'objectif est d'utiliser les réseaux sociaux de manière intentionnelle, et non de subir passivement ce qu'on te montre.",
                    "reponse": "",
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'reseaux' and ("construire" in texte_lower or "scroll" in texte_lower or "utile" in texte_lower):
        return {
            "type": "questionnaire",
            "etapes": [
                {
                    "question": "Sur quelle application as-tu le plus tendance à scroller sans but ?",
                    "contexte": "Prends conscience de tes habitudes de consommation. Est-ce au réveil ? Dans les transports ? Le soir dans le lit ?",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Choisis une activité utile à faire à la place pendant les 30 prochaines minutes.",
                    "contexte": "Ça peut être avancer sur un projet, lire un livre, écouter un podcast instructif, ranger ton espace, ou juste marcher.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "J'ai tenu mes 30 minutes sans scroller !",
                    "contexte": "Si tu l'as fait, tu viens de prouver que tu pouvais reprendre le contrôle de ton attention. Félicitations !",
                    "reponse": None,
                    "bouton": "Valider mon défi"
                }
            ],
            "etape_courante": 0
        }

    # ------------------ RELATION AMOUREUSE ------------------
    elif categorie == 'amour' and "peine de cœur" in texte_lower:
        return {
            "type": "questionnaire",
            "intro": "Tu as rompu ? Tu as été trompé(e) ? Tu as été blessé(e) ? Ne reste pas dans la douleur — c’est le moment de te reconstruire et de rayonner encore plus fort.",
            "message_validation": "On est fière de toi. Ce que tu viens de faire n’était pas facile, mais c'est le premier pas vers ta nouvelle lumière.",
            "etapes": [
                {
                    "question": "Qu’est-ce qui t’a fait le plus mal dans cette histoire ? Dis-le, une bonne fois.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Choisis une action concrète cette semaine pour prendre soin de toi et rayonner davantage — ton corps, ton style, ta confiance, une sortie entre ami(e)s.",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Prends soin de toi, avance sur tes projets, entoure-toi de gens qui te tirent vers le haut. N’accepte plus jamais moins que ce que tu mérites.",
                    "reponse": None,
                    "bouton": "Oui, je l’ai fait pour moi"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'amour' and "marcher dessus" in texte_lower:
        return {
            "type": "questionnaire",
            "message_validation": "Bravo pour ton courage. Poser ses limites est le plus beau cadeau que tu puisses te faire.",
            "etapes": [
                {
                    "question": "Dans ta relation actuelle ou une relation récente, y a-t-il des moments où tu t’es laissé(e) marcher dessus pour ne pas perdre l’autre ?",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Qu’est-ce que tu as accepté que tu n’aurais jamais dû accepter ?",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "Pose cette limite dès aujourd’hui — dis-le clairement à la personne concernée, ou à toi-même si ce n’est pas encore possible de le dire en face. Ne recule plus.",
                    "reponse": None,
                    "bouton": "Oui, je l’ai fait pour moi"
                }
            ],
            "etape_courante": 0
        }
    elif categorie == 'amour' and "donner son corps" in texte_lower:
        return {
            "type": "questionnaire",
            "intro": "Ton corps n’est pas un moyen de garder quelqu’un. Il mérite d’aller à une personne qui te respecte et que tu aimes vraiment.",
            "message_validation": "Tu as repris le contrôle de ta valeur. Sois fière de cette honnêteté envers toi-même.",
            "etapes": [
                {
                    "question": "As-tu déjà dit oui alors que tu voulais dire non, juste pour ne pas décevoir quelqu’un ?",
                    "reponse": "",
                    "bouton": "Suivant"
                },
                {
                    "question": "À partir de maintenant : dis non quand tu n’as pas envie, même si ça déplaît. N’accepte de te donner qu’à quelqu’un qui te mérite vraiment. Choisis une de ces règles et applique-la dès aujourd’hui.",
                    "reponse": None,
                    "bouton": "Oui, je l’ai fait pour moi"
                }
            ],
            "etape_courante": 0
        }

    # ------------------ SPIRITUALITÉ ------------------
    elif categorie == 'spiritualite' and "bain" in texte_lower:
        return {
            "type": "checklist",
            "intro": "Ce rituel nettoie les lourdeurs énergétiques et redonne de la clarté mentale.",
            "etapes": [
                {"label": "Rassemble le matériel : Trouve du gros sel, des feuilles de citronnelle (ou basilic) et de l'eau tiède.", "done": False},
                {"label": "Trouve le bon moment : Fais ce bain de préférence le soir juste avant de dormir, ou tôt le matin au réveil.", "done": False},
                {"label": "La purification : Rince-toi consciemment du haut vers le bas, en visualisant les mauvaises énergies s'écouler.", "done": False},
                {"label": "L'affirmation : Affirme à voix haute avec conviction que tout blocage te quitte et que tu te renouvelles.", "done": False}
            ]
        }
    elif categorie == 'spiritualite' and "offrande" in texte_lower:
        return {
            "type": "checklist",
            "intro": "Ce geste de don désintéressé active la loi d'abondance et attire les bonnes opportunités.",
            "etapes": [
                {"label": "Prépare ton offrande : Choisis une somme symbolique, un bon repas chaud, ou un présent réellement utile.", "done": False},
                {"label": "Choisis le moment : Le vendredi ou le dimanche matin sont des moments particulièrement propices.", "done": False},
                {"label": "L'action du don : Donne-la à une personne dans le besoin (âgée, enfant, ou guide), avec une intention de cœur pure.", "done": False}
            ]
        }
    elif categorie == 'spiritualite' and "prière" in texte_lower:
        return {
            "type": "checklist",
            "intro": "Cette pratique intime brise les freins invisibles de ton esprit et élève profondément ta fréquence.",
            "etapes": [
                {"label": "La préparation : Prépare une bougie blanche et prévois au moins 10 minutes de calme absolu, sans téléphone.", "done": False},
                {"label": "L'atmosphère : Fais-le dans le silence total (l'idéal étant très tôt, entre 5h et 6h du matin).", "done": False},
                {"label": "L'ancrage : Allume la bougie et tiens-toi debout, les pieds bien ancrés dans le sol, l'esprit clair.", "done": False},
                {"label": "L'élévation : Proclame tes bénédictions à voix haute, avec une foi et une conviction inébranlables.", "done": False}
            ]
        }
        
    return None

def get_precomputed_program_stats(user):
    """
    Pré-calcule les statistiques de tous les programmes pour l'utilisateur
    afin d'éviter le problème des requêtes N+1.
    """
    from .models import DomaineSemaine, DomaineUtilisateur, ActionBonusUtilisateur
    from django.db.models import Count, Sum
    
    stats = {}
    
    # 1. Totaux de domaines par programme (indépendant de l'utilisateur)
    domaines = DomaineSemaine.objects.exclude(categorie='spiritualite').values('semaine__programme_id').annotate(total=Count('id'))
    for d in domaines:
        prog_id = d['semaine__programme_id']
        stats[prog_id] = {'total': d['total'], 'termines': 0, 'a_commence': False, 'xp_d': 0, 'xp_b': 0}
        
    if user and user.is_authenticated:
        # 2. Domaines terminés par programme
        termines = DomaineUtilisateur.objects.filter(
            utilisateur=user, statut='completed'
        ).exclude(domaine__categorie='spiritualite').values('domaine__semaine__programme_id').annotate(total=Count('id'))
        
        for t in termines:
            prog_id = t['domaine__semaine__programme_id']
            if prog_id not in stats:
                stats[prog_id] = {'total': 6, 'termines': 0, 'a_commence': False, 'xp_d': 0, 'xp_b': 0}
            stats[prog_id]['termines'] = t['total']
            
        # 3. Programmes commencés
        engages = DomaineUtilisateur.objects.filter(
            utilisateur=user
        ).values('domaine__semaine__programme_id').distinct()
        
        for e in engages:
            prog_id = e['domaine__semaine__programme_id']
            if prog_id in stats:
                stats[prog_id]['a_commence'] = True
                
        # 4. XP par programme (Domaines)
        xp_domaines = DomaineUtilisateur.objects.filter(
            utilisateur=user
        ).values('domaine__semaine__programme_id').annotate(total=Sum('xp_gagnes'))
        
        for x in xp_domaines:
            prog_id = x['domaine__semaine__programme_id']
            if prog_id in stats:
                stats[prog_id]['xp_d'] = x['total'] or 0
                
        # 5. XP par programme (Bonus)
        xp_bonus = ActionBonusUtilisateur.objects.filter(
            utilisateur=user
        ).values('domaine__semaine__programme_id').annotate(total=Sum('xp_gagnes'))
        
        for x in xp_bonus:
            prog_id = x['domaine__semaine__programme_id']
            if prog_id in stats:
                stats[prog_id]['xp_b'] = x['total'] or 0
                
    return stats
