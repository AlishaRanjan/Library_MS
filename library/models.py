"""
Models.py is used to create Books table, Student table, Borrower table and ThroughModel Table.
"""
from django.db import models

class Books(models.Model):
    """
    Books table is used to store book information.
    It contain two fields:
    book_name: It take book name as input.
    total_copies: It input total number of copies of the book name entered.
    """
    book_name=models.CharField(max_length=200, null=False)
    total_copies = models.IntegerField(default=1)

    def __str__(self):
        return str(self.book_name)


class Student(models.Model):
    """
    Student table is used to store student information.
    It contain two field:
    student_name: It take student name as a input.
    student_id: It take student id as a input.
    """
    student_name = models.CharField(max_length=20, null=False)
    student_id= models.CharField(max_length=10, null=False)

    def __str__(self):
        return str(self.student_name)


class Borrower(models.Model):
    """
    Borrower table is used to store the information of which student bought which book.
    This class contain two field:
    student: It contain those student information who have borrowed a book.
    book: It contain book issued by this student. It is a many to many field refering to Book model.
    """
    student = models.CharField(max_length=20, null=False)
    book = models.ManyToManyField(Books)

    def __str__(self):
        return str(self.student)


class ThroughModel(models.Model):
    """
    ThroughModel is used to implement Borrower table.
    It contain two field:
    borrow: Foregin key to Borrower table
    student: Foregin key to Student table
    """
    borrow= models.ForeignKey(Borrower, on_delete=models.CASCADE)
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    