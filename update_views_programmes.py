import re

with open('core/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update get_programme_actuel
content = re.sub(
    r'def get_programme_actuel\(\):\n\s*return Programme.objects.filter\(statut=\'en_cours\'\).first\(\)',
    '''def get_programme_actuel(utilisateur=None):
    if utilisateur and utilisateur.is_authenticated:
        programmes = Programme.objects.all().order_by('ordre', 'date_debut')
        for prog in programmes:
            domaines_termines = DomaineUtilisateur.objects.filter(
                utilisateur=utilisateur, 
                domaine__semaine__programme=prog,
                statut='completed'
            ).exclude(domaine__categorie='spiritualite').count()
            if domaines_termines < 6:
                return prog
        return programmes.last() if programmes else None
    return Programme.objects.filter(statut='en_cours').first()''',
    content
)

# 2. Update get_semaine_en_cours definition
content = content.replace(
    'def get_semaine_en_cours(programme=None):',
    'def get_semaine_en_cours(programme=None, utilisateur=None):'
)
content = content.replace(
    'programme = get_programme_actuel()',
    'programme = get_programme_actuel(utilisateur)'
)

# 3. Update callers in views.py
content = content.replace(
    'programme_actuel = get_programme_actuel()\n    semaine_en_cours = get_semaine_en_cours(programme_actuel)',
    'programme_actuel = get_programme_actuel(request.user if request.user.is_authenticated else None)\n    semaine_en_cours = get_semaine_en_cours(programme_actuel, request.user if request.user.is_authenticated else None)'
)

content = content.replace(
    'semaine_en_cours = get_semaine_en_cours(programme)',
    'semaine_en_cours = get_semaine_en_cours(programme, request.user)'
)

content = content.replace(
    'semaine = get_semaine_en_cours()\n',
    'semaine = get_semaine_en_cours(utilisateur=request.user)\n'
)

# 4. Update programmes_list view
old_programmes_list = '''@login_required
def programmes_list(request):
    programme_actuel = Programme.objects.filter(statut='en_cours').first()
    programmes_a_venir = Programme.objects.filter(statut='a_venir').order_by('date_debut')
    programmes_precedents = Programme.objects.filter(statut='archive').order_by('-date_debut')
    
    # Calculate progress for current program
    if programme_actuel:
        domaines_termines = DomaineUtilisateur.objects.filter(
            utilisateur=request.user, 
            domaine__semaine__programme=programme_actuel,
            statut='completed'
        ).exclude(domaine__categorie='spiritualite').count()
        total_domaines = DomaineSemaine.objects.filter(semaine__programme=programme_actuel).count()
        programme_actuel.progression = domaines_termines
        programme_actuel.total = 6 # Fixé à 6 domaines obligatoires selon les règles métier
        programme_actuel.a_commence = domaines_termines > 0 or DomaineUtilisateur.objects.filter(utilisateur=request.user, domaine__semaine__programme=programme_actuel, statut='engaged').exists()

    # Calculate progress for archived programs
    for prog in programmes_precedents:
        domaines_termines = DomaineUtilisateur.objects.filter(
            utilisateur=request.user, 
            domaine__semaine__programme=prog,
            statut='completed'
        ).exclude(domaine__categorie='spiritualite').count()
        prog.progression = domaines_termines
        prog.total = 6
        prog.a_commence = domaines_termines > 0 or DomaineUtilisateur.objects.filter(utilisateur=request.user, domaine__semaine__programme=prog, statut='engaged').exists()

    return render(request, 'core/programmes_list.html', {
        'programme_actuel': programme_actuel,
        'programmes_a_venir': programmes_a_venir,
        'programmes_precedents': programmes_precedents,
    })'''

new_programmes_list = '''@login_required
def programmes_list(request):
    programmes = Programme.objects.all().order_by('ordre', 'date_debut')
    
    programme_actuel = None
    programmes_a_venir = []
    programmes_termines = []
    
    for prog in programmes:
        domaines_termines = DomaineUtilisateur.objects.filter(
            utilisateur=request.user, 
            domaine__semaine__programme=prog,
            statut='completed'
        ).exclude(domaine__categorie='spiritualite').count()
        
        prog.progression = domaines_termines
        prog.total = 6
        prog.a_commence = domaines_termines > 0 or DomaineUtilisateur.objects.filter(utilisateur=request.user, domaine__semaine__programme=prog, statut='engaged').exists()
        
        if domaines_termines >= 6:
            prog.statut_user = 'termine'
            programmes_termines.append(prog)
        elif not programme_actuel:
            prog.statut_user = 'en_cours'
            programme_actuel = prog
        else:
            prog.statut_user = 'a_venir'
            programmes_a_venir.append(prog)
            
    return render(request, 'core/programmes_list.html', {
        'programme_actuel': programme_actuel,
        'programmes_a_venir': programmes_a_venir,
        'programmes_termines': programmes_termines,
    })'''

content = content.replace(old_programmes_list, new_programmes_list)

with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("views.py updated successfully.")
