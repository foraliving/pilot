from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Video, Interview_Question_Map, Interview, Question, \
    Interview_Question_Video_Map, User_Add_Ons


class AssignmentPage(TestCase):
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

    def test_verify_volunteer_name(self):
        """
        Test when the interview has assigned a volunteer
        :return:
        """
        interview = Interview.objects.get(pk=1)
        response = self.client.get(
            reverse('assignment', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' Conduct interview with <a href="/foraliving/volunteer/profile/1/1">Vivian')

    def test_group_name(self):
        """
        Test to verify that the group name is displayed on the assignment page
        :return:
        """
        group = Group.objects.get(name='Science')
        group.user_set.add(2)
        interview = Interview.objects.get(pk=1)
        response = self.client.get(
            reverse('assignment', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Science Assignment')

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
            reverse('assignment', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)

    def test_disable_send_completed_videos(self):
        """
        Verify the disable button when the interview has not videos saved
        :return:
        """
        self.client.login(username='student_admin', password='admin123')
        interview = Interview.objects.get(pk=1)
        response = self.client.get(
            reverse('assignment', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<button class=\'btn btn-menu btn-title border-radius\' disabled> Go")

    def test_count_question(self):
        """
        Verify the count questions when the interview has not questions.
        :return:
        """
        interview = Interview.objects.get(pk=1)
        response = self.client.get(
            reverse('assignment', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3. Select interview questions")

    def test_interview_with_questions(self):
        """
        Verify the question number when the interview has questions
        :return:
        """
        interview = Interview.objects.get(pk=1)
        question = Question.objects.get(pk=1)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response = self.client.get(
            reverse('assignment', kwargs={'interview_id': interview.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3. Select interview questions (1 selected)")

    def test_create_question(self):
        """
        Create questions on the interview
        :return:
        """
        interview = Interview.objects.get(pk=1)
        response = self.client.post(
            reverse('select_question', kwargs={'interview_id': interview.id}), data={'question':[1, 2, 3]})
        self.assertRedirects(response, reverse('assignment', kwargs={'interview_id': interview.id}),
                             msg_prefix='Questions Added Successfully')
        count = Interview_Question_Map.objects.filter(interview=interview).count()
        self.assertEquals(count, 3)

    def test_edit_question(self):
        """
        Test for edit questions on the interview
        :return:
        """
        interview = Interview.objects.get(pk=1)
        response = self.client.post(
            reverse('select_question_edit', kwargs={'interview_id': interview.id}), data={'question': [1, 2, 3,4,5]})
        self.assertRedirects(response, reverse('assignment', kwargs={'interview_id': interview.id}),
                             msg_prefix='Questions Edited Successfully')

        count = Interview_Question_Map.objects.filter(interview=interview).count()
        self.assertEquals(count, 5)



