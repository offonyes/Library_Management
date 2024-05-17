from rest_framework import serializers

from accounts_app.models import CustomUser
from .models import Book, Genre, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres', 'published_date']

    def to_representation(self, instance):
        instance = Book.objects.prefetch_related('authors', 'genres').get(pk=instance.pk)
        return super().to_representation(instance)


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
