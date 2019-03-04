from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from .models import Candidate
from .forms import CandidateForm, CommentForm
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

def save_candidate(request, form):
    if form.edit:
        template = "candidates/includes/edit_form.html"
    else:
        template = "candidates/includes/create_form.html"
    if request.is_ajax():
        data = {}
        if request.method == "POST":
            if form.is_valid():
                candidate = form.save(commit=False)
                if not form.edit:
                    candidate.creator = request.user
                try:
                    candidate.save()
                except IntegrityError:
                    data["is_valid"] = False
                    form.add_error('cid',f'Candidate with this ID exists [{request.user.candidates.get(cid=request.POST.get("cid")).name}]')
                else:
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
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate, edit=True)
    else:
        form = CandidateForm(instance=candidate, edit=True)
    return save_candidate(request, form)

@login_required
def delete_candidate(request, cid):
    data = {}
    if request.is_ajax():
        candidate = get_object_or_404(Candidate, cid=cid, creator=request.user)
        if request.method == 'POST':
            candidate.delete()
            data["deleted"] = True
            new_candidates = Candidate.objects.filter(creator=request.user).order_by("name")
            data["html_candidate_list"] = render_to_string("candidates/includes/candidate_list.html",{"candidates":new_candidates})
        else:
            data["html_form"] = render_to_string("candidates/includes/delete_form.html", {"candidate": candidate}, request)
        return JsonResponse(data)
    else:
        raise PermissionDenied("Cannot access this endpoint in this manner.")

@login_required
def all_candidate_comments(request, cid):
    candidate = request.user.candidates.get(cid=cid)
    # comments = candidate.candidate_comments.all()
    text = '''Lorem ipsum dolor sit amet, consectetur adipisicing elit. Necessitatibus laborum qui, sit eum mollitia!
    Blanditiis impedit quas commodi itaque, eveniet earum recusandae deserunt assumenda in, omnis obcaecati,
    ducimus rerum autem ut veniam iste aut, illo quasi est ullam quos incidunt unde! Mollitia recusandae consequatur
    ipsam labore non! Pariatur sapiente quam quis, praesentium quasi ipsum officia, magnam cumque ex expedita delectus
    sequi labore voluptatem distinctio, fugiat iure possimus. Fuga exercitationem odio, voluptates nisi quisquam veritatis
    rem ad iure eaque facere libero atque reiciendis earum porro quas consequatur commodi consequuntur temporibus
    reprehenderit esse est ut neque iste. Aliquam culpa est amet laborum.
    '''
    comments = [
        {'title':"Test Title", 'text':text, 'type':"Note", 'starred':False, 'created': timezone.now(), 'modified': timezone.now()},
        {'title':"Test Title 2", 'text':text[:300], 'type':"Note", 'starred':False, 'created': timezone.now(), 'modified': timezone.now()}
    ]
    return render(request, "comments/all_comments.html", {'candidate': candidate, 'comments':comments})

@login_required
def create_candidate_comment(request, cid):
    candidate = get_object_or_404(Candidate, cid=cid, creator = request.user)
    if request.method == 'POST':
        form = CommentForm(request=request)
        return HttpResponse("Posted")
    else:
        form = CommentForm(request=request)
        html_form = render_to_string("comments/includes/create_comment_form.html", {"candidate": candidate, "form": form}, request)
        return JsonResponse({"html_form":html_form})
