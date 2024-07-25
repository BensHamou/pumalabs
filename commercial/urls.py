from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('products/', listProductList, name='products'),
    path("products/delete-product/<int:id>", deleteProductView, name="delete_product"),
    path("products/edit-product/<int:id>", editProductView, name="edit_product"),
    path("products/create-product/", createProductView, name="create_product"),

    path('emplacements/', listEmplacementView, name='emplacements'),
    path("emplacements/delete-emplacement/<int:id>", deleteEmplacementView, name="delete_emplacement"),
    path("emplacements/edit-emplacement/<int:id>", editEmplacementView, name="edit_emplacement"),
    path("emplacements/create-emplacement/", createEmplacementView, name="create_emplacement"),

    path('categories/', listCategoryView, name='categories'),
    path("categories/delete-category/<int:id>", deleteCategoryView, name="delete_category"),
    path("categories/create-category/", createCategoryView, name="create_category"),
    path("categories/edit-category/<int:id>", editCategoryView, name="edit_category"),

    path('complaints/', listComplaintsList, name='list_complaint'),
    path('complaints/create/', createComplaintView, name='create_complaint'),
    path('complaints/<int:id>/', detailComplaintView , name='complaint_detail'),
    path('complaints/<int:id>/delete/', deleteComplaintView, name='delete_complaint'),
    path('complaints/<int:id>/update/', editComplaintView, name='edit_complaint'),
    path('complaints/<int:id>/confirm/', confirmComplaint, name='confirm_complaint'),
    path('complaints/<int:id>/cancel/', cancelComplaint, name='cancel_complaint'),
    path('complaints/<int:id>/complete/', completeComplaintView, name='complete_complaint'),
    path('complaints/<int:id>/finish/', finishComplaintView, name='finish_complaint'),
    
    path('live_search/', live_search, name='live_search'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)