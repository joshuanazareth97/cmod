from django.contrib import admin
from .models import Candidate, Comment, Reminder, Document
# Register your models here.
admin.site.register(Candidate)
# admin.site.register(Comment)
admin.site.register(Document)
admin.site.register(Reminder)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields=('created','modified','hash')
