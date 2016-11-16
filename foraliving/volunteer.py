from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.contrib.auth.models import User
from foraliving.models import Volunteer_User_Add_Ons

class VolunteerProfile(LoginRequiredMixin, generic.View):
    """Generic view to display the volunteer profile,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'volunteer/profile.html'


    def get(self, request, user_id):
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user_id)
        return render(request, self.question_view, {'volunteer': volunteer})
