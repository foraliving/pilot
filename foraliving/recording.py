from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from foraliving.models import Interview_Question_Map, Question


class RecordingType(LoginRequiredMixin, generic.View):
    """Generic view to display the recording page,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL

    recording_view = 'recording/recording_type.html'

    def get(self, request):
        return render(request, self.recording_view)

class RecordingSetup(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (microphone),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup1.html'

    def get(self, request):
        return render(request, self.setup_view)

class RecordingSetup2(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (face),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup2.html'

    def get(self, request):
        return render(request, self.setup_view)


class RecordingSetup3(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (battery),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup3.html'

    def get(self, request):
        return render(request, self.setup_view)

class QuestionInterview(LoginRequiredMixin, generic.View):
    """Generic view to display the question of the interview,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'recording/questions.html'

    def get(self, request):
        questions = Interview_Question_Map.objects.filter(interview=1)
        return render(request, self.question_view, {'questions': questions})

class Recording(LoginRequiredMixin, generic.View):
    """Generic view to display the recording interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'recording/recording.html'

    def get(self, request, question_id):
        questions = Question.objects.get(pk=question_id)
        return render(request, self.question_view, {'questions': questions, 'question_name': questions.name})