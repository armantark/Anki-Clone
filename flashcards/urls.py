from django.urls import path
from . import views

app_name = 'flashcards'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_word/', views.create_word, name='create_word'),
    path('view_cards/', views.view_cards, name='view_cards'),
]
