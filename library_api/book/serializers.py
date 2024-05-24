from rest_framework import serializers

from .models import Book,BookBorrow,BookCopy


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        
class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookBorrow
        fields = "__all__"

class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = "__all__"