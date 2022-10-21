from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .confirmation import get_tokens_for_user, send_email
from .filters import TitleFilter
from .permissions import AuthorAndStaffOrReadOnly, IsAdmin, IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GettingTokenSerializer,
                          ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)


class SignupUserAPIView(generics.CreateAPIView):
    """Обработка запроса на регистрацию нового пользователя."""
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(**serializer.validated_data)
        except IntegrityError:
            msg = 'Пользователь с такими данными уже существует'
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        send_email(serializer.validated_data['email'], confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenAuthApiView(generics.CreateAPIView):
    """Получение access-токена."""
    serializer_class = GettingTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']):
            token = get_tokens_for_user(user)
            return JsonResponse({'token': token['access']},
                                status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Обработка запросов к эндпоинтам:
        "users/", "users/username/", "users/me/"."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdmin, )
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(IsAuthenticated, ),
            url_path='me',
            url_name='me')
    def me(self, request, pk=None):
        user = User.objects.get(username=request.user)
        if request.method == 'PATCH':
            serializer = self.serializer_class(user,
                                               data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка запросов о произведениях к эндпоинтам "titles/"."""
    queryset = Title.objects.select_related(
        'category').prefetch_related(
        'genre').annotate(rating=Avg('reviews__score'))
    serializer_class = TitleWriteSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewGenreModelViewset(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Класс для обработки запросов о категориях и жанрах произведений."""
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoryViewSet(ReviewGenreModelViewset):
    """Обработка запросов о категориях произведений
        на эндпоинты "categories/"."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ReviewGenreModelViewset):
    """Обработка запросов о жанрах произведений
        на эндпоинты "genres/"."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Обработка запросов об отзывах к произведениям
        на эндпоинты "reviews/"."""
    serializer_class = ReviewSerializer
    permission_classes = (AuthorAndStaffOrReadOnly, )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.select_related('author').all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorAndStaffOrReadOnly, )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        queryset = review.comments.select_related('author').all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
