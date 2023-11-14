from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name = 'sign-up'),
    #path('userprofile/<int:user_id>/', views.GetProfileData.as_view(), name='profile-data'),
    #path('update/password', views.UpdatePassword.as_view(), name='password-patch'),
    #path('update/username', views.UpdateUsername.as_view(), name='username-patch'),
    #path('update/email', views.UpdateEmail.as_view(), name='email-patch'),
    #path('update/biography', views.UpdateBiography.as_view(), name='biography-patch'),
    #path('update/profile-picture', views.UpdateProfilePicture.as_view(), name='profile-picture-patch'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]