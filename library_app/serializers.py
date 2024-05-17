from rest_framework import serializers
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
