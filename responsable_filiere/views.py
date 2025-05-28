from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Matiere, Module, Semestre, Classe, Professeur, Etudiant, CustomUser, Examen, Evenement
from django.contrib.auth.decorators import login_required

def redirect_to_login(request):
    return redirect('login')

@login_required
def index(request):
    nb_etudiants = Etudiant.objects.count()
    nb_matieres = Matiere.objects.count()
    nb_professeurs = Professeur.objects.count()

    context = {
        'nb_etudiants': nb_etudiants,
        'nb_matieres': nb_matieres,
        'nb_professeurs': nb_professeurs,
    }

    return render(request, '01_index.html', context)

@login_required
def liste_matieres(request):
    matieres = Matiere.objects.select_related('module__semestre').all()
    return render(request, '01_subjects.html', {'matieres': matieres})

@login_required
def edit_matiere(request, id):
    return HttpResponse(f"Édition de la matière {id}")

@login_required
def supprimer_matiere(request, id):
    return HttpResponse(f"Suppression de la matière {id}")


@login_required
def ajouter_matiere(request):
    modules = Module.objects.all()
    classes = Classe.objects.all()
    semestres = Semestre.objects.all()

    if request.method == "POST":
        nom = request.POST.get('nom')
        classe_id = request.POST.get('classe')
        module_id = request.POST.get('module')
        semestre_id = request.POST.get('semestre')
        credits = request.POST.get('credits')
        volume_horaire = request.POST.get('volume_horaire')

        module = Module.objects.get(id=module_id)
        classe = Classe.objects.get(id=classe_id)
        semestre = Semestre.objects.get(id=semestre_id)
        matiere = Matiere.objects.create(
            nom=nom,
            classe=classe,
            module=module,
            semestre=semestre,
            credits=credits if credits else None,
            volume_horaire=volume_horaire if volume_horaire else None
        )
        return redirect('liste_matieres')

    return render(request, '01_add-subject.html', {
        'modules': modules,
        'classes': classes,
        'semestres': semestres
    })

@login_required
def edit_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    modules = Module.objects.all()
    classes = Classe.objects.all()
    semestres = Semestre.objects.all()

    if request.method == "POST":
        matiere.nom = request.POST.get('nom')
        matiere.classe_id = request.POST.get('classe')
        matiere.module_id = request.POST.get('module')
        matiere.semestre_id = request.POST.get('semestre')
        matiere.credits = request.POST.get('credits')
        matiere.volume_horaire = request.POST.get('volume_horaire')
        matiere.save()
        return redirect('liste_matieres')

    return render(request, '01_edit-subject.html', {
        'matiere': matiere,
        'modules': modules,
        'classes': classes,
        'semestres': semestres,
    })

@login_required
def supprimer_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    matiere.delete()
    return redirect('liste_matieres')

@login_required
def ajouter_module(request):
    classes = Classe.objects.all()
    semestres = Semestre.objects.all()

    if request.method == "POST":
        nom = request.POST.get('nom')
        semestre_id = request.POST.get('semestre')
        semestre = Semestre.objects.get(id=semestre_id)
        module = Module.objects.create(nom=nom, semestre=semestre)
        return redirect('liste_modules')

    return render(request, '01_add-module.html', {
    'classes': classes,
    'semestres': semestres
})

@login_required
def liste_modules(request):
    modules = Module.objects.select_related('semestre').all()
    return render(request, '01_modules.html', {'modules': modules})


@login_required
def supprimer_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    module.delete()
    return redirect('liste_modules')


@login_required
def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    semestres = Semestre.objects.all()


    if request.method == "POST":
        module.nom = request.POST.get("nom")
        module.semestre = Semestre.objects.get(id=request.POST.get("semestre"))
        module.save()
        return redirect("liste_matieres")

    context = {
        "module":module,
        "semestres": semestres,
    }
    return render(request, "01_edit-module.html", context)



@login_required
def liste_semestres(request):
    semestres = Semestre.objects.select_related('classe').all()
    return render(request, '01_semestres.html', {'semestres': semestres})

@login_required
def ajouter_semestre(request):
    classes = Classe.objects.all()

    if request.method == "POST":
        nom = request.POST.get("nom")
        numero = request.POST.get("numero")
        classe_id = request.POST.get("classe")

        if nom and numero and classe_id:
            classe = Classe.objects.get(id=classe_id)
            Semestre.objects.create(nom=nom, numero=numero, classe=classe)
            return redirect('liste_semestres')

    return render(request, '01_add-semestre.html', {'classes': classes})

@login_required
def modifier_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    classes = Classe.objects.all()

    if request.method == 'POST':
        semestre.nom = request.POST.get('nom')
        semestre.numero = request.POST.get('numero')
        classe_id = request.POST.get('classe')
        semestre.classe = get_object_or_404(Classe, id=classe_id)
        semestre.save()
        return redirect('liste_semestres')

    return render(request, '01_edit-semestre.html', {
        'semestre': semestre,
        'classes': classes
    })

@login_required
def supprimer_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    semestre.delete()
    return redirect('liste_semestres')

