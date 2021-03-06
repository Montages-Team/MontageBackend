from django.contrib import admin

from .models import Impression, Question


class QuestionInline(admin.TabularInline):
    model = Impression


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # 入力フィールド
    fields = ['user', 'about', 'category', 'is_personal']
    # 登録したものが見れるところ
    list_display = ('id', 'about', 'category', 'appeared_at', 'updated_at', 'is_personal')
    filter_horizontal = ('user',)


class ImpressionInline(admin.StackedInline):
    model = Impression


@admin.register(Impression)
class ImpressionAdmin(admin.ModelAdmin):
    fields = ['question', 'user', 'content', 'posted_at', 'is_collaged', 'created_by', 'impression_img_url']
    list_display = ('id', 'question', 'user', 'content', 'posted_at', 'is_collaged', 'created_by', 'impression_img_url')
    readonly_fields = ('posted_at',)
