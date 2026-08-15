from django.conf import settings

def global_settings(request):
    return {
        'WHATSAPP_GROUP_LINK': getattr(settings, 'WHATSAPP_GROUP_LINK', 'https://chat.whatsapp.com/GdR1kJsTenpEwJYN8KgPt3'),
    }
