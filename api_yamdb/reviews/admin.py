from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'score', 'author', 'title')
    search_fields = ('title', 'author')
    list_filter = ('score', 'text',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['name'],
    }


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['name'],
    }


admin.site.register(Review, ReviewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title)
admin.site.register(Comment)
