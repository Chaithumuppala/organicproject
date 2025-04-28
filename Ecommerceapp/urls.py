from django.urls import path
from Ecommerceapp import views

urlpatterns = [
    path('',views.index,name='index'),
    path('copy',views.copy,name='copy'),


]