from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name='home'),
    path('index', views.index, name='index'),
    path('add', views.add, name='add'),
    path('<int:item_id>/', views.details, name='details'), 
    path('<int:item_id>/borow/', views.borow, name='borow'),
    path('logout', views.logoutUser, name="logout"),
    path('register', views.register, name='register'),
    path('login', views.loginUser, name='login'),
    path('search', views.search, name='search'),
]
