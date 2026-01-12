from .views import *
from django.urls import path

urlpatterns=[
    path("",blogapi,name='blogapi'),
    path("Blogsave",Blogsave.as_view(),name='Blogsave'),
    path("Blogretrive/<int:pk>/",Blogretrive.as_view(),name='Blogretrive'),
    path("Blogupdate/<int:pk>/",Blogupdate.as_view(),name='Blogupdate'),
    path("Blogdelete/<int:pk>/",Blogdelete.as_view(),name='Blogdelete'),
    path("Register",Register.as_view(),name='Register'),
    path("Login",Login.as_view(),name='Login'),
    path("LogoutView",LogoutView.as_view(),name='LogoutView'),
    path('comments', CommentCreateAPIView.as_view(), name='create-comment'),
    path('comments/<int:blog_id>/', BlogCommentsListAPIView.as_view(), name='list-comments'),
    # path('send-email/', send_email_view, name='send_email'),





    

    




    
]