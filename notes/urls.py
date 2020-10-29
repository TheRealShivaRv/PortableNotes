from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notes/', views.notes, name='notes'),
    path('noteviewer/<str:title>', views.noteviewer, name='noteviewer'),
    path('deletenotes/', views.deletenotes, name='deletenotes'),
    path('search/', views.search, name='search')
]
