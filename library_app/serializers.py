from rest_framework import serializers

from accounts_app.models import CustomUser
from library_app.models import Book, Genre, Author, BookReservation, BooksBorrow


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    borrow_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'stock', 'published_year', 'borrow_count', 'image_link']
        depth = 1


class CreateBookSerializer(serializers.ModelSerializer):
    borrow_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'stock', 'published_year', 'borrow_count', 'image_link']


class TopBooksSerializer(serializers.ModelSerializer):
    borrow_count = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'borrow_count']


class TopUsersLateReturnsSerializer(serializers.ModelSerializer):
    late_return_count = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'late_return_count']


class TopBooksLateReturnsSerializer(serializers.ModelSerializer):
    late_return_count = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'late_return_count']


class BorrowCountLastYearSerializer(serializers.ModelSerializer):
    borrow_count_last_year = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'borrow_count_last_year']


class BookReservationSerializer(serializers.ModelSerializer):
    reservation_status = serializers.CharField(source='get_reservation_status_display', read_only=True)

    class Meta:
        model = BookReservation
        read_only_fields = ['expiration_date', 'reservation_status']
        exclude = ['borrower']
        depth = 1


class CreateBookReservationSerializer(serializers.ModelSerializer):
    reservation_status = serializers.CharField(source='get_reservation_status_display', read_only=True)

    class Meta:
        model = BookReservation
        read_only_fields = ['expiration_date', 'reservation_status']
        exclude = ['borrower']


class BooksBorrowSerializer(serializers.ModelSerializer):
    borrowed_status = serializers.CharField(source='get_borrowed_status_display', read_only=True)

    class Meta:
        model = BooksBorrow
        depth = 1
        exclude = ['borrower']
