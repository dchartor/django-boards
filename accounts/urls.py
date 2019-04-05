from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as auth_views


from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.txt',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url=reverse_lazy('accounts:password_reset_done')),
        name='password_reset'),

    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),

    re_path(r'^reset/'
            r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}'
            r'-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url=reverse_lazy('accounts:password_reset_complete')),
            name='password_reset_confirm'),

    re_path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name='password_reset_complete'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url=reverse_lazy('accounts:password_change_done')),
        name='password_change'),
        
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'),
        name='password_change_done'),
]
