from django.urls import path
from .views import homepage, all_candidates, create_candidate


urlpatterns = [
    path("", homepage, name="home"),
    path("candidates/all", all_candidates, name="all_candidates"),
    path("candidates/create", create_candidate, name="create_candidate"),
]
