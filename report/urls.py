from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('postes/', views.listPosteView, name='postes'),
    path("postes/delete-poste/<int:id>", views.deletePosteView, name="delete_poste"),
    path("postes/edit-poste/<int:id>", views.editPosteView, name="edit_poste"),
    path("postes/create-poste/", views.createPosteView, name="create_poste"),
    path("postes/edit-standard/<int:id>", views.editStandardView, name="edit_standard"),
    path("postes/delete-standard/<int:id>", views.deleteStandardView, name="delete_standard"),
    path("postes/create-standard/<int:id>", views.createStandardView, name="create_standard"),
    path("postes/default-standard/<int:id>", views.setDefaultStandardView, name="default_standard"),

    path('reports/', ReportList.as_view(), name='list_report'),
    path('', ReportList.as_view(), name='list_report'),
    path('report/create/', ReportCreate.as_view(), name='create_report'),
    path('report/<int:pk>/update/', ReportUpdate.as_view(), name='update_report'),
    path('report/<int:pk>/delete/', delete_report, name='delete_report'),
    path('report/<int:pk>/', ReportDetail.as_view(), name='report_detail'),
    
    path('report/get-data-by-usine/', views.get_data_by_usine, name='get_data_by_usine'),

    ]