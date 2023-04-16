from django.contrib import admin
from .models import Invite
from django.contrib import admin
from .models import School
from .models import User, Member

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'address',]
    search_fields = ['name',]

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name',]
    search_fields = ['username', 'first_name',]

class MemberAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'school',]
    search_fields = ['username', 'first_name', 'school',]

class InviteAdmin(admin.ModelAdmin):
    list_display = ['inviter', 'invited',]
    search_fields = ['inviter', 'invited',]
    # list_filter = ['inviter', 'invited,']

# Register your models here.
admin.site.register(School, SchoolAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Invite, InviteAdmin)