@login_required
def ajouter_professeur(request):
    matieres = Matiere.objects.all()

    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        telephone = request.POST.get("telephone")
        sexe = request.POST.get("sexe")
        date_naissance = request.POST.get("date_naissance")
        adresse = request.POST.get("adresse")
        matieres_ids = request.POST.getlist("matieres")

        professeur = Professeur.objects.create(
            nom=nom,
            email=email,
            telephone=telephone,
            date_naissance=date_naissance,
            adresse=adresse
        )
        professeur.sexe = sexe
        professeur.save()
        professeur.matieres.set(matieres_ids)

        return redirect("liste_professeurs")

    return render(request, "01_add-teacher.html", {"matieres": matieres})

@login_required
def liste_professeurs(request):
    professeurs = Professeur.objects.prefetch_related('matieres').all()
    return render(request, '01_teachers.html', {'professeurs': professeurs})

@login_required
def edit_professeur(request, professeur_id):
    professeur = get_object_or_404(Professeur, id=professeur_id)
    matieres = Matiere.objects.all()

    if request.method == "POST":
        professeur.nom = request.POST.get("nom")
        professeur.email = request.POST.get("email")
        professeur.telephone = request.POST.get("telephone")
        professeur.sexe = request.POST.get("sexe")
        professeur.date_naissance = request.POST.get("date_naissance")
        professeur.adresse = request.POST.get("adresse")
        professeur.save()
        professeur.matieres.set(request.POST.getlist("matieres"))

        return redirect("liste_professeurs")

    return render(request, "01_edit-teacher.html", {
        "professeur": professeur,
        "matieres": matieres
    })

@login_required
def supprimer_professeur(request, professeur_id):
    professeur = get_object_or_404(Professeur, id=professeur_id)
    professeur.delete()
    return redirect('liste_professeurs')

@login_required
def liste_etudiants(request):
    etudiants = Etudiant.objects.prefetch_related('classe').all()
    return render(request, '01_students.html', {'etudiants': etudiants})

@login_required
def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.delete()
    return redirect('liste_etudiants')

@login_required
def ajouter_etudiant(request):
    classes = Classe.objects.all()
    if request.method == "POST":
        prenom = request.POST.get("prenom")
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        date_naissance = request.POST.get("date_naissance")
        matricule = request.POST.get("matricule")
        date_inscription = request.POST.get("date_inscription")
        telephone = request.POST.get("telephone"),
        classe_id = request.POST.get('classe')
        
        classe = Classe.objects.get(id=classe_id)

        Etudiant.objects.create(
            prenom=prenom,
            nom=nom,
            email=email,
            date_naissance=date_naissance,
            matricule=matricule,
            date_inscription=date_inscription,
            telephone=telephone,
            classe = classe
        )

        return redirect("liste_etudiants")

    return render(request, "01_add-student.html", {'classes':classes})

@login_required
def edit_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    classes = Classe.objects.all()

    if request.method == 'POST':
        etudiant.prenom = request.POST.get('prenom')
        etudiant.nom = request.POST.get('nom')
        etudiant.email = request.POST.get('email')
        etudiant.matricule = request.POST.get('matricule')
        etudiant.date_naissance = request.POST.get('date_naissance')
        etudiant.date_inscription = request.POST.get('date_inscription')
        etudiant.telephone = request.POST.get('telephone')
        etudiant.classe = Classe.objects.get(id=request.POST.get('classe'))
        etudiant.save()
        return redirect('liste_etudiants')

    return render(request, '01_edit-student.html', {'etudiant': etudiant, 'classes': classes})


@login_required
def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.delete()
    return redirect('liste_etudiants')

@login_required
def events_json(request):
    events = []
    for evenement in Evenement.objects.prefetch_related('classes_concernees').all():
        classes = ', '.join(cl.nom for cl in evenement.classes_concernees.all())
        events.append({
            "title": f"{evenement.titre} ({classes})",
            "start": f"{evenement.date}T{evenement.heure_debut}",
            "end": f"{evenement.date}T{evenement.heure_de_fin}",
            "description": evenement.type_evenement.capitalize(),
        })
    return JsonResponse(events, safe=False)


@login_required
def liste_evenements(request):
    return render(request, '01_event.html') 

@login_required
def ajouter_evenement(request):
    classes = Classe.objects.all()
    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        date = request.POST.get("date")
        heure_debut = request.POST.get("heure_debut")
        heure_de_fin = request.POST.get("heure_fin")
        type_evenement = request.POST.get("type_evenement")
        classes_ids = request.POST.getlist("classes_concernees")

        evenement = Evenement.objects.create(
            titre=titre,
            description=description,
            date=date,
            heure_debut=heure_debut,
            heure_de_fin=heure_de_fin,
            type_evenement=type_evenement,
        )
        evenement.classes_concernees.set(classes_ids)

        # Créer un Examen si c'est un examen
        if type_evenement == "examen":
            # À adapter selon ton modèle (il faut une matière)
            # Examen.objects.create(evenement=evenement, matiere=...)
            pass

        return redirect('liste_evenements')

    return render(request, "01_add-event.html", {'classes': classes})

