from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User


class Expert(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    about = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    # slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    
    def __str__(self) -> str:
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('expert', kwargs={'slug': self.user})


class Kite(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, verbose_name='URL')
    text = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT)
    expert = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    photo1 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo2 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo3 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo4 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('kite', kwargs={'slug': self.slug})
    
    def get_kiteedit_url(self):
        return reverse('kiteedit', kwargs={'pk': self.pk})
    
    def get_kitedel_url(self):
        return reverse('kitedel', kwargs={'id': self.pk})

    def get_expert_url(self):
        return reverse('expert', kwargs={'slug': self.expert})
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name',]
    
    
class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('brand', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name',]
