import json
from django.urls import reverse
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
        class_id = request.GET.get("class")
        assignment = request.GET.get("assignment")
        user_add_ons = User_Add_Ons.objects.get(user=request.user)
        class_info = Class.objects.filter(teacher=user_add_ons)
        group_list = Group.objects.all()
        return render(request, self.question_view,
                      {'class_info': class_info, 'group_list': group_list,
                       'class_id': class_id, 'assignment': assignment})


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
        assignment = Assignment.objects.get(pk=assignment_id)
        volunteer_initial = Volunteer_User_Add_Ons.objects.values('user')
        volunteers = User.objects.filter(pk__in=volunteer_initial)
        try:
            group = Group.objects.get(user=user_id)
        except ObjectDoesNotExist:
            group = None

        user = User.objects.get(pk=user_id)

        return render(request, self.question_view,
                      {'volunteers': volunteers, 'group': group, 'userInfo': user, 'assignment_id': assignment_id,
                       'user_id': user_id, 'class': assignment.falClass.id})


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
        class_id = request.GET.get('class')
        if class_id and class_id != '0':
            assignments = Assignment.objects.filter(falClass__in=class_id).values('pk')
            interview = Interview.objects.filter(assignment__in=assignments).values('pk')
            interview_question = Interview_Question_Map.objects.filter(interview_id__in=interview)
            videos = Interview_Question_Video_Map.objects.filter(interview_question__in=interview_question).order_by(
                '-video')
        else:
            class_id = 0
            school = School.objects.get(pk=user_add_ons.school.id)
            user_school = User_Add_Ons.objects.filter(school=school)
            videos = Video.objects.filter(created_by__in=user_school)
            videos = Interview_Question_Video_Map.objects.filter(video__in=videos).order_by('-video')
        return render(request, self.question_view, {'videos': videos, 'classname': classname, 'class_id': class_id})


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


def student_list(request, class_id, assignment_id):
    """
    Return the student list in relation
    :param request:
    :param class_id:
    :return:
    """
    cursor_v = connection.cursor()
    cursor_v.execute(
        """select au.id, au.username, au.first_name, au.last_name,  fi.interviewee_id, au2.first_name, au2.last_name, au2.id, ag.name, ag.id, fi.id as "interview_id",
        (Select count(*) From foraliving_video fv2
        inner join foraliving_interview_question_video_map fiqvm2 on fv2.id=fiqvm2.video_id
        inner join foraliving_interview_question_map fiqm2 on fiqvm2.interview_question_id=fiqm2.id
        inner join foraliving_interview fi2 on fi2.id=fiqm2.interview_id
        where fi2.id=fi.id and (fv2.status = 'pending' or  fv2.status = 'new') ) as pending,

        (Select count(*) From foraliving_video fv3
        inner join foraliving_interview_question_video_map fiqvm3 on fv3.id=fiqvm3.video_id
        inner join foraliving_interview_question_map fiqm3 on fiqvm3.interview_question_id=fiqm3.id
        inner join foraliving_interview fi3 on fi3.id=fiqm3.interview_id
        where fi3.id=fi.id and fv3.status = 'approved' ) as approvals

        from auth_user au
        inner join foraliving_student_class fsc on au.id=fsc.student_id and (fsc."falClass_id"=(%s))
        left join auth_user_groups aug on au.id=aug.user_id
        left join auth_group ag on ag.id=aug.group_id
        left join foraliving_interview fi on ag.id=fi.group_id and (fi.assignment_id=(%s))
        left join auth_user au2 on fi.interviewee_id=au2.id
        left join foraliving_assignment fa on fa.id=fi.assignment_id and (fsc."falClass_id"=(%s))
        group by au.id, au.username, au.first_name, au.last_name,  fi.interviewee_id, au2.first_name, au2.last_name, au2.id, ag.name, ag.id, fi.id""",
        (class_id, assignment_id, class_id,))

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
    class_id = request.GET.get("class_id")
    if class_id:
        group_class = Class_Group.objects.filter(falClass=class_id).values('group')
        groups = Group.objects.filter(pk__in=group_class)
        leads_as_json = serializers.serialize('json', groups)
    else:
        leads_as_json = None

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
        class_id = request.POST.get('class_id')
        classObject = Class.objects.get(pk=class_id)
        group_name = request.POST.get("group_name")
        group = request.POST.get('group')

        if group_name:
            groupObject = Group.objects.create(name=group_name)
            groupObject.save()
            groupClass = Class_Group.objects.create(group=groupObject, falClass=classObject)
            groupClass.save()
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
        count_group = (Group.objects.filter(name__iexact=group).count())
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

        return redirect(
            reverse('teacher_class') + '?class=' + str(assignment.falClass.id) + '&assignment=' + str(assignment.id))


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
    groups = Group.objects.exclude(pk__in=group).values('pk')

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
    groups = Group.objects.exclude(pk__in=group).values('pk')

    student_class = Student_Class.objects.filter(falClass=assignment.falClass).values('student_id')

    students = User.objects.filter(pk__in=student_class, groups__in=groups).values('groups')

    group = Group.objects.filter(pk__in=students)

    leads_as_json = serializers.serialize('json', group)
    return HttpResponse(leads_as_json, content_type='application/json')


