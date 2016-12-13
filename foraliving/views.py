import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
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
    """
    Class to create new volunters on the sysmtem
    """
    volunteer_view = 'volunteer/volunteer_signup.html'
    login_view = login_url = settings.LOGIN_URL

    def get(self, request):
        """
        Method to render the template
        :param request:
        :return:
        """
        email = request.GET.get('email')
        userForm = volunteerUserSignupForm()
        infoForm = volunteerSignupForm()

        return render(request, self.volunteer_view,
                      {'userForm': userForm, 'infoForm': infoForm, 'email': email})

    def post(self, request):
        """
        Method to save the data from the volunteer form
        :param request:
        :return:
        """
        if request.method == 'POST':
            userForm = volunteerUserSignupForm(request.POST)
            infoForm = volunteerSignupForm(request.POST)

            if not userForm.is_valid() or not infoForm.is_valid():
                return render(request, self.volunteer_view,
                      {'userForm': userForm, 'infoForm': infoForm})

            if userForm.is_valid():
                newUser = userForm.save(commit=False)
                if infoForm.is_valid():
                    newVolunteer = infoForm.save(commit=False)
                    #encrypted password
                    newUser.set_password(newUser.password)
                    newUser.save()
                    newVolunteer.user = User.objects.get(username=newUser.username)
                    newVolunteer.save()
                    return HttpResponse(newVolunteer.id)


def uniqueEmail(request):
    """
    Method to validate if the email exist on the system
    :param request:
    :return:
    """
    if request.is_ajax():
        email = request.GET.get('email')
        count_user = (User.objects.filter(email=email).count())
        if count_user >= 1:
            return HttpResponse('true')
        else:
            return HttpResponse('false')


def uniqueUsername(request):
    """
    Method to validate if the username exist on the system
    :param request:
    :return:
    """
    if request.is_ajax():
        username = request.GET.get('username')
        count_user = (User.objects.filter(username=username).count())
        if count_user >= 1:
            return HttpResponse('true')
        else:
            return HttpResponse('false')


def categories(request):
    """
    Method to get the skills saved on the system
    :param request:
    :return:
    """
    if request.method == 'GET':
        skill = Skill.objects.all()
        new_skill = []
        for data in skill:
            new_skill.append(data.name)
        return HttpResponse(json.dumps(new_skill))


def interests(request):
    """
    Method to get the interests saved on the system
    :param request:
    :return:
    """
    if request.method == 'GET':
        interest = Interest.objects.all()
        new_interest = []
        for data in interest:
            new_interest.append(data.name)
        return HttpResponse(json.dumps(new_interest))


def createSkill(request, volunteer_id):
    """
    Method to create skills and interests
    :param request:
    :param volunteer_id:
    :return:
    """
    if request.method == 'POST':
        volunteer = Volunteer_User_Add_Ons.objects.get(pk=volunteer_id)

        skills = request.POST.getlist('skills')
        interests = request.POST.getlist('interests')

        # call to create the skills
        createInputToken(request, skills, 'Skill', volunteer_id)

        # call to create the interests
        createInputToken(request, interests, 'Interest', volunteer_id)

        return HttpResponse('ok')


def createInputToken(request, dataInput, model, volunteer_id):
    """
    Method to create the skills or interests
    :param request:
    :param data:
    :param model:
    :param relation:
    :return:
    """
    volunteer = Volunteer_User_Add_Ons.objects.get(pk=volunteer_id)

    # for loop to list of the Skills
    for data in dataInput:
        data = json.loads(data)
        # for loop to the array objects of the Skill input
        for field in data:
            # for loop to objects with the values of the skills
            for key, value in field.items():
                if key == "value":
                    try:
                        # try get the skill or interest with the name saved in the variable "value"
                        if model == "Skill":
                            variable = Skill.objects.get(name__iexact=value)
                        else:
                            variable = Interest.objects.get(name__iexact=value)
                    except:
                        # if the object doesn't exist, the Skill or interest object is saved
                        if model == "Skill":
                            variable = Skill(name=value)
                        else:
                            variable = Interest(name=value)
                        variable.save()
                    # Add the skill or interest object to the skills or interests relation
                    if model == "Skill":
                        volunteer.skills.add(variable)
                    else:
                        volunteer.interests.add(variable)
