from django.urls import path

from kites import views


urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('index/', views.Index.as_view(), name='home'),
    path('register/', views.UserRegister.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('brand/<slug:slug>/', views.Brand.as_view(), name='brand'),

    path('kite/add/', views.AddKite.as_view(), name='addkite'),
    path('kite/edit/<int:pk>/', views.KiteEdit.as_view(), name='kiteedit'),
    path('kite/del/<int:id>', views.kite_del, name='kitedel'),
    path('kite/<slug:slug>/', views.Kite.as_view(), name='kite'),

    path('expert/', views.Expert.as_view(), name='experts'),
    path('expert/<slug:slug>/', views.Expert.as_view(), name='expert'),

    path('profile/edit/<slug:slug>/', views.ExpertEdit.as_view(), name='expertedit'),
    path('profile/<slug:slug>/', views.UserProfile.as_view(), name='profile'),
]