from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Candidates")
    designation = models.CharField(max_length=50, default="N/A")

class Comment(models.Model):
    title = models.CharField(max_length=140)
    text = models.CharField(max_length=1000)
    type_choices = (
        ('NT','Note'),
        ('BR', 'Briefing'),
        ('EV', 'Evaluation')
    )
    type = models.CharField(max_length=2, choices = type_choices, default="NT")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Document(models.Model):
    title = models.CharField(max_length=140)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to=lambda instance, filename: f"{instance.candidate.id}/{filename}")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Reminder(models.Model):
    title = models.CharField(max_length=140)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="documents")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="documents")
    due_date = models.DateField
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
