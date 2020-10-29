from django.shortcuts import render, redirect
from datetime import datetime
from .models import NotesFile
from django.contrib import messages
def dashboard(request):
    notes = NotesFile.objects.filter(username=request.user.username)
    notetitles = []
    for note in notes:
        title = note.title
        notetitles.append(title)
    context = {
        'notes': notes,
        'notetitles': notetitles
    }
    return render(request, 'dashboard.html', context)
def noteviewer(request, title):
    notes = NotesFile.objects.get(title=title)
    title = notes.title
    text = notes.note
    datetimestamp = notes.time
    if request.method == 'POST':
        title = request.POST['title']
        note = request.POST['note']
        notes.title = title
        notes.note = note
        newdatetimestamp = datetime.now()
        notes.time = newdatetimestamp
        notes.save()
        return redirect('noteviewer',title=title)
    context = {
        'title': title,
        'text': text,
        'datetimestamp': datetimestamp
    }
    return render(request, 'notesviewer.html',context)
def notes(request):
    datetimestamp = datetime.now()
    context = {
        'datetimestamp': datetimestamp,
    }
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['note']
        time = datetimestamp
        username = request.user.username
        context = {
            'datetimestamp': datetimestamp,
            'title': title,
            'text': text,
            'time': time,
            'username':username,
        }
        if NotesFile.objects.filter(title=title, username=username).exists():
            messages.error(request, 'A note with this title already exists')
            return render(request, 'notesapp.html', context)
        else:
            query = NotesFile(title=title, note=text, time=time, username=username)
            query.save()
            messages.success(request, 'Note saved successfully')
            return redirect('dashboard')
    return render(request, 'notesapp.html', context)
def deletenotes(request):
    if request.method == 'POST':
        title = request.POST['title']
        notes = NotesFile.objects.get(title=title, username=request.user.username)
        notes.delete()
        messages.success(request, 'Note deleted successfully')
        return redirect('dashboard')
def search(request):
    if request.method == 'POST':
        searchinput = request.POST['searchinput']
        notefiles = NotesFile.objects.filter(title__icontains=searchinput)
        notetitles = []
        for notefile in notefiles:             
            notetitles.append(notefile.title)
        print('notetitles:', notetitles)
        context = {
            'notetitles': notetitles,
        }
        return render(request, 'search.html', context)
    else:
        return redirect('dashboard')
