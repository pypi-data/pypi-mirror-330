from django.contrib import admin
from .models import Post  # Импортируем модель Post

# Регистрируем модель Post в админке
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Поля, которые будут отображаться в списке
    search_fields = ('title', 'content')    # Поля, по которым можно искать
    list_filter = ('created_at',)           # Фильтры справа
    ordering = ('-created_at',)             # Сортировка по умолчанию