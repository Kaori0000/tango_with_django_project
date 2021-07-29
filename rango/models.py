from threading import TIMEOUT_MAX
from django.db import models
from django.template.defaultfilters import slugify #import the function slugify from Django

# Create your models here.

#create a Category class that inherit from Model class
class Category(models.Model):
    NAME_MAX_LENGTH = 128 #to avoid repeating the code

    #the class attribute name is made of chars with max length = 128, and it's unique 
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True) 
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    #adding a nested Meta class with verbose_name_plural attribute to fix the typo on the Django administraion interface
    class Meta: 
        verbose_name_plural = 'Categories'

    def __str__(self): #toString
        return self.name




#create a Page class that inherit from Model class
class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

     # Category and Page have a 1:M relationthip, thus model.ForeignKey
      # delete the Page associated with the Category, when Category is deleted 
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default= 0)

    def __str__(self):
        return self.title
