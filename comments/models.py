from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def gen_doc_filepath(instance, filename):
    return f"{self.candidate.id}\\{filename}"

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
    starred = models.BooleanField(default=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Document(models.Model):
    title = models.CharField(max_length=140)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_documents")
    file = models.FileField(upload_to=gen_doc_filepath)
    starred = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_documents")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Reminder(models.Model):
    title = models.CharField(max_length=140)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_reminders")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reminders")
    due_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
