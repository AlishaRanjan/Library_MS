"""
Url file.
"""
from django.urls import path
from django.views.decorators.cache import cache_page
from library.views import Book, Student, BookDetail , ReturnBook, BorrowBook, BookPresence
from library.views import book_available

urlpatterns = [
    path('book_availability/',cache_page(60*60)(book_available)),
    path('book_presence/',cache_page(60*60)(BookPresence.as_view())),
    path('book/',Book.as_view()),
    path('student/', Student.as_view()),
    path('returnbook/', ReturnBook.as_view()),
    path('borrowbook/', BorrowBook.as_view()),
    path('book_detail/',BookDetail.as_view()),
]
