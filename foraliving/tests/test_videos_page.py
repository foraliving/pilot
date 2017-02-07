from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from foraliving.models import Video, Interview_Question_Map, Interview, Question, \
    Interview_Question_Video_Map, User_Add_Ons


class VideosPage(TestCase):
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
        self.client.login(username='student_admin', password='admin123')

    def test_display_videos_page_student(self):
        """
        Test to display the videos when the user is student
        :return:
        """
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        user = User_Add_Ons.objects.get(user=self.user)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        video = Video(name=interview_question.question.name, url="www.foraliving.org", tags="student", created_by=user,
                      creation_date="2016-11-11", status="approved")
        video.save()
        interview_question_video = Interview_Question_Video_Map(interview_question=interview_question, video=video)
        interview_question_video.save()
        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "www.foraliving.org")
        self.assertContains(response, interview_question.question.name)


    def test_display_school_name_student(self):
        """
        If the user is student, display the school name on the top page
        :return:
        """
        self.user = User.objects.get(pk=2)
        user = User_Add_Ons.objects.get(user=self.user)
        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.school.name)


    def test_display_videos_page_teacher(self):
        """
        Test to display the videos when the user is teacher
        :return:
        """
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        self.user = User.objects.get(pk=3)
        user = User_Add_Ons.objects.get(user=self.user)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        video = Video(name=interview_question.question.name, url="www.youtube.com/watch?v=oFnH9TsNRPo", tags="student", created_by=user,
                      creation_date="2016-11-11", status="approved")
        video.save()
        interview_question_video = Interview_Question_Video_Map(interview_question=interview_question, video=video)
        interview_question_video.save()
        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "www.youtube.com/watch?v=oFnH9TsNRPo")
        self.assertContains(response, interview_question.question.name)


    def test_display_school_name_teacher(self):
        """
        If the user is teacher, display the school name on the top page
        :return:
        """
        self.user = User.objects.get(pk=3)
        user = User_Add_Ons.objects.get(user=self.user)
        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.school.name)


    def test_display_videos_page_volunteer(self):
        """
        Test to display the videos when the user is volunteer
        :return:
        """
        self.client.logout()
        self.client.login(username='volunteer_admin', password='admin123')
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        user = User_Add_Ons.objects.get(user=self.user)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        video = Video(name=interview_question.question.name, url="www.youtube.com/watch?v=oFnH9TsNRPo", tags="student",
                      created_by=user,
                      creation_date="2016-11-11", status="approved")
        video.save()
        interview_question_video = Interview_Question_Video_Map(interview_question=interview_question, video=video)
        interview_question_video.save()
        response = self.client.get(reverse('videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "/foraliving/media/www.youtube.com/watch?v=oFnH9TsNRPo")
        self.assertContains(response, "Profile")
        self.assertContains(response, "Get Interviewed")


