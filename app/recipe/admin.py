from django.contrib import admin
from recipe.models import Tag

# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['user','name']
    search_fields = ['user__username','name']
    list_per_page = 20
