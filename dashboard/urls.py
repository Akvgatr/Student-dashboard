from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', login_required(views.notes), name='notes'),  # Protected route
    path('delete_note/<int:pk>/', login_required(views.delete_note), name="delete-note"),
    path('notes_detail/<int:pk>/', login_required(views.NotesDetailView.as_view()), name="notes-detail"),

    path('home/homework/', login_required(views.homework), name='homework'),
    path('update_homework/<int:pk>', login_required(views.update_homework), name="update_homework"),
    path('delete_homework/<int:pk>', login_required(views.delete_homework), name="delete_homework"),

    path('youtube', login_required(views.youtube), name="youtube"),

    path('todo', login_required(views.todo), name="todo"),
    path('update_todo/<int:pk>', login_required(views.update_todo), name="update_todo"),
    path('delete_todo/<int:pk>', login_required(views.delete_todo), name="delete_todo"),

    path('books', login_required(views.books), name="books"),

    path('dictionary', login_required(views.dictionary), name="dictionary"),

    path('wiki', login_required(views.wiki), name='wiki'),

    path('conversion', login_required(views.conversion), name='conversion'),
]
