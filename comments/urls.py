from django.urls import path
from .views import homepage, all_candidates


urlpatterns = [
    path("", homepage, name="home"),
    path("candidates/all", all_candidates, name="all_candidates")
]
