================
django-import-excel
================

django-import-excel - App for load data from excel (a excel file load on django form)

Settings
=========

INSTALLED_APPS = [
     ...
     'import_excel',
     ...
]

Example
=============

Model:

    class Book(models.Model):
    
        name = models.CharField(max_length=255)
        author = models.CharField(max_length=255)

Excel File:

name | author
Tom Sawyer | Mark Twain
The Sands of Mars | Arthur C. Clarke

Form:

    class BookImportForm(ImportExcelForm):
    
        @transaction.autocommit
        def update_callback(self, request, converted_items):
             for book_item in converted_items[:1]:
                  name = book_item[0]
                  author = book_item[1]
                  Book.objects.create(name=name, author=author)

urls.py:

    urlpatterns = patterns('',
          url(r'^/books/import-from-excel/$', permission_required('books.add_book')(import_excel), {
                 'FormClass': BookImportForm, 'next_url': '/books/', 'with_good': True, 'template_name': 'import_excel/import_excel.html',
          }, name='book-import-excel'),
    ),

