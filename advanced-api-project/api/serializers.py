from rest_framework import serializers
from datetime import date
from .models import Book, Author

#implementation of the author class
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
    # validation to ensure publication year is not the future
    def validate(self, data):
        current_year = date.today().year
        if data['publication_year'] > current_year:
            raise serializers.ValidationError("Publication year can not be in the future.")
        return data