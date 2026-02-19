# Trafficapp/admin.py
from django.contrib import admin
from .models import QuizTest, QuizQuestion

class QuizQuestionInline(admin.TabularInline):
    model = QuizQuestion
    extra = 1

class QuizTestAdmin(admin.ModelAdmin):
    inlines = [QuizQuestionInline]

admin.site.register(QuizTest, QuizTestAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')

    def has_add_permission(self, request):
        return False