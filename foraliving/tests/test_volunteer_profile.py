from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Video, Interview_Question_Map, Interview, Question, \
    Interview_Question_Video_Map, User_Add_Ons, Volunteer_User_Add_Ons

class ContactForm(TestCase):
    """
        Test Calls fot all method related with the complete videos interface
    """
    fixtures = ['initial_data']

    def setUp(self):
        """
            Setup the initial conditions for execute the tests
        :return:
        """
        self.client = Client()
        self.client.login(username='volunteer_admin', password='admin123')

    def test_display_videos_volunteer(self):
        """
        In the section your videos, the volunteer could see their videos.
        :return:
        """
        self.user = User.objects.get(pk=1)
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        user = User.objects.get(pk=2)
        user = User_Add_Ons.objects.get(user=user)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        video = Video(name=interview_question.question.name, url="www.youtube.com/watch?v=oFnH9TsNRPo", tags="student", created_by=user,
                      creation_date="2016-11-11", status="Approved by teacher")
        video.save()
        interview_question_video = Interview_Question_Video_Map(interview_question=interview_question, video=video)
        interview_question_video.save()
        response = self.client.get(
            reverse('volunteer_profile', kwargs={'interview_id': 0, 'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "www.youtube.com/watch?v=oFnH9TsNRPo")
        self.assertContains(response, self.user.first_name)

    def test_display_information_volunteer(self):
        """
        In the section carrier information, the user can see the information the volunteer
        :return:
        """
        self.user = User.objects.get(pk=1)
        volunteer = Volunteer_User_Add_Ons.objects.get(user=self.user)
        response = self.client.get(
            reverse('volunteer_profile', kwargs={'interview_id': 0, 'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, volunteer.workTitle)
        self.assertContains(response, volunteer.workIndustry)

    def test_display_edit_option(self):
        """
        In the section carrier information, the user can see the information the volunteer
        :return:
        """
        self.user = User.objects.get(pk=1)
        volunteer = Volunteer_User_Add_Ons.objects.get(user=self.user)
        response = self.client.get(
            reverse('volunteer_profile', kwargs={'interview_id': 0, 'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/foraliving/volunteer/profile/edit/1/")