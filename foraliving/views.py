from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.template import loader
from django.views import generic
from .forms import *
from .models import *
from django.contrib.auth.models import User, Group
from foraliving.recording import *


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return redirect('videos')
    else:
        videoDemo = Video.objects.filter(tags__contains='homepage', tags__icontains='demo')
        videos = Video.objects.filter(tags__contains='homepage', ).exclude(tags__icontains='demo')
    return render(request, 'homepage.html', {'videos': videos, 'videoDemo': videoDemo,})


def twopage(request):
    return render(request, 'home.html')


def sitetheme(request):
    return render(request, 'FAL_Theme.html')


def interviewSetup(request):
    return render(request, 'interview_setup.html')


def record(request):
    return render(request, 'record.html')


class VolunteerForm(generic.View):
    volunteer_view = 'volunteer/volunteer_signup.html'
    login_view = login_url = settings.LOGIN_URL

    def get(self, request):
        userForm = volunteerUserSignupForm()
        infoForm = volunteerSignupForm()

        return render(request, self.volunteer_view,
                      {'userForm': userForm, 'infoForm': infoForm})

    def post(self, request):
        if request.method == 'POST':
            userForm = volunteerUserSignupForm(request.POST)
            infoForm = volunteerSignupForm(request.POST)
            if userForm.is_valid():
                newUser = userForm.save(commit=False)
                if infoForm.is_valid():
                    newVolunteer = infoForm.save(commit=False)
                    newUser.set_password(newUser.password)
                    newUser.save()
                    newVolunteer.user = User.objects.get(username=newUser.username)
                    newVolunteer.save()

            return redirect(self.login_view)


def uniqueEmail(request):
    if request.is_ajax():
        email = request.GET.get('email')
        count_user = (User.objects.filter(email=email).count())
        if count_user >= 1:
            return HttpResponse('true')
        else:
            return HttpResponse('false')


def uniqueUsername(request):
    if request.is_ajax():
        username = request.GET.get('username')
        count_user = (User.objects.filter(username=username).count())
        if count_user >= 1:
            return HttpResponse('true')
        else:
            return HttpResponse('false')
