from django.urls import path
from . import views


urlpatterns = [
    path('postes/', views.listPosteView, name='postes'),
    path("postes/delete-poste/<int:id>", views.deletePosteView, name="delete_poste"),
    path("postes/edit-poste/<int:id>", views.editPosteView, name="edit_poste"),
    path("postes/create-poste/", views.createPosteView, name="create_poste"),
    path("postes/edit-standard/<int:id>", views.editStandardView, name="edit_standard"),
    path("postes/delete-standard/<int:id>", views.deleteStandardView, name="delete_standard"),
    path("postes/create-standard/<int:id>", views.createPosteView, name="create_standard"),
    
    ]