from django.urls import path
from . import views  # Import views module from the same directory
from .views import display_image,DisplayImageView
from .views import DisplayImageView

urlpatterns = [
    path('home/', views.HomePage, name='home'),
    path('display/', DisplayImageView.as_view(), name='display_image'),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
    #  path('display/user/<int:user_id>/', UserImageView.as_view(), name='user_image'),
]