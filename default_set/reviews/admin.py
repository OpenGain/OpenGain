from django.contrib import admin
from .models import *
from main import opengain_admin


@admin.register(Review, site=opengain_admin)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('created', 'user', 'review', 'admin_answer', 'is_public')
    list_editable = ('is_public', 'admin_answer')
    raw_id_fields = ('user', )