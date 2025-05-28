from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from responsable_filiere.models import Etudiant, Classe, Examen

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

@responsable_classe_required
def dashboard_responsable_classe(request):
    classe = request.user.etudiant_profile.classe if request.user.is_student else None
    emploi = EmploiDuTemps.objects.filter(classe=classe) if classe else []
    planning = {}

    for jour in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']:
        planning[jour] = {
            '08:00 - 10:00': 'Libre',
            '10:15 - 12:15': 'Libre',
            '14:00 - 16:00': 'Libre',
            '16:15 - 18:15': 'Libre',
        }

    for e in emploi:
        planning[e.jour][e.horaire] = e.matiere

    return render(request, 'responsable_classe/02_index.html', {
        'planning': planning,
    })

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
