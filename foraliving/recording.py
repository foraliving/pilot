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

class RecordingSetupMicrophone(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (microphone),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup_microphone.html'

    def get(self, request):
        return render(request, self.setup_view)

class RecordingSetupFace(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (face),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup_face.html'

    def get(self, request):
        return render(request, self.setup_view)


class RecordingSetupBattery(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (battery),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup_battery.html'

    def get(self, request):
        return render(request, self.setup_view)

class QuestionInterview(LoginRequiredMixin, generic.View):
    """Generic view to display the question of the interview,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'recording/questions.html'

    def get(self, request, interview_id):
        practice_question = Question.objects.get(
            name="What is your favorite book and why? (student practice question)")
        questions = Interview_Question_Map.objects.filter(interview=interview_id)
        question_default = Interview_Question_Map.objects.filter(question_id=practice_question.id, interview_id=interview_id)
        if not questions or not question_default:
            new_data = Interview_Question_Map(interview_id=interview_id, question_id=practice_question.id)
            new_data.save()
        questions = Interview_Question_Map.objects.filter(interview=interview_id)
        return render(request, self.question_view, {'questions': questions})

class Recording(LoginRequiredMixin, generic.View):
    """Generic view to display the recording interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'recording/recording.html'

    def get(self, request, question_id):
        questions = Question.objects.get(pk=question_id)
        return render(request, self.question_view, {'questions': questions, 'question_name': questions.name})