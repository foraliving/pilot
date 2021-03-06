# Add documentation link
from __future__ import unicode_literals
from django.contrib.auth.models import User, Group
from categories.models import CategoryBase
from django.db import models
from datetime import datetime


class Skill(CategoryBase):
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self.name)


class Interest(CategoryBase):
    class Meta:
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self.name)


class LMS(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'LMS'
        verbose_name_plural = 'LMS'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class LMS_Web_Service(models.Model):
    web_service_name = models.CharField(max_length=128)
    # depending on the options we might be able to do a choicefield here
    web_service_method = models.CharField(max_length=128)
    web_service_url = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'LMS Web Service'
        verbose_name_plural = 'LMS Web Services'

    def __str__(self):
        return self.web_service_name + " - " + self.web_service_method

    def __unicode__(self):
        return self.web_service_name


class School(models.Model):
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class User_Add_Ons(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # The user's ID w/in their LMS
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Add-ons'
        verbose_name_plural = 'User Add-ons'

    def __str__(self):
        return self.user.username + " - " + self.school.name

    def __unicode__(self):
        return str(self.user)


class Volunteer_User_Add_Ons(models.Model):
    """
    The name of the model is incorrect, but for the moment doesn't change because it's implies to update many interfaces.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, )
    canGetText = models.BooleanField(default=True)
    workTitle = models.CharField(max_length=25)
    isBusinessOwner = models.BooleanField(default=True)
    workIndustry = models.CharField(max_length=25)
    yearsInIndustry = models.IntegerField()
    linkedinProfile = models.CharField(max_length=128, null=True, blank=True, )
    hsGradChoices = (
        (1, '1-4'),
        (2, '5-10'),
        (3, '11 or more'),
        (4, 'Have not graduated'),)
    yearsSinceHSGraduation = models.IntegerField(choices=hsGradChoices)
    collegeLevelChoice = (
        (1, "Associate"),
        (2, "Bachelor's"),
        (3, "Master's"),
        (4, "Doctoral"),
        (5, "None"),)
    collegeLevel = models.IntegerField(choices=collegeLevelChoice)
    collegeMajor = models.CharField(max_length=128, null=True, blank=True)
    skills = models.ManyToManyField(Skill, null=True, blank=True)
    interests = models.ManyToManyField(Interest, max_length=128, null=True, blank=True)

    # User_Skill_Map
    # User_Interest_Map

    class Meta:
        verbose_name = 'Volunteer add-ons'
        verbose_name_plural = 'Volunteer add-ons'

    def __str__(self):
        return self.user.username + " - " + self.workTitle

    def __unicode__(self):
        return "Volunteer: " + str(self.user)

        # return "Volunteer: "


class User_Group_Role_Map(models.Model):
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User_Add_Ons, on_delete=models.CASCADE)
    role = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.user.group.name + ": " + self.user.username + "-" + self.role

    def __unicode__(self):
        return str(self.group) + ': ' + str(self.user) + '-' + str(self.role)


class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    lms = models.ForeignKey(LMS, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User_Add_Ons, on_delete=models.CASCADE, )
    name = models.CharField(max_length=128)
    academic_year = models.IntegerField(default=None, null=True)
    semester = models.CharField(max_length=128, default=None, null=True)

    class Meta:
        verbose_name = 'FAL Class'
        verbose_name_plural = 'FAL Classes'

    def __str__(self):
        return self.name + " - " + self.teacher.user.first_name

    def __unicode__(self):
        return str(self.name) + ':' + str(self.teacher)


class Class_Group(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    falClass = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Class Groups'
        verbose_name_plural = 'Class Groups'

    def __str__(self):
        return self.user.group.name + " - " + self.falClass.name

    def __unicode__(self):
        return str(self.group.name) + ':' + str(self.falClass.name)


class Student_Class(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    falClass = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return self.student.username + ": " + self.falClass.name

    def __unicode__(self):
        return str(self.student) + ':' + str(self.falClass)


class Assignment(models.Model):
    title = models.CharField(max_length=128)
    falClass = models.ForeignKey(Class, on_delete=models.CASCADE)
    document = models.CharField(max_length=128, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.title + " - " + self.falClass.name

    def __unicode__(self):
        return str(self.title) + '  (' + str(self.falClass) + ')'


class Interview(models.Model):
    interviewer = models.CharField(max_length=256)
    interviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviewee', )
    group = models.ForeignKey(Group)
    date = models.DateTimeField(default=datetime.now, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment')

    def __str__(self):
        return self.assignment.title + " - " + self.group.name

    def __unicode__(self):
        return 'Interview of ' + str(self.interviewee) + ' by ' + str(self.assignment)


class Question(models.Model):
    name = models.CharField(max_length=128)
    created_by = models.ForeignKey(User_Add_Ons, on_delete=models.CASCADE, )
    creation_date = models.DateTimeField()

    def __str__(self):
        return self.name + " - " + self.created_by.user.username

    def __unicode__(self):
        return str(self.created_by) + ':' + str(self.name)


class Interview_Question_Map(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, )
    question = models.ForeignKey(Question, on_delete=models.CASCADE, )

    class Meta:
        verbose_name = 'Interview Question'
        verbose_name_plural = 'Interview Questions'

    def __str__(self):
        return self.question.name + " - " + self.interview.interviewee.username

    def __unicode__(self):
        return str(self.question) + ' (' + str(self.interview) + ')'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, )
    result = models.CharField(max_length=128)
    created_by = models.ForeignKey(User_Add_Ons, on_delete=models.CASCADE, )
    creation_date = models.DateTimeField()

    def __unicode__(self):
        return str(self.question)

    def __str__(self):
        return self.question.name + "(" + self.result + ")"


class Video(models.Model):
    # interview = models.ForeignKey(Interview, on_delete=models.CASCADE, null=True, blank=True, )
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=128)
    tags = models.CharField(max_length=128, null=True, blank=True, )
    created_by = models.ForeignKey(User_Add_Ons, on_delete=models.CASCADE, )
    creation_date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(max_length=128)

    def __str__(self):
        return str(self.name) + ' (' + str(self.creation_date) + ')'
    def __unicode__(self):
        return str(self.name) + ' (' + str(self.creation_date) + ')'


class Question_Video_Map(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, )
    video = models.ForeignKey(Video, on_delete=models.CASCADE, )

    class Meta:
        verbose_name = 'Video Question'
        verbose_name_plural = 'Video Questions'

    def __str__(self):
        return str(self.question.name) + " - " + str(self.video.name)

    def __unicode__(self):
        return str(self.question) + ':' + str(self.video)


class Interview_Question_Video_Map(models.Model):
    interview_question = models.ForeignKey(Interview_Question_Map, on_delete=models.CASCADE, )
    video = models.ForeignKey(Video, on_delete=models.CASCADE, )

    class Meta:
        verbose_name = 'Interview Question Video'
        verbose_name_plural = 'Interview Video Questions'

    def __str__(self):
        return str(self.interview_question.id) + " - " + str(self.video.name)

    def __unicode__(self):
        return str(self.interview_question) + '-' + str(self.video)


class Video_Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, )
    comment = models.CharField(max_length=128)
    created_by = models.ForeignKey(User_Add_Ons, on_delete=models.CASCADE, )
    creation_date = models.DateTimeField()

    class Meta:
        verbose_name = 'Video Comment'
        verbose_name_plural = 'Video Comments'

    def __str__(self):
        return self.video.name + ' (' + str(self.created_by) + ', ' + str(self.creation_date) + ')'

    def __unicode__(self):
        return str(self.video) + ' (' + str(self.created_by) + ', ' + str(self.creation_date) + ')'


class Assignment_Submission(models.Model):
    name = models.CharField(max_length=128)
    group = models.ForeignKey(Group)

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'

    def __str__(self):
        return str(self.group.name) + ':' + str(self.name)

    def __unicode__(self):
        return str(self.group) + ':' + str(self.name)


class Type(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return str(self.name)


class User_Type(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Type)

    def __str__(self):
        return str(self.user.username) + ':' + str(self.type.name)

    def __unicode__(self):
        return str(self.user.username) + ':' + str(self.type.name)


class Submission_Interview_Map(models.Model):
    submission = models.ForeignKey(Assignment_Submission, on_delete=models.CASCADE, )
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, )

    class Meta:
        verbose_name = 'Interview Submission'
        verbose_name_plural = 'Interview Submissions'

    def __str__(self):
        return str(self.submission.name) + ':' + str(self.interview.interviewee)

    def __unicode__(self):
        return str(self.submission) + ':' + str(self.interview)
