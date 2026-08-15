from django import template

register = template.Library()

@register.filter
def get_checked_items(etape):
    """
    Reçoit l'étape (dict) entière plutôt que etape.items — voir la note dans
    is_checklist ci-dessous sur l'ambiguïté de `etape.items` côté template.
    """
    if not isinstance(etape, dict):
        return []
    items = etape.get('items')
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict) and item.get('done', False)]

@register.filter
def is_checklist(etape):
    """
    Détecte si une étape doit être rendue comme une checklist dans le
    récapitulatif, de façon générique (utilisable pour n'importe quel défi,
    pas seulement le CV) :
    - soit le flag explicite is_checklist_etape est posé,
    - soit l'étape contient structurellement une vraie liste 'items'
      (utile pour des données enregistrées avant l'ajout du flag).

    Fait exprès de ne PAS utiliser `etape.items` côté template : en Django,
    quand la clé 'items' est absente d'un dict, le lookup retombe sur la
    méthode native dict.items() (qui renvoie des tuples clé/valeur), ce qui
    fait planter tout traitement en aval. Ce filtre lit `items` en Python
    pur via .get(), qui n'a pas cette ambiguïté.
    """
    if not isinstance(etape, dict):
        return False
    if etape.get('is_checklist_etape'):
        return True
    items = etape.get('items')
    return isinstance(items, list) and len(items) > 0
