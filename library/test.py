"""
This file is written for Unit testing of this project.
"""
import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from library.views import (book_available , BookPresence, Student, Book,
                                ReturnBook, BorrowBook, BookDetail)
from .models import Books as BookModel, Student as StudentModel, Borrower as BorrowerModel


class TestBookGet(TestCase):
    """
    Test class for Book View.
    """
    def setUp(self):
        """
        SetUp function.
        """
        self.factory=APIRequestFactory()

    def test1(self):
        """
        Unit test to check if the book is added to the library.
        """
        exp ={'status':True, 'message':"Book is added to the library"}
        view = Book.as_view()
        request= self.factory.get('/book/?book_name=b5&total_copies=2')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test2(self):
        """
        Unit test to check if the book is already present in the library.
        """
        exp ={'status':False,'message':"Book is already in the database."}
        BookModel.objects.create(book_name= "b7", total_copies= 2)
        view = Book.as_view()
        request= self.factory.get('/book/?book_name=b7&total_copies=2')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        BookModel.objects.all().delete()
        self.assertEqual(data_dic, exp)


class TestStudentGet(TestCase):
    """
    Test Class for Student View.
    """
    def setUp(self):
        """
        SetUp function.
        """
        self.factory =APIRequestFactory()

    def test1(self):
        """
        Unit test to check if the student is added to the library.
        """
        exp={'status':True, 'message':"Student is added to the library database"}
        view = Student.as_view()
        request= self.factory.get('/student/?student_name=student122&student_id=122')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test2(self):
        """
        Unit test to check if the student is already present in the database.
        """
        exp={'status':False, 'message':"Student is already present in the database"}
        StudentModel.objects.create(student_name= "student122", student_id= "122")
        view = Student.as_view()
        request= self.factory.get('/student/?student_name=student122&student_id=122')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        StudentModel.objects.all().delete()
        self.assertEqual(data_dic, exp)



