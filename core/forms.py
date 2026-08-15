from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profil

INDICATIFS = [
    ('+225', "Côte d'Ivoire +225"),
    ('+33', 'France +33'),
    ('+221', 'Sénégal +221'),
    ('+223', 'Mali +223'),
    ('+226', 'Burkina Faso +226'),
    ('+229', 'Bénin +229'),
    ('+228', 'Togo +228'),
    ('+224', 'Guinée +224'),
    ('+237', 'Cameroun +237'),
    ('+233', 'Ghana +233'),
    ('+234', 'Nigeria +234'),
    ('+1', 'États-Unis +1'),
]


class InscriptionForm(UserCreationForm):
    indicatif = forms.ChoiceField(
        choices=INDICATIFS,
        initial='+225',
        widget=forms.Select(attrs={'class': 'select-indicatif'}),
    )
    telephone = forms.CharField(
        max_length=20,
        label="Numéro de téléphone",
        widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': '07 00 00 00 00'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': "Choisis un nom d'utilisateur"})
        self.fields['username'].help_text = "Lettres, chiffres, . + - _ uniquement."
        self.fields['password1'].widget.attrs.update({'placeholder': "Choisis un mot de passe"})
        self.fields['password2'].widget.attrs.update({'placeholder': "Retape le même mot de passe"})

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profil.objects.create(
                utilisateur=user,
                telephone=self.cleaned_data['indicatif'] + self.cleaned_data['telephone'],
            )
        return user


class ConnexionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': "Ton nom d'utilisateur"})
        self.fields['password'].widget.attrs.update({'placeholder': '••••••••'})


class PhotoProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ('photo_profil',)


class InfosCompteForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'placeholder': "Ton nom d'utilisateur"}),
    )
    telephone = forms.CharField(
        max_length=25,
        label="Numéro de téléphone",
        widget=forms.TextInput(attrs={'type': 'tel', 'placeholder': '+225 07 00 00 00 00'}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
