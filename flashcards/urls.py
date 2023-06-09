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
    # Create a URL pattern for the manage_words view
    path('manage_words/', views.manage_words, name='manage_words'),
    path('manage_words/<int:word_id>/', views.manage_words, name='manage_words_with_id'),
    # Create a URL pattern for the delete_word function
    path('delete_word/<int:word_id>/', views.delete_word, name='delete_word'),
    # Create a URL pattern for the check_word function
    path('check_word/', views.check_word, name='check_word'),
    # Create a URL pattern for the view_cards view
    path('view_cards/', views.view_cards, name='view_cards'),
    path('about/', views.about, name='about'),
]
