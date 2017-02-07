from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Video, Interview_Question_Map, Interview, Question, \
    Interview_Question_Video_Map, User_Add_Ons, Question_Video_Map


class Recording(TestCase):
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

    def test_display_default_question(self):
        """
        If the interview has not question, display the default question.
        :return:
        """
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response = self.client.get(
            reverse('question_interview', kwargs={'interview_id': interview.id, 'camera_id': 0}))
        self.assertEqual(response.status_code, 200)

    def test_display_questions_interview(self):
        """
        Display the question selected using the interview_id
        :return:
        """
        question = Question.objects.get(pk=23)
        interview = Interview.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        count = Interview_Question_Map.objects.filter(interview=interview).count()
        iq = Interview_Question_Map.objects.filter(interview=interview)
        response = self.client.get(
            reverse('question_interview', kwargs={'interview_id': interview.id, 'camera_id': 0}))
        self.assertEqual(response.status_code, 200)

    def test_display_count_video(self):
        """
        If the video has video saved, display the number videos
        :return:
        """
        question = Question.objects.get(pk=23)
        interview = Interview.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        count = Interview_Question_Map.objects.filter(interview=interview).count()
        iq = Interview_Question_Map.objects.filter(interview=interview)
        response = self.client.get(
            reverse('question_interview', kwargs={'interview_id': interview.id, 'camera_id': 0}))
        self.assertEqual(response.status_code, 200)

    def test_save_video(self):
        """
        Test to verify that the video is saved on the database
        :return:
        """
        file = open('examples/test.webm', 'r', encoding='utf-8', errors='ignore')
        question = Question.objects.get(pk=23)
        interview = Interview.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response = self.client.post(
            reverse('save_recording'), data={'data': file, 'interview_question': interview_question.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Done")
        interview_question_video = Interview_Question_Video_Map.objects.get(interview_question=interview_question)
        self.assertIn('q23', interview_question_video.video.url)

    def test_verify_status_default(self):
        """
        Test to verify the default status on the video.
        :return:
        """
        file = open('examples/test.webm', 'r', encoding='utf-8', errors='ignore')
        question = Question.objects.get(pk=4)
        interview = Interview.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response = self.client.post(
            reverse('save_recording'), data={'data': file, 'interview_question': interview_question.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Done")
        interview_question_video = Interview_Question_Video_Map.objects.get(interview_question=interview_question)
        self.assertIn('new', interview_question_video.video.status)

    def test_verify_created_by_video(self):
        """
        Test to verify the user that created the video on the system
        :return:
        """
        file = open('examples/test.webm', 'r', encoding='utf-8', errors='ignore')
        question = Question.objects.get(pk=4)
        interview = Interview.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response = self.client.post(
            reverse('save_recording'), data={'data': file, 'interview_question': interview_question.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Done")
        interview_question_video = Interview_Question_Video_Map.objects.get(interview_question=interview_question)
        self.assertEquals(interview_question_video.video.created_by.user.first_name, "Noelia")

    def test_verify_create_question_video(self):
        """
        Test to verify that the question video object is created on the database
        :return:
        """
        file = open('examples/test.webm', 'r', encoding='utf-8', errors='ignore')
        question = Question.objects.get(pk=4)
        interview = Interview.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response = self.client.post(
            reverse('save_recording'), data={'data': file, 'interview_question': interview_question.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Done")
        question_video = Question_Video_Map.objects.get(question=question)
        self.assertEquals(question_video.question.name, question.name)

    def test_verify_interview_question(self):
        """
        Test to verify that the interview question object is created on the database
        :return:
        """
        file = open('examples/test.webm', 'r', encoding='utf-8', errors='ignore')
        question = Question.objects.get(pk=4)
        interview = Interview.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response = self.client.post(
            reverse('save_recording'), data={'data': file, 'interview_question': interview_question.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Done")
        interview_question_video = Interview_Question_Video_Map.objects.get(interview_question=interview_question)
        self.assertEquals(interview_question_video.interview_question.interview, interview)

