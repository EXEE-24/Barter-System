# ads/admin.py
from django.contrib import admin
from .models import Category, Ad
from exchange.models import ExchangeProposal

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'condition', 'created_at')
    list_filter = ('category', 'condition')
    search_fields = ('title', 'description')
