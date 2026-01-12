from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class Blogserializers(serializers.ModelSerializer):
    created_by=serializers.SlugRelatedField(read_only=True,slug_field="username")
    class Meta:
        model=Blog
        fields="__all__"

# serializers.py
from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']



class Registerserializer(serializers.ModelSerializer):
    def create(self,data):
        username=data.get("username")
        password=data.get("password")
        # if email:
        #     checkemail=User.objects.filter(email=email).exists()
        #     if checkemail:
        #         raise serializers.errors("Email already exists")
        #     else:
        #         username = email.split('@')[0]  # simple username from email

        users=User.objects.create_user(username=username,password=password)
        if users:
                    return users
        else:
                    raise serializers.errors("user not created something error")
        # else:
        #     raise serializers.errors("Please give the Input")


    class Meta:
        model=User
        fields=["email","password","username"]
from django.contrib.auth import authenticate, login

# Login Sefrom django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        print("email",username)
        print("password",password)

        # Try using username if your model still uses it
        user = authenticate(username=username, password=password)
        print(user)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user
