from django.urls import path, include
from rest_framework.routers import DefaultRouter

from catalog import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('books', views.BookViewSet)

app_name = 'catalog'

urlpatterns = [
    path('', include(router.urls)),
]
