from django.urls import path, include
from . import views


app_name = 'post_liker'


urlpatterns = [
    path('users/singup/',
         views.UserSignupView.as_view(),
         name='user_signup'),
    path('users/token/', views.UserObtainToken.as_view(), name='token_obtain_pair'),
]
