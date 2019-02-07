from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
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
    return render(request, "candidates/all_candidates.html", context)

def save_candidate(request, form, edit=False):
    if edit:
        template = "candidates/includes/edit_form.html"
    else:
        template = "candidates/includes/create_form.html"
    if request.is_ajax():
        data = {}
        if request.method == "POST":
            if form.is_valid():
                candidate = form.save(commit=False)
                if not edit:
                    candidate.creator = request.user
                candidate.save()
                data["is_valid"] = True
                candidates = Candidate.objects.filter(creator=request.user).order_by("name")
                data["html_candidate_list"] = render_to_string("candidates/includes/candidate_list.html",{"candidates":candidates})
            else:
                data["is_valid"] = False
        data["html_form"] = render_to_string(template, {"form": form}, request)
        return JsonResponse(data)
    else:
        raise PermissionDenied("Cannot access this endpoint in this manner.")

@login_required
def create_candidate(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
    else:
        form = CandidateForm()
    return save_candidate(request, form)

@login_required
def edit_candidate(request, cid):
    candidate = get_object_or_404(Candidate, cid=cid, creator=request.user)
    return HttpResponse(f"<h3>CID: {cid} <br /> {candidate.name}</h3>")
