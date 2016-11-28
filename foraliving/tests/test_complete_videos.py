from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Video, Interview_Question_Map, Interview, Question,\
    Interview_Question_Video_Map, User_Add_Ons


class CompleteVideos(TestCase):
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

    def test_exist_videos(self):
        """
            Here I test when the interview has not video.
        :return:
        """
        interview = Interview.objects.get(pk=1)
        response = self.client.get(
            reverse('complete_video', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have not recorded any videos yet.')

    def test_verify_group(self):
        """
            If the user has group, the complete videos interface should contain the group name
        :return:
        """
        group = Group.objects.get(name='Student')
        group.user_set.add(2)
        interview = Interview.objects.get(pk=1)
        response = self.client.get(
            reverse('complete_video', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Student Assignment')

    def test_verify_user_without_group(self):
        """
            In this case, on the top page is the first_name because the user has not group
        :return:
        """
        self.client.logout()
        self.client.login(username="volunteer_admin", password="admin123")
        self.user = User.objects.get(pk=1)
        interview = Interview.objects.get(pk=1)
        response = self.client.get(
            reverse('complete_video', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)

    def test_verify_videos_approved(self):
        """
        Verify the number of videos approved on one interview
        :return:
        """
        self.client.logout()
        self.client.login(username='student_admin', password='admin123')
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        user = User_Add_Ons.objects.get(user=self.user)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        video = Video(name="Test", url="www.foraliving.org", tags="student", created_by=user,
                      creation_date="2016-11-11", status="Approved by teacher")
        video.save()
        video_2 = Video(name="Test2", url="www.foraliving.org", tags="student", created_by=user,
                        creation_date="2016-11-11", status="Under Review by teacher")
        video_2.save()
        interview_question_video = Interview_Question_Video_Map(interview_question=interview_question, video=video)
        interview_question_video_2 = Interview_Question_Video_Map(interview_question=interview_question, video=video_2)
        interview_question_video.save()
        interview_question_video_2.save()
        response = self.client.get(
            reverse('complete_video', kwargs={'interview_id': interview.id}))
        self.assertContains(response, "1 video has been approved!")

    def test_send_video_teacher(self):
        """
            Verify that the video change of status when the student clicks on the button send by teacher
        :return:
        """
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        self.user = User.objects.get(pk=2)
        user = User_Add_Ons.objects.get(user=self.user)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        video = Video(name="Test", url="www.foraliving.org", tags="student", created_by=user,
                      creation_date="2016-11-11", status="pending")
        video.save()
        interview_question_video = Interview_Question_Video_Map(interview_question=interview_question, video=video)
        interview_question_video.save()
        send = response = self.client.get(
            reverse('send_email', kwargs={'video_id': video.id}))

        video_status= Video.objects.get(pk=video.id)
        self.assertEquals(video_status.status, "Under Review by teacher")



