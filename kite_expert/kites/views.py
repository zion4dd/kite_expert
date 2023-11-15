from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy

from kites import models
from kites import utils
from kites import forms

from kite_expert.settings import USER_IS_ACTIVE


class Index(utils.DataMixin, ListView):
    template_name = 'kites/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='All kites')
        return context | context_user

    def get_queryset(self):
        return models.Kite.objects\
                    .values('name', 'slug')\
                    .filter(is_published=True)\
                    .distinct()
                        

class Brand(utils.DataMixin, ListView):
    BRAND = None
    template_name = 'kites/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title=self.BRAND)
        return context | context_user

    def get_queryset(self):
        slug = self.kwargs['slug']
        kite_set = models.Kite.objects\
                    .values('name', 'brand__name', 'slug')\
                    .filter(brand__slug=slug, is_published=True)\
                    .distinct()
        self.BRAND = kite_set[0]['brand__name'] if kite_set else 'None'
        return kite_set
    
        # self.BRAND = models.Brand.objects.get(slug=slug)
        # return self.BRAND.kite_set.values('name').filter(is_published=True).distinct()
        # return models.Kite.objects.filter(brand=self.BRAND, is_published=True)


class Kite(utils.DataMixin, ListView):
    template_name = 'kites/kite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['object_list']:
            return self.get_user_context(title=self.kwargs['slug'])

        c = context['object_list'][0]
        context_user = self.get_user_context(title=c.name,
                                             brand=c.brand.name)
        return context | context_user

    def get_queryset(self):
        return models.Kite.objects\
                    .filter(slug=self.kwargs['slug'], 
                            is_published=True)\
                    .order_by('time_create')\
                    # .select_related('expert')


class KiteAdd(LoginRequiredMixin, utils.DataMixin, CreateView):
    form_class = forms.KiteForm
    template_name = 'kites/form_cycle_for.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Add kite')
        return context | context_user
    
    def form_valid(self, form):# FIXME to forms.py
        form.instance.expert = self.request.user
        form.save()
        return redirect(reverse_lazy('kite', kwargs={'slug': form.instance.slug}))


class KiteEdit(LoginRequiredMixin, UserPassesTestMixin, utils.DataMixin, UpdateView):
    model = models.Kite
    form_class = forms.KiteForm
    template_name = 'kites/form_cycle_for.html'

    def test_func(self):
        k = models.Kite.objects.get(pk=self.kwargs['pk'])
        return self.request.user.id == k.expert_id
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Kite edit')
        return context | context_user
    
    def get_success_url(self):
        if self.object.is_published:
            return reverse_lazy('kite', kwargs={'slug': self.object.slug})
        return reverse_lazy('profile', kwargs={'slug': self.request.user.username}) + '#' + self.object.slug
    

@login_required
def kite_del(request, id):
    k = models.Kite.objects.get(pk=id)
    if request.user.id == k.expert_id:
        k.delete()
    return redirect(request.GET.get('next', 'home'))

    
class Expert(utils.DataMixin, ListView):
    template_name = 'kites/expert.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Experts')
        return context | context_user

    def get_queryset(self):
        if self.kwargs.get('slug'):
            return models.Expert.objects\
                    .filter(user__username=self.kwargs['slug'])
        return models.Expert.objects.all()


class ExpertEdit(LoginRequiredMixin, UserPassesTestMixin, utils.DataMixin, UpdateView):
    model = models.Expert
    form_class = forms.ExpertForm
    template_name = 'kites/form_cycle_for.html'
    slug_field = 'user__username'
    # fields = ['about', 'photo']

    def test_func(self):
        return self.request.user.username == self.kwargs['slug']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Expert edit')
        return context | context_user
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'slug': self.request.user.username})
    

class UserRegister(utils.DataMixin, CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'kites/form_cycle_for.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Register')
        return context | context_user

    def form_valid(self, form):
        'метод вызывается при успешной отправке формы'
        if USER_IS_ACTIVE:
            user = form.save()
            login(self.request, user) # автологин
        else: # деактивация пользователя
            form.instance.is_active = False
            user = form.save()
        models.Expert.objects.create(user=user) # создание эксперта для юзера
        return redirect('home')
    

class UserLogin(utils.DataMixin, LoginView):
    form_class = forms.UserLoginForm
    template_name = 'kites/form_cycle_for.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title='Login')
        return context | context_user
    
    def get_success_url(self):
        return reverse_lazy('home')


class UserProfile(LoginRequiredMixin, UserPassesTestMixin, utils.DataMixin, DetailView):
    model = models.Expert
    template_name = 'kites/profile.html'
    slug_field = 'user__username'

    def test_func(self):
        return self.request.user.username == self.kwargs['slug']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_user = self.get_user_context(title=self.kwargs['slug'])
        context['expert_kites'] = models.Kite.objects\
                                    .filter(expert=self.request.user.id)\
                                    .order_by('is_published', 'brand')
        return context | context_user


def user_logout(request):
    logout(request)
    return redirect('home')

