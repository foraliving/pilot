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
    User_Group_Role_Map, Interview_Question_Video_Map, User_Add_Ons, Volunteer_User_Add_Ons, Assignment
from django.views.decorators.clickjacking import xframe_options_exempt


class CompleteVideo(LoginRequiredMixin, generic.View):
    """Generic view to display the complete videos interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/complete_videos.html'

    @xframe_options_exempt
    def get(self, request):
        count = 0
        count_approved = 0
        count_pending = 0
        show_count = 0

        try:
            group = Group.objects.get(user=request.user.id)
            user_group = User.objects.get(groups=group)
            users = User_Add_Ons.objects.filter(user=user_group)
            video_user = Video.objects.filter(created_by__in=users)
            videos= Interview_Question_Video_Map.objects.filter(video__in=video_user)
        except ObjectDoesNotExist:
            group = None
            video_user = Video.objects.filter(created_by=request.user.id)
            videos = Interview_Question_Video_Map.objects.filter(video__in=video_user)

        if videos:
            for data in videos:
                if data.video.status == "Under Review by teacher":
                    count = count + 1
                if data.video.status == "pending":
                    count_pending = count_pending + 1
                if data.video.status == "Approved by teacher":
                    count_approved = count_approved + 1

            if count !=0 or count_pending != 0:
                show_count = True

        volunteer = Volunteer_User_Add_Ons.objects.get(pk=videos[0].interview_question.interview.interviewee.id)

        return render(request, self.question_view, {'videos': videos, 'group': group, 'volunteer': volunteer, 'show_count': show_count, 'count_approved': count_approved})


class StudentAssignment(LoginRequiredMixin, generic.View):
    """Generic view to display the assignment interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/assignment.html'

    def get(self, request):
        group = None
        exist_video = None
        interview = Interview.objects.filter(interviewer_id=request.user.id)
        videos = Video.objects.filter(created_by=request.user.id)
        if not interview:
            questions = ""
            question_number = ""
        else:
            interview = Interview.objects.get(interviewer_id=request.user.id)
            questions = Interview_Question_Map.objects.filter(interview_id=interview.id)
            question_number = Interview_Question_Map.objects.filter(interview_id=interview.id).count()
            try:
                group = Group.objects.get(user=request.user.id)
            except ObjectDoesNotExist:
                group = ""
        for question in questions:
            interview_question_video = Interview_Question_Video_Map.objects.filter(interview_question=question.id)
            if interview_question_video:
                exist_video = True
        return render(request, self.question_view, {
            'questions': questions, 'videos': videos, 'question_number': question_number, 'group': group, 'interview': interview, 'exist_video': exist_video})


class ConductVideo(LoginRequiredMixin, generic.View):
    """Generic view to display the how conduct video interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/conduct_video.html'

    def get(self, request):
        return render(request, self.question_view)


class SelectQuestion(LoginRequiredMixin, generic.View):
    """Generic view to display the question select interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/select_question.html'
    assignment_view = 'assignment'

    def get(self, request, interview_id):
        questions = Question.objects.all()
        return render(request, self.question_view, {'questions': questions})

    def post(self, request, interview_id):
        selected_values = request.POST.getlist('question')

        for values in selected_values:
            new_data = Interview_Question_Map(interview_id=interview_id, question_id=values)
            new_data.save()
        messages.success(request, "Questions Added Successfully")
        return redirect(self.assignment_view)


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
        for question in questions:
            all = []
            all.append(question.id)
            all.append(question.name)
            all.append("no")
            for select_question in select_questions:
                if select_question.question.id == question.id:
                    all[2] = "yes"
            new_question.append(all)
        return render(request, self.question_view, {'questions': new_question, 'select_questions': select_questions})

    def post(self, request, interview_id):
        selected_values = request.POST.getlist('question')
        select_questions = Interview_Question_Map.objects.filter(interview_id=interview_id).delete()
        for values in selected_values:
            new_data = Interview_Question_Map(interview_id=interview_id, question_id=values)
            new_data.save()
        messages.success(request, "Questions Edited Successfully")
        return redirect(self.assignment_view)


class SendEmail(LoginRequiredMixin, generic.View):
    """Generic view to send the email by teacher"""
    login_url = settings.LOGIN_URL
    complete_videos_view = 'complete_video'

    def get(self, request, video_id):
        interview_question_video = Interview_Question_Video_Map.objects.get(video=video_id)

        assignment = Assignment.objects.get(pk=interview_question_video.interview_question.interview.assignment.id)

        interview_question = Interview_Question_Map.objects.filter(interview=interview_question_video.interview_question.interview)
        interview_question_video_map = Interview_Question_Video_Map.objects.filter(interview_question=interview_question)

        count = 0
        for data in interview_question_video_map:
            if data.video.status == "Under Review by teacher":
                count = count + 1

        if count >= 1:
            email_to = assignment.falClass.teacher.user.email
            message = EmailMessage('student/send_email.html', {'assignment': assignment}, "noelia.pazos@viaro.net",
                                   to=[email_to])
            message.send()
        video = Video.objects.get(pk=video_id)
        video.status = 'Under Review by teacher'
        video.save()
        return redirect(self.complete_videos_view)
