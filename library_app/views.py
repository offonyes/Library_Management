from datetime import timedelta

from django.db.models import Count, Q, F
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from accounts_app.models import CustomUser
from library_app.models import Book, Author, Genre, BookReservation
from library_app.serializers import BookSerializer, AuthorSerializer, GenreSerializer, TopBooksSerializer, \
    TopBooksLateReturnsSerializer, TopUsersLateReturnsSerializer, BorrowCountLastYearSerializer, \
    BookReservationSerializer


def index(request):
    return render(request, template_name='index.html')


class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class MyViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, JWTAuthentication)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['id']
    search_fields = ['title']
    pagination_class = BookPagination

    def get_permissions(self):
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
    ordering = ['borrow_count']

    def get_queryset(self):
        qs = Book.objects.annotate(
            borrow_count=Count('borrows',
                               filter=Q(borrows__borrowed_status='returned') | Q(borrows__borrowed_status='borrowed')))
        return qs


@extend_schema(tags=['Genres'], description='Retrieve a list of genres. You can search for genres by title.')
class GenreViewSet(MyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@extend_schema(tags=['Authors'], description='Retrieve a list of author. You can search for authors by title.')
class AuthorViewSet(MyViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


@extend_schema(tags=['Statistics'])
class TopBooksView(generics.ListAPIView):
    serializer_class = TopBooksSerializer

    def get_queryset(self):
        qs = Book.objects.annotate(
            borrow_count=Count('borrows',
                               filter=Q(borrows__borrowed_status='returned') | Q(borrows__borrowed_status='borrowed')))
        qs = qs.order_by('-borrow_count')[:10]
        return qs


@extend_schema(tags=['Statistics'])
class TopUsersLateReturnsView(generics.ListAPIView):
    serializer_class = TopUsersLateReturnsSerializer

    def get_queryset(self):
        return CustomUser.objects.annotate(
            late_return_count=Count('borrows', filter=Q(borrows__return_date__gt=F('borrows__borrowed_date') + timedelta(days=10)))
        ).order_by('-late_return_count')[:100]


@extend_schema(tags=['Statistics'])
class TopBooksLateReturnsView(generics.ListAPIView):
    serializer_class = TopBooksLateReturnsSerializer

    def get_queryset(self):
        return Book.objects.annotate(
            late_return_count=Count('borrows', filter=Q(borrows__return_date__gt=F('borrows__borrowed_date') + timedelta(days=10)))
        ).order_by('-late_return_count')[:100]


@extend_schema(tags=['Statistics'])
class BorrowCountLastYearView(generics.ListAPIView):
    serializer_class = BorrowCountLastYearSerializer

    def get_queryset(self):
        last_year = timezone.now() - timedelta(days=365)
        qs = Book.objects.annotate(
            borrow_count=Count('borrows', filter=Q(borrows__borrowed_date__gte=last_year)) )
        return qs


@extend_schema(tags=['User Management'])
class BookReservationView(viewsets.ModelViewSet):
    queryset = BookReservation.objects.all()
    serializer_class = BookReservationSerializer
    pagination_class = BookPagination
    http_method_names = ['get', 'post', 'cancel']

    def get_permissions(self):
        if self.action not in ['delete']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return BookReservation.objects.filter(borrower=self.request.user,
                                              reservation_status__in=['reserved'])

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.reservation_status in ['picked_up', 'reservation_expired', 'reservation_canceled']:
            return Response({'error': 'Reservation is already cancelled or has expired.'},
                            status=status.HTTP_400_BAD_REQUEST)
        reservation.reservation_status = 'reservation_canceled'
        reservation.save()
        return Response({'message': 'Reservation cancelled successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='history')
    def history_reservations(self, request):
        history_reservations = BookReservation.objects.filter(borrower=request.user)
        page = self.paginate_queryset(history_reservations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(history_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


