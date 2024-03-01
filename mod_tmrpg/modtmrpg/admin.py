from django.contrib import admin
from modtmrpg.models import *

# Register your models here.
@admin.register(Moder)
class AuthorAdmin(admin.ModelAdmin):
    pass
