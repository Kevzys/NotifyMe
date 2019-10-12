from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('home/<int:id>', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('viewstocklist/', views.view_list, name='view'),
    path('addtolist/<int:id>', views.addToList, name='addstock')
]
