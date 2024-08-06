from django.urls import path, include

from drf_yasg.utils import swagger_auto_schema
from rest_framework import routers
from knox.views import (
    LogoutAllView,
    LogoutView,
)

from api.views import (
    IndexAPIView,
    NotesViewSet,
    LoginView,
)

router = routers.DefaultRouter()
router.register('notes', NotesViewSet)

urlpatterns = [
    path('', IndexAPIView.as_view(), name='index'),
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', 
         swagger_auto_schema(method='post')(LogoutView.as_view()), 
         name='logout'),
    path('logout_all/', 
         swagger_auto_schema(method='post')(LogoutAllView.as_view()), 
         name='logout_all'),
]
