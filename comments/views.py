from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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
        "candidates": Candidate.objects.filter(creator=request.user).order_by("name")

    }
    print(context["candidates"])
    return render(request, "candidates/all_candidates.html", context)

@login_required
def create_candidate(request):
    if request.is_ajax():
        data = {}
        if request.method == "POST":
            form = CandidateForm(request.POST)
            if form.is_valid():
                candidate = form.save(commit=False)
                candidate.creator = request.user
                candidate.save()
                data["is_valid"] = True
                candidates = Candidate.objects.filter(creator=request.user).order_by("name")
                data["html_candidate_list"] = render_to_string("candidates/includes/candidate_list.html",{"candidates":candidates})
            else:
                data["is_valid"] = False
        else: #GET request
            form = CandidateForm()
        data["html_form"] = render_to_string("candidates/includes/create_form.html", {"form": form}, request)
        return JsonResponse(data)
    else:
        raise PermissionDenied("Cannot access this endpoint in this manner.")
