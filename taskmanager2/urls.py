from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('task/add/', views.add_task, name='add_task'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
]
