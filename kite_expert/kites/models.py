from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Expert(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self): # для отображения записей БД
        return reverse('expert', kwargs={'slug': self.name})


class Kite(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    expert = models.ForeignKey(User, on_delete=models.PROTECT)
    photo1 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo2 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo3 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo4 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_kiteedit_url(self): # для отображения записей БД
        return reverse('kiteedit', kwargs={'slug': self.pk})
    
    def get_kitedel_url(self):
        return reverse('kitedel', kwargs={'slug': self.name, 'id': self.pk})

    def get_expert_url(self):
        return reverse('expert', kwargs={'slug': self.expert})
    
    # def save(self, *args, **kwargs):
    #     if self.photo1:
    #         self.photo1 = resize_image(self.photo1)
    #     super(Kite, self).save(*args, **kwargs)
    

class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self): # для отображения записей БД
        return reverse('brand', kwargs={'slug': self.name})
