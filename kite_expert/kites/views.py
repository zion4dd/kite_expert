from typing import Any, Dict, List

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.cache import cache

from kites import models
from kites import utils
from kites import forms
from .tasks import resize_photo_kite, resize_photo_expert

from kite_expert.settings import USER_IS_ACTIVE


class Index(utils.DataMixin, ListView):
    template_name = 'kites/index.html'
    title_page = 'All kites'

    def get_queryset(self):
        return models.Kite.objects.values('name', 'slug')\
                                  .filter(is_published=True)\
                                  .distinct()


class Brand(utils.DataMixin, ListView):
    template_name = 'kites/index.html'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title=context['object_list'][0]['brand__name'])
        return context

    def get_queryset(self) -> Dict:
        slug = self.kwargs['slug']
        return models.Kite.objects.values('name', 'brand__name', 'slug')\
                                  .filter(brand__slug=slug, is_published=True)\
                                  .distinct()
    

class Kite(utils.DataMixin, ListView):
    template_name = 'kites/kite.html'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title=context['object_list'][0].name, 
                       brand=context['object_list'][0].brand.name)
        return context

    def get_queryset(self) -> List[models.Kite]:
        return models.Kite.objects.filter(slug=self.kwargs['slug'], 
                                          is_published=True)\
                                  .order_by('time_create')\
                                  .select_related('expert')


class KiteAdd(LoginRequiredMixin, utils.DataMixin, CreateView):
    form_class = forms.KiteForm
    template_name = 'kites/form_cycle_for.html'
    title_page = 'Add kite'
    
    def form_valid(self, form):
        form.instance.expert = self.request.user
        kite = form.save()
        resize_photo_kite.delay(kite.pk)
        cache.clear()
        return super().form_valid(form)
        # auto redirect to get_absolute_url in models.Kite
        # return redirect(reverse_lazy('kite', kwargs={'slug': form.instance.slug}))


class KiteEdit(LoginRequiredMixin, UserPassesTestMixin, utils.DataMixin, UpdateView):
    model = models.Kite
    form_class = forms.KiteForm
    template_name = 'kites/form_cycle_for.html'
    title_page = 'Edit kite'

    def test_func(self):
        return self.request.user.id == self.get_object().expert_id
    
    def get_success_url(self):
        # cache.clear()  # если не ипользуется метод form_valid (без celery)
        if self.object.is_published:
            return reverse_lazy('kite', kwargs={'slug': self.object.slug})
        return reverse_lazy('profile') + '#' + self.object.slug
    
    def form_valid(self, form):
        kite = form.save()
        resize_photo_kite.delay(kite.pk)
        cache.clear()
        return super().form_valid(form)


@login_required
def kite_del(request, id):
    kite = models.Kite.objects.get(pk=id)
    if request.user.id == kite.expert_id:
        kite.delete()
        cache.clear()
    return redirect('home')
    # return redirect(request.GET.get('next', 'home'))

    
class Expert(utils.DataMixin, ListView):
    template_name = 'kites/expert.html'
    title_page = 'Experts'

    def get_queryset(self):
        if self.kwargs.get('slug'):
            return models.Expert.objects.filter(user__username=self.kwargs['slug'])
        return models.Expert.objects.all().select_related('user')


class UserRegister(utils.DataMixin, CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'kites/form_cycle_for.html'
    success_url = reverse_lazy('login')
    title_page = 'Register'
    
    def form_valid(self, form):
        'метод вызывается при успешной отправке формы'
        if USER_IS_ACTIVE:
            user = form.save()
            # login(self.request, user) # автологин
        else: # деактивация пользователя
            form.instance.is_active = False
            user = form.save()
        models.Expert.objects.create(user=user) # создание эксперта для юзера
        return super().form_valid(form)
    

class UserLogin(utils.DataMixin, LoginView):
    form_class = forms.UserLoginForm
    template_name = 'kites/form_cycle_for.html'
    title_page = 'Login'
    
    def get_success_url(self):
        cache.clear()
        return reverse_lazy('profile')


class UserProfile(LoginRequiredMixin, utils.DataMixin, DetailView):
    # model = models.Expert  # замена на queryset
    queryset = models.Expert.objects.select_related('user')
    template_name = 'kites/profile.html'
    title_page = 'Profile'

    def get_object(self):
        return models.Expert.objects.get(user=self.request.user.pk)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(expert_kites=models.Kite.objects\
                                            .filter(expert=self.request.user.id)\
                                            .order_by('is_published', 'brand')\
                                            .select_related('brand'))
        return context


class UserProfileEdit(LoginRequiredMixin, utils.DataMixin, UpdateView):
    model = models.Expert
    form_class = forms.ExpertForm
    template_name = 'kites/form_cycle_for.html'
    slug_field = 'user__username'
    title_page = 'Edit profile'
    
    def get_object(self):
        return models.Expert.objects.get(user=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        expert = form.save()
        resize_photo_expert.delay(expert.pk)
        return super().form_valid(form)


class UserPasswordChange(LoginRequiredMixin, utils.DataMixin, PasswordChangeView):
    form_class = forms.UserPasswordChangeForm
    success_url = reverse_lazy('profile')
    template_name='kites/form_cycle_for.html'
    title_page = "Password change"


def user_logout(request):
    logout(request)
    cache.clear()
    return redirect('home')

