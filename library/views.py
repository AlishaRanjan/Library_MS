"""
Views.py contain different function that is to be performed in the tables.
"""
from django.http.response import JsonResponse
from django.db.models import Q
from django.views import View
from .models import (Books as BookModel, Borrower as BorrowerModel, Student as StudentModel)


class Book(View):
    """
    Book class is used to add new book in the Library.
    """
    def get(self,request):
        """Adding the book to the library"""
        book_name = request.GET.get('book_name')
        total_copies = request.GET.get('total_copies')
        _ , created= BookModel.objects.get_or_create(book_name=book_name.lower(),
                                                total_copies=total_copies)
        if created is False:
            return JsonResponse({'status':False,'message':"Book is already in the database."})

        message, status_code = "Book is added to the library", True
        return JsonResponse({'status': status_code, 'message': message})


class Student(View):
    """
    Student class is used to add new student.
    """
    def get(self, request):
        """Adding the student to the library"""
        student_name = request.GET.get('student_name')
        student_id = request.GET.get('student_id')
        _ , created= StudentModel.objects.get_or_create(student_name=student_name.lower(),
                                                        student_id=student_id)
        if created is False:
            return JsonResponse({'status': False, 'message':
                        "Student is already present in the database"})
        message, status_code = "Student is added to the library database", True
        return JsonResponse({'status': status_code, 'message': message})


class BookPresence(View):
    """
    BookPresence class is used to check if the given book is present in the database.
    """
    def get(self, request):
        """Checking if the book is present in the library"""
        book_name = request.GET.get('book_name')
        try:
            BookModel.objects.get(book_name=book_name)
        except BookModel.DoesNotExist:
            return JsonResponse({'status': False, 'message':
                        "The book is not present in the library"})
        return JsonResponse({'status': True, 'message': "The book is present in the library"})


def book_available(request):
    """
    book_available function is used to check if the given book is available in the library
    so that we can issue it.
    """
    book_name = request.GET.get('book_name')
    response={}

    try:
        book_detail=BookModel.objects.get(book_name=book_name)
    except BookModel.DoesNotExist:
        return JsonResponse({'status': False, 'message':
                        "Book is not available."})

    if book_detail.total_copies > 0:
        response={'status':True, 'message':"Books is available.You can issue it."}
    else:
        response={'status':False, 'message':"Book is not available in the library."}
    return JsonResponse(response, safe = False)


def student_verification(student_id):
    """
    A function to return if the student is present in the library database.
    """
    try:
        return StudentModel.objects.get(id=student_id)
    except StudentModel.DoesNotExist:
        return None

def book_verification(book_id):
    """
    A function to return if the book is present in the library database.
    """
    try:
        return BookModel.objects.get(id=book_id)
    except BookModel.DoesNotExist:
        return None


class ReturnBook(View):
    """
    ReturnBook class is used when a book is being returned by a student.
    """
    def get(self, request):
        """
        Returning the book back to the library
        """
        book_id= request.GET.get('book_id')
        student_id= request.GET.get('student_id')
        book_return= book_verification(book_id)
        if book_return is None:
            return JsonResponse({'status':False, 'message':"Book not present in the Library"})

        student_info = student_verification(student_id)
        if student_info is None:
            return JsonResponse({'status':False, 'message':
                        "Can't find the student with the given ID"})

        try:
            get_book_info=BorrowerModel.objects.get(Q(book= book_id) & Q(student= student_id))
        except BorrowerModel.DoesNotExist:
            get_book_info=None

        if get_book_info is not None:
            response={'status':False,'message':'This student has not borrowed the given Book.'}
        else:
            del get_book_info
            book_return.total_copies= book_return.total_copies + 1
            book_return.save()
            response={'status':True, 'message': 'Book is returned'}

        return JsonResponse(response)


class BorrowBook(View):
    """
    BorrowBook class is used when a user want to issue a book from library.
    """
    def get(self, request):
        """
        This function issue the book to the student.
        """
        book_id = request.GET.get('book_id')
        studentid = request.GET.get('studentid')

        book = book_verification(book_id)
        if book is None:
            return JsonResponse({'status': False, 'message': "Can't issue the book"})

        student_info = student_verification(studentid)
        if student_info is None:
            return JsonResponse({'status':False, 'message':
                            "Can't find the student with the given ID"})

        try:
            get_book_info = BorrowerModel.objects.get(Q(book= book_id) & Q(student= studentid))
        except BorrowerModel.DoesNotExist:
            get_book_info=None

        if get_book_info is None:
            book_borrow= BorrowerModel.objects.create(student=studentid)
            book_borrow.book.add(book)
            if book.total_copies >0:
                book.total_copies= book.total_copies - 1
                book.save()
                return JsonResponse({'status': True, 'message': "Book is issued"})
            return JsonResponse({'status': False, 'message': "Books out of stock"})
        return JsonResponse({'status': False, 'message':
                            "The book is already issued by this student"})


class BookDetail(View):
    """
    BookDetail class is used when a user want to know which student has issued the book.
    """
    def get(self,request):
        """
        Function to display those student who has issued this book.
        """
        book_name = request.GET.get('book_name')
        books=None
        try:
            books= BookModel.objects.get(book_name=book_name.lower())
        except BookModel.DoesNotExist:
            return JsonResponse({"status": False, 'message':"Book not found"})

        borrow_book = BorrowerModel.objects.filter(book=books.id)

        response= {'status':False, 'message':
                                "No student has borrowed this book"}
        student_list = []
        for relation in borrow_book:
            student_id = relation.student
            students= StudentModel.objects.get(id=student_id)
            student_list.append(students.student_name)
            response={'status':True, 'message':student_list}
        return JsonResponse(response)
