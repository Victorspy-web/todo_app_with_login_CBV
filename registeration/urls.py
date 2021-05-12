from django.contrib.auth.views import LogoutView
from django.urls import path
from registeration.views import CustomLoginView, CustomLogoutView, RegisterPage

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('register/', RegisterPage.as_view(), name='register'),


    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
