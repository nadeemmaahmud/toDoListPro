from django.urls import path
from . views import todo, create, edit, delete, complete, completed, all, all_category, edit_category, add_category, delete_category, search_task

urlpatterns = [
    path('', todo, name='todo'),
    path('create/', create, name='create'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('delete/<int:pk>/', delete, name='delete'),
    path('complete/<int:pk>/', complete, name='complete'),
    path('all/', all, name='all'),
    path('completed/', completed, name='completed'),
    path('all-category/', all_category, name='all_category'),
    path('add-category/', add_category, name='add_category'),
    path('edit-category/<int:pk>/', edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', delete_category, name='delete_category'),
    path('search/', search_task, name='search_task'),
]