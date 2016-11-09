from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from foraliving.models import Video, Interview_Question_Map, Interview
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin


class CompleteVideo(LoginRequiredMixin, generic.View):
    """Generic view to display the complete videos interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/complete_videos.html'

    @xframe_options_exempt
    def get(self, request):
        videos = Video.objects.filter(created_by=request.user.id)
        return render(request, self.question_view, {'videos': videos})


class StudentAssignment(LoginRequiredMixin, generic.View):
    """Generic view to display the assignment interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/assignment.html'

    def get(self, request):
        interview = Interview.objects.filter(interviewer_id=request.user.id)
        videos = Video.objects.filter(created_by=request.user.id)
        if not interview:
            questions = ""
        else:
            interview = Interview.objects.get(interviewer_id=request.user.id)
            questions = Interview_Question_Map.objects.filter(interview_id=interview.id)
        return render(request, self.question_view, {'questions': questions, 'videos': videos})


class ConductVideo(LoginRequiredMixin, generic.View):
    """Generic view to display the assignment interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'student/conduct_video.html'

    def get(self, request):
        return render(request, self.question_view)