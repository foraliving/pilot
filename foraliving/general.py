from datetime import date
from django.conf import settings
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.views import generic
from mail_templated import EmailMessage
from foraliving.models import Video, Interview_Question_Map, Interview, Question, \
    User_Group_Role_Map, Interview_Question_Video_Map, User_Add_Ons, Volunteer_User_Add_Ons, Assignment, School, Class, User_Type
from django.views.decorators.clickjacking import xframe_options_exempt


class Videos(LoginRequiredMixin, generic.View):
    """Generic view to display the how conduct video interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    conduct_view = 'general/videos.html'

    def get(self, request):
        videos = ""
        school = None
        user = User.objects.get(id=request.user.id)
        user_type = User_Type.objects.get(user=user)
        if user_type.type.name == "Volunteer":
            videos = Video.objects.filter(status='approved')
        else:
            user_add_ons = User_Add_Ons.objects.get(user=request.user.id)
            school = School.objects.get(pk=user_add_ons.school.id)
            user_school = User_Add_Ons.objects.filter(school=school)
            videos = Video.objects.filter(created_by__in=user_school, status='approved')
        videos = Interview_Question_Video_Map.objects.filter(video__in=videos).order_by('-video')
        return render(request, self.conduct_view, {'videos': videos, 'school': school, 'user_type': user_type.type.name})
