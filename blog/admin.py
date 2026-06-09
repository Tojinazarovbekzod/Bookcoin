from django.contrib import admin
from .models import Book, Comment, Tag, Rating, User, Notification, PurchaseHistory


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display  = ('title', 'author', 'genre', 'price', 'rating', 'published', 'publish_date')
    list_filter   = ('genre', 'published', 'on_top')
    search_fields = ('title', 'author')
    list_editable = ('price', 'rating', 'published')
    fieldsets = (
        ('Book Info', {
            'fields': ('title', 'author', 'genre', 'body', 'content')
        }),
        ('Marketplace', {
            'fields': ('price', 'rating', 'cover_image')
        }),
        ('Settings', {
            'fields': ('published', 'on_top', 'tag')
        }),
    )

    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ('author', 'post', 'short_text')
    search_fields = ('author', 'text', 'post__title')
    list_filter   = ('post',)

    def short_text(self, obj):
        return obj.text[:60]
    short_text.short_description = 'Text'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(User)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display  = ('post', 'value')
    list_filter   = ('value',)
    search_fields = ('post__title',)
    list_editable = ('value',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display  = ('title', 'icon', 'color', 'is_active', 'created_at')
    list_filter   = ('is_active', 'color', 'icon')
    list_editable = ('is_active',)
    search_fields = ('title', 'message')


@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display  = ('user', 'book_title', 'book_genre', 'price', 'purchased_at')
    list_filter   = ('book_genre',)
    search_fields = ('book_title', 'user__username')
    readonly_fields = ('user', 'book_title', 'book_author', 'book_genre', 'price', 'book_img', 'purchased_at')


