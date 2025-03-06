from django.urls import path
from authcart import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('auth/signup/',views.signup,name='signup'),
]