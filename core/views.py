from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils import timezone
from .models import (
    Programme, Semaine, Defi, StatutDefi, EspacePersonnel, NoteEvolution, MessageInspirant, Profil,
    Action, ActionUtilisateur, PratiqueSpirituelle, PratiqueUtilisateur, CATEGORIES_ACTION, THEMES_COULEUR,
    XP_DEFI_TERMINE, XP_BONUS_PREUVE, XP_ENGAGEMENT, DomaineSemaine, ActionProposee, DomaineUtilisateur,
    ActionBonusUtilisateur,
)
from .forms import InscriptionForm, PhotoProfilForm, InfosCompteForm
import random

def _ajouter_xp(utilisateur, montant):
    profil, _ = Profil.objects.get_or_create(utilisateur=utilisateur, defaults={'telephone': ''})
    profil.xp_total += montant
    profil.save()

ICONES_CATEGORIE = {
    'pro': 'briefcase',
    'argent': 'wallet',
    'objectifs': 'target',
    'moi': 'sparkles',
    'reseaux': 'smartphone',
    'amour': 'heart',
    'entourage': 'users',
}

def get_programme_actuel(utilisateur=None):
    # 1. Récupérer tous les programmes publiés triés par ordre
    programmes_publies = Programme.objects.filter(publie=True).order_by('ordre')
    
    if not programmes_publies.exists():
        # Fallback s'il n'y a aucun programme publié (peu probable en prod)
        return Programme.objects.order_by('ordre').first()
        
    if utilisateur and utilisateur.is_authenticated:
        for prog in programmes_publies:
            total_domaines = DomaineSemaine.objects.filter(semaine__programme=prog).exclude(categorie='spiritualite').count()
            prog_total = total_domaines if total_domaines > 0 else 6
            
            domaines_termines = DomaineUtilisateur.objects.filter(
                utilisateur=utilisateur, 
                domaine__semaine__programme=prog,
                statut='completed'
            ).exclude(domaine__categorie='spiritualite').count()
            
            if domaines_termines < prog_total:
                # C'est le premier programme publié que l'utilisateur n'a pas terminé
                return prog
                
        # Si tous les programmes publiés sont terminés, on renvoie le premier non publié
        # pour qu'il s'affiche en "Bientôt disponible", ou à défaut le dernier publié
        prochain_non_publie = Programme.objects.filter(publie=False).order_by('ordre').first()
        if prochain_non_publie:
            return prochain_non_publie
        return programmes_publies.last()
        
    # Utilisateur non connecté : on renvoie le premier programme publié
    return programmes_publies.first()

def enrich_programme(prog, user, programme_actuel=None):
    if not prog:
        return None
        
    total_domaines = DomaineSemaine.objects.filter(semaine__programme=prog).exclude(categorie='spiritualite').count()
    prog.total = total_domaines if total_domaines > 0 else 6
    
    if user and user.is_authenticated:
        domaines_termines = DomaineUtilisateur.objects.filter(
            utilisateur=user, 
            domaine__semaine__programme=prog,
            statut='completed'
        ).exclude(domaine__categorie='spiritualite').count()
        prog.progression = domaines_termines
        prog.a_commence = domaines_termines > 0 or DomaineUtilisateur.objects.filter(utilisateur=user, domaine__semaine__programme=prog, statut='engaged').exists()
    else:
        prog.progression = 0
        prog.a_commence = False

    prog.pourcentage = int((prog.progression / prog.total) * 100) if prog.total > 0 else 0
    
    # Harmonisation stricte des statuts
    if not prog.publie:
        prog.statut_user = 'a_venir'
        prog.button_text = 'Bientôt disponible'
    elif prog.progression >= prog.total and prog.total > 0 and prog.a_commence:
        prog.statut_user = 'termine'
        prog.button_text = 'Voir mes réalisations'
    else:
        # C'est un programme publié et non terminé
        # S'il ne s'agit pas du programme actif, c'est qu'il est bloqué (soit l'utilisateur n'a pas fini le précédent)
        if programme_actuel and prog.id != programme_actuel.id:
            prog.statut_user = 'a_venir'
            prog.button_text = 'Bientôt disponible'
        else:
            prog.statut_user = 'en_cours'
            if prog.progression == 0:
                prog.button_text = 'Commencer le programme'
            else:
                prog.button_text = 'Continuer le programme'
            
    return prog

def get_semaine_en_cours(programme=None, utilisateur=None):
    if not programme:
        programme = get_programme_actuel(utilisateur)
    if not programme:
        return None
        
    semaines = Semaine.objects.filter(programme=programme).order_by('date_rendez_vous', 'id')
    for semaine in semaines:
        if utilisateur and utilisateur.is_authenticated:
            stats = get_semaine_stats(semaine, utilisateur)
            if not stats['terminee']:
                return semaine
        else:
            return semaine
            
    return semaines.last()

