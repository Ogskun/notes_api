from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login

from drf_yasg.utils import swagger_auto_schema
from rest_framework import (
    permissions,
    status,
    viewsets,
)
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from knox.views import LoginView as KnoxLoginView

from core.models import Note

from api.serializers import (
    NoteSerializer,
)


class IndexAPIView(View):

    def get(self, request):
        return HttpResponse(
            """
            .  ..__..___..___ __.  .__..__ ._.
            |\ ||  |  |  [__ (__   [__][__) | 
            | \||__|  |  [___.__)  |  ||   _|_
                                  
            """,
            content_type='text/plain',
        )


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class NotesViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = None
    queryset = Note.objects.filter(is_deleted=False).order_by('id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)