from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView, name="logout"),
    path('signup', views.SignupView.as_view(), name="signup"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('profiledit', views.ProfileEdit.as_view(), name="profiledit"),
    path('pass_get', views.GetPasswView.as_view(), name="pass_get"),
]