def get_semaine_stats(semaine, utilisateur):
    if not semaine or not utilisateur.is_authenticated:
        return {'score': 0, 'xp_semaine': 0, 'terminee': False, 'statut_global': None}
    
    score = DomaineUtilisateur.objects.filter(
        utilisateur=utilisateur, 
        domaine__semaine=semaine, 
        statut='completed'
    ).exclude(domaine__categorie='spiritualite').count()
    
    xp_domaines = sum([du.xp_gagnes for du in DomaineUtilisateur.objects.filter(utilisateur=utilisateur, domaine__semaine=semaine)])
    xp_bonus = sum([ab.xp_gagnes for ab in ActionBonusUtilisateur.objects.filter(utilisateur=utilisateur, domaine__semaine=semaine)])
    
    xp_semaine = xp_domaines + xp_bonus
    
    statut_global = None
    if hasattr(semaine, 'defi'):
        statut_global, _ = StatutDefi.objects.get_or_create(utilisateur=utilisateur, defi=semaine.defi)
        # Note: XP_DEFI_TERMINE (50) could be added here if we strictly tie it to statut_global='completed'.
        # However, the 50 XP is added to profil directly. We'll add 50 to visual total if it's completed.
        if statut_global.statut == 'completed':
            xp_semaine += 50
            
    return {
        'score': score,
        'xp_semaine': xp_semaine,
        'terminee': score >= 6,
        'statut_global': statut_global
    }

def home(request):
    aujourdhui = timezone.now().date()
    programme_actuel = get_programme_actuel(request.user if request.user.is_authenticated else None)
    semaine_en_cours = get_semaine_en_cours(programme_actuel, request.user if request.user.is_authenticated else None)
    
    prochain_rdv = Semaine.objects.filter(date_rendez_vous__gt=aujourdhui).order_by('date_rendez_vous').first()
        
    programme_termine = False
    dernier_programme_complete = None
    prochain_programme = None
    if request.user.is_authenticated:
        stats = get_semaine_stats(semaine_en_cours, request.user)
        score_semaine = stats['score']
        semaine_terminee = stats['terminee']
            
        # Stats de progression (Goalmap style) - pour l'instant global
        defis_termines = DomaineUtilisateur.objects.filter(utilisateur=request.user, statut='completed').exclude(domaine__categorie='spiritualite').count()
        total_defis = DomaineSemaine.objects.exclude(categorie='spiritualite').count()
        pourcentage = int((defis_termines / total_defis) * 100) if total_defis > 0 else 0
        membres_actifs = User.objects.filter(is_active=True).count()
        
        if programme_actuel:
            programme_actuel = enrich_programme(programme_actuel, request.user, programme_actuel=programme_actuel)
        
        if pourcentage >= 100 and programme_actuel:
            programme_termine = True
            dernier_programme_complete = programme_actuel
            prochain_programme = Programme.objects.filter(statut='a_venir').order_by('date_debut').first()
        elif not programme_actuel:
            dernier_programme_complete = Programme.objects.filter(statut='archive').order_by('-date_debut').first()
            if dernier_programme_complete:
                programme_termine = True
            prochain_programme = Programme.objects.filter(statut='a_venir').order_by('date_debut').first()
            
        return render(request, 'core/dashboard.html', {
            'programme_actuel': programme_actuel,
            'semaine_en_cours': semaine_en_cours,
            'prochain_rdv': prochain_rdv,
            'score_semaine': score_semaine,
            'semaine_terminee': semaine_terminee,
            'defis_termines': defis_termines,
            'total_defis': total_defis,
            'pourcentage': pourcentage,
            'programme_termine': programme_termine,
            'dernier_programme_complete': dernier_programme_complete,
            'prochain_programme': prochain_programme,
            'membres_actifs': membres_actifs,
        })
    else:
        citations = MessageInspirant.objects.filter(is_active=True)
        citation = random.choice(citations) if citations.exists() else None

        return render(request, 'core/home.html', {
            'citation': citation,
            'programme_actuel': programme_actuel,
            'semaine_en_cours': semaine_en_cours,
            'prochain_rdv': prochain_rdv,
        })