class TestBookAvailableGet(TestCase):
    """
    Test Class for book availability function.
    """
    def setUp(self):
        """
        SetUp function.
        """
        self.factory =APIRequestFactory()

    def test1(self):
        """
        Unit test to check if the book is available or not.
        """
        exp={'status':False, 'message':"Book is not available."}
        request= self.factory.get('/book_availability/?book_name=book5')
        actual= book_available(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test2(self):
        """
        Unit test to check book is available in the library and you can issue it.
        """
        exp={'status':True, 'message':"Books is available.You can issue it."}
        BookModel.objects.create(book_name= "b2", total_copies= 2)
        request= self.factory.get('/book_availability/?book_name=b2')
        actual= book_available(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        BookModel.objects.all().delete()
        self.assertEqual(data_dic, exp)

    def test3(self):
        """
        Unit test to check book is available in the library, but you cannot issue it.
        """
        exp={'status':False, 'message':"Book is not available in the library."}
        BookModel.objects.create(book_name= "b2", total_copies= 0)
        request= self.factory.get('/book_availability/?book_name=b2')
        actual= book_available(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        BookModel.objects.all().delete()
        self.assertEqual(data_dic, exp)


class TestBookPresenceGET(TestCase):
    """
    Test Class for Book presence view.
    """
    def setUp(self):
        """
        SetUp function.
        """
        self.factory =APIRequestFactory()

    def test1(self):
        """
        Unit test to check book is not present in the library.
        """
        exp={'status':False, 'message':"The book is not present in the library"}
        view= BookPresence.as_view()
        request= self.factory.get('/book_presence/?book_name=book12')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test2(self):
        """
        Unit test to check book is present in the library.
        """
        exp={'status':True, 'message':"The book is present in the library"}
        BookModel.objects.create(book_name= "b2", total_copies= 2)
        view= BookPresence.as_view()
        request= self.factory.get('/book_presence/?book_name=b2')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        BookModel.objects.all().delete()
        self.assertEqual(data_dic, exp)



class TestReturnBookGet(TestCase):
    """
    Test class for Return Book View.
    """
    def setUp(self):
        """
        SetUp function.
        """
        self.factory=APIRequestFactory()

    def test1(self):
        """
        Unit test to check book id is not valid. Book is not present in the library.
        """
        exp={'status':False, 'message':"Book not present in the Library"}
        view= ReturnBook.as_view()
        request= self.factory.get('/returnbook/?book_id=12&student_id=121')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)


    def test2(self):
        """
        Unit test to check if the student id is not valid. Student is not present in the database.
        Also work well when book id is valid.
        """
        exp={'status':False, 'message':"Can't find the student with the given ID"}
        book=BookModel.objects.create(book_name="book5", total_copies=12)
        ids= book.id
        view= ReturnBook.as_view()
        request= self.factory.get(f'/returnbook/?book_id={ids}&student_id=121')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        BookModel.objects.all().delete()
        StudentModel.objects.all().delete()
        self.assertEqual(data_dic, exp)


    def test3(self):
        """
        Unit test to check if that the book is returned when student name and user name are valid.
        It work when both book id and student id is valid.
        """
        exp={'status':True, 'message':'Book is returned'}
        book=BookModel.objects.create(book_name= "b10", total_copies= 2)
        student=StudentModel.objects.create( student_name= "stu11",student_id= "121" )
        view= ReturnBook.as_view()
        request= self.factory.get(f'/returnbook/?book_id={book.id}&student_id={student.id}')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        BookModel.objects.all().delete()
        StudentModel.objects.all().delete()
        self.assertEqual(data_dic, exp)


class TestBorrowBookGet(TestCase):
    """
    Test Class for Borrow Book view.
    """
    def setUp(self):
        """
        SetUp function.
        """
        self.factory =APIRequestFactory()

    def test1(self):
        """
        Unit test to check book is not present in the library.
        """
        exp={'status':False, 'message':"Can't issue the book"}
        view= BorrowBook.as_view()
        request= self.factory.get('/borrowbook/?book_id=12&studentid=121')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test2(self):
        """
        Unit test to check if the student id is not valid. Student is not present in the database.
        Also work well when book id is valid.
        """
        exp={'status':False, 'message':"Can't find the student with the given ID"}
        book=BookModel.objects.create(book_name="b5", total_copies=12)
        view= BorrowBook.as_view()
        request= self.factory.get(f'/borrowbook/?book_id={book.id}&studentid=121')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        BookModel.objects.all().delete()
        StudentModel.objects.all().delete()
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test3(self):
        """
        Unit test to check if the book is issued.
        """
        exp ={'status':True, 'message':"Book is issued"}
        book=BookModel.objects.create(book_name= "b11", total_copies= 1)
        student=StudentModel.objects.create(student_name= "stu11",student_id= "121")
        view= BorrowBook.as_view()
        request= self.factory.get(f'/borrowbook/?book_id={book.id}&studentid={student.id}')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        BookModel.objects.all().delete()
        StudentModel.objects.all().delete()
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test4(self):
        """
        Unit test to check when book is out of stock.
        """
        exp = {'status':False, 'message':"Books out of stock"}
        book=BookModel.objects.create(book_name= "b13", total_copies= 0)
        student=StudentModel.objects.create( student_name= "stu11",student_id= "121" )
        view= BorrowBook.as_view()
        request= self.factory.get(f'/borrowbook/?book_id={book.id}&studentid={student.id}')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        BookModel.objects.all().delete()
        StudentModel.objects.all().delete()
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test5(self):
        """
        Unit test to show that user cannot issue the same book more than once.
        """
        exp={'status':False, 'message':"The book is already issued by this student"}
        book=BookModel.objects.create(book_name= "b14", total_copies= 2)
        student=StudentModel.objects.create( student_name= "stu11",student_id= "121" )
        view= BorrowBook.as_view()
        request=self.factory.get(f'/borrowbook/?book_id={book.id}&studentid={student.id}')
        request_again= self.factory.get(f'/borrowbook/?book_id={book.id}&studentid={student.id}')
        view(request)
        actual= view(request_again)
        data = actual.content
        data_string = data.decode('utf-8')
        BookModel.objects.all().delete()
        StudentModel.objects.all().delete()
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)


class TestBookDetailGet(TestCase):
    """
    Test Class to check the Book Detail view.
    """
    def setUp(self):
        """
        SetUp function.
        """
        self.factory =APIRequestFactory()

    def test1(self):
        """
        Unit test to check if the book is not present in the library.
        """
        exp={'status':False, 'message':"Book not found"}
        view = BookDetail.as_view()
        request= self.factory.get('/book_detail/?book_name=book5')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)

    def test2(self):
        """
        Unit test to display student list who has issued the book.
        """
        exp={'status':True, 'message':['abc']}
        student_detail= StudentModel.objects.create(student_name= "abc", student_id= "121" )
        borrow_detail= BorrowerModel.objects.create(student= student_detail.id)
        borrow_detail.book.create(book_name= "b10", total_copies= 2)
        view = BookDetail.as_view()
        request= self.factory.get('/book_detail/?book_name=b10')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        StudentModel.objects.all().delete()
        BorrowerModel.objects.all().delete()
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)


    def test3(self):
        """
        Unit test to check when no student has issued this book.
        """
        exp={"status":False, 'message':"No student has borrowed this book"}
        BookModel.objects.create(book_name="b20", total_copies=2)
        view = BookDetail.as_view()
        request= self.factory.get('/book_detail/?book_name=b20')
        actual= view(request)
        data = actual.content
        data_string = data.decode('utf-8')
        BookModel.objects.all().delete()
        data_dic = json.loads(data_string)
        self.assertEqual(data_dic, exp)
