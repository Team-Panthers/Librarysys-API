from rest_framework import serializers

from .models import Library
from .services.library_service import library_service




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
    library = serializers.PrimaryKeyRelatedField(queryset=Library.objects.all())
    number_of_copies = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        book, error = library_service.add_book(**validated_data)
        if error:
            raise serializers.ValidationError(error)
        return book
