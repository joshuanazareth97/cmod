from django.urls import path
from .views import homepage, all_candidates, create_candidate, edit_candidate, delete_candidate


urlpatterns = [
    path("", homepage, name="home"),
    path("candidates/all", all_candidates, name="all_candidates"),
    path("candidates/create", create_candidate, name="create_candidate"),
    path("candidates/<cid>/edit", edit_candidate, name="edit_candidate"),
    path("candidates/<cid>/delete", delete_candidate, name="delete_candidate"),
]
