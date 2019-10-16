from . import views
from django.urls import path, include
from rest_framework import routers
from .api import StockViewSet, StockListViewSet

router = routers.DefaultRouter()
router.register('api/stocks', StockViewSet, 'stocks')
router.register('api/stocklist', StockListViewSet, 'stocklist')

urlpatterns = [
    path('', views.index, name='index'),
    path('home/<int:id>', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('viewstocklist/', views.view_list, name='view'),
    path('addtolist/<int:id>', views.addToList, name=''),
    path('removelist/<int:id>', views.removelist, name='removelist'),
    path('removestock/<int:id>/<str:symbol>', views.removestock, name='removestock'),
    path('', include(router.urls)),
]
