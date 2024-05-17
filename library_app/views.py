from rest_framework import viewsets, permissions, filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from library_app.models import Book, Author, Genre
from library_app.serializers import BookSerializer, AuthorSerializer, GenreSerializer


class MyViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, JWTAuthentication)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['id']
    search_fields = ['title']

    def get_permissions(self):
        print(self.action)
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


@extend_schema(tags=['Books'], description='Retrieve a list of books. You can search for books by title,'
                                           ' genre, author, published year.')
class BookViewSet(MyViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['id', 'title', 'authors__name', 'genres__name']


@extend_schema(tags=['Genres'], description='Retrieve a list of genres. You can search for genres by title.')
class GenreViewSet(MyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@extend_schema(tags=['Authors'], description='Retrieve a list of author. You can search for authors by title.')
class AuthorViewSet(MyViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
