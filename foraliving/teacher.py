import json
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from .forms import *
from foraliving.models import Class, User_Add_Ons, Volunteer_User_Add_Ons


class TeacherStudentT1(LoginRequiredMixin, generic.View):
    """Generic view to display the teacher student class interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'teacher/students_t1.html'

    def get(self, request):
        """
        :param request:
        :return:
        """
        user_add_ons = User_Add_Ons.objects.get(user=request.user)
        class_info = Class.objects.filter(teacher=user_add_ons)
        return render(request, self.question_view, {'class_info': class_info})

class TeacherVolunteerT6(LoginRequiredMixin, generic.View):
    """Generic view to display the volunteer list,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'teacher/volunteer_t6.html'

    def get(self, request):
        """
        :param request:
        :return:
        """
        volunteer_initial = Volunteer_User_Add_Ons.objects.values('user')
        volunteers = User.objects.filter(pk__in=volunteer_initial)
        return render(request, self.question_view, {'volunteers': volunteers})

class TeacherVideosT8(LoginRequiredMixin, generic.View):
    """Generic view to display the teacher videos,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'teacher/videos_t8.html'

    def get(self, request):
        """
        :param request:
        :return:
        """
        user_add_ons = User_Add_Ons.objects.get(user=request.user.id)
        classname = Class.objects.filter(teacher=user_add_ons)
        school = School.objects.get(pk=user_add_ons.school.id)
        user_school = User_Add_Ons.objects.filter(school=school)
        videos = Video.objects.filter(created_by__in=user_school)
        videos = Interview_Question_Video_Map.objects.filter(video__in=videos).order_by('-video')
        return render(request, self.question_view, {'videos': videos, 'classname': classname})