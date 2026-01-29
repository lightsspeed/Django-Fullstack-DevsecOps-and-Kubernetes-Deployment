from django.contrib import admin
from .models import Category, Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at', 'is_active')
    list_filter = ('is_active', 'is_public', 'category')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChoiceInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice', 'user', 'voted_at')
    list_filter = ('voted_at',)

admin.site.register(Choice)
