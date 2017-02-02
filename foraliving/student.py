from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.views import generic
from django.http import HttpResponse
from mail_templated import EmailMessage
from foraliving.models import Video, Interview_Question_Map, Interview, Question, \
    User_Group_Role_Map, Interview_Question_Video_Map, User_Add_Ons, Volunteer_User_Add_Ons, Assignment, Student_Class
from django.views.decorators.clickjacking import xframe_options_exempt


class CompleteVideo(LoginRequiredMixin, generic.View):
    """Generic view to display the complete videos interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/complete_videos.html'

    @xframe_options_exempt
    def get(self, request, interview_id):
        count = 0
        count_approved = 0
        count_pending = 0
        show_count = 0
        volunteer = ""

        try:
            group = Group.objects.exclude(name=request.user.username).get(user=request.user.id)
        except ObjectDoesNotExist:
            group = None
        interview_question = Interview_Question_Map.objects.filter(interview_id=interview_id)
        video_archived = Video.objects.filter(status="archived").values('id')
        videos = Interview_Question_Video_Map.objects.filter(interview_question__in=interview_question).exclude(video__in=video_archived)

        if videos:
            volunteer = Volunteer_User_Add_Ons.objects.get(user=videos[0].interview_question.interview.interviewee.id)
            for data in videos:
                if data.video.status == "pending":
                    count = count + 1
                if data.video.status == "new":
                    count_pending = count_pending + 1
                if data.video.status == "approved":
                    count_approved = count_approved + 1

            if count != 0 or count_pending != 0:
                show_count = True

        return render(request, self.question_view,
                      {'videos': videos, 'group': group, 'volunteer': volunteer, 'show_count': show_count,
                       'count_approved': count_approved, 'interview': interview_id})


class StudentAssignment(LoginRequiredMixin, generic.View):
    """Generic view to display the assignment interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/assignment.html'

    def get(self, request, interview_id):
        group = None
        exist_video = None
        interview = Interview.objects.get(pk=interview_id)
        videos = Video.objects.filter(created_by=request.user.id)

        questions = Interview_Question_Map.objects.filter(interview_id=interview_id)
        question_number = Interview_Question_Map.objects.filter(interview_id=interview.id).count()
        try:
            group = Group.objects.exclude(name=request.user.username).get(user=request.user.id)
        except ObjectDoesNotExist:
            group = ""
        for question in questions:
            interview_question_video = Interview_Question_Video_Map.objects.filter(interview_question=question.id)
            if interview_question_video:
                exist_video = True

        group_name = Group.objects.filter(user=request.user.id)
        count_interview = (Interview.objects.filter(group__in=group_name).count())
        if count_interview >= 1 and interview_id is not None:
            return render(request, self.question_view, {
                'questions': questions, 'question_number': question_number, 'group': group, 'interview': interview,
                'exist_video': exist_video})
        else:
            return redirect('assignment_list')


class ConductVideo(LoginRequiredMixin, generic.View):
    """Generic view to display the how conduct video interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    conduct_view = 'student/conduct_video.html'

    def get(self, request, interview_id):
        return render(request, self.conduct_view, {'interview': interview_id})


class SelectQuestion(LoginRequiredMixin, generic.View):
    """Generic view to display the question select interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/select_question.html'
    assignment_view = 'assignment'

    def get(self, request, interview_id):
        questions = Question.objects.all()
        return render(request, self.question_view, {'questions': questions, 'interview_id': interview_id})

    def post(self, request, interview_id):
        selected_values = request.POST.getlist('question')

        for values in selected_values:
            new_data = Interview_Question_Map(interview_id=interview_id, question_id=values)
            new_data.save()
        messages.success(request, "Questions Added Successfully")
        return redirect(self.assignment_view, interview_id=interview_id)


class SelectQuestionEdit(LoginRequiredMixin, generic.View):
    """Generic view to display the question selected for edit,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/select_question_edit.html'
    assignment_view = 'assignment'

    def get(self, request, interview_id):
        new_question = []
        questions = Question.objects.all()
        select_questions = Interview_Question_Map.objects.filter(interview_id=interview_id)
        interview_question_videos = Interview_Question_Video_Map.objects.filter(interview_question__in=select_questions)
        for question in questions:
            all = []
            all.append(question.id)
            all.append(question.name)
            all.append("no")
            for sq in select_questions:
                if sq.question.id == question.id:
                    all[2] = "selected"
                    for iqv in interview_question_videos:
                        if iqv.interview_question.question.id == sq.question.id:
                            all[2] = "yes"
            new_question.append(all)
        return render(request, self.question_view,
                      {'questions': new_question, 'select_questions': select_questions, 'interview_id': interview_id})

    def post(self, request, interview_id):
        selected_values = request.POST.getlist('question')
        sqv = request.POST.getlist('iq')

        for data in sqv:
            Interview_Question_Map.objects.filter(interview_id=interview_id, question_id=data).delete()

        for values in selected_values:
            new_data = Interview_Question_Map(interview_id=interview_id, question_id=values)
            new_data.save()
        messages.success(request, "Questions Edited Successfully")
        return redirect(self.assignment_view, interview_id=interview_id)


class SendEmail(LoginRequiredMixin, generic.View):
    """Generic view to send the email by teacher"""
    login_url = settings.LOGIN_URL

    def get(self, request, video_id):
        interview_question_video = Interview_Question_Video_Map.objects.get(video=video_id)

        interview_question = Interview_Question_Map.objects.filter(
            interview=interview_question_video.interview_question.interview)

        interview_question_video_map = Interview_Question_Video_Map.objects.filter(
            interview_question__in=interview_question)

        count = 0
        for data in interview_question_video_map:
            if data.video.status == "pending":
                count = count + 1

        assignment = Assignment.objects.get(pk=interview_question_video.interview_question.interview.assignment.id)
        if count == 0:
            email_to = assignment.falClass.teacher.user.email
            message = EmailMessage('student/send_email.html', {'assignment': assignment}, "noelia.pazos@viaro.net",
                                   to=['noelia3pazos@gmail.com'])
            message.send()

        video = Video.objects.get(pk=video_id)
        video.status = 'pending'
        video.save()
        return redirect('complete_video', interview_id=interview_question_video.interview_question.interview.id)


class AssignmentList(LoginRequiredMixin, generic.View):
    """Generic View to display the assignment list """
    login_url = settings.LOGIN_URL
    select_assignment = 'student/select_assignment.html'

    def get(self, request):
        try:
            group = Group.objects.filter(user=request.user.id)
        except ObjectDoesNotExist:
            group = None

        student_class = Student_Class.objects.get(student=request.user.id)
        assignment = Assignment.objects.filter(falClass=student_class.falClass)
        interview = Interview.objects.filter(assignment__in=assignment, group__in=group)

        count_interview = (Interview.objects.filter(group__in=group, assignment__in=assignment).count())

        if count_interview ==1:
            return redirect('assignment', interview_id=interview[0].id)
        else:
            return render(request, self.select_assignment, {'interview': interview})


def delete_video(request):
    """
    Method to remove a video
    :param request:
    :return:
    """
    video_id = request.POST.get('video_id')
    video = Video.objects.filter(pk=video_id).update(status='archived')
    return HttpResponse('true')

