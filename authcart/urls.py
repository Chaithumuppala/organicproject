from django.urls import path
from authcart import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('auth/signup/',views.signup,name='signup'),
    path('activate/<uidb64>/<token>/',views.ActivateAccountView.as_view(),name='activate'),
]