from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Etudiant
from .forms import InscriptionForm, EtudiantForm, ConnexionForm

# verification si c'est un admin qui se connecte(staff ou superuser)
def est_admin(user):
    return user.is_staff

# première vue : page d'accueil
def accueil(request):
    #recuperation des etudiant specifique avec un filter()
    etudiants = Etudiant.objects.filter(status='valide')
    #recuperation de la filiere
    filiere_choisie = request.Get.get('filiere', '')
    #recuperation du terme de recherche
    recherche = request.Get.get('recherche', '')
    if filiere_choisie and filiere_choisie != 'toutes':
        #on filitre encore
        etudiants = etudiants.filter(filiere=filiere_choisie)
    #si user tape quelques choses dans la recherche
    if recherche:
        #filtre par nom ou prenom et importation de Q pour faire les requetes OR
        from django.db.models import Q
        etudiants = etudiants.filter(
            Q(nom_icontains=recherche) | Q(prenom_icontains=recherche)
        ) 

    #les statistiques
    total_inscrits = Etudiant.objects.count()
    total_valides = Etudiant.objects.filter(status='valide').count()
    #recuperation de la liste des filiere
    filieres = Etudiant.FILIERES
    return render(request, 'etudiants/accueil.html', {
        'etudiants': etudiants,
        'filieres': filieres,
        'filiere_choisie': filiere_choisie,
        'recherche': recherche,
        'total_inscrits': total_inscrits,
        'total_valides': total_valides,
    })

#deuxieme vue: inscription
def inscription(request):
    #soumission du formulaire
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            #connexion automatique de l'utilisateur apres son inscription
            login(request,user)
            #message apres creation de compte
            messages.success(request, "compte crée avec succès | Déposer votre porfolio")
            #redirection directement vers la page de dépot de porfolio
            return redirect('etudiants:deposer')
    else:
        #si la methode du formulaire est GET on cree un formulaire vide
        form = InscriptionForm()
    return render(request,'etudiants/inscription.html', {'form':form})


#troisieme vue : connexion
def connexion_vue(request):
    if request.user.is_authenticated:
        return redirect('etudiants:mon_espace')
    if request.method == 'POST':
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #verification de ces infos dans la base de donnees
            user = authenticate(request, username=username, password=password)
            if user is not None:
                #creation d'une session pour que django sans souvienne
                login(request,user)
                messages.success(request,f"bienvenue {user.username}")
                #redirection ssi user c'est connecté
                next_url = request.GET.get('next', 'etudiants:mon_espace')
                return redirect(next_url)
            else:
                messages.error(request,"nom d'utilisateur ou mot de passe incorrect")
        else:
            form = ConnexionForm()
        return render(request,'etudiants/connexion.html',{'form':form})

#quatrième vue : deconnexion
def deconnexion_vue(request):
    #destruction de la session avec logout()
    messages.info(request,"vous avez été déconnecté")
    return redirect('etudiants:accueil')             


