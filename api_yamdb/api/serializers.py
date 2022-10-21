import datetime as dt

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.validators import UserDataValidation
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer, UserDataValidation):
    '''Сериализация данных пользователя.'''

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class SignupSerializer(serializers.Serializer, UserDataValidation):
    '''Сериализация данных пользователя при регистрации
        через эндпоинт auth/sighup.'''
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)


class GettingTokenSerializer(serializers.Serializer, UserDataValidation):
    '''Сериализация данных для получения access-токена.'''
    username = serializers.CharField(required=True, max_length=150)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id', )


class TitleWriteSerializer(serializers.ModelSerializer):
    """Основной метод записи информации."""

    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f'Год не может быть больше {current_year}')
        return value


class TitleReadSerializer(serializers.ModelSerializer):
    """Основной метод получения информации."""

    category = CategorySerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы к произведениям. """
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на одно произведение дважды'
                )
        return data

    def validate_score(self, value):
        if 0 >= value or value > 10:
            raise serializers.ValidationError(
                'Оценка может быть только числом от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Комментарии к отзывам."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
