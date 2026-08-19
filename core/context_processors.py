from django.conf import settings

def global_settings(request):
    theme = 'bleu_or'
    if request.user.is_authenticated:
        try:
            theme = request.user.profil.theme_couleur
        except Exception:
            pass

    return {
        'WHATSAPP_GROUP_LINK': getattr(settings, 'WHATSAPP_GROUP_LINK', 'https://chat.whatsapp.com/GdR1kJsTenpEwJYN8KgPt3'),
        'user_theme': theme,
    }
