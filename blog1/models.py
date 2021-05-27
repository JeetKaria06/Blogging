from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(default="")
    slugtitle = models.SlugField(default="")
    
    def slug(self):
        return slugify(self.title) 

class Author(models.Model):
    username = models.CharField(primary_key=True, max_length=500)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    articles = models.ManyToManyField(Article)