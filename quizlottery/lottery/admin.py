from django.contrib import admin
from .models import Questions, GoldCard, LotteryList

# =======================
# Question Admin
# =======================
@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'answer1', 'answer2', 'correct_answer', 'amount', 'is_active', 'register_date')
    list_filter = ('is_active', 'register_date')
    search_fields = ('question', 'answer1', 'answer2')
    ordering = ('-register_date',)
    fieldsets = (
        ('Question Info', {
            'fields': ('question', 'answer1', 'answer2', 'correct_answer', 'amount', 'is_active')
        }),
    )


# =======================
# GoldCard Admin
# =======================
@admin.register(GoldCard)
class GoldCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'serial', 'register_date', 'expire_date')
    search_fields = ('user__mobile_number', 'serial', 'question__question')
    list_filter = ('register_date', 'expire_date')
    ordering = ('-register_date',)
    readonly_fields = ('serial',)  # serial auto-generated, not editable


# =======================
# LotteryList Admin
# =======================
@admin.register(LotteryList)
class LotteryListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'gold_card')
    search_fields = ('user__mobile_number', 'question__question', 'gold_card__serial')
    list_filter = ('question',)
    ordering = ('id',)
