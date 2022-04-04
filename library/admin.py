from django.contrib import admin
from .models import Books, Borrower, Student

# Register your models here.

admin.site.register(Books)
admin.site.register(Borrower)
admin.site.register(Student)