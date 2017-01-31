import os

from django.conf import settings
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Volunteer_User_Add_Ons, Class, Assignment, Interview, User_Add_Ons


class TestUpload(TestCase):
    """
        Test Upload CSV feature, this feature upload a csv with students,
        create a class and assign all students to the class
    """
    fixtures = ['initial_data']

    def setUp(self):
        """
            Simulate the teacher login and start the test client
        """
        self.client = Client()
        self.client.login(username='teacher_admin', password='admin123')

    def test_download_template_link(self):
        """
            Verify the Template Downloadable link
        """
        response = self.client.get(reverse('teacher_add_class'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' href="/foraliving/teacher/class/new/download/template">Download template')

    def test_add_new_class(self):
        """
            Verify the post method to add the new class and assign students to the new class
        """
        path = 'files/test_file.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        response = None

        with open(file_path, 'rb') as fh:
            response = self.client.post(
                reverse('teacher_add_class'),
                data={
                    'class_name': 'TestAddClass',
                    'students_csv': fh
                },
                follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' students added correctly')

    def test_add_new_class_too_many_headers(self):
        """
            Verify the post method to add the new class and assign students to the new class
            Error:
                Too many headers
        """
        path = 'files/test_file_more_headers.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        response = None

        with open(file_path, 'rb') as fh:
            response = self.client.post(
                reverse('teacher_add_class'),
                data={
                    'class_name': 'TestAddClass',
                    'students_csv': fh
                },
                follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, ' Too many headers, the file must have 3 headers')

    def test_add_new_class_wrong_headers(self):
        """
            Verify the post method to add the new class and assign students to the new class
            Error:
                wrong headers
        """
        path = 'files/test_file_wrong_headers.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        response = None

        with open(file_path, 'rb') as fh:
            response = self.client.post(
                reverse('teacher_add_class'),
                data={
                    'class_name': 'TestAddClass',
                    'students_csv': fh
                },
                follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Students")
        self.assertContains(response, " should have to be ")

    def test_add_new_class_no_name(self):
        """
            Verify the post method to add the new class and assign students to the new class
            Error:
                No class name
        """
        path = 'files/test_file.csv'
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        response = None

        with open(file_path, 'rb') as fh:
            response = self.client.post(
                reverse('teacher_add_class'),
                data={
                    'class_name': '',
                    'students_csv': fh
                },
                follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Class name missed")
