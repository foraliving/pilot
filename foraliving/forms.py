from django import forms
from django.forms import CharField, Form, PasswordInput
from .models import *
from django.contrib.auth.models import User, Group
from django.db.models.fields import BLANK_CHOICE_DASH


class volunteerUserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', ]


class volunteerSignupForm(forms.ModelForm):
    hsGradChoices = (
        ("", 'Select range'),
        (1, '1-4'),
        (2, '5-10'),
        (3, '11 or more'),
        (4, 'Have not graduated'),)
    collegeLevelChoice = (
        ("", "Select"),
        (1, "associate"),
        (2, "bachelor's"),
        (3, "master's"),
        (4, "doctoral"),
        (5, "none"),)
    canGetText = forms.TypedChoiceField(coerce=lambda x: x == 'True', choices=((True, 'Yes'), (False, 'No')),
                                        widget=forms.RadioSelect, label="Can we text you on this number?", required=True)
    isBusinessOwner = forms.BooleanField(label="I am a business owner", initial=True, required=False)
    yearsInIndustry = forms.CharField(label="Number of years in this industry", required=True,
                                      widget=forms.NumberInput(attrs={'size': '10', 'placeholder': ''}))
    workTitle = forms.CharField(label="Work title", required=False)
    workIndustry = forms.CharField(label="Work industry", required=False)
    linkedinProfile = forms.CharField(label="Your Linkedin profile", required=False)
    yearsSinceHSGraduation = forms.ChoiceField(hsGradChoices, label="Year since high school graduation", required=True)
    collegeLevel = forms.ChoiceField(choices=collegeLevelChoice, label="Highest college degree",
                                     required=True, initial="")
    collegeMajor = forms.CharField(label="College major(s)", required=False)

    skills = forms.CharField(label="Please enter skills related to your job, role and industry",
                             required=False)
    interests = forms.CharField(label="Please provide some interests that lead you to your career choice",
                                required=False)

    def __init__(self, *args, **kwargs):
        super(volunteerSignupForm, self).__init__(*args, **kwargs)
        self.fields['yearsInIndustry'].widget.attrs['style'] = "width:20%"

    class Meta:
        model = Volunteer_User_Add_Ons
        # fields = '__all__'
        exclude = ['user']


class TeacherAddClass(forms.Form):
    class_name = forms.CharField(label="Class name")
    students_csv = forms.FileField(required=True, label='Upload File')


class TeacherAddClassAssignment(forms.Form):
    assignment_name = forms.CharField(label="Assignment name")
    description = forms.CharField(label="Description", required=False)
