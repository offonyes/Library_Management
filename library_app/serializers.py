from rest_framework import serializers

from accounts_app.models import CustomUser
from .models import Book, Genre, Author, BookReservation


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
        fields = ['id', 'title', 'authors', 'genres', 'published_date', 'borrow_count', 'image_link']

    # def to_representation(self, instance):
    #     instance = Book.objects.prefetch_related('authors', 'genres').get(pk=instance.pk)
    #     return super().to_representation(instance)


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
    class Meta:
        model = BookReservation
        fields = '__all__'
        read_only_fields = ['expiration_date', 'borrower', 'reservation_status']
