from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Candidate
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
    return render(request, "all_candidates.html", context)