@login_required
def examens(request):
    examens = Examen.objects.select_related('matiere', 'evenement') \
                            .prefetch_related('evenement__classes_concernees') \
                            .all()
    return render(request, '01_exam.html', {'examens': examens})


@login_required
def ajouter_examen(request):
    classes = Classe.objects.all()
    matieres = Matiere.objects.all()

    if request.method == "POST":
        titre = request.POST.get("titre")
        description = request.POST.get("description")
        date = request.POST.get("date")
        heure_debut = request.POST.get("heure_debut")
        heure_fin = request.POST.get("heure_fin")
        classe_id = request.POST.get("classe")
        matiere_id = request.POST.get("matiere")

        # Créer l'événement
        evenement = Evenement.objects.create(
            titre=titre,
            description=description or "",
            date=date,
            heure_debut=heure_debut,
            heure_de_fin=heure_fin,
            type_evenement='examen'
        )
        evenement.classes_concernees.add(classe_id)

        # Créer l'examen lié à l'événement
        Examen.objects.create(
            evenement=evenement,
            matiere=Matiere.objects.get(id=matiere_id)
        )
        return redirect('examens')

    return render(request, '01_add-exam.html', {
        'classes': classes,
        'matieres': matieres
    })

@login_required
def get_matieres(request, classe_id):
    matieres = Matiere.objects.filter(classe_id=classe_id).values('id', 'nom')
    return JsonResponse({'matieres': list(matieres)})

@login_required
def edit_examen(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    matieres = Matiere.objects.filter(classe=examen.evenement.classes_concernees.first())
    classes = Classe.objects.all()

    if request.method == 'POST':
        # mise à jour de l'événement lié à l'examen
        evenement = examen.evenement
        evenement.titre = request.POST.get('titre')
        evenement.description = request.POST.get('description')
        evenement.date = request.POST.get('date')
        evenement.heure_de_debut = request.POST.get('heure_debut')
        evenement.heure_de_fin = request.POST.get('heure_fin')

        classe_id = request.POST.get('classe')
        evenement.classes_concernees.set([classe_id])

        evenement.save()

        # mise à jour de la matière liée à l'examen
        matiere_id = request.POST.get('matiere')
        examen.matiere = Matiere.objects.get(id=matiere_id)
        examen.save()

        return redirect('examens')

    context = {
        'examen': examen,
        'matieres': matieres,
        'classes': classes
    }
    return render(request, '01_edit-exam.html', context)


@login_required
def gestion_utilisateurs(request):
    users = CustomUser.objects.exclude(is_superuser=True)
    return render(request, '01_settings.html', {'users': users})

@login_required
def toggle_activation(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    return redirect('gestion_utilisateurs')

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
User = get_user_model()

@login_required
def creation_comptes_etudiants(request):
    if request.method == 'POST':
        ids = request.POST.getlist('etudiants')
        responsables = request.POST.getlist('responsables')  # liste des IDs cochés comme responsables

        for id in ids:
            etu = Etudiant.objects.get(id=id)
            if not etu.user:
                username = etu.prenom.lower() + str(etu.id)
                if not CustomUser.objects.filter(username=username).exists():
                    password = "passer"
                    # Détection si cet étudiant doit être responsable de classe
                    is_resp = str(id) in responsables
                    is_resp_adjoint = False
                    classe = etu.classe

                    # Vérifier combien de responsables existent déjà pour cette classe
                    nb_resps = CustomUser.objects.filter(
                        is_responsable_de_classe=True,
                        classe_responsable=classe
                    ).count()

                    # Si déjà un responsable, le suivant devient adjoint
                    if is_resp and nb_resps == 1:
                        is_resp_adjoint = True
                    elif is_resp and nb_resps >= 2:
                        is_resp = False  # On ne crée pas plus de 2 responsables

                    user = CustomUser.objects.create_user(
                        username=username,
                        email=etu.email,
                        password=password,
                        first_name=etu.prenom,
                        last_name=etu.nom,
                        is_student=True,
                        is_responsable_de_classe=is_resp,
                        is_responsable_adjoint=is_resp_adjoint,
                        classe_responsable=classe if is_resp else None,
                    )
                    etu.user = user
                    etu.save()
        return redirect('gestion_utilisateurs')

    etudiants = Etudiant.objects.filter(user__isnull=True)
    return render(request, '01_add-user.html', {'etudiants': etudiants})



@login_required
def evenements(request):
    return render(request, '01_event.html')

@login_required
def authentification():
    return None

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirection selon le rôle
                if getattr(user, 'is_responsable_de_classe', False):
                    return redirect('dashboard_responsable_classe')  # nom de l'url dans responsable_classe/urls.py
                else:
                    return redirect('index')  # dashboard général
            else:
                return render(request, '01_login.html', {'error': "Votre compte est désactivé."})
        else:
            return render(request, '01_login.html', {'error': "Nom d'utilisateur ou mot de passe invalide."})

    return render(request, '01_login.html')

from django.contrib.auth import logout

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
