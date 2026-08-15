import re

with open('core/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update get_programme_actuel
old_get_prog = '''def get_programme_actuel(utilisateur=None):
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
    return Programme.objects.filter(statut='en_cours').first()'''

new_get_prog = '''def get_programme_actuel(utilisateur=None):
    if utilisateur and utilisateur.is_authenticated:
        from django.utils import timezone
        aujourdhui = timezone.now().date()
        programmes = Programme.objects.all().order_by('ordre', 'date_debut')
        for prog in programmes:
            domaines_termines = DomaineUtilisateur.objects.filter(
                utilisateur=utilisateur, 
                domaine__semaine__programme=prog,
                statut='completed'
            ).exclude(domaine__categorie='spiritualite').count()
            if domaines_termines < 6:
                if prog.date_disponibilite and prog.date_disponibilite > aujourdhui:
                    return None
                return prog
        return programmes.last() if programmes else None
    return Programme.objects.filter(statut='en_cours').first()'''

content = content.replace(old_get_prog, new_get_prog)

# Update programmes_list
old_programmes_list = '''@login_required
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

new_programmes_list = '''@login_required
def programmes_list(request):
    programmes = Programme.objects.all().order_by('ordre', 'date_debut')
    
    programme_actuel = None
    programmes_a_venir = []
    programmes_termines = []
    
    found_first_incomplete = False
    from django.utils import timezone
    aujourdhui = timezone.now().date()
    
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
        elif not found_first_incomplete:
            found_first_incomplete = True
            if prog.date_disponibilite and prog.date_disponibilite > aujourdhui:
                prog.statut_user = 'a_venir'
                prog.is_next = True
                programmes_a_venir.append(prog)
            else:
                prog.statut_user = 'en_cours'
                programme_actuel = prog
        else:
            prog.statut_user = 'a_venir'
            prog.is_next = False
            programmes_a_venir.append(prog)
            
    return render(request, 'core/programmes_list.html', {
        'programme_actuel': programme_actuel,
        'programmes_a_venir': programmes_a_venir,
        'programmes_termines': programmes_termines,
    })'''

content = content.replace(old_programmes_list, new_programmes_list)

with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
