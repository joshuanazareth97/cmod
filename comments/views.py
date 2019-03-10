from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.core.exceptions import PermissionDenied
from django.db import IntegrityError

from .models import Candidate, Comment
from .forms import CandidateForm, CommentForm
# Create your views here.

@login_required
def homepage(request):
    recent_candidates = request.user.candidates.all().order_by("-modified")
    context = {
        "user": request.user,
        "candidates": recent_candidates[:5]
    }
    return render(request, "homepage.html", context)

@login_required
def search(request):
    if request.is_ajax() and request.method == 'GET':
        try:
            search_term = request.GET["search_term"]
            print(search_term)
            return JsonResponse({"results":"test string"})
        except KeyError:
            return HttpResponseBadRequest("Cannot access endpoint without a search term.")
    else:
            raise PermissionError("Cannot access this endpoint wihout AJAX, or through POST")

@login_required
def all_candidates(request):
    if request.method == "GET":
        candidates = Candidate.objects.filter(creator=request.user)
        order_term = request.GET.get("orderby", "name")
        context = {
            "user": request.user,
            "candidates": candidates.order_by(order_term)
        }
        if request.is_ajax():
            candidates_html_list = render_to_string("candidates/includes/candidate_list.html", context)
            return JsonResponse({"html_list": candidates_html_list})
        else:
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
        else:
            data["html_form"] = render_to_string("candidates/includes/delete_form.html", {"candidate": candidate}, request)
        return JsonResponse(data)
    else:
        raise PermissionDenied("Cannot access this endpoint in this manner.")


@login_required
def all_candidate_comments(request, cid):
    if request.method == "GET":
        candidate = get_object_or_404(Candidate, cid=cid, creator = request.user)
        comments = candidate.candidate_comments.all().order_by("-created")
        if request.is_ajax():
            html_comment_list = render_to_string("comments/includes/comment_list.html", {"comments": comments})
            return JsonResponse({"html_list": html_comment_list})
        else:
            return render(request, "comments/all_comments.html", {'candidate': candidate, 'comments':comments})
    else:
        raise PermissionDenied("Cannot access this endpoint using POST.")


@login_required
def create_candidate_comment(request, cid):
    candidate = get_object_or_404(Candidate, cid=cid, creator = request.user)
    data = {}
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data["is_valid"] = True
            comment = form.save(commit=False)
            comment.candidate = candidate
            comment.author = request.user
            comment.save()
            comments = candidate.candidate_comments.all().order_by("-created")
            data["html_comment_list"] = render_to_string("comments/includes/comment_list.html",{"comments":comments})
        else:
            data["is_valid"] = False
    else:
        form = CommentForm()
    data["html_form"] = render_to_string("comments/includes/create_comment_form.html", {"candidate": candidate, "form": form}, request)
    return JsonResponse(data)


@login_required
def edit_candidate_comment(request, hash_id):
    comment = get_object_or_404(Comment, hash=hash_id, author=request.user)
    data = {}
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            data["is_valid"] = True
            form.save()
        else:
            data["is_valid"] = False
            data["html_form"] = render_to_string("comments/includes/edit_comment_form.html", {"candidate": comment.candidate, "form": form}, request)
    else:
        form = CommentForm(instance=comment)
        data["html_form"] = render_to_string("comments/includes/edit_comment_form.html", {"candidate": comment.candidate, "form": form}, request)
    return JsonResponse(data)


@login_required
def delete_candidate_comment(request, hash_id):
    comment = get_object_or_404(Comment, hash=hash_id, author=request.user)
    data = {}
    if request.is_ajax() and request.method == 'POST':
        try:
            comment.delete()
            data["deleted"] = True
        except:
            data["deleted"] = False
        return JsonResponse(data)
    else:
        raise PermissionDenied("Cannot access this endpoint using GET or without AJAX.")


@login_required
def star_candidate_comment(request, hash_id):
    comment = get_object_or_404(Comment,  hash=hash_id, author=request.user)
    data = {}
    if request.is_ajax() and request.method == 'POST':
        comment.starred = not comment.starred
        try:
            comment.save(skip_update_timestamp=True)
            data["toggled"] = True
        except:
            data["toggled"] = False
        return JsonResponse(data)
    else:
        raise  PermissionDenied("Cannot access this endpoint using GET or without AJAX.")
