
from django.urls import path
from blogapp import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('change-password/', auth_views.PasswordChangeView.as_view(success_url = reverse_lazy('password_changed')), name='change-password'),
    path('', views.index, name='index'),
    path('signin', views.user_signin, name='signin'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('password_changed/', views.password_changed, name='password_changed'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('post/<int:id>/', views.view_post, name='post'),
    path('delete_com/<int:id>/', views.delete_com, name='delete'),
    path('edit_comment/<int:id>/', views.edit_comment, name='edit'),
    path('create_post', views.create_post, name='create_post'),
    path('message/<int:id>/', views.message, name='message')

]
