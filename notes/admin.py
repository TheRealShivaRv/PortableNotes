from django.contrib import admin
from .models import NotesFile
class NotesFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'username', 'note', 'time')
admin.site.register(NotesFile, NotesFileAdmin)
