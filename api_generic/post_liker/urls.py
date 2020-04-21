from django.urls import path, include
from . import views
from rest_framework import routers


app_name = 'post_liker'

router = routers.DefaultRouter()
router.register('posts', views.PostsViewset)

urlpatterns = [
    path('users/singup/',
         views.UserSignupView.as_view(),
         name='user_signup'),
    path('users/token/', views.UserObtainToken.as_view(), name='token_obtain_pair'),
    path('', include(router.urls)),

]
