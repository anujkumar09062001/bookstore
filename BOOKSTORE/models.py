from django.db import models

# Create your models here.

class book(models.Model):
    DEFAULT = 'default.png'

    name = models.CharField(max_length=50, default="")
    bookname = models.CharField(max_length=50, default="")
    description = models.CharField(max_length=200)
    email_id = models.EmailField(max_length=200)
    picture = models.ImageField(upload_to='img', max_length=200, null=True, blank=True, default=DEFAULT)

    def __str__(self):
        return f'{self.bookname} : {self.description}'