from django.contrib import admin
from .models import Book, Comment, Tag, Rating, User

admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(User)


