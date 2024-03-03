from django.contrib import admin
from modtmrpg.models import *

# Register your models here.
@admin.register(Moder)
class AuthorAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

@admin.register(Pex)
class AuthorAdmin(admin.ModelAdmin):
    ordering = ['-hierarchy']

@admin.register(Discord)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(RegisterFormModel)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(MediaItem)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(MediaCategory)
class AuthorAdmin(admin.ModelAdmin):
    pass





