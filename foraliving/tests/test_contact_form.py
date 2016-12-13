from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group


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
        self.client.login(username='student_admin', password='admin123')


    def test_first_name_required(self):
        """
            Reason: First Name is required
        """
        response = self.client.post(
            reverse('contact'),
            data={'first_name': '', 'last_name': 'pazos', 'email': 'noelia.pazos@viaro.net'},
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "First Name is required")

    def test__email_required(self):
        """
            Reason: Email is required
        """
        response = self.client.post(
            reverse('contact'),
            data={'first_name': 'Narcy', 'last_name': 'Pazos', 'email': ''},
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Email is required")

    def test__last_name_required(self):
        """
            Reason: Last name is required
        """
        response = self.client.post(
            reverse('contact'),
            data={'first_name': 'Narcy', 'last_name': '', 'email': 'noelia.pazos@viaro.net'},
            follow=True
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Last Name is required")

    def test_send_invitation(self):
        """
            Here we test the send invitation (Successful case)
        """
        response = self.client.post(
            reverse('contact'),
            data={'first_name': 'Narcy', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net'},
            follow=True)
        self.assertRedirects(response, 'volunteer/contact.html',
                             msg_prefix='Invitation Sent Successfully')

