from django.contrib import admin
from modtmrpg.models import *
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect

# Register your models here.
# @admin.register(Moder)
# class AuthorAdmin(admin.ModelAdmin):
#     readonly_fields = ('id', 'pex')
#     change_list_template = 'modtmrpg/changeAdmin.html'

#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path("<int:pk>/deny/", self.admin_site.admin_view(self.deny_view)),
#             path("<int:pk>/approve/", self.admin_site.admin_view(self.approve_view)),
#         ]
#         return my_urls + urls

#     def deny_view(self, request, pk):
#         # application = Moder.objects.get(pk=pk)

#         if request.method == "POST":
#             # Do something here:
#             # Send email, delete the application form, etc
#             return HttpResponse('хуй')
#             # return redirect("admin:sr_app_educationaldiscountapplication_changelist")

#         # context = dict(
#         #     self.admin_site.each_context(request),
#         #     object=application,
#         #     opts=EducationalDiscountApplication._meta,
#         #     title="Deny Application?",
#         # )
#         return HttpResponse('хуй2')
#         # return TemplateResponse(request, "admin/sr_app/educationaldiscountapplication/deny_application.html", context)
        
#     def approve_view(self, request, pk):
#         return HttpResponse('апруве')

@admin.register(Moder)
class AuthorAdmin(admin.ModelAdmin):
    # readonly_fields = ('id', 'pex')
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

@admin.register(EcoLog)
class AuthorAdmin(admin.ModelAdmin):
    pass




