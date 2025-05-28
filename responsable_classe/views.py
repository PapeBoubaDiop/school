from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from responsable_filiere.models import Lecon, Absence,Etudiant, Classe, Examen, Professeur, Evenement, Seance

# Create your views here.
from django.shortcuts import redirect
from functools import wraps

def responsable_classe_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not getattr(user, 'is_responsable_de_classe', False):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@responsable_classe_required
def index(request):
    user = request.user

    if not user.is_responsable_de_classe:
        return redirect('login')

    classe = user.classe_responsable
    etudiants = Etudiant.objects.filter(classe=classe)
    absences = 5
    devoirs = Examen.objects.filter(evenement__classes_concernees=classe)

    prochain_devoir = devoirs.order_by('evenement__date').first()

    context = {
        'etudiants_count': etudiants.count(),
        'absences_count': absences,
        'devoirs_count': devoirs.count(),
        'prochain_devoir': prochain_devoir,
        'classe': classe,
    }

    return render(request, '02_index.html', context)
from responsable_filiere.models import EmploiDuTemps



from django.shortcuts import render
from responsable_filiere.models import Matiere
from django.contrib.auth.decorators import login_required

@responsable_classe_required
def matieres_view(request):
    user = request.user
    if user.is_responsable_de_classe:
        classe = getattr(user, 'etudiant_profile', None).classe if hasattr(user, 'etudiant_profile') else None
        matieres = Matiere.objects.filter(classe=classe) if classe else []
    else:
        matieres = Matiere.objects.none()
    
    return render(request, '02_matieres.html', {'matieres': matieres})

@responsable_classe_required
def professeurs_view(request):
    professeurs = Professeur.objects.all()
    return render(request, '02_professeurs.html', {'professeurs': professeurs})

@responsable_classe_required
def etudiants_view(request):
    user = request.user
    classe = getattr(user, 'classe_responsable', None)
    etudiants = Etudiant.objects.filter(classe=classe) if classe else []
    return render(request, '02_etudiants.html', {'etudiants': etudiants})


@responsable_classe_required
def get_type_display_label(self):
    labels = {
        'projet': 'Projet',
        'tp': 'TP',
        'dm': 'Devoir Maison',
        'ds': 'Devoir Surveillé',
        'expose': 'Exposé'
    }
    return labels.get(self.type_evenement, self.type_evenement.title())


@responsable_classe_required
def evenements_examens_view(request):
    classe = request.user.classe_responsable
    evenements = Evenement.objects.filter(
        examens__isnull=False,
        classes_concernees=classe
    ).order_by('date', 'heure_debut')
    return render(request, '02_devoir_projet.html', {'evenements': evenements})

@responsable_classe_required
def emploi_du_temps_view(request):
    classe = request.user.classe_responsable
    horaires = [
        ('08:00', '10:00'),
        ('10:15', '12:15'),
        ('14:30', '16:30'),
        ('16:45', '18:45'),
    ]
    jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi']

    emploi = []
    seances = Seance.objects.filter(classe=classe)

    # Ajoute ce print ici pour debug
    print([(seance.heure_debut.strftime('%H:%M'), seance.heure_fin.strftime('%H:%M'), seance.jour) for seance in seances])
    
    # Prépare un dict {(plage, jour): seance}
    seances_dict = {}
    for seance in seances:
        plage = f"{seance.heure_debut.strftime('%H:%M')} - {seance.heure_fin.strftime('%H:%M')}"
        seances_dict[(plage, seance.jour)] = seance

    for h in horaires:
        plage = f"{h[0]} - {h[1]}"
        ligne = [plage]
        for jour in jours:
            ligne.append(seances_dict.get((plage, jour)))
        emploi.append(ligne)

    return render(request, '02_emploi_temps.html', {
        'emploi': emploi,
        'jours': jours,
        'classe': classe,
    })


from django.shortcuts import render, redirect, get_object_or_404
from responsable_filiere.models import Absence, Etudiant, Seance

@responsable_classe_required
def absences_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    classe = seance.classe
    etudiants = Etudiant.objects.filter(classe=classe)

    if request.method == 'POST':
        date = request.POST.get('date')
        type_absence = request.POST.get('type_absence')
        commentaire = request.POST.get('commentaire')
        absents_ids = request.POST.getlist('absents')

        for etudiant_id in absents_ids:
            etudiant = Etudiant.objects.get(id=etudiant_id)
            Absence.objects.create(
                date=date,
                seance=seance,
                type_absence=type_absence,
                etudiant=etudiant,
                justification=commentaire
            )

        return redirect('emploi_du_temps_view')

    return render(request, '02_absences.html', {
        'seance': seance,
        'etudiants': etudiants,
    })


@responsable_classe_required
def ajouter_lecon_seance(request, seance_id):
    seance = get_object_or_404(Seance, id=seance_id)
    matieres = Matiere.objects.filter(classe=seance.classe)
    professeurs = Professeur.objects.all()
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        travail = request.POST.get('travail')

        Lecon.objects.update_or_create(
            seance=seance,
            defaults={
                'titre': titre,
                'contenu': contenu,
                'travail': travail,
            }
        )
        return redirect('cahier_texte')

    return render(request, '02_ajouter_lecon.html', {
        'seance': seance,
        'matieres': matieres,
        'professeurs': professeurs,
    })

@responsable_classe_required
def cahier_texte(request):
    classe = request.user.classe_responsable
    lecons = Lecon.objects.filter(seance__classe=classe).select_related('seance', 'seance__matiere', 'seance__professeur').order_by('-seance__jour', '-seance__heure_debut')
    return render(request, '02_cahier_texte.html', {'lecons': lecons, 'classe': classe})