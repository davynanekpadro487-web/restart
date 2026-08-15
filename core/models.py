from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

THEMES_COULEUR = [
    ('bleu_or', 'Bleu & Or'),
    ('violet_or', 'Violet & Or'),
    ('sombre', 'Sombre'),
]

class Profil(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True, verbose_name="Photo de profil")
    xp_total = models.PositiveIntegerField(default=0, verbose_name="XP")
    theme_couleur = models.CharField(max_length=20, choices=THEMES_COULEUR, default='bleu_or', verbose_name="Thème de couleurs")

    def __str__(self):
        return f"Profil de {self.utilisateur.username}"

class Programme(models.Model):
    STATUT_CHOICES = [
        ('a_venir', 'À venir'),
        ('en_cours', 'En cours'),
        ('archive', 'Précédent / Archive'),
    ]
    theme = models.CharField(max_length=200, verbose_name="Thème principal")
    description = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='a_venir')
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre de parcours")
    publie = models.BooleanField(default=False, verbose_name="Publié")
    illustration = models.ImageField(upload_to='programmes_illus/', blank=True, null=True, verbose_name="Illustration (PNG/JPG)")
    date_disponibilite = models.DateField(null=True, blank=True, verbose_name="Date de disponibilité")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date de début")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date de fin")

    def __str__(self):
        return f"{self.ordre} - {self.theme} ({self.get_statut_display()})"

    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"

class Semaine(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name="semaines")
    ordre = models.PositiveIntegerField(verbose_name="Semaine N°")
    date_rendez_vous = models.DateField(verbose_name="Date du mercredi", default=timezone.now)
    theme = models.CharField(max_length=200, verbose_name="Thème de la semaine")
    objectif = models.CharField(max_length=255)
    questions = models.TextField(verbose_name="Questions de réflexion (une par ligne)", help_text="Séparez les questions par un saut de ligne.")

    def __str__(self):
        return f"Semaine du {self.date_rendez_vous.strftime('%d/%m/%Y')} - {self.theme}"

    class Meta:
        ordering = ['date_rendez_vous']

    def get_questions_list(self):
        return [q.strip() for q in self.questions.split('\n') if q.strip()]

class Defi(models.Model):
    semaine = models.OneToOneField(Semaine, on_delete=models.CASCADE, related_name="defi")
    titre = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.titre

XP_ENGAGEMENT = 5
XP_ACTION_COMMENCEE = 5
XP_DEFI_TERMINE = 20
XP_BONUS_PREUVE = 10

class StatutDefi(models.Model):
    STATUT_CHOICES = [
        ('none', 'Non commencé'),
        ('started', 'J\'ai commencé'),
        ('completed', 'J\'ai terminé'),
    ]
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="statuts_defis")
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE, related_name="statuts_utilisateurs")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='none')
    preuve_photo = models.ImageField(upload_to='preuves/', blank=True, null=True, verbose_name="Photo preuve")
    xp_defi_accorde = models.BooleanField(default=False)
    xp_photo_accorde = models.BooleanField(default=False)
    mis_a_jour_le = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utilisateur', 'defi')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.defi.titre} : {self.get_statut_display()}"


CATEGORIES_ACTION = [
    ('pro', 'Ma vie professionnelle / mes études'),
    ('argent', 'Mon argent'),
    ('objectifs', 'Mes objectifs'),
    ('moi', 'Moi-même'),
    ('reseaux', 'Réseaux sociaux'),
    ('amour', 'Relation amoureuse'),
    ('spiritualite', 'Spiritualité'),
]

class DomaineSemaine(models.Model):
    semaine = models.ForeignKey(Semaine, on_delete=models.CASCADE, related_name="domaines")
    categorie = models.CharField(max_length=20, choices=CATEGORIES_ACTION)
    titre = models.CharField(max_length=255)
    pourquoi_ca_compte = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.semaine.theme} - {self.get_categorie_display()}"

class ActionProposee(models.Model):
    domaine = models.ForeignKey(DomaineSemaine, on_delete=models.CASCADE, related_name="actions")
    texte = models.TextField()

    def __str__(self):
        return self.texte[:50]

