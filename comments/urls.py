from django.urls import path
from .views import homepage, all_candidates, create_candidate, edit_candidate, delete_candidate, all_candidate_comments, create_candidate_comment


urlpatterns = [
    path("", homepage, name="home"),
    path("candidates/all", all_candidates, name="all_candidates"),
    path("candidates/create", create_candidate, name="create_candidate"),
    path("candidates/<cid>/edit", edit_candidate, name="edit_candidate"),
    path("candidates/<cid>/delete", delete_candidate, name="delete_candidate"),
    path("candidates/<cid>/comments/all", all_candidate_comments, name="candidate_comments"),
    path("candidates/<cid>/comments/create", create_candidate_comment, name="create_comment"),
]
