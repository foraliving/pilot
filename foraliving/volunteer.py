import json
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from foraliving.views import createInputToken
from .forms import *
from foraliving.models import Volunteer_User_Add_Ons, Interview, Interview_Question_Video_Map, Interview_Question_Map
from mail_templated import EmailMessage


class VolunteerProfile(LoginRequiredMixin, generic.View):
    """Generic view to display the volunteer profile,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'volunteer/profile.html'

    def get(self, request, user_id, interview_id):
        """
        Method to render the template with the videos and information of the volunteer
        :param request:
        :param user_id:
        :param interview_id:
        :return:
        """
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user_id)
        interview = Interview.objects.filter(interviewee=user_id)
        interview_question = Interview_Question_Map.objects.filter(interview__in=interview)
        interview_question_video = Interview_Question_Video_Map.objects.filter(
            interview_question__in=interview_question).order_by('-video')
        return render(request, self.question_view,
                      {'volunteer': volunteer, 'interview': interview_id, 'videos': interview_question_video})


class Contact(LoginRequiredMixin, generic.View):
    """Generic view to display the volunteer profile,
    this will be shown after login success"""
    contact_view = 'volunteer/contact.html'
    login_url = settings.LOGIN_URL

    def get(self, request):
        if request.user.is_superuser:
            return render(request, self.contact_view)
        else:
            return redirect(self.login_url)

    def post(self, request):
        if request.method == 'POST':
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phone = request.POST.get("phone")
            workTitle = request.POST.get("work_title")
            if email == "":
                messages.error(request, "Email is required.")
            elif first_name == "":
                messages.error(request, "First Name is required.")
            elif last_name == "":
                messages.error(request, "Last Name is required.")
            else:
                email_to = email
                domain = request.build_absolute_uri('/')[:-1]
                url = domain + "/volunteer/create/?email=" + email_to + "&phone=" + phone + "&workTitle=" + workTitle + "&first_name=" + first_name + "&last_name=" + last_name;
                message = EmailMessage('volunteer/invitation.html',
                                       {'url': url, 'first_name': first_name, 'last_name': last_name, 'phone': phone, 'workTitle': workTitle},
                                       "noelia.pazos@viaro.net", cc=["jacquie@foraliving.org"],
                                       to=[email_to])
                message.send()
            messages.success(request, "Invitation Sent Successfully")
            return redirect(self.contact_view)


class VolunteerEdit(LoginRequiredMixin, generic.View):
    """
    Class to edit the volunteer information
    """
    url_volunteer_edit = 'volunteer/profile_edit.html'
    url_volunteer_list = 'volunteer_profile'
    login_url = settings.LOGIN_URL

    def get(self, request, user_id):
        """
            Return the volunteer information to edit the profile.
        """
        user = User.objects.get(pk=request.user.id)
        volunteer_user = User.objects.get(pk=user_id)
        if user.id == volunteer_user.id:
            volunteer = get_object_or_404(Volunteer_User_Add_Ons, user=user_id)
            infoForm = volunteerSignupForm(instance=volunteer)

            return render(
                request,
                self.url_volunteer_edit,
                {
                    'infoForm': infoForm,
                    'user_id': volunteer.user.id,
                    'volunteer': volunteer
                }
            )
        else:
            return redirect(self.login_url)


    def post(self, request, user_id):
        """
            Method to receive the profile information that the user want to edit.
        """
        volunteer = get_object_or_404(Volunteer_User_Add_Ons, user=user_id)
        volunteer_form = volunteerSignupForm(request.POST, instance=volunteer)

        if not volunteer_form.is_valid():
            return render(
                request,
                self.url_volunteer_edit,
                {
                    'infoForm': volunteer_form,
                    'user_id': volunteer.user.id
                }
            )
        volunteer_form.save()
        messages.success(request, "Profile Edited Successfully")

        return HttpResponse(volunteer.id)

def editSkill(request, volunteer_id):
    """Method to edit skills and interests"""
    if request.method == 'POST':
        volunteer = Volunteer_User_Add_Ons.objects.get(pk=volunteer_id)
        for data in volunteer.skills.all():
            volunteer.skills.remove(data)

        for data in volunteer.interests.all():
            volunteer.interests.remove(data)

        skills = request.POST.getlist('skills')
        interests = request.POST.getlist('interests')

        # call to save the skills
        createInputToken(request, skills, 'Skill', volunteer_id)
        # call to save the interests
        createInputToken(request, interests, 'Interest', volunteer_id)

        return HttpResponse('ok')
