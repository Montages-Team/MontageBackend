from django.contrib import admin

from .models import MontageUser


class MontageUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('identifier_id', 'display_name', 'username',
                       'profile_img_url')
        }),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields': ('is_staff', 'is_superuser'),
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('identifier_id',),
    }), )
    list_display = (
        'id',
        'identifier_id',
        'username',
        'display_name',
        'is_superuser',
        'created_date',
        'modified_date',
    )
    # 編集ページへのリンクをつける項目はどれか示す
    list_display_links = (('identifier_id', ))
    list_filter = ('identifier_id', )
    search_fields = ['identifier_id']
    ordering = ('identifier_id', )
    # manytomanyを一括で横に追加削除できる
    filter_horizontal = ()


admin.site.register(MontageUser, MontageUserAdmin)
