from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Candidate
from .forms import CandidateForm
# Create your views here.

@login_required
def homepage(request):
    context = {
        "user": request.user,

    }
    return render(request, "homepage.html", context)

@login_required
def all_candidates(request):
    candidate = Candidate.objects.filter(creator=request.user)
    context = {
        "user": request.user,
        "candidates": Candidate.objects.filter(creator=request.user)

    }
    print(context["candidates"])
    return render(request, "candidates/all_candidates.html", context)

@login_required
def create_candidate(request):
    form = CandidateForm()
    context = {
        "form": form
    }
    html_form = render_to_string("candidates/includes/create_form.html", context, request)
    print("form requested")
    return JsonResponse ({"html_form":html_form})
