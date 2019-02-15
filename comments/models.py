from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def gen_doc_filepath(instance, filename):
    return f"{self.candidate.cid}\\{filename}"

class TimeStammpedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Candidate(models.Model):
    name = models.CharField(max_length=200)
    cid = models.CharField("Candidate ID", max_length=20)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidates")
    designation = models.CharField(max_length=50, default="N/A")

    class Meta:
        unique_together = ("cid", "creator")

    def __str__(self):
        return f"{self.name} [{self.cid}]"

class Comment(TimeStammpedModel):
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


class Document(TimeStammpedModel):
    title = models.CharField(max_length=140)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_documents")
    file = models.FileField(upload_to=gen_doc_filepath)
    starred = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_documents")


class Reminder(TimeStammpedModel):
    title = models.CharField(max_length=140)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="candidate_reminders")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reminders")
    due_date = models.DateField()
