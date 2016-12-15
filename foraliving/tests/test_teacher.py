from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Volunteer_User_Add_Ons, Class, Assignment, Interview, User_Add_Ons


class Teacher(TestCase):
    """
        Test Calls fot all method related with the teacher interface
    """
    fixtures = ['initial_data']

    def setUp(self):
        """
            Setup the initial conditions for execute the tests
        :return:
        """
        self.client = Client()
        self.client.login(username='teacher_admin', password='admin123')

    def test_verify_teacher_selection_navigation_general(self):
        """
        Test to verify the select options on the menu if the user is teacher
        :return:
        """
        response = self.client.get(
            reverse('videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' href="/foraliving/teacher/class/">Student')
        self.assertContains(response, ' href="/foraliving/teacher/volunteer/list/">Volunteers')
        self.assertContains(response, ' href="/foraliving/teacher/videos/">Videos')

    def test_verify_teacher_selection_navigation_student(self):
        """
        Test to verify the select options on the menu if the user is teacher
        :return:
        """
        response = self.client.get(
            reverse('teacher_class'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' href="/foraliving/teacher/class/">Student')
        self.assertContains(response, ' href="/foraliving/teacher/volunteer/list/">Volunteers')
        self.assertContains(response, ' href="/foraliving/teacher/videos/">Videos')

    def test_verify_teacher_selection_navigation_volunteer(self):
        """
        Test to verify the select options on the menu if the user is teacher
        :return:
        """
        response = self.client.get(
            reverse('teacher_volunteer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' href="/foraliving/teacher/class/">Student')
        self.assertContains(response, ' href="/foraliving/teacher/class/">Student')
        self.assertContains(response, ' href="/foraliving/teacher/volunteer/list/">Volunteers')
        self.assertContains(response, ' href="/foraliving/teacher/videos/">Videos')

    def test_verify_teacher_selection_navigation_videos(self):
        """
        Test to verify the select options on the menu if the user is teacher
        :return:
        """
        response = self.client.get(
            reverse('teacher_videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' href="/foraliving/teacher/class/">Student')
        self.assertContains(response, ' href="/foraliving/teacher/volunteer/list/">Volunteers')
        self.assertContains(response, ' href="/foraliving/teacher/videos/">Videos')

    def test_volunteer_list_name(self):
        """
        Test to verify that the volunteer list contains the user.first_name
        :return:
        """
        response = self.client.get(reverse('teacher_volunteer'))
        volunteer_initial = Volunteer_User_Add_Ons.objects.values('user')
        volunteers = User.objects.filter(pk__in=volunteer_initial)
        self.assertEqual(response.status_code, 200)

        for data in volunteers:
            self.assertContains(response, data.first_name)

    def test_volunteer_list_workTitle(self):
        """
        Test to verify that the volunteer list contains the volunteer.workTitle
        :return:
        """
        response = self.client.get(reverse('teacher_volunteer'))
        volunteer_initial = Volunteer_User_Add_Ons.objects.values('user')
        volunteers = User.objects.filter(pk__in=volunteer_initial)
        self.assertEqual(response.status_code, 200)

        for data in volunteers:
            self.assertContains(response, data.volunteer_user_add_ons.workTitle)

    def test_volunteer_list_interests(self):
        """
        Test to verify that the volunteer list contains the volunteer.interests
        :return:
        """
        response = self.client.get(reverse('teacher_volunteer'))
        volunteer_initial = Volunteer_User_Add_Ons.objects.values('user')
        volunteers = User.objects.filter(pk__in=volunteer_initial)
        self.assertEqual(response.status_code, 200)

        for data in volunteers:
            for interest in data.volunteer_user_add_ons.interests.all():
                self.assertContains(response, interest.name)

    def test_volunteer_list_skills(self):
        """
        Test to verify that the volunteer list contains the volunteer.skills
        :return:
        """
        response = self.client.get(reverse('teacher_volunteer'))
        volunteer_initial = Volunteer_User_Add_Ons.objects.values('user')
        volunteers = User.objects.filter(pk__in=volunteer_initial)
        self.assertEqual(response.status_code, 200)

        for data in volunteers:
            for skill in data.volunteer_user_add_ons.skills.all():
                self.assertContains(response, skill.name)