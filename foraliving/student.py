from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.contrib.auth.models import User, Group
from foraliving.models import Video, Interview_Question_Map, Interview, Question, User_Group_Role_Map, Interview_Question_Video_Map, User_Add_Ons
from django.views.decorators.clickjacking import xframe_options_exempt


class CompleteVideo(LoginRequiredMixin, generic.View):
    """Generic view to display the complete videos interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/complete_videos.html'

    @xframe_options_exempt
    def get(self, request):
        try:
            group = Group.objects.get(user=request.user.id)
            user_group = User.objects.get(groups=group)
            users = User_Add_Ons.objects.filter(user=user_group)
            video_user = Video.objects.filter(created_by__in=users)
            videos= Interview_Question_Video_Map.objects.filter(video__in=video_user)
        except ObjectDoesNotExist:
            group = None
            print ("b")
            video_user = Video.objects.filter(created_by=request.user.id)
            videos = Interview_Question_Video_Map.objects.filter(video=video_user)
        return render(request, self.question_view, {'videos': videos, 'group': group})


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
