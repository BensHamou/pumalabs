from django.urls import path
from .views import *


urlpatterns = [

    path('products/', listProductList, name='products'),
    path("products/delete-product/<int:id>", deleteProductView, name="delete_product"),
    path("products/edit-product/<int:id>", editProductView, name="edit_product"),
    path("products/create-product/", createProductView, name="create_product"),

    path('emplacements/', listEmplacementView, name='emplacements'),
    path("emplacements/delete-emplacement/<int:id>", deleteEmplacementView, name="delete_emplacement"),
    path("emplacements/edit-emplacement/<int:id>", editEmplacementView, name="edit_emplacement"),
    path("emplacements/create-emplacement/", createEmplacementView, name="create_emplacement"),

    path('complaints/', listComplaintsList, name='list_complaint'),
    path('complaints/create/', createComplaintView, name='create_complaint'),
    path('complaints/<int:pk>/', detailComplaintView , name='complaint_detail'),
    path('complaints/<int:pk>/delete/', deleteComplaintView, name='delete_complaint'),
    path('complaints/<int:pk>/update/', editComplaintView, name='edit_complaint'),
    path('complaints/<int:pk>/confirm/', confirmComplaint, name='confirm_complaint'),
    path('complaints/<int:pk>/cancel/', cancelComplaint, name='cancel_complaint'),
    path('complaints/<int:pk>/complete/', completeComplaintView, name='complete_complaint'),
    path('complaints/<int:pk>/finish/', finishComplaintView, name='finish_complaint'),
    
]

