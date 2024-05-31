from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from library.models import Library

from .services.user_service import user_service
from .models import UserLibraryRelation
from book.models import BookBorrow
from book.serializers import BorrowBookSerializer3

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = User.objects.filter(email=credentials['email']).first()

        if user and user.check_password(credentials['password']):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError('Invalid credentials')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",'email', 'password']
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user, error = user_service.create_user(email, password)
        if error:
            return serializers.ValidationError(error)
        return user


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('id', 'name',)


class UserLibraryRelationSerializer(serializers.ModelSerializer):
    library = LibrarySerializer()

    class Meta:
        model = UserLibraryRelation
        fields = ('library', 'is_admin')


class UserSerializer(serializers.ModelSerializer):
    libraries = serializers.SerializerMethodField()
    borrowed_books = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", 'libraries',"borrowed_books")

    def get_libraries(self, obj):
        user_library_relations = user_service.get_user_libraries(user=obj)
        return UserLibraryRelationSerializer(user_library_relations, many=True).data
    
    def get_borrowed_books(self,obj):
        books_borrowed = BookBorrow.objects.filter(is_returned=False,user=obj)
        return BorrowBookSerializer3(books_borrowed, many=True).data
    
    
class UserSerializer2(serializers.ModelSerializer):
    borrowed_books = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "email","borrowed_books")
    
    def get_borrowed_books(self,obj):
        books_borrowed = BookBorrow.objects.filter(is_returned=False,user=obj,library=self.context.get("library"))
        return BorrowBookSerializer3(books_borrowed, many=True).data
        