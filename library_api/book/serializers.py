from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Book,BookBorrow,BookCopy,Publisher,Author
from library.models import Library

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
        
class BookSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id","title",'publisher',"authors"]
        depth = 1

class BorrowBookSerializer2(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = BookBorrow
        fields = ["id","due_date","is_overdue","user"]
        
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ('id', 'name',)
        
class BookCopySerializer2(serializers.ModelSerializer):
    book = BookSerializer2()
    class Meta:
        model = BookCopy
        fields = ['id',"book_copy_id","book"]
        
class BorrowBookSerializer3(serializers.ModelSerializer):
    library = LibrarySerializer()
    book_copy = BookCopySerializer2()
    class Meta:
        model = BookBorrow
        fields = ["due_date","is_overdue","book_copy","library"]
        

      
class BookCopyDetailSerializer(serializers.ModelSerializer):
    borrowed_by = serializers.SerializerMethodField()
    book = BookSerializer()
    class Meta:
        model = BookCopy
        fields = "__all__"  
        
    def get_borrowed_by(self,obj):
        book_borrow = obj.borrow.all()
        book_borrow = book_borrow.filter(library=obj.library,is_returned=False).first()
        data = BorrowBookSerializer2(book_borrow).data
        return data
        
        