def update_video(request, video_id, flag_id):
    """
    Method to update the video status and return the count of new videos pending
    :param request:
    :return:
    """
    if flag_id == '1':
        video = Video.objects.filter(pk=video_id).update(status='pending')
    else:
        video = Video.objects.filter(pk=video_id).update(status='approved')

    interview_question_video = Interview_Question_Video_Map.objects.get(video=video_id)
    interview_question = Interview_Question_Map.objects.filter(
        interview=interview_question_video.interview_question.interview)
    interview_question_video_map = Interview_Question_Video_Map.objects.filter(
        interview_question__in=interview_question)

    count = 0
    for data in interview_question_video_map:
        if data.video.status == "pending" or data.video.status == "new":
            count = count + 1

    return HttpResponse(count)

def delete_interview(request):
    """
    Method to remove a volunteer
    :param request:
    :return:
    """
    interview = request.POST.get('interview_id')
    Interview.objects.filter(pk=interview).delete()
    return HttpResponse('true')

def delete_class(request):
    """
    Method to remove a class
    :param request:
    :return:
    """
    class_id = request.POST.get('class_id')
    Class.objects.filter(pk=class_id).delete()
    return HttpResponse('true')


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


class GroupInterface(LoginRequiredMixin, generic.View):
    """Generic view to display the group interface"""
    login_url = settings.LOGIN_URL
    group_view = 'teacher/group_t4.html'

    def get(self, request, class_id, assignment_id, group_id):
        """
        :param request:
        :return:
        """
        count = 0
        group = Group.objects.get(pk=group_id)
        student_class = Student_Class.objects.filter(falClass=class_id).values('student')
        try:
            interview = Interview.objects.get(assignment=assignment_id, group=group_id)
            interview_question = Interview_Question_Map.objects.filter(interview_id=interview.id)
            videos = Interview_Question_Video_Map.objects.filter(interview_question__in=interview_question)
            volunteer = Volunteer_User_Add_Ons.objects.get(user=interview.interviewee.id)

            for data in videos:
                if data.video.status == "pending" or data.video.status == 'new':
                    count = count + 1

        except:
            interview = None
            videos = None
            volunteer = None

        users = User.objects.filter(groups__in=group_id, pk__in=student_class)
        return render(request, self.group_view, {'group': group, 'users': users,
                'interview': interview, 'videos': videos, 'volunteer': volunteer, 'count': count})


class AddClass(LoginRequiredMixin, generic.View):
    template = 'teacher/add_class.html'

    def get(self, request):
        form = TeacherAddClass()

        return render(
            request,
            self.template,
            {
                'add_class_form': form
            }
        )

def studentPersonalInfo(request, class_id):
    """
    :param request:
    :param class_id:
    :return:
    """
    student_class = Student_Class.objects.filter(falClass=class_id).values('student')
    students = User.objects.filter(pk__in=student_class).values('id', 'first_name', 'last_name', 'username', 'email')

    return JsonResponse({'results': list(students)})

def getPassword(request):
    """
    :param request:
    :return:
    """
    user_id = request.GET.get('user_id')
    user = User.objects.get(pk=user_id).values('password')
    return HttpResponse(user)
