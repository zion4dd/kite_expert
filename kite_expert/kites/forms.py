from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db.models.fields.files import ImageFieldFile
from django.utils.text import slugify
from django import forms
from django.forms.widgets import ClearableFileInput

from kites import models


class ThumbnailImageInput(ClearableFileInput):
    template_name = 'overrides/clearable_file_input.html'


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Login', widget=forms.TextInput(attrs={'class': 'form-name'}))
    password1 = forms.CharField(max_length=100, label='Pass1', widget=forms.PasswordInput(attrs={'class': 'form-name'}))
    password2 = forms.CharField(max_length=100, label='Pass2', widget=forms.PasswordInput(attrs={'class': 'form-name'}))
    # email = forms.EmailField(max_length=255, label='Email', widget=forms.EmailInput(attrs={'class': 'form-name'}))
    # first_name = forms.CharField(max_length=100, label='Nickname', widget=forms.TextInput(attrs={'class': 'form-name'}))
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-name'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-name'}))


class KiteForm(forms.ModelForm):

    class Meta:
        model = models.Kite
        fields = ['brand', 'name', 'text', 'photo1', 'photo2', 'photo3', 'photo4', 'is_published']
        widgets = {
            'photo1': ThumbnailImageInput,
            'photo2': ThumbnailImageInput,
            'photo3': ThumbnailImageInput,
            'photo4': ThumbnailImageInput,
        }

    def clean_name(self):
        return self.cleaned_data['name'].upper()
    
    def clean_slug(self):
        return slugify(self.cleaned_data['name'])
    
    def clean_photo1(self):
        img = self.cleaned_data.get('photo1')
        return resize_image(img)
    
    def clean_photo2(self):
        img = self.cleaned_data.get('photo2')
        return resize_image(img)
    
    def clean_photo3(self):
        img = self.cleaned_data.get('photo3')
        return resize_image(img)
    
    def clean_photo4(self):
        img = self.cleaned_data.get('photo4')
        return resize_image(img)


class BrandForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data["name"].upper()
    
    def clean_slug(self):
        return slugify(self.cleaned_data["name"])


class ExpertForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = models.Expert
        fields = ['about', 'photo']
        widgets = {
            'photo': ThumbnailImageInput,
        }

    def clean_photo(self):
        img = self.cleaned_data.get('photo')
        return resize_image(img)


def resize_image(image):
    from io import BytesIO
    from django.core.files.base import ContentFile
    from django.core.files.uploadedfile import InMemoryUploadedFile
    from PIL import Image

    if not image or isinstance(image, ImageFieldFile):
        return image
    
    max_size = 1200
    im = Image.open(BytesIO(image.read()))
    w, h = im.size
    format = im.format
        
    cut = abs(w - h) // 2
    if w >= h: 
        box = (cut, 0, w - cut, h)
    else: 
        box = (0, cut, w, h - cut)
    im = im.crop(box=box)
    if im.width > max_size:
        im = im.resize(size=(max_size, max_size))

    new_image = BytesIO()
    im.save(new_image, format=format)
    new_image = ContentFile(new_image.getvalue())
    return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)
        
