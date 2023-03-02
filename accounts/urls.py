from django.urls import path, reverse_lazy
from .views import LoginDetailView, RegistrationView, account_detail, logout_user, order_history, \
    success_registration, PasswordsChangeView, PasswordsResetView, PasswordsResetDoneView, \
    PasswordsResetConfirmView, PasswordsResetCompleteView, OrderHistoryView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginDetailView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('success_registration/', success_registration, name='success_registration'),
    path('reset_password/', PasswordsResetView.as_view(), name='reset_password'),
    path('reset_password_send/', PasswordsResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordsResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complate/',
         PasswordsResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('account_detail/', account_detail, name='account_detail'),
    path('change_password/', PasswordsChangeView.as_view(template_name='accounts/change_password.html'),
         name='change_password'),
    path('order_history/', OrderHistoryView.as_view(), name='order_history'),
    path('log_out/', logout_user, name='log_out'),

]
