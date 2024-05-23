from django.contrib.auth import get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from library.models import Library

from .services.user_service import user_service
from .models import UserLibraryRelation

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
        fields = ['email', 'password']

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

    class Meta:
        model = User
        fields = ("id,"'email', 'libraries')

    def get_libraries(self, obj):
        user_library_relations = user_service.get_user_libraries(user=obj)
        return UserLibraryRelationSerializer(user_library_relations, many=True).data
