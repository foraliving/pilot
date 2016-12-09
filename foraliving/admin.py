from django.contrib import admin
from .models import *
from categories.models import CategoryBase

# This should do for the time being. We'll add customization as needed 
modList = [LMS, LMS_Web_Service, School, User_Add_Ons, Class,
           Assignment, Question, Answer, Video, Video_Comment, Interview, Volunteer_User_Add_Ons]


#
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'parent')
    fields = ('parent', 'name', 'active')
    list_per_page = 25


class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'parent')
    fields = ('parent', 'name', 'active')
    list_per_page = 25


admin.site.register(Skill, SkillAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(modList)
