from django.urls import path
from django.contrib.auth import views as authViews

from authy.views import SignUp, PasswordChange, PasswordChangeDone, EditProfile, like, unlike

urlpatterns = [
    path('profile/edit', EditProfile, name='edit-profile'),
    path('signup/', SignUp, name='signup'),
    path('login/', authViews.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    path('changepassword/', PasswordChange, name='change-password'),
    path('changepassword/done', PasswordChangeDone, name='change-password-done'),
    path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
    path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('passwordreset/complete', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('<username>/review/<imdb_id>/like', like, name='review_like'),
    path('<username>/review/<imdb_id>/unlike', unlike, name='review_unlike'),
]
