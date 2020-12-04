from django.urls import path
from authy.views import SignUp, PasswordChange, PasswordChangeDone, EditProfile
from django.contrib.auth import views as authViews
urlpatterns = [
    path('profile/edit', EditProfile, name='edit-profile'),
    path('signup/', SignUp, name='signup'),
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authViews.LogOutView.as_view(), {'next_page': 'login'}, name='logout'),
]
