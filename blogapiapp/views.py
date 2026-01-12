from django.shortcuts import render,HttpResponse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView


def blogapi(req):
    return HttpResponse("BlogApi")

class Blogsave(GenericAPIView,CreateModelMixin,ListModelMixin):
    queryset=Blog.objects.all()   
    serializer_class=Blogserializers
    authentication_classes=[TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):    # Hooks Method
        print("login fun")

        serializer.save(created_by=self.request.user)   # When we use hooks method should be use request don't use req
    
    def get_queryset(self):   # Hooks Method
        print("2nd")
        blog_data=Blog.objects.filter(created_by=self.request.user).order_by('-created_at')
        return blog_data


    def post(self,req):
        print("withour login fun")
        return self.create(req)
    
    def get(self,req):
        print("1st")
        return self.list(req)
    
 


class Blogretrive(GenericAPIView,RetrieveModelMixin):
    queryset=Blog.objects.all()
    serializer_class=Blogserializers

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(created_by=self.request.user)

    def get(self,req,pk):
        return self.retrieve(req,pk=pk)
    
class Blogupdate(GenericAPIView,UpdateModelMixin,DestroyModelMixin):
    queryset=Blog.objects.all()
    serializer_class=Blogserializers

    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(created_by=self.request.user)

    def put(self,req,pk):
        return self.update(req,pk=pk)
    
    def patch(self,req,pk):
        return self.partial_update(req,pk=pk)

class Blogdelete(GenericAPIView,DestroyModelMixin):
    queryset=Blog.objects.all()
    serializer_class=Blogserializers
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(created_by=self.request.user)


    def delete(self,req,pk):
        return self.destroy(req,pk=pk)
    
# Create a comment
class CommentCreateAPIView(CreateAPIView):  #  when we use this module don't need post or get method 
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
# views.py

class BlogCommentsListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return Comment.objects.filter(post_id=blog_id)

    
class Register(GenericAPIView,CreateModelMixin):
    queryset=User.objects.all()
    serializer_class=Registerserializer

    def post(self,req):
        serializers=Registerserializer(data=req.data)
        if serializers.is_valid():
            user=serializers.save()
            token=Token.objects.create(user=user)
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'user_id': user.id,
            }, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(GenericAPIView,CreateModelMixin):
    queryset=User.objects.all()
    serializer_class=LoginSerializer
    try:

        def post(self,req):
            serializers=LoginSerializer(data=req.data)
            if serializers.is_valid():
                user=serializers.validated_data
                token=Token.objects.get(user=user)
                return Response({token.key})
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("the error is",e)

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class LogoutView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the user's token (logout)
            request.user.auth_token.delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST)

# from django.http import JsonResponse
# from .tasks import send_email_task

# def send_email_view(request):
#     subject = "Hello from Celery"
#     message = "This is a test email sent using Celery"
#     recipient_list = ['vinothkumars@accsysconsulting.com']

#     send_email_task.delay(subject, message, recipient_list)

#     return JsonResponse({"message": "Email is being sent in background."})
