from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Patient URLs
    path('patient/login/', views.patient_login, name='patient_login'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/create-request/', views.create_request, name='create_request'),
    
    # Helper URLs
    path('helper/login/', views.helper_login, name='helper_login'),
    path('helper/dashboard/', views.helper_dashboard, name='helper_dashboard'),
    path('helper/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    
    # Logout
    path('logout/', views.user_logout, name='logout'),
]