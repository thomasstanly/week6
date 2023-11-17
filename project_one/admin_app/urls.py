from django.urls import path
from admin_app import views

urlpatterns = [
    path('admin_login/',views.admin_log_page,name= 'adm_log_page'),
    path('admin_home/',views.admin_home_page,name='admin_home_page'),
    path('admin_logout/',views.admin_logout,name="admin_logout"),
    path('admin_edit/<id>',views.admin_edit,name='admin_edit'),
    path('admin_delete/<id>',views.admin_delete,name='admin_delete'),
    path('admin_create/',views.admin_create,name="admin_create"),
    path('search/',views.admin_search,name='admin_search'),
]