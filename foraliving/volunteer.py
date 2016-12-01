from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.contrib.auth.models import User
from foraliving.models import Volunteer_User_Add_Ons, Interview, Interview_Question_Video_Map, Interview_Question_Map


class VolunteerProfile(LoginRequiredMixin, generic.View):
    """Generic view to display the volunteer profile,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'volunteer/profile.html'


    def get(self, request, user_id, interview_id):
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user_id)
        interview = Interview.objects.filter(interviewee__in=user_id)
        interview_question = Interview_Question_Map.objects.filter(interview__in=interview)
        interview_question_video = Interview_Question_Video_Map.objects.filter(interview_question__in=interview_question).order_by('-video')
        return render(request, self.question_view, {'volunteer': volunteer, 'interview': interview_id, 'videos': interview_question_video})
