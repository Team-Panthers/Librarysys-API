from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Book,BookBorrow,BookCopy,Publisher,Author

User = get_user_model()
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
        
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id", "email")


class BorrowBookSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BookBorrow
        fields = ["id","due_date","is_overdue","user"]

      
class BookCopyDetailSerializer(serializers.ModelSerializer):
    borrowed_by = serializers.SerializerMethodField()
    book = BookSerializer()
    class Meta:
        model = BookCopy
        fields = "__all__"  
        
    def get_borrowed_by(self,obj):
        book_borrow = obj.borrow.all()
        book_borrow = book_borrow.filter(library=obj.library,is_returned=False).first()
        data = BorrowBookSerializer(book_borrow).data
        return data
        
        