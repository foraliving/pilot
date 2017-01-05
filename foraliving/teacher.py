import json
import psycopg2
from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
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

    def post(self, request, class_id, option):
        """
        :param request:
        :param class_id:
        :param option:
        :return:
        """


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


from django.core import serializers


def asignment_list(request, class_id):
    """
    :param request:
    :param class_id:
    :return:
    """

    assignment = Assignment.objects.filter(falClass=class_id).values('id', 'title')
    if not assignment:
        assignment = []
    return JsonResponse({'results': list(assignment)})


def get_student(request, assignment_id):
    """
    :param request:
    :param class_id:
    :return:
    """
    conn = psycopg2.connect(
        database=connection.settings_dict['NAME'],
        host=connection.settings_dict['HOST'],
        port=connection.settings_dict['PORT'],
        user=connection.settings_dict['USER'],
        password=connection.settings_dict['PASSWORD'],
        connect_timeout=3
    )

    cursor_v = conn.cursor()
    cursor_v.execute(
        """select auth_user.id, username, first_name, last_name, auth_group.name,
 (Select (first_name || ' ' || last_name) from auth_user inner join foraliving_interview on auth_user.id=foraliving_interview.interviewee_id where assignment_id=%s)
  as info from auth_user inner join auth_user_groups on auth_user.id=auth_user_groups.user_id inner join auth_group on auth_group.id=auth_user_groups.group_id
  inner join foraliving_interview
on auth_group.id=foraliving_interview.group_id where assignment_id = %s group by auth_user.id, username, first_name, last_name, auth_group.name""", [assignment_id, assignment_id])
    results = cursor_v.fetchall()
    return JsonResponse({'results': list(results)})
