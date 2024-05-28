from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from library.services.library_service import library_service
from user.services.user_service import user_service

User = get_user_model()


@shared_task
def send_daily_emails():
    libraries = library_service.all()
    for library in libraries:
        users = user_service.library_users(library)
        for user in users:
            borrowed_books = user_service.get_user_borrowed_books(user, library)
            if borrowed_books:
                book_list = "\n".join([
                                          f"Title: {book.book_copy.book.title},Book_code: {book.book_copy.book_copy_id}, Due Date: {book.due_date}"
                                          for book in borrowed_books])
                message = f"""
                Dear {user.email},

                This is a reminder that you have borrowed books from our library. The books and their due dates are listed below:

                {book_list}

                Please ensure to return them on time to avoid any case.

                Thank you,
                {library.name} Library
                """

                send_mail(
                    'Daily Book Borrowed Reminder',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
from datetime import datetime



@shared_task
def print_time():
    current_time = datetime.now()
    print("Current time:", current_time)
