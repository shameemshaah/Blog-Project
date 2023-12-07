from django.contrib import admin
from .models import Blog,Comment,UserOTP

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display=('title','created_date','updated_date','author')
    list_filter = ('title','author')
    search_fields = ('title','content')



admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)
admin.site.register(UserOTP)

