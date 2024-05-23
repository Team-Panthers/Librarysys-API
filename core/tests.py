from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, BookCopy, Library, Rack, Author, Publisher

class LibraryTestCase(TestCase):
    def setUp(self):
        self.library = Library.objects.create(name="library1", no_of_rack=4)

    def test_rack_created(self):
        racks = Rack.objects.all().count()
        self.assertEqual(racks, 4)


class AddBookViewTest(APITestCase):
    def setUp(self):
        self.library = Library.objects.create(name="library1", no_of_rack=4)

    def test_add_book(self):
        url  = reverse("add-book", kwargs={"library_id":self.library.id})
        data = {
                "title": "Hello World",
                "authors": [
                    {"first_name": "Fola", "last_name": "David"},
                    {"first_name": "Fola2", "last_name": "David"}
                ],
                "publisher": {
                    "name": "Fola"
                },
                "bookcopy": [
                    {"bookcopy_id": "24"},
                    {"bookcopy_id": "41"}
                ]
            }
        response = self.client.post(url, data, format='json')
        book = Book.objects.first()
        bookcopy = BookCopy.objects.filter(library=self.library).first()

        self.assertEqual(bookcopy.rack, Rack.objects.filter(library=self.library).first())
        
        self.assertIsNotNone(book) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

    def test_racks_less_than_bookcopies(self):
            url  = reverse("add-book", kwargs={"library_id":self.library.id})
            data = {
                    "title": "Hello World",
                    "authors": [
                        {"first_name": "Fola", "last_name": "David"},
                        {"first_name": "Fola2", "last_name": "David"}
                    ],
                    "publisher": {
                        "name": "Fola"
                    },
                    "bookcopy": [
                        {"bookcopy_id": "24"},
                        {"bookcopy_id": "41"},
                        {"bookcopy_id": "44"},
                        {"bookcopy_id": "34"},
                        {"bookcopy_id": "46"}
                    ]
                }
            response = self.client.post(url, data, format='json')
            bookcopy = BookCopy.objects.filter(library=self.library).last()
            count = BookCopy.objects.filter(library=self.library).count()
            
            with self.assertRaises(Rack.DoesNotExist):
                Rack.objects.get(library=self.library, book_copy=bookcopy)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)