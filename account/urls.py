from django.urls import path
from . import views
from .views import CustomLoginView


urlpatterns = [

    path('login_success/', views.login_success, name='login_success'),

    path("dashboard/", views.homeView, name="home"),
    path("refresh-users/", views.refreshUsersList, name="refresh_users"),
    path("users/edit-user/<int:id>", views.editUserView, name="edit_user"),
    path("users/delete-user/<int:id>", views.deleteUserView, name="delete_user"),
    path("users/", views.listUsersView, name="users"),
    path("new_users/", views.listNewUsersView, name="new_users"),
    path('users/details/<int:id>', views.userDetailsView, name='details'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', CustomLoginView.as_view(), name='login'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logoutView, name='logout'),

    path('usines/', views.listUsineView, name='usines'),
    path("usines/delete-usine/<int:id>", views.deleteUsineView, name="delete_usine"),
    path("usines/edit-usine/<int:id>", views.editUsineView, name="edit_usine"),
    path("usines/create-usine/", views.createUsineView, name="create_usine"),

    path('horaires/', views.listHoraireView, name='horaires'),
    path("horaires/delete-horaire/<int:id>", views.deleteHoraireView, name="delete_horaire"),
    path("horaires/edit-horaire/<int:id>", views.editHoraireView, name="edit_horaire"),
    path("horaires/create-horaire/", views.createHoraireView, name="create_horaire"),
]

