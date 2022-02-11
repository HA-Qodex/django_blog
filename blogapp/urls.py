from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    path('posts/', PostView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('addLike/', AddLike.as_view()),
    path('addComment/', AddComment.as_view()),
    path('addReply/', ReplyView.as_view()),
    path('login/', obtain_auth_token),
    path('registration/', Registration.as_view()),
]