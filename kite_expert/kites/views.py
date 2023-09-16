from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
# from django.utils.text import slugify

from kites import models
from kites import utils
from kites import forms


class Index(utils.DataMixin, ListView):
    model = models.Kite
    template_name = 'kites/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='All kites')
        return context | context_user

    def get_queryset(self):
        return models.Kite.objects\
            .values('name')\
                .filter(is_published=True)\
                    .distinct()
    

class Brand(utils.DataMixin, ListView):
    model = models.Kite
    template_name = 'kites/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = context['object_list'][0]
        context_user = self.get_user_context(title=c['brand__name'], 
                                            brand_selected=c['brand_id'],
                                            )
        return context | context_user

    def get_queryset(self):
        return models.Kite.objects\
            .values('name', 'brand', 'brand_id', 'brand__name')\
                .distinct()\
                    .filter(brand__name=self.kwargs['slug'], is_published=True)


class Kite(utils.DataMixin, ListView):
    model = models.Kite
    template_name = 'kites/kite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c = context['object_list'][0]
        context_user = self.get_user_context(title=c.name,
                                             brand_selected=c.brand_id,
                                             )
        return context | context_user

    def get_queryset(self):
        return models.Kite.objects.filter(name=self.kwargs['slug'], 
                                        is_published=True
                                        )#.select_related('expert')


class AddKite(LoginRequiredMixin, utils.DataMixin, CreateView):
    form_class = forms.KiteForm
    template_name = 'kites/form_as_p.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Add kite')
        return context | context_user
    
    def form_valid(self, form):
        form.instance.expert = self.request.user
        form.save()
        return redirect('home')


class KiteEdit(LoginRequiredMixin, utils.DataMixin, UpdateView):
    model = models.Kite
    form_class = forms.KiteForm
    template_name = 'kites/form_as_p.html'
    slug_field = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Kite edit')
        return context | c_def
    
    def get_success_url(self):
        return reverse_lazy('home')

    
class Expert(utils.DataMixin, ListView):
    model = models.Expert
    template_name = 'kites/expert.html'
    # slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Experts')
        return context | context_user

    def get_queryset(self):
        # print(self.kwargs.get('slug'))
        if self.kwargs.get('slug'):
            return models.Expert.objects\
                .filter(name__username=self.kwargs['slug'])#.select_related('expert')
        return models.Expert.objects.all()


class ExpertEdit(LoginRequiredMixin, utils.DataMixin, UpdateView):
    model = models.Expert
    template_name = 'kites/form_as_p.html'
    slug_field = 'name__username'
    fields = ['about', 'photo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Expert edit')
        return context | c_def
    
    def get_success_url(self):
        return reverse_lazy('experts')
    

class UserRegister(utils.DataMixin, CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'kites/form_as_p.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Register')
        return context | context_user

    def form_valid(self, form):
        'метод вызывается при успешной отправке формы и делает автологин'
        print(form.cleaned_data) # данные формы
        # form.instance.is_active = False
        user = form.save()
        'создание эксперта на основе формы юзера'
        models.Expert.objects.create(name=user) # slug=slugify(user) | slug=user.username
        login(self.request, user)
        return redirect('home')
    

class UserLogin(utils.DataMixin, LoginView):
    form_class = forms.UserLoginForm
    template_name = 'kites/form_as_p.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return context | c_def
    
    def get_success_url(self):
        return reverse_lazy('home')


def user_logout(request):
    logout(request)
    return redirect('home')

