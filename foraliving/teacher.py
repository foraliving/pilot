import json
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render
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
        group_list = Group.objects.all()
        return render(request, self.question_view, {'class_info': class_info, 'group_list': group_list})


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


class TeacherVolunteerT6a(LoginRequiredMixin, generic.View):
    """Generic view to display the volunteer list,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'teacher/volunteer_t6a.html'

    def get(self, request, user_id, assignment_id):
        """
        :param request:
        :return:
        """
        volunteer_initial = Volunteer_User_Add_Ons.objects.values('user')
        volunteers = User.objects.filter(pk__in=volunteer_initial)
        try:
            group = Group.objects.get(user=user_id)
        except ObjectDoesNotExist:
            group = None

        user = User.objects.get(pk=user_id)

        return render(request, self.question_view,
                      {'volunteers': volunteers, 'group': group, 'userInfo': user, 'assignment_id': assignment_id,
                       'user_id': user_id})


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

    cursor_v = connection.cursor()
    cursor_v.execute(
        """SELECT au.id, au.username, au.first_name, au.last_name, ag.name, fi.interviewee_id, au2.first_name, au2.last_name
            FROM auth_user au
            INNER JOIN auth_user_groups aug ON au.id=aug.user_id
            INNER JOIN auth_group ag ON ag.id=aug.group_id
            INNER JOIN foraliving_interview fi ON ag.id=fi.group_id
            INNER JOIN foraliving_assignment fa ON fi.assignment_id=fa.id
            INNER JOIN auth_user au2 ON fi.interviewee_id=au2.id
            WHERE fi.assignment_id =%s
            GROUP BY au.id, au.username, au.first_name, au.last_name, ag.name, fi.interviewee_id, au2.first_name, au2.last_name""",
        [assignment_id])
    results = cursor_v.fetchall()
    return JsonResponse({'results': list(results)})


def student_list(request, class_id):
    """
    Return the student list in relation
    :param request:
    :param class_id:
    :return:
    """

    cursor_v = connection.cursor()
    cursor_v.execute(
        """select au.id, au.username, au.first_name, au.last_name, fi.interviewee_id, au2.first_name, au2.last_name, au2.id,  ag.name
from auth_user au
inner join foraliving_student_class fsc on au.id=fsc.student_id
left join auth_user_groups aug on au.id=aug.user_id
left join auth_group ag on ag.id=aug.group_id
left join foraliving_interview fi on ag.id=fi.group_id
left join auth_user au2 on fi.interviewee_id=au2.id
where fsc."falClass_id"=%s
group by au.id, au.username, au.first_name, au.last_name, fi.interviewee_id, au2.first_name, au2.last_name, au2.id, ag.name""",
        [class_id])

    results = cursor_v.fetchall()
    return JsonResponse({'results': list(results)})


def list_student_group(request):
    """
    Return the student list in relation with id lists
    :param request:
    :return:
    """
    students = request.POST.getlist("selected[]")
    student = User.objects.filter(pk__in=students)

    leads_as_json = serializers.serialize('json', student)

    return HttpResponse(leads_as_json, content_type='application/json')


def list_groups(request):
    users = User.objects.values('username')
    groups = Group.objects.exclude(name__in=users)
    groups_json = serializers.serialize('json', groups)
    leads_as_json = serializers.serialize('json', groups)

    return HttpResponse(leads_as_json, content_type='application/json')



class AssignGroup(LoginRequiredMixin, generic.View):
    """Generic view to assign a student list to group"""
    login_url = settings.LOGIN_URL

    def post(self, request):
        """
        :param request:
        :return:
        """
        students = request.POST.getlist("selected[]")
        student = User.objects.filter(pk__in=students)

        group_name = request.POST.get("group_name")
        group = request.POST.get('group')

        if group_name:
            groupObject = Group.objects.create(name=group_name)
            groupObject.save()
        else:
            groupObject = Group.objects.get(pk=group)

        for data in students:
            groupObject.user_set.add(data)

        return JsonResponse({'results': list(students)})


def uniqueGroup(request):
    """
    Method to validate if the group name exist on the system
    :param request:
    :return:
    """
    if request.is_ajax():
        group = request.GET.get('group')
        count_group = (Group.objects.filter(name=group).count())
        if count_group >= 1:
            return HttpResponse('true')
        else:
            return HttpResponse('false')


class AssignVolunteer(LoginRequiredMixin, generic.View):
    """Generic view to assign a volunteer to an interview"""
    login_url = settings.LOGIN_URL

    def get(self, request, volunteer_id, assignment_id, user_id):
        """
        :param request:
        :return:
        """
        assignment = Assignment.objects.get(pk=assignment_id)
        volunteer = User.objects.get(pk=volunteer_id)
        try:
            group = Group.objects.get(user=user_id)
        except ObjectDoesNotExist:
            user = User.objects.get(pk=user_id)
            group = Group.objects.create(name=user.username)
            group.save()
            group.user_set.add(user)

        interview = Interview.objects.create(group=group, assignment=assignment, interviewee=volunteer)

        return redirect('teacher_class')


class TeacherVolunteerT9(LoginRequiredMixin, generic.View):
    """Generic view to display the volunteer list,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'teacher/volunteer_t9.html'

    def get(self, request, user_id):
        """
        :param request:
        :return:
        """
        user = User.objects.get(pk=user_id)
        user_add_ons = User_Add_Ons.objects.get(user=request.user)
        classes = Class.objects.filter(teacher=user_add_ons)
        return render(request, self.question_view, {'volunteer': user, 'classes': classes})


def studentList(request, assignment_id):
    """
    Method to get the student groups
    :param request:
    :return:
    """
    assignment = Assignment.objects.get(pk=assignment_id)
    group = Interview.objects.filter(assignment=assignment).values('group')
    groups = Group.objects.exclude(pk__in =group).values('pk')

    student_class = Student_Class.objects.filter(falClass=assignment.falClass).values('student_id')

    students = User.objects.filter(pk__in=student_class, groups__isnull=True)
    leads_as_json = serializers.serialize('json', students)
    return HttpResponse(leads_as_json, content_type='application/json')


def groupList(request, assignment_id):
    """
    Method to get the student groups
    :param request:
    :return:
    """
    assignment = Assignment.objects.get(pk=assignment_id)
    group = Interview.objects.filter(assignment=assignment).values('group')
    groups = Group.objects.exclude(pk__in =group).values('pk')

    student_class = Student_Class.objects.filter(falClass=assignment.falClass).values('student_id')

    students = User.objects.filter(pk__in=student_class, groups__in=groups).values('groups')

    group = Group.objects.filter(pk__in=students)

    leads_as_json = serializers.serialize('json', group)
    return HttpResponse(leads_as_json, content_type='application/json')


class CreateInterview(LoginRequiredMixin, generic.View):
    """Generic view to create a new interview"""
    login_url = settings.LOGIN_URL

    def post(self, request):
        """
        :param request:
        :return:
        """
        assignment_id = request.POST.get("assignment")
        result = request.POST.get("result")
        option = request.POST.get("new_option")
        volunteer_id = request.POST.get("volunteer_id")

        volunteer = User.objects.get(pk=volunteer_id)
        assignment = Assignment.objects.get(pk=assignment_id)

        if result == "a":
            student = User.objects.get(pk=option)
            group = Group.objects.create(name=student.username)
            group.save()
            group.user_set.add(student)
        else:
            group = Group.objects.get(pk=option)

        interview = Interview.objects.create(group=group, assignment=assignment, interviewee=volunteer)

        return HttpResponse('true')
