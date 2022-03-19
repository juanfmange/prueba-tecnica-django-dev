from django.urls import path
from .views import LoginView, RegisterView, UserView, LogoutView, Cookie
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('cookie', Cookie.as_view()),
    path('token', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
]
