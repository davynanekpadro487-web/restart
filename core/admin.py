from django.contrib import admin
from .models import (
    Programme, Semaine, Defi, StatutDefi, EspacePersonnel, NoteEvolution,
    MessageInspirant, Profil, Action, ActionUtilisateur, PratiqueSpirituelle, PratiqueUtilisateur,
)

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'telephone', 'xp_total', 'theme_couleur')

class SemaineInline(admin.StackedInline):
    model = Semaine
    extra = 4

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('theme', 'statut', 'date_debut', 'date_fin')
    list_filter = ('statut',)
    inlines = [SemaineInline]

@admin.register(Semaine)
class SemaineAdmin(admin.ModelAdmin):
    list_display = ('programme', 'date_rendez_vous', 'theme')
    list_filter = ('programme', 'date_rendez_vous')

class ActionInline(admin.TabularInline):
    model = Action
    extra = 6

class PratiqueSpirituelleInline(admin.StackedInline):
    model = PratiqueSpirituelle
    extra = 1

@admin.register(Defi)
class DefiAdmin(admin.ModelAdmin):
    list_display = ('titre', 'semaine')
    inlines = [ActionInline, PratiqueSpirituelleInline]

@admin.register(StatutDefi)
class StatutDefiAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'defi', 'statut', 'xp_defi_accorde', 'xp_photo_accorde', 'mis_a_jour_le')
    list_filter = ('statut',)

@admin.register(ActionUtilisateur)
class ActionUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'action', 'terminee', 'xp_photo_accorde')
    list_filter = ('terminee',)

@admin.register(PratiqueUtilisateur)
class PratiqueUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'pratique', 'faite')
    list_filter = ('faite',)

class NoteEvolutionInline(admin.TabularInline):
    model = NoteEvolution
    extra = 1

@admin.register(EspacePersonnel)
class EspacePersonnelAdmin(admin.ModelAdmin):
    list_display = ('utilisateur',)
    inlines = [NoteEvolutionInline]

@admin.register(MessageInspirant)
class MessageInspirantAdmin(admin.ModelAdmin):
    list_display = ('texte', 'auteur', 'is_active')
    list_filter = ('is_active',)
