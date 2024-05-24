from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Library,Rack,Storage
from .services.library_service import library_service

from book.models import BookBorrow, Book,BookCopy

User = get_user_model()

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"

    def create(self, validated_data):
        user = self.context.get('user')
        library, error = library_service.create_library(**validated_data, admin_user=user)

        if error:
            raise serializers.ValidationError(error)
        return library

    def update(self, instance, validated_data):
        library, error = library_service.edit_library(instance, **validated_data)
        if error:
            raise serializers.ValidationError(error)
        return library


class LibraryBookAddSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    publishers = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    authors = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )
    number_of_copies = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        library = self.context.pop('library')
        validated_data['library'] = library
        book, error = library_service.add_book(**validated_data)
        if error:
            raise serializers.ValidationError(error)
        return book


class LibraryBorrowBookSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    class Meta:
        model = BookBorrow
        fields = ['book', 'due_date', 'is_returned','user']
        read_only_fields = ['is_returned']

    def create(self, validated_data):
        validated_data['library'] = self.context.pop('library')
        borrow_book, error = library_service.borrow_book(**validated_data)
        if error:
            raise serializers.ValidationError(error)
        return borrow_book

class LibraryBorrowBookCopy(LibraryBorrowBookSerializer):
    book_copy = serializers.PrimaryKeyRelatedField(queryset=BookCopy.objects.all(), write_only=True)

    class Meta:
        model = BookBorrow
        fields = ['book_copy', 'due_date', 'is_returned','user']
        read_only_fields = ['is_returned']

    def create(self, validated_data):
        book_copy = validated_data.pop('book_copy')
        validated_data['book'] = book_copy
        return super().create(validated_data)

class LibraryReturnSerializer(serializers.Serializer):
    book_copy = serializers.PrimaryKeyRelatedField(queryset=BookCopy.objects.all(), write_only=True)

    def create(self, validated_data):
        validated_data['library'] = self.context.pop('library')
        book_copy, error = library_service.return_book(**validated_data)

        if error:
            raise serializers.ValidationError(error)
        return book_copy


class RackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rack
        fields = "__all__"

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"