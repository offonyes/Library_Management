from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets, permissions, filters, generics, status, serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema

from accounts_app.models import CustomUser
from library_app.models import Book, Author, Genre, BookReservation, BooksBorrow
from library_app.serializers import BookSerializer, AuthorSerializer, GenreSerializer, TopBooksSerializer, \
    TopBooksLateReturnsSerializer, TopUsersLateReturnsSerializer, BorrowCountLastYearSerializer, \
    BookReservationSerializer, BooksBorrowSerializer, CreateBookSerializer, CreateBookReservationSerializer


class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class MyViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    ordering = ['id']
    search_fields = ['name']
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
    search_fields = ['id', 'title', 'authors__name', 'genres__name']

    def get_queryset(self):
        qs = (Book.objects.annotate(
            borrow_count=Count(
                'borrows',
                filter=Q(borrows__borrowed_status__in=['borrowed', 'returned', 'overdue', 'overdue_returned'])))
              .prefetch_related('authors', 'genres'))
        return qs

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BookSerializer
        return CreateBookSerializer


@extend_schema(tags=['Genres'], description='Retrieve a list of genres. You can search for genres by title.')
class GenreViewSet(MyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@extend_schema(tags=['Authors'], description='Retrieve a list of author. You can search for authors by title.')
class AuthorViewSet(MyViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


@extend_schema(tags=['Statistics'], description='Top 10 books by borrows count.')
class TopBooksView(generics.ListAPIView):
    serializer_class = TopBooksSerializer

    def get_queryset(self):
        return Book.objects.annotate(
            borrow_count=Count(
                'borrows',
                filter=Q(borrows__borrowed_status__in=['returned', 'overdue', 'borrowed', 'overdue_returned']))
            ).order_by('-borrow_count')[:10]


@extend_schema(tags=['Statistics'], description='Top users by late return count.')
class TopUsersLateReturnsView(generics.ListAPIView):
    serializer_class = TopUsersLateReturnsSerializer

    def get_queryset(self):
        return CustomUser.objects.annotate(
            late_return_count=Count(
                'borrows',
                filter=Q(borrows__borrowed_status__in=['overdue', 'overdue_returned']))
        ).order_by('-late_return_count')[:100]


@extend_schema(tags=['Statistics'], description='Top books by late return count.')
class TopBooksLateReturnsView(generics.ListAPIView):
    serializer_class = TopBooksLateReturnsSerializer

    def get_queryset(self):
        return Book.objects.annotate(
            late_return_count=Count(
                'borrows',
                filter=Q(borrows__borrowed_status__in=['overdue', 'overdue_returned']))
        ).order_by('-late_return_count')[:100]


@extend_schema(tags=['Statistics'], description='Borrow count last year.')
class BorrowCountLastYearView(generics.ListAPIView):
    serializer_class = BorrowCountLastYearSerializer

    def get_queryset(self):
        last_year = timezone.now() - timedelta(days=365)
        qs = Book.objects.annotate(
            borrow_count_last_year=Count('borrows', filter=Q(borrows__borrowed_date__gte=last_year)))
        return qs


@extend_schema(tags=['User Management'])
class BookReservationView(viewsets.ModelViewSet):
    queryset = BookReservation.objects.all()
    pagination_class = BookPagination
    http_method_names = ['get', 'post']
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return BookReservation.objects.filter(
            borrower=self.request.user, reservation_status__in=['reserved', 'wishlist']
        ).prefetch_related('book__authors', 'book__genres')

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBookReservationSerializer
        return BookReservationSerializer

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        user = self.request.user
        if book is None:
            raise serializers.ValidationError({'error': 'This book does not exist'})

        if BookReservation.objects.filter(borrower=user, book=book, reservation_status='reserved').exists():
            raise serializers.ValidationError({'detail': 'You have already reserved this book.'}, code='invalid')

        if user.borrows.filter(borrowed_status__in=['borrowed', 'overdue']).count() >= 5:
            raise serializers.ValidationError({'detail': 'You already have an active 5 borrowings. '
                                                         'Please return it before making'
                                                         ' a new reservation.'}, code='invalid')
        if user.reservations.filter(reservation_status='reserved').count() >= 5:
            raise serializers.ValidationError({'detail': 'You already have an active 5 reservation. '
                                                         'Please complete or cancel it before making'
                                                         ' a new reservation.'}, code='invalid')

        borrowed_count = book.borrows.filter(borrowed_status__in=['borrowed', 'overdue']).count()
        reserved_count = book.reservations.filter(reservation_status='reserved').count()

        if (borrowed_count + reserved_count) >= book.stock:
            raise serializers.ValidationError({'detail': 'Not enough books available. You can add to wishlist.'})

        wishlist_reservation = BookReservation.objects.filter(borrower=user, book=book,
                                                              reservation_status='wishlist').first()
        if wishlist_reservation:
            wishlist_reservation.reservation_status = 'reserved'
            wishlist_reservation.save()
        else:
            serializer.save(borrower=user)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        reservation = self.get_object()

        # Can delete this !!!
        # if reservation.reservation_status in ['picked_up', 'reservation_expired', 'reservation_canceled']:
        #     return Response({'error': 'Reservation is already cancelled or has expired.'},
        #                     status=status.HTTP_400_BAD_REQUEST)

        reservation.reservation_status = 'reservation_canceled'
        reservation.save()
        return Response({'message': 'Reservation cancelled successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='history')
    def history_reservations(self, request):
        history_reservations = BookReservation.objects.filter(borrower=request.user
                                                              ).prefetch_related('book__authors', 'book__genres')
        page = self.paginate_queryset(history_reservations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(history_reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='add_wishlist')
    def add_wishlist(self, request):
        try:
            book = Book.objects.get(pk=request.data['book'])
        except Book.DoesNotExist:
            return Response({'error': 'This book does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        wishlist, created = BookReservation.objects.get_or_create(
            borrower=request.user,
            book=book,
            reservation_status='wishlist',
        )
        if not created:
            return Response({'error': 'You have added this book to wishlist'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Book added to wishlist successfully'}, status=status.HTTP_200_OK)


@extend_schema(tags=['User Management'])
class ActiveBooksBorrowListView(generics.ListAPIView):
    serializer_class = BooksBorrowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = BookPagination

    def get_queryset(self):
        return BooksBorrow.objects.filter(
            borrower=self.request.user,
            borrowed_status__in=['borrowed', 'overdue'],
            return_date__isnull=True
        ).prefetch_related('book__authors', 'book__genres')


@extend_schema(tags=['User Management'])
class BooksBorrowHistoryListView(generics.ListAPIView):
    pagination_class = BookPagination
    serializer_class = BooksBorrowSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return BooksBorrow.objects.filter(
            borrower=self.request.user).prefetch_related('book__authors', 'book__genres')
