from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryGenreAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для произведений."""
    list_display = (
        'name',
        'year',
        'description',
        'category'
    )
    search_fields = ('name',)
    list_filter = ('category', 'genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для обзоров."""
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    search_fields = ('author',)
    list_filter = ('score',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев."""
    list_display = (
        'review',
        'text',
        'pub_date'
    )
    search_fields = ('author',)


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
