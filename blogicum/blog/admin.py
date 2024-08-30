from django.contrib import admin

from .models import Category, Comments, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 1


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


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
    )
    search_fields = (
        'name',
    )
    inlines = (PostInline,)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comments, CommentsAdmin)
