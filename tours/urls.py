from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('', views.home, name='home'),
    path('packages/', views.packages_list, name='packages_list'), # New dedicated route
    path('package/<int:pk>/', views.package_detail, name='package_detail'),
    path('package/<int:pk>/inquire/', views.submit_inquiry, name='submit_inquiry'),
    path('tailor-made/', views.tailor_made, name='tailor_made'), # Add this line
]