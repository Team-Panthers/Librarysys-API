from rest_framework import serializers

from .models import Book,BookBorrow,BookCopy


class BookSerializer(serializers.ModelSerializer):
    copies_left = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Book
        fields = "__all__"

    def get_copies_left(self, obj):
        return BookCopy.objects.filter(book=obj,is_borrowed=False).count()

class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrow
        fields = "__all__"

class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = "__all__"