from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm, 
    PasswordChangeForm)
from django.utils.text import slugify
# from django.db.models.fields.files import ImageFieldFile

from kites import models
# from kite_expert.settings import MAX_IMAGE_SIZE


class ThumbnailImageInput(forms.widgets.ClearableFileInput):
    template_name = 'overrides/clearable_file_input.html'


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100, label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(max_length=255, label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(max_length=100, label='Pass1', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(max_length=100, label='Pass2', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # first_name = forms.CharField(max_length=100, label='Nickname', widget=forms.TextInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        "проверка уникальности поля email"
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой почтовый адрес уже существует.')
        return email


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Pass', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label='New Pass1', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label='New Pass2', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class BrandForm(forms.ModelForm):
    def clean_name(self):
        return self.cleaned_data["name"].upper()
    
    def clean_slug(self):
        return slugify(self.cleaned_data["name"])


class ExpertForm(forms.ModelForm):

    class Meta:
        model = models.Expert
        fields = ['about', 'photo']
        widgets = {
            'photo': ThumbnailImageInput,
        }

# для сжатия фото до сохранения на диск:

#     def clean_photo(self):
#         img = self.cleaned_data.get('photo')
#         return resize_image(img)


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
    
# для сжатия фото до сохранения на диск:

    # def clean_photo1(self):
    #     img = self.cleaned_data.get('photo1')
    #     return resize_image(img)
    
    # def clean_photo2(self):
    #     img = self.cleaned_data.get('photo2')
    #     return resize_image(img)
    
    # def clean_photo3(self):
    #     img = self.cleaned_data.get('photo3')
    #     return resize_image(img)
    
    # def clean_photo4(self):
    #     img = self.cleaned_data.get('photo4')
    #     return resize_image(img)


# def resize_image(image):
#     from io import BytesIO
#     from django.core.files.base import ContentFile
#     from django.core.files.uploadedfile import InMemoryUploadedFile
#     from PIL import Image

#     if not image or isinstance(image, ImageFieldFile):
#         return image
    
#     im = Image.open(BytesIO(image.read()))

#     max_size = MAX_IMAGE_SIZE
#     w, h = im.size
#     format = im.format
        
#     cut = abs(w - h) // 2
#     if w >= h: 
#         box = (cut, 0, w - cut, h)
#     else: 
#         box = (0, cut, w, h - cut)
#     im = im.crop(box=box)
#     if im.width > max_size:
#         im = im.resize(size=(max_size, max_size))

#     new_image = BytesIO()
#     im.save(new_image, format=format)
#     new_image = ContentFile(new_image.getvalue())
#     return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)
        
