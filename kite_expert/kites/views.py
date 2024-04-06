from typing import Dict, List

from django.contrib.auth import logout  # login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from kite_expert.settings import PROFILE_IMAGE, USER_IS_ACTIVE
from kites import forms, models, utils

from .tasks import resize_photo_expert, resize_photo_kite


class Index(utils.DataMixin, ListView):
    template_name = "kites/index.html"
    title_page = "All kites"

    def get_queryset(self):
        return (
            models.Kite.objects.values("name", "slug")
            .filter(is_published=True)
            .distinct()
        )


class Brand(utils.DataMixin, ListView):
    template_name = "kites/index.html"
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(title=context["object_list"][0]["brand__name"])
        return context

    def get_queryset(self) -> Dict:
        slug = self.kwargs["slug"]
        return (
            models.Kite.objects.values("name", "brand__name", "slug")
            .filter(brand__slug=slug, is_published=True)
            .distinct()
        )


class Kite(utils.DataMixin, ListView):
    template_name = "kites/kite.html"
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            title=context["object_list"][0].name,
            brand=context["object_list"][0].brand.name,
        )
        return context

    def get_queryset(self) -> List[models.Kite]:
        return (
            models.Kite.objects.filter(slug=self.kwargs["slug"], is_published=True)
            .order_by("time_create")
            .select_related("user")
        )


class KiteAdd(LoginRequiredMixin, utils.DataMixin, CreateView):
    form_class = forms.KiteForm
    template_name = "kites/form_cycle_for.html"
    title_page = "Add kite"

    def form_valid(self, form):
        form.instance.user = self.request.user
        kite = form.save()
        resize_photo_kite.delay(kite.pk)
        cache.clear()
        return super().form_valid(form)
        # auto redirect to get_absolute_url in models.Kite
        # return redirect(reverse_lazy('kites:kite', kwargs={'slug': form.instance.slug}))


class KiteEdit(LoginRequiredMixin, UserPassesTestMixin, utils.DataMixin, UpdateView):
    model = models.Kite
    form_class = forms.KiteForm
    template_name = "kites/form_cycle_for.html"
    title_page = "Edit kite"

    def test_func(self):
        return self.request.user.id == self.get_object().user_id

    def get_success_url(self):
        # cache.clear()  # если не ипользуется метод form_valid (без celery)
        if self.object.is_published:
            return reverse_lazy("kites:kite", kwargs={"slug": self.object.slug})
        return reverse_lazy("kites:profile") + "#" + self.object.slug

    def form_valid(self, form):
        kite = form.save()
        resize_photo_kite.delay(kite.pk)
        cache.clear()
        return super().form_valid(form)


@login_required
def kite_del(request, id):
    kite = models.Kite.objects.get(pk=id)
    if request.user.id == kite.user_id:
        kite.delete()
        cache.clear()
    return redirect("kites:home")
    # return redirect(request.GET.get('next', 'kites:home'))


class Expert(utils.DataMixin, ListView):
    template_name = "kites/expert.html"
    title_page = "Experts"
    extra_context = {"profile_image": PROFILE_IMAGE}

    def get_queryset(self):
        if self.kwargs.get("slug"):
            return models.Expert.objects.filter(user__username=self.kwargs["slug"])
        return models.Expert.objects.all().select_related("user")


class UserRegTest(utils.DataMixin, FormView):
    form_class = forms.UserRegTestForm
    template_name = "kites/form_cycle_for.html"
    title_page = "Register Test"
    extra_context = {"comment": "Заполни форму кириллицей"}

    def form_valid(self, form):
        return redirect("kites:register", tk=utils.get_token())


class UserRegister(UserPassesTestMixin, utils.DataMixin, CreateView):
    form_class = forms.UserRegisterForm
    template_name = "kites/form_cycle_for.html"
    success_url = reverse_lazy("kites:login")
    title_page = "Register"

    def test_func(self):
        return self.kwargs["tk"] == utils.get_token()

    def form_valid(self, form):
        "метод вызывается при успешной отправке формы"
        if USER_IS_ACTIVE:
            user = form.save()
            # login(self.request, user) # автологин
        else:  # деактивация пользователя
            form.instance.is_active = False
            user = form.save()
        models.Expert.objects.create(user=user)  # создание эксперта для юзера
        return super().form_valid(form)


class UserLogin(utils.DataMixin, LoginView):
    form_class = forms.UserLoginForm
    template_name = "kites/form_cycle_for.html"
    title_page = "Login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        href = reverse_lazy("kites:password_reset")
        context.update(bottom=f'<br><a href="{href}">I forgot my password</a>')
        return context

    def get_success_url(self):
        cache.clear()
        return reverse_lazy("kites:profile")


class UserProfile(LoginRequiredMixin, utils.DataMixin, DetailView):
    # model = models.Expert  # замена на queryset
    queryset = models.Expert.objects.select_related("user")
    template_name = "kites/profile.html"
    title_page = "Profile"
    extra_context = {"profile_image": PROFILE_IMAGE}

    def get_object(self):
        return models.Expert.objects.get(user=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            user_kites=models.Kite.objects.filter(user=self.request.user.id)
            .order_by("is_published", "brand")
            .select_related("brand")
        )
        return context


class UserProfileEdit(LoginRequiredMixin, utils.DataMixin, UpdateView):
    model = models.Expert
    form_class = forms.ExpertForm
    template_name = "kites/form_cycle_for.html"
    slug_field = "user__username"
    title_page = "Edit profile"

    def get_object(self):
        return models.Expert.objects.get(user=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy("kites:profile")

    def form_valid(self, form):
        expert = form.save()
        resize_photo_expert.delay(expert.pk)
        return super().form_valid(form)


class UserPasswordChange(LoginRequiredMixin, utils.DataMixin, PasswordChangeView):
    form_class = forms.UserPasswordChangeForm
    success_url = reverse_lazy("kites:profile")
    template_name = "kites/form_cycle_for.html"
    title_page = "Password change"


def user_logout(request):
    logout(request)
    cache.clear()
    return redirect("kites:home")
