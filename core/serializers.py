from rest_framework import serializers
from core.models import Book, BookCopy, Library, Author, Publisher, Rack


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ["id", "name", "no_of_rack"]

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Author
        fields = ["first_name", "last_name"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["name"]


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ["bookcopy_id"]



class AddBookSerializer(serializers.Serializer):
    title = serializers.CharField()
    authors = AuthorSerializer(many=True)
    publisher = PublisherSerializer()
    bookcopy = BookCopySerializer(many=True)

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        publisher_data = validated_data.pop('publisher')
        bookcopy_data = validated_data.pop('bookcopy')
        library = Library.objects.get(id=self.context["library_id"])
        title = validated_data['title']

        publisher, created = Publisher.objects.get_or_create(**publisher_data)
        book = Book.objects.create(title=title, publisher=publisher, library=library)

        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            book.authors.add(author)
        
        lib_racks = library.racks.all()
        for copy_data in bookcopy_data:
            empty_rack = library.racks.filter(book_copy__isnull=True).first()
            bookcopy = BookCopy.objects.create(library=library, **copy_data, book=book)
            if empty_rack:
                empty_rack.book_copy = bookcopy
                empty_rack.save()
            else:
                pass

        book_data = BookSerializer(book).data
        book_data['bookcopy'] = BookCopySerializer(book.copies.all(), many=True).data
        book_data['authors'] = AuthorSerializer(book.authors.all(), many=True).data
        book_data['publisher'] = PublisherSerializer(book.publisher).data


        return book_data
