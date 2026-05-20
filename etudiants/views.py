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
    filiere_choisie = request.GET.get('filiere', '')
    #recuperation du terme de recherche
    recherche = request.GET.get('recherche', '')
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
                return render(request,'etudiants/connexion.html',{'form':form})
        else:
            #form = ConnexionForm()
            return render(request,'etudiants/connexion.html',{'form':form})
    else:
        form = ConnexionForm()
        return render(request,'etudiants/connexion.html',{'form':form})


#quatrième vue : deconnexion
def deconnexion_vue(request):
    #destruction de la session avec logout()
    logout(request)
    messages.info(request,"vous avez été déconnecté")
    return redirect('etudiants:accueil')             

#cinqième vue : depot du porfolio
#@login_required si user n'est pas connecté django le redirige automatiquement vers le LOGIN_URL
@login_required
def deposer_portfolio(request):
    #avec hasattr on verifie si un attribut existe à l'occurence on verifie si un user à deje un profil etudiant
    if hasattr(request.user, 'etudiant'):
        messages.info(request, "Vous avez déjà déposé un portfolio.")
        return redirect('etudiants:mon_espace')

    if request.method == 'POST':
        #request.FILES est un dictionnaird des fichiers uploadés
        form = EtudiantForm(request.POST, request.FILES)
        if form.is_valid():
             #commit=False == on cree un objet mais on ne sauvegarde pas
            etudiant = form.save(commit=False)
            #liasion de cet etudiant à l'utilisateur connecté
            etudiant.user = request.user
            #attente de l'approbation de l'admin
            etudiant.statut = 'en_attente'
            #sauvegarde total dans la base de donnees
            etudiant.save()
            messages.success(request, "Portfolio soumis ! En attente de validation.")
            return redirect('etudiants:mon_espace')
    else:
        form = EtudiantForm()

    # on ajoute les stats pour le panneau latéral
    return render(request, 'etudiants/deposer.html', {
        'form': form,
        'total_inscrits': Etudiant.objects.count(),
        'total_valides': Etudiant.objects.filter(status='valide').count(),
    })

#sixième vue : MON ESPACE
@login_required
def mon_espace(request):
    #essaie de la recuperation du profil de l'etudiant connecté
    try:
        #request.user.etudiant = acces grace au related_name = 'eudiant' du modele
        etudiant = request.user.etudiant
    except Etudiant.DoesNotExist:
        etudiant = None
    return render(request,'etudiants/mon_espace.html',{'etudiant':etudiant})

#septième vie: MODIFIER SON PROFIL
@login_required
def modifier_profil(request):
    #get_objet_or_404 = recuper l'etudiant ou affiche une page 404
    etudiant = get_object_or_404(Etudiant, user=request.user) 
    if request.method == 'POST':
        #instance = etudiant == on modifie l'etudiant existant
        form =EtudiantForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            etudiant = form.save(commit=False)
            #les modification repasse en attente
            etudiant.status = 'en_attente'
            etudiant.save()
            messages.success(request, "Profil modifié. En attente de revalidation")
            return redirect('sudents:mon_espace')
        else:
            form = EtudiantForm(instance=etudiant)
        return render(request,'etudiants/modifier.html',{
            'form':form,
            'etudiant':etudiant
            })    

#huitième vue : SUPPRIMMER UN PROFIL
@login_required
def supprimer_profil(request):
    etudiant = get_object_or_404(Etudiant, user=request.user)
    if request.method == 'POST':
        #.delete() suppression de l'objet dans la BD
        etudiant.delete()
        messages.success(request, "votre profil à été supprimé.")
        return redirect('etudiants:accueil')
    #si la methode est GET on affiche une page de confirmation avant de supprimer
    return render(request, 'etudiants/supprimer.html', {'etudiant':etudiant})

#neuvième vue =  DASHBOARD ADMIN
#si @user_passes_test(est_admin) = si est_admin(user) retourne False, renvoie vers la page de connexion
@user_passes_test(est_admin)
def dashboard(request):
    #recuperation des etudiants groupées par status
    en_attente = Etudiant.objects.filter(status='en_attente')
    valides = Etudiant.objects.filter(status='valide')
    rejetes = Etudiant.objects.filter(status='rejete')
    return render(request, 'etudiants/dashboard.html', {
        'en_attente': en_attente,
        'valides': valides,
        'rejetes': rejetes,
        'total' : Etudiant.objects.count(),
    })

#dixième vue : VALIDER UN PORFOLIO(admin)
@user_passes_test(est_admin)
def valider_porfolio(request,etudiant_id):
    #recuperation de l'etudiant par son ID(celui de l'url)
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.status = 'valide'
    etudiant.save()
    messages.success(request, f"Porfolio de {etudiant} validé et publié avec succes")
    return redirect('etudiants;dashboard')

#onzième vue : REJETER UN PORFOLIO(admin)
@user_passes_test(est_admin)
def rejeter_porfolio(request,etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.status = 'rejete'
    etudiant.save()
    messages.warning(request, f"Porfolio de {etudiant} rejeté.")
    return redirect('etudiants:dashboard')    

#douzième vue : PAGE CONTACT
def contact(request):
    return render(request, 'etudiants/contact.html')




       
        