def register(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie ! Bienvenue sur Restart.')
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def programmes_list(request):
    programmes = Programme.objects.all().order_by('ordre', 'date_debut')
    
    programmes_en_cours = []
    programmes_a_venir = []
    programmes_termines = []
    
    programme_actif = get_programme_actuel(request.user)
    
    for prog in programmes:
        prog = enrich_programme(prog, request.user, programme_actuel=programme_actif)
        
        if prog.statut_user == 'termine':
            programmes_termines.append(prog)
        elif prog.statut_user == 'a_venir':
            prog.is_next = (len(programmes_a_venir) == 0)
            programmes_a_venir.append(prog)
        else:
            # S'il n'est ni terminé ni à venir, c'est obligatoirement le programme "en_cours" (actif)
            programmes_en_cours.append(prog)
                
    return render(request, 'core/programmes_list.html', {
        'programmes_en_cours': programmes_en_cours,
        'programmes_a_venir': programmes_a_venir,
        'programmes_termines': programmes_termines,
    })

@login_required
def programme_detail(request, programme_id):
    programme = get_object_or_404(Programme, id=programme_id)
    semaines = programme.semaines.all().order_by('date_rendez_vous')
    
    semaine_en_cours = get_semaine_en_cours(programme, request.user)
    aujourdhui = timezone.now().date()
    
    for sem in semaines:
        stats = get_semaine_stats(sem, request.user)
        sem.score_semaine = stats['score']
        sem.terminee = stats['terminee']
        
        if stats['terminee']:
            sem.status_badge = 'termine'
        elif stats['score'] > 0:
            sem.status_badge = 'en_cours'
        elif semaine_en_cours and sem.id == semaine_en_cours.id:
            sem.status_badge = 'en_cours'
        elif sem.date_rendez_vous and sem.date_rendez_vous < aujourdhui:
            sem.status_badge = 'passe'
        else:
            sem.status_badge = 'a_venir'

    return render(request, 'core/programme_detail.html', {
        'programme': programme,
        'semaines': semaines,
    })

@login_required
def defi_redirect_actuel(request):
    semaine = get_semaine_en_cours(utilisateur=request.user)
    if semaine:
        return redirect('defi_semaine', semaine_id=semaine.id)
    return render(request, 'core/defi_vide.html')

@login_required
def defi_redirect_programme(request, programme_id):
    programme = get_object_or_404(Programme, id=programme_id)
    semaine = get_semaine_en_cours(programme)
    if semaine:
        return redirect('defi_semaine', semaine_id=semaine.id)
    return render(request, 'core/defi_vide.html')

@login_required
def get_categories_data(request, semaine):
    categories_data = []
    score_semaine = 0
    spiritualite_terminee = False
    
    if not semaine:
        return categories_data, score_semaine, spiritualite_terminee
        
    domaines_disponibles = DomaineSemaine.objects.filter(semaine=semaine)
    choix_user = DomaineUtilisateur.objects.filter(utilisateur=request.user, domaine__semaine=semaine)
    choix_dict = {c.domaine_id: c for c in choix_user}
    
    bonus_user = ActionBonusUtilisateur.objects.filter(
        utilisateur=request.user, 
        domaine__semaine=semaine, 
        statut='completed'
    ).select_related('action_choisie')
    
    bonus_dict = {}
    for b in bonus_user:
        if b.domaine_id not in bonus_dict:
            bonus_dict[b.domaine_id] = []
        bonus_dict[b.domaine_id].append(b)
    
    domaines_par_cat = {code: None for code, _ in CATEGORIES_ACTION}
        
    for d in domaines_disponibles:
        etat = choix_dict.get(d.id)
        d.etat_utilisateur = etat
        domaines_par_cat[d.categorie] = d
        
    for code, label in CATEGORIES_ACTION:
        d = domaines_par_cat[code]
        if d:
            cat_terminee = d.etat_utilisateur and d.etat_utilisateur.statut == 'completed'
            cat_engagee = d.etat_utilisateur and d.etat_utilisateur.statut == 'engaged'
            
            if cat_terminee:
                if code == 'spiritualite':
                    spiritualite_terminee = True
                else:
                    score_semaine += 1
                
            categories_data.append({
                'code': code,
                'label': label,
                'icone': ICONES_CATEGORIE.get(code, 'circle'),
                'domaine': d,
                'terminee': cat_terminee,
                'engagee': cat_engagee,
                'optionnel': code == 'spiritualite',
                'bonus_termines': bonus_dict.get(d.id, []),
                'bonus_count': len(bonus_dict.get(d.id, [])),
            })
            
    return categories_data, score_semaine, spiritualite_terminee

@login_required
def defi_semaine(request, semaine_id):
    semaine = get_object_or_404(Semaine, id=semaine_id)
    defi = semaine.defi if semaine and hasattr(semaine, 'defi') else None
    
    # Déterminer si on consulte le programme actuellement en cours
    semaine_en_cours = get_semaine_en_cours(utilisateur=request.user)
    is_active_week = (semaine_en_cours and semaine.id == semaine_en_cours.id)
    
    statut_global = None
    if defi:
        statut_global, _ = StatutDefi.objects.get_or_create(utilisateur=request.user, defi=defi)

    categories_data, score_semaine, spiritualite_terminee = get_categories_data(request, semaine)
    total_categories = 6 # Les 6 domaines obligatoires
    
    just_completed_week = False
    if score_semaine >= total_categories and statut_global:
        if statut_global.statut != 'completed':
            statut_global.statut = 'completed'
            statut_global.save()
            _ajouter_xp(request.user, 50)
            messages.success(request, 'Incroyable ! Tu as terminé tous les domaines essentiels. +50 XP bonus !')
            just_completed_week = True
            
            # Génération automatique du bilan immédiate
            espace, _ = EspacePersonnel.objects.get_or_create(utilisateur=request.user)
            date_str = semaine.date_rendez_vous.strftime('%d/%m/%Y') if semaine.date_rendez_vous else timezone.now().strftime('%d/%m/%Y')
            titre_bilan = f"Semaine du {date_str} - Bilan"
            bilan_existe = espace.notes.filter(type_note='bilan', texte__startswith=titre_bilan).exists()
            if not bilan_existe:
                bilan_texte = f"{titre_bilan}\n\nCe que j'ai accompli cette semaine :\n\nCe dont je suis fière :\n\nMon prochain objectif :"
                NoteEvolution.objects.create(espace_personnel=espace, texte=bilan_texte, type_note='bilan')

    # Redirection vers la page "Semaine Complète" si terminé
    if score_semaine >= total_categories:
        if just_completed_week:
            return redirect(f"/defi/semaine-complete/{semaine.id}/?celebration=true")
        return redirect('semaine_complete', semaine_id=semaine.id)

    prog_count = score_semaine + (1 if spiritualite_terminee else 0)
    prog_max = 7
    if score_semaine >= total_categories and not spiritualite_terminee:
        prog_max = 6
        
    prog_percent = int((prog_count / prog_max) * 100) if prog_max > 0 else 0

    premier_domaine_non_termine_id = None
    for cat in categories_data:
        if not cat['terminee']:
            premier_domaine_non_termine_id = cat['domaine'].id
            break

    return render(request, 'core/defi.html', {
        'semaine': semaine,
        'defi': defi,
        'categories_data': categories_data,
        'score_semaine': score_semaine,
        'total_categories': total_categories,
        'semaine_terminee': score_semaine >= total_categories,
        'spiritualite_terminee': spiritualite_terminee,
        'show_celebration': request.GET.get('celebration') == 'true' or just_completed_week,
        'prog_count': prog_count,
        'prog_max': prog_max,
        'prog_percent': prog_percent,
        'premier_domaine_non_termine_id': premier_domaine_non_termine_id,
        'is_active_week': is_active_week,
    })

@login_required
def defis_historique(request):
    programmes_termines_historique = []
    toutes_semaines = Semaine.objects.select_related('programme')
    for sem in toutes_semaines:
        domaines_termines_count = DomaineUtilisateur.objects.filter(
            utilisateur=request.user, 
            domaine__semaine=sem,
            statut='completed'
        ).exclude(domaine__categorie='spiritualite').count()
        if domaines_termines_count >= 6:
            programmes_termines_historique.append(sem)
            
    return render(request, 'core/defis_historique.html', {
        'programmes_termines_historique': programmes_termines_historique,
    })

@login_required
def commencer_bonus(request, domaine_id, action_id):
    domaine = get_object_or_404(DomaineSemaine, id=domaine_id)
    action = get_object_or_404(ActionProposee, id=action_id, domaine=domaine)
    
    bonus, created = ActionBonusUtilisateur.objects.get_or_create(
        utilisateur=request.user,
        domaine=domaine,
        action_choisie=action
    )
    
    # Point 4 : si le bonus est déjà validé, afficher directement son résumé sans réinitialiser
    if bonus.statut == 'completed':
        return redirect(f'/defi/{domaine_id}/domaine/?bonus_id={bonus.id}')
    
    # Initialize the action data like in choisir_action
    if created or not bonus.donnees_action:
        from .utils import get_initial_action_data
        texte = action.texte
        bonus.donnees_action = get_initial_action_data(domaine.categorie, texte, is_bonus=True)
        bonus.save()
        
    return redirect(f'/defi/{domaine_id}/domaine/?bonus_id={bonus.id}')

@login_required
def domaine_detail(request, domaine_id):
    domaine = get_object_or_404(DomaineSemaine, id=domaine_id)
    actions_proposees = list(domaine.actions.all())
    
    bonus_utilisateurs = ActionBonusUtilisateur.objects.filter(utilisateur=request.user, domaine=domaine)
    bonus_dict = {b.action_choisie_id: b for b in bonus_utilisateurs}
    for action in actions_proposees:
        action.bonus_user = bonus_dict.get(action.id)
    
    bonus_id = request.GET.get('bonus_id') or request.POST.get('bonus_id')
    is_bonus = False
    
    if bonus_id:
        domaine_user = get_object_or_404(ActionBonusUtilisateur, id=bonus_id, utilisateur=request.user)
        is_bonus = True
    else:
        domaine_user, created = DomaineUtilisateur.objects.get_or_create(utilisateur=request.user, domaine=domaine)
    
    if request.method == 'POST':
        action_post = request.POST.get('action_type')
        
        if action_post == 'choisir_action':
            action_id = request.POST.get('action_id')
            if action_id:
                action_choisie = get_object_or_404(ActionProposee, id=action_id, domaine=domaine)
                domaine_user.action_choisie = action_choisie
                domaine_user.statut = 'engaged'
                
                # INITIALISATION DES COMPOSANTS
                texte = action_choisie.texte
                from .utils import get_initial_action_data
                
                initial_data = get_initial_action_data(domaine.categorie, texte, is_bonus=False)
                if initial_data:
                    domaine_user.donnees_action = initial_data
                
                domaine_user.save()
                return redirect('domaine_detail', domaine_id=domaine.id)
                
        elif action_post == 'etape_1_argent':
            # Point 2+3 : Sauvegarder la liste des dépenses avec le tag utile/nécessaire
            depenses = request.POST.getlist('depense[]')
            montants = request.POST.getlist('montant[]')
            utilites = request.POST.getlist('utilite[]')
            
            data = {'depenses': []}
            for i, (d, m) in enumerate(zip(depenses, montants)):
                if d.strip():
                    utilite = utilites[i] if i < len(utilites) else 'utile'
                    data['depenses'].append({'nom': d.strip(), 'montant': m.strip(), 'utile': utilite})
                    
            domaine_user.donnees_action = data
            domaine_user.save()
            # On passe à l'étape 2 — affichage du total
            if is_bonus:
                return redirect(f"{request.path}?etape=2&bonus_id={bonus_id}")
            return redirect(f"{request.path}?etape=2")
            
        elif action_post == 'etape_2_argent':
            # Point 3 : étape 2 = affichage du total, pas de sélection — simple passage à l'étape 3
            if is_bonus:
                return redirect(f"{request.path}?etape=3&bonus_id={bonus_id}")
            return redirect(f"{request.path}?etape=3")
            
        elif action_post == 'etape_3_argent':
            # Point 3 : Enregistrer la réponse 'où aurais-tu mis cet argent' et valider
            reponse_engagement = request.POST.get('reponse_engagement', '')
            data = domaine_user.donnees_action or {}
            data['reponse_engagement'] = reponse_engagement
                        
            xp_to_add = 10 if is_bonus else XP_DEFI_TERMINE
            domaine_user.donnees_action = data
            domaine_user.statut = 'completed'
            domaine_user.xp_gagnes += xp_to_add
            _ajouter_xp(request.user, xp_to_add)
            domaine_user.save()
            
            msg = 'Action bonus réalisée ! +10 XP' if is_bonus else 'Défi réalisé ! +20 XP'
            messages.success(request, msg)
            if is_bonus:
                return redirect(f"{request.path}?bonus_id={bonus_id}")
            return redirect(f"{request.path}")
            
        elif action_post == 'update_checklist_etape':
            step_index = request.POST.get('step_index')
            item_index = request.POST.get('index')
            is_checked = request.POST.get('is_checked') == 'true'
            
            data = domaine_user.donnees_action or {}
            if 'etapes' in data and step_index is not None and item_index is not None:
                s_idx = int(step_index)
                i_idx = int(item_index)
                if 0 <= s_idx < len(data['etapes']) and 'items' in data['etapes'][s_idx]:
                    if 0 <= i_idx < len(data['etapes'][s_idx]['items']):
                        data['etapes'][s_idx]['items'][i_idx]['done'] = is_checked
                        domaine_user.donnees_action = data
                        domaine_user.save()
                        
                        # Calculer all_done et any_done pour l'étape actuelle
                        etape_items = data['etapes'][s_idx].get('items', [])
                        all_done = all(item.get('done', False) for item in etape_items) if etape_items else False
                        any_done = any(item.get('done', False) for item in etape_items) if etape_items else False
                        
                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            return JsonResponse({'status': 'success', 'all_done': all_done, 'any_done': any_done})
                        return redirect(f"{request.path}?bonus_id={bonus_id}" if is_bonus else f"{request.path}")

        elif action_post == 'update_checklist':
            index = request.POST.get('index')
            is_checked = request.POST.get('is_checked') == 'true'
            
            data = domaine_user.donnees_action or {}
            if 'etapes' in data and index is not None:
                idx = int(index)
                if 0 <= idx < len(data['etapes']):
                    data['etapes'][idx]['done'] = is_checked
                    domaine_user.donnees_action = data
                    
                    # Vérifier si tout est coché
                    all_done = all(etape.get('done', False) for etape in data['etapes'])
                    domaine_user.save()
                    
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'status': 'success', 'all_done': all_done})
                        
                    return redirect(f"{request.path}?bonus_id={bonus_id}" if is_bonus else f"{request.path}")
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
                
            return redirect(f"{request.path}?bonus_id={bonus_id}" if is_bonus else f"{request.path}")
            
        elif action_post == 'next_question':
            data = domaine_user.donnees_action or {}
            if 'etapes' in data and 'etape_courante' in data:
                idx = data['etape_courante']
                if 0 <= idx < len(data['etapes']):
                    # Enregistrer la réponse texte, uniquement pour les étapes qui en
                    # attendent une (reponse initialement "" et non None). Les étapes
                    # checklist et les étapes de confirmation (reponse initiale = None,
                    # ou clé absente) n'ont pas de champ texte dans le formulaire : on ne
                    # doit pas écraser leur valeur avec une chaîne vide, sinon le
                    # récapitulatif ne peut plus les distinguer d'une vraie non-réponse.
                    if data['etapes'][idx].get('reponse') is not None:
                        data['etapes'][idx]['reponse'] = request.POST.get('reponse', '')

                    # Passer à l'étape suivante
                    next_idx = idx + 1
                    
                    if next_idx < len(data['etapes']):
                        data['etape_courante'] = next_idx
                        domaine_user.donnees_action = data
                        domaine_user.save()
                        return redirect(f"{request.path}?bonus_id={bonus_id}" if is_bonus else f"{request.path}")
                    else:
                        # Toutes les étapes sont terminées
                        xp_to_add = 10 if is_bonus else XP_DEFI_TERMINE
                        data['etape_courante'] = next_idx
                        domaine_user.donnees_action = data
                        domaine_user.statut = 'completed'
                        domaine_user.xp_gagnes += xp_to_add
                        _ajouter_xp(request.user, xp_to_add)
                        domaine_user.save()
                        msg = 'Action bonus réalisée ! +10 XP' if is_bonus else 'Défi réalisé ! +20 XP'
                        messages.success(request, msg)
                        return redirect(f"{request.path}?etape=validation&bonus_id={bonus_id}" if is_bonus else f"{request.path}?etape=validation")
                        
            return redirect(f"{request.path}?bonus_id={bonus_id}" if is_bonus else f"{request.path}")

        elif action_post == 'validation_generique':
            xp_to_add = 10 if is_bonus else XP_DEFI_TERMINE
            domaine_user.statut = 'completed'
            domaine_user.xp_gagnes += xp_to_add
            _ajouter_xp(request.user, xp_to_add)
            domaine_user.save()
            
            msg = 'Action bonus réalisée ! +10 XP' if is_bonus else 'Défi réalisé ! +20 XP'
            messages.success(request, msg)
            return redirect(f"{request.path}?etape=validation&bonus_id={bonus_id}" if is_bonus else f"{request.path}?etape=validation")
            
        elif action_post == 'ajouter_preuve':
            fichier = request.FILES.get('preuve_fichier')
            texte = request.POST.get('preuve_texte')
            
            deja_prouve = bool(domaine_user.preuve_fichier or domaine_user.preuve_texte)
            
            if fichier:
                domaine_user.preuve_fichier = fichier
            if texte:
                domaine_user.preuve_texte = texte
                
            if (fichier or texte) and not deja_prouve:
                # On ajoute les XP bonus pour la preuve car c'est le premier ajout
                _ajouter_xp(request.user, XP_BONUS_PREUVE)
                domaine_user.xp_gagnes += XP_BONUS_PREUVE
                
            domaine_user.save()
            messages.success(request, 'Preuve ajoutée avec succès ! +10 XP')
            
            # Si on est déjà "completed", on regarde si le domaine est validé et qu'on a atteint 6/6
            stats = get_semaine_stats(domaine.semaine, request.user)
            if stats['terminee']:
                return redirect('semaine_complete', semaine_id=domaine.semaine.id)
            return redirect('defi_semaine', semaine_id=domaine.semaine.id)

    etape = request.GET.get('etape', '1')
    
    checklist_all_done = False
    checklist_stats = {'total': 0, 'cochees': 0}
    if domaine_user.donnees_action and domaine_user.donnees_action.get('type') == 'checklist':
        etapes = domaine_user.donnees_action.get('etapes', [])
        checklist_all_done = len(etapes) > 0 and all(e.get('done', False) for e in etapes)
        checklist_stats['total'] = len(etapes)
        checklist_stats['cochees'] = sum(1 for e in etapes if e.get('done', False))
        
    next_bonus = None
    if is_bonus or domaine_user.statut == 'completed':
        actions_faites_ids = list(ActionBonusUtilisateur.objects.filter(
            utilisateur=request.user, domaine=domaine, statut='completed'
        ).values_list('action_choisie_id', flat=True))
        
        main_user = DomaineUtilisateur.objects.filter(utilisateur=request.user, domaine=domaine).first()
        if main_user and main_user.action_choisie:
            actions_faites_ids.append(main_user.action_choisie.id)
            
        for action in actions_proposees:
            if action.id not in actions_faites_ids and (is_bonus or action.id != getattr(main_user.action_choisie, 'id', None)):
                next_bonus = action
                break
    
    # Calcul des totaux pour le flux "Suivre ses dépenses sans culpabilité"
    total_depenses = 0
    total_regrets = 0
    if domaine_user.donnees_action and domaine_user.donnees_action.get('depenses'):
        for dep in domaine_user.donnees_action['depenses']:
            try:
                montant = float(str(dep.get('montant', 0)).replace(' ', '').replace(',', '.') or 0)
            except (ValueError, TypeError):
                montant = 0
            total_depenses += montant
            if dep.get('utile') == 'pas_necessaire':
                total_regrets += montant
        # Format avec séparateur de milliers
        total_depenses = f"{int(total_depenses):,}".replace(',', ' ')
        total_regrets = f"{int(total_regrets):,}".replace(',', ' ')

    return render(request, 'core/domaine_detail.html', {
        'domaine': domaine,
        'domaine_user': domaine_user,
        'actions_proposees': actions_proposees,
        'etape': etape,
        'xp_defi_termine': 10 if is_bonus else XP_DEFI_TERMINE,
        'xp_bonus_preuve': XP_BONUS_PREUVE,
        'is_bonus': is_bonus,
        'bonus_id': bonus_id,
        'checklist_all_done': checklist_all_done,
        'checklist_stats': checklist_stats,
        'next_bonus': next_bonus,
        'total_depenses': total_depenses,
        'total_regrets': total_regrets,
    })


