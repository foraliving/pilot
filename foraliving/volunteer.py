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
from foraliving.models import Student_Class
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

        user = User.objects.get(id=request.user.id)
        user_type = User_Type.objects.get(user=user)

        return render(request, self.question_view,
                      {'volunteer': volunteer, 'interview': interview_id, 'videos': interview_question_video, 'user_type': user_type.type.name})


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


class GetInterviewed(LoginRequiredMixin, generic.View):
    """
        This view will show the list of pending interview for a volunteer
    """
    template = 'volunteer/get_interviewed.html'

    def get(self, request):
        # First of all we get the pending interviews of the volunteer
        interviews = Interview.objects.filter(interviewee=request.user)
        return_data = []
        for interview in interviews:
            # We get all students assigned to interverview.assignment class
            # that belongs to the interview.group
            students = Student_Class.objects.filter(falClass=interview.assignment.falClass)
            users = interview.group.user_set.all()
            students_class_group = self.get_students_group(students, users)

            # We want to return the username-firstname of each student
            user_names = ''
            group_name = interview.group

            for s in students:
                print(s.student)
            print(students)
            print(users)
            print(students_class_group)
            # This is the general case (more than one student)
            if (len(students_class_group) > 1):
                cont = 0
                for user in students_class_group:
                    user_names += user.first_name
                    if not(cont == (len(users) - 1)):
                        user_names += ', '
                    cont += 1
            # This is the base case (Just one student)
            else:
                user_names = students_class_group[0].first_name

            return_data.append(
                {
                    'interview': interview,
                    'group_users': user_names,
                    'group_name': group_name
                }
            )

        return render(
            request,
            self.template,
            {'interviews_data': return_data}
        )

    def get_students_group(self, students=[], group=[]):
        students_in_group = []
        for student in students:
            if student.student in group:
                students_in_group.append(student.student)

        return students_in_group


class ReviewQuestionsView(LoginRequiredMixin, generic.View):
    def get(self, request, interview_id):
        questions = Interview_Question_Map.objects.filter(interview=interview_id)

        return questions
