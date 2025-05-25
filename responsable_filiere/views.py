from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Matiere, Module, Semestre, Classe, Professeur, Etudiant, Examen


def index(request):
    return render(request, '01_index.html')

def liste_matieres(request):
    matieres = Matiere.objects.select_related('module__semestre').all()
    return render(request, '01_subjects.html', {'matieres': matieres})


def edit_matiere(request, id):
    return HttpResponse(f"Édition de la matière {id}")

def supprimer_matiere(request, id):
    return HttpResponse(f"Suppression de la matière {id}")


def ajouter_matiere(request):
    modules = Module.objects.all()
    classes = Classe.objects.all()
    semestres = Semestre.objects.all()

    if request.method == "POST":
        nom = request.POST.get('nom')
        classe_id = request.POST.get('classe')
        module_id = request.POST.get('module')
        semestre_id = request.POST.get('semestre')

        module = Module.objects.get(id=module_id)
        classe = Classe.objects.get(id=classe_id)
        semestre = Semestre.objects.get(id=semestre_id)
        matiere = Matiere.objects.create(nom=nom, classe=classe, module=module, semestre=semestre)
        return redirect('liste_matieres')

    return render(request, '01_add-subject.html', {
    'modules': modules,
    'classes': classes,
    'semestres': semestres
})

def edit_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    classes = Classe.objects.all()
    semestres = Semestre.objects.all()
    modules = Module.objects.all()

    if request.method == "POST":
        matiere.nom = request.POST.get("nom")
        matiere.classe = Classe.objects.get(id=request.POST.get("classe"))
        matiere.semestre = Semestre.objects.get(id=request.POST.get("semestre"))
        matiere.module = Module.objects.get(id=request.POST.get("module"))
        matiere.save()
        return redirect("liste_matieres")

    context = {
        "matiere": matiere,
        "classes": classes,
        "semestres": semestres,
        "modules": modules,
    }
    return render(request, "01_edit-subject.html", context)

def supprimer_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    matiere.delete()
    return redirect('liste_matieres')


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

def liste_modules(request):
    modules = Module.objects.select_related('semestre').all()
    return render(request, '01_modules.html', {'modules': modules})


def supprimer_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    module.delete()
    return redirect('liste_modules')


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




def liste_semestres(request):
    semestres = Semestre.objects.select_related('classe').all()
    return render(request, '01_semestres.html', {'semestres': semestres})

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


def supprimer_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    semestre.delete()
    return redirect('liste_semestres')

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

def liste_professeurs(request):
    professeurs = Professeur.objects.prefetch_related('matieres').all()
    return render(request, '01_teachers.html', {'professeurs': professeurs})

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

def supprimer_professeur(request, professeur_id):
    professeur = get_object_or_404(Professeur, id=professeur_id)
    professeur.delete()
    return redirect('liste_professeurs')

def liste_etudiants(request):
    etudiants = Etudiant.objects.prefetch_related('classe').all()
    return render(request, '01_students.html', {'etudiants': etudiants})

def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.delete()
    return redirect('liste_etudiants')

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


def supprimer_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.delete()
    return redirect('liste_etudiants')

def events_json(request):
    events = []
    examens = Examen.objects.select_related('matiere', 'evenement').prefetch_related('evenement__classes_concernees')

    for exam in examens:
        classes = ', '.join(cl.nom for cl in exam.evenement.classes_concernees.all())
        events.append({
            "title": f"{exam.matiere.nom} ({classes})",
            "start": f"{exam.evenement.date}T{exam.evenement.heure_de_debut}",
            "end": f"{exam.evenement.date}T{exam.evenement.heure_de_fin}",
            "description": exam.evenement.type_evenement.capitalize(),
        })

    return JsonResponse(events, safe=False)


# def events_json(request):
#     events = [
#         {
#             "title": "Test d'événement",  # Accents corrects
#             "start": "2025-05-28T08:00:00",
#             "end": "2025-05-28T18:00:00",
#             "description": "Exemple d'événement",  # Accents corrects
#             "color": "#378006"  # Code couleur hexadécimal valide
#         }
#     ]
    
#     # Utilisez ensure_ascii=False pour conserver les accents
#     return JsonResponse(events, safe=False, json_dumps_params={'ensure_ascii': False})


def examens(request):
    return render(request, '01_exam.html')

def ajouter_examen(request):
    return render(request, '01_add-exam.html')

def modifier_examen(request):
    return render(request, '01_edit-exam.html')

def evenements(request):
    return render(request, '01_event.html')

def authentification(request):
    return render(request, '01_settings.html')

def login_view(request):
    return render(request, 'login.html')