@login_required
def journal(request):
    espace, created = EspacePersonnel.objects.get_or_create(utilisateur=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_note':
            texte = request.POST.get('note_texte')
            type_note = request.POST.get('type_note', 'libre')
            if texte:
                NoteEvolution.objects.create(espace_personnel=espace, texte=texte, type_note=type_note)
                messages.success(request, 'Note ajoutée !')
        return redirect('journal')

    filtre = request.GET.get('filtre', 'toutes')
    if filtre == 'libre':
        notes = espace.notes.filter(type_note='libre')
    elif filtre == 'defi':
        notes = espace.notes.exclude(type_note='libre')
    else:
        notes = espace.notes.all()
        
    prefill_text = request.GET.get('prefill_text', '')
    prefill_type = request.GET.get('prefill_type', 'libre')

    return render(request, 'core/journal.html', {
        'espace': espace,
        'notes': notes,
        'filtre': filtre,
        'prefill_text': prefill_text,
        'prefill_type': prefill_type,
    })

@login_required
def progression(request):
    programme_actuel = get_programme_actuel(request.user if request.user.is_authenticated else None)
    semaine_en_cours = get_semaine_en_cours(programme_actuel, request.user if request.user.is_authenticated else None)
    stats_cours = get_semaine_stats(semaine_en_cours, request.user) if semaine_en_cours else {'score': 0, 'xp_semaine': 0}
    
    # Nombre de défis débutés et terminés au niveau global
    defis_termines = DomaineUtilisateur.objects.filter(utilisateur=request.user, statut='completed').exclude(domaine__categorie='spiritualite').count()
    defis_debutes = DomaineUtilisateur.objects.filter(utilisateur=request.user, statut='started').exclude(domaine__categorie='spiritualite').count()
    total_defis = DomaineSemaine.objects.exclude(categorie='spiritualite').count()
    pourcentage = int((defis_termines / total_defis) * 100) if total_defis > 0 else 0
    
    # Historique des programmes commencés
    programmes = Programme.objects.all().order_by('ordre', 'date_debut')
    programmes_historique = []
    
    for prog in programmes:
        domaines_termines = DomaineUtilisateur.objects.filter(
            utilisateur=request.user, 
            domaine__semaine__programme=prog,
            statut='completed'
        ).exclude(domaine__categorie='spiritualite').count()
        
        a_commence = domaines_termines > 0 or DomaineUtilisateur.objects.filter(utilisateur=request.user, domaine__semaine__programme=prog, statut='engaged').exists()
        
        if a_commence:
            prog.progression = domaines_termines
            prog.total = 6
            prog.xp_total = sum([du.xp_gagnes for du in DomaineUtilisateur.objects.filter(utilisateur=request.user, domaine__semaine__programme=prog)])
            prog.xp_total += sum([ab.xp_gagnes for ab in ActionBonusUtilisateur.objects.filter(utilisateur=request.user, domaine__semaine__programme=prog)])
            
            # Add completion bonus if 6/6 is reached in at least one week? For now just use the basic logic.
            programmes_historique.append(prog)
            
    # Dernier défi validé
    dernier_defi = DomaineUtilisateur.objects.filter(utilisateur=request.user, statut='completed').order_by('-mis_a_jour_le').first()
    
    try:
        dernieres_notes = request.user.espace_personnel.notes.all()[:3]
    except EspacePersonnel.DoesNotExist:
        dernieres_notes = []

    return render(request, 'core/progression.html', {
        'programme_actuel': programme_actuel,
        'stats_cours': stats_cours,
        'defis_termines': defis_termines,
        'defis_debutes': defis_debutes,
        'total_defis': total_defis,
        'pourcentage': pourcentage,
        'programmes_historique': programmes_historique,
        'dernier_defi': dernier_defi,
        'dernieres_notes': dernieres_notes
    })

@login_required
def semaine_complete(request, semaine_id):
    semaine = get_object_or_404(Semaine, id=semaine_id)
    stats = get_semaine_stats(semaine, request.user)
    
    if not stats['terminee']:
        return redirect('defi_semaine', semaine_id=semaine.id)
        
    # Génération automatique du bilan si non existant
    espace, _ = EspacePersonnel.objects.get_or_create(utilisateur=request.user)
    date_str = semaine.date_rendez_vous.strftime('%d/%m/%Y') if semaine.date_rendez_vous else timezone.now().strftime('%d/%m/%Y')
    titre_bilan = f"Semaine du {date_str} - Bilan"
    bilan_existe = espace.notes.filter(type_note='bilan', texte__startswith=titre_bilan).exists()
    
    if not bilan_existe:
        bilan_texte = f"{titre_bilan}\n\nCe que j'ai accompli cette semaine :\n\nCe dont je suis fière :\n\nMon prochain objectif :"
        NoteEvolution.objects.create(
            espace_personnel=espace,
            texte=bilan_texte,
            type_note='bilan'
        )
        
    # Get categories_data directly to reuse the domain cards template
    categories_data, score_semaine, spiritualite_terminee = get_categories_data(request, semaine)
    
    return render(request, 'core/semaine_complete.html', {
        'semaine': semaine,
        'stats': stats,
        'categories_data': categories_data,
        'score_semaine': score_semaine,
        'show_celebration': request.GET.get('celebration') == 'true',
    })

def communaute(request):
    citations = MessageInspirant.objects.filter(is_active=True)
    return render(request, 'core/communaute.html', {'citations': citations})

@login_required
def profil(request):
    profil_utilisateur, created = Profil.objects.get_or_create(
        utilisateur=request.user, defaults={'telephone': ''}
    )

    espace, created = EspacePersonnel.objects.get_or_create(utilisateur=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_espace':
            espace.objectifs = request.POST.get('objectifs', espace.objectifs)
            espace.vision = request.POST.get('vision', espace.vision)
            espace.qualites = request.POST.get('qualites', espace.qualites)
            espace.save()
            messages.success(request, 'Boussole mise à jour !')
            return redirect('profil')
        elif 'photo_profil' in request.FILES:
            form_photo = PhotoProfilForm(request.POST, request.FILES, instance=profil_utilisateur)
            if form_photo.is_valid():
                form_photo.save()
                messages.success(request, 'Photo de profil mise à jour !')
            return redirect('profil')

    defis_termines = DomaineUtilisateur.objects.filter(utilisateur=request.user, statut='completed').count()

    return render(request, 'core/profil.html', {
        'profil': profil_utilisateur,
        'defis_termines': defis_termines,
        'espace': espace,
    })

@login_required
def parametres(request):
    profil_utilisateur, created = Profil.objects.get_or_create(
        utilisateur=request.user, defaults={'telephone': ''}
    )

    infos_form = InfosCompteForm(
        user=request.user,
        initial={'username': request.user.username, 'telephone': profil_utilisateur.telephone},
    )
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_infos':
            infos_form = InfosCompteForm(request.POST, user=request.user)
            if infos_form.is_valid():
                request.user.username = infos_form.cleaned_data['username']
                request.user.save()
                profil_utilisateur.telephone = infos_form.cleaned_data['telephone']
                profil_utilisateur.save()
                messages.success(request, 'Tes informations ont été mises à jour !')
                return redirect('parametres')

        elif action == 'change_password':
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mot de passe modifié avec succès !')
                return redirect('parametres')

        elif action == 'update_theme':
            theme_choisi = request.POST.get('theme_couleur')
            if theme_choisi in dict(THEMES_COULEUR):
                profil_utilisateur.theme_couleur = theme_choisi
                profil_utilisateur.save()
                messages.success(request, 'Thème mis à jour !')
            return redirect('parametres')

        elif action == 'delete_account':
            request.user.delete()
            logout(request)
            messages.success(request, 'Ton compte a été supprimé.')
            return redirect('home')

    return render(request, 'core/parametres.html', {
        'infos_form': infos_form,
        'password_form': password_form,
        'profil': profil_utilisateur,
        'themes_couleur': THEMES_COULEUR,
    })
