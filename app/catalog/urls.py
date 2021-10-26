from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'catalog'

urlpatterns = [
    path('', include(router.urls)),
]
