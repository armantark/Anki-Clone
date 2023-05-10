# Import the path function from django.urls
from django.urls import path

# Import the views module from the current application
from . import views

# Set the app_name to 'flashcards'
app_name = 'flashcards'

# Define the urlpatterns list for the flashcards app
urlpatterns = [
    # Create a URL pattern for the index view
    path('', views.index, name='index'),
    # Create a URL pattern for the create_word view
    path('create_word/', views.create_word, name='create_word'),
    # Create a URL pattern for the view_cards view
    path('view_cards/', views.view_cards, name='view_cards'),
]