class DomaineUtilisateur(models.Model):
    STATUT_CHOICES = [
        ('none', 'À faire'),
        ('engaged', 'En cours'),
        ('completed', 'Réalisé'),
    ]
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="domaines_choisis")
    domaine = models.ForeignKey(DomaineSemaine, on_delete=models.CASCADE, related_name="choix_utilisateurs")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='none')
    
    action_choisie = models.ForeignKey(ActionProposee, on_delete=models.SET_NULL, null=True, blank=True)
    donnees_action = models.JSONField(blank=True, null=True, verbose_name="Données interactives du flux")
    
    preuve_fichier = models.ImageField(upload_to='preuves_domaines/', blank=True, null=True)
    preuve_texte = models.TextField(blank=True, null=True)
    
    xp_gagnes = models.IntegerField(default=0)
    
    date_creation = models.DateTimeField(auto_now_add=True)
    mis_a_jour_le = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utilisateur', 'domaine')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.domaine.titre} - {self.get_statut_display()}"

class ActionBonusUtilisateur(models.Model):
    STATUT_CHOICES = [
        ('none', 'À faire'),
        ('engaged', 'En cours'),
        ('completed', 'Réalisé'),
    ]
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actions_bonus")
    domaine = models.ForeignKey(DomaineSemaine, on_delete=models.CASCADE, related_name="bonus_utilisateurs")
    action_choisie = models.ForeignKey(ActionProposee, on_delete=models.CASCADE)
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='engaged')
    donnees_action = models.JSONField(blank=True, null=True)
    
    preuve_fichier = models.ImageField(upload_to='preuves_domaines/', blank=True, null=True)
    preuve_texte = models.TextField(blank=True, null=True)
    
    xp_gagnes = models.IntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    mis_a_jour_le = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('utilisateur', 'action_choisie')

    def __str__(self):
        return f"{self.utilisateur.username} - Bonus: {self.action_choisie.texte[:30]} - {self.get_statut_display()}"

class Action(models.Model):
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE, related_name="actions")
    categorie = models.CharField(max_length=20, choices=CATEGORIES_ACTION)
    texte = models.CharField(max_length=255, verbose_name="Action proposée")

    class Meta:
        ordering = ['categorie', 'id']

    def __str__(self):
        return f"[{self.get_categorie_display()}] {self.texte}"

class ActionUtilisateur(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="actions_choisies")
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="choix_utilisateurs")
    terminee = models.BooleanField(default=False)
    preuve_photo = models.ImageField(upload_to='preuves/', blank=True, null=True, verbose_name="Photo preuve")
    xp_photo_accorde = models.BooleanField(default=False)

    class Meta:
        unique_together = ('utilisateur', 'action')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.action.texte}"

class PratiqueSpirituelle(models.Model):
    defi = models.ForeignKey(Defi, on_delete=models.CASCADE, related_name="pratiques")
    titre = models.CharField(max_length=200)
    materiel = models.CharField(max_length=255, verbose_name="Matériel")
    moment = models.CharField(max_length=255, verbose_name="Moment")
    impact = models.CharField(max_length=255, verbose_name="Impact")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.titre

class PratiqueUtilisateur(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pratiques_faites")
    pratique = models.ForeignKey(PratiqueSpirituelle, on_delete=models.CASCADE, related_name="realisations")
    faite = models.BooleanField(default=False)

    class Meta:
        unique_together = ('utilisateur', 'pratique')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.pratique.titre}"

class EspacePersonnel(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name="espace_personnel")
    objectifs = models.TextField(blank=True, null=True, verbose_name="Mes objectifs")
    vision = models.TextField(blank=True, null=True, verbose_name="Ma vision de vie")
    qualites = models.TextField(blank=True, null=True, verbose_name="Mes qualités")

    def __str__(self):
        return f"Espace de {self.utilisateur.username}"

class NoteEvolution(models.Model):
    TYPE_CHOICES = [
        ('libre', 'Note libre'),
        ('defi', 'Réflexion liée à un défi'),
        ('bilan', 'Bilan de semaine')
    ]
    espace_personnel = models.ForeignKey(EspacePersonnel, on_delete=models.CASCADE, related_name="notes")
    texte = models.TextField()
    type_note = models.CharField(max_length=20, choices=TYPE_CHOICES, default='libre')
    date_creation = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"Note ({self.get_type_note_display()}) du {self.date_creation.strftime('%d/%m/%Y')}"

class MessageInspirant(models.Model):
    texte = models.TextField()
    auteur = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Citation de {self.auteur or 'Anonyme'}"
