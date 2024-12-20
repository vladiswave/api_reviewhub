from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка для пользователей."""
    pass


class CategoryGenreAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = (
        'name',
        'slug',
    )
    list_editable = ('name',)
    search_fields = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Админка для произведений."""
    list_display = (
        'name',
        'year',
        'description',
        'genre',
        'category',
    )
    list_editable = (
        'year',
        'genre',
        'category',
    )
    search_fields = ('name',)
    list_filter = ('category', 'genre',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для обзоров."""
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев."""
    pass


admin.site.register(Category, CategoryGenreAdmin)
admin.site.register(Genre, CategoryGenreAdmin)
