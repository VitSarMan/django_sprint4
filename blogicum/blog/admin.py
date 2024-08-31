from django.contrib import admin

from .models import Category, Comments, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'created_at',
        'post',
        'author',
    )
    search_fields = (
        'post',
        'author',
        'text',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'created_at',
        'is_published',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'title',
    )
    inlines = (PostInline,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'is_published',
        'author',
        'location',
        'category',
        'pub_date',
    )
    list_editable = (
        'is_published',
        'category',
        'location',
    )
    search_fields = (
        'title',
        'text',
    )
    list_filter = (
        'is_published',
        'author',
        'pub_date',
    )
    list_per_page = 30
    list_display_links = ('title',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
    )
    search_fields = (
        'name',
    )
    inlines = (PostInline,)
