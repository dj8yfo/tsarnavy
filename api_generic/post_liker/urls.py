from django.urls import path, include
from . import views
from rest_framework import routers


app_name = "post_liker"

router = routers.DefaultRouter()
router.register("posts", views.PostsViewset)
router.register("actions", views.ActionViewset)

urlpatterns = [
    path("users/singup/", views.UserSignupView.as_view(), name="user_signup"),
    path("users/token/", views.UserObtainToken.as_view(), name="token_obtain_pair"),
    path(
        "user/<pk>/last_actions", views.LastActionsView.as_view(), name="last_actions"
    ),
    path(
        "api/analytics/", views.LikesAnalytics.as_view(), name="likes_analysis"
    ),
    path("", include(router.urls)),
]
