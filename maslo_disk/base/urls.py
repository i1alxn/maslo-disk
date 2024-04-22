from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('update/', views.UpdateUser.as_view(), name='update'),
    path('folder/<str:pk>/', views.folderPage, name='folder'),
]