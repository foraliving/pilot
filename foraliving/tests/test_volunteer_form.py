from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Volunteer_User_Add_Ons, Skill, Interest, User_Add_Ons


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

    def test_first_name_required(self):
        """
            Reason: First Name is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': '', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'password': 'admin123', 'phone': '181-12578946', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_last_name_required(self):
        """
            Reason: Last Name is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': '', 'email': 'noelia.pazos@viaro.net',
                  'password': 'admin123', 'phone': '181-12578946', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_email_required(self):
        """
            Reason: Email is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': '',
                  'password': 'admin123', 'phone': '181-12578946', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_username_required(self):
        """
            Reason: Username is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net', 'username': '',
                  'password': 'admin123', 'phone': '181-12578946', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_password_required(self):
        """
            Reason: Password is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': '', 'phone': '181-12578946', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_phone_required(self):
        """
            Reason: Phone is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': 'admin123', 'phone': '', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_can_get_text_required(self):
        """
            Reason: Can Get Text is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': 'admin123', 'phone': '181-1235889', 'canGetText': '',
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_yearssincehsgraduation_required(self):
        """
            Reason: Years Since HS Graduation is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': 'admin123', 'phone': '181-1235889', 'canGetText': True,
                  'yearsSinceHSGraduation': "", 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_collegelevel_required(self):
        """
            Reason: College Level is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': 'admin123', 'phone': '181-1235889', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': '', 'yearsInIndustry': 5},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_years_in_industry_required(self):
        """
            Reason: Years in the Industry is required
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': 'admin123', 'phone': '181-1235889', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': ''},
            follow=True
        )
        self.assertContains(response, "This field is required", 1)
        self.assertEquals(response.status_code, 200)

    def test_user_created(self):
        """
        When the user fill the form, a user should be created in the system
        :return:
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': 'admin123', 'phone': '181-1235889', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        user = User.objects.get(username="noelia_pazos")
        self.assertEquals(user.username, "noelia_pazos")
        self.assertEquals(response.status_code, 200)

    def test_volunteer_created(self):
        """
        When the user fill the form, a volunteer should be created in the system
        :return:
        """
        response = self.client.post(
            reverse('vSignup'),
            data={'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                  'username': 'noelia_pazos',
                  'password': 'admin123', 'phone': '181-1235889', 'canGetText': True,
                  'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5},
            follow=True
        )
        user = User.objects.get(username="noelia_pazos")
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user)
        self.assertEquals(volunteer.user.username, "noelia_pazos")
        self.assertEquals(response.status_code, 200)

    def test_edit_volunteer(self):
        """
        A volunteer could edit their profile
        :return:
        """
        self.client.login(username='volunteer_admin', password='admin123')
        user = User.objects.get(username="volunteer_admin")
        response = self.client.post(
            reverse('volunteer_profile_edit', kwargs={'user_id': user.id}),
            data={
                'first_name': 'Noelia', 'last_name': 'Pazos', 'email': 'noelia.pazos@viaro.net',
                'username': 'noelia_pazos',
                'password': 'admin123', 'phone': '181-1235889', 'canGetText': True,
                'yearsSinceHSGraduation': 1, 'collegeLevel': 1, 'yearsInIndustry': 5
            }
        )

        volunteer_edit = Volunteer_User_Add_Ons.objects.get(user=user)
        self.assertEquals(volunteer_edit.phone, "181-1235889")
        self.assertEquals(response.status_code, 200)

    def test_volunteer_create_skills(self):
        """
        The volunteer can add a list of skills in the volunteer form
        :return:
        """

        skill = Skill(name='business')
        skill.save()
        import json
        skills = json.dumps([{"label": skill.name, "value": skill.name}])
        user = User.objects.get(username="volunteer_admin")
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user)
        response = self.client.post(
            reverse('createSkill', kwargs={'volunteer_id': volunteer.id}),
            data={
                "skills": [skills]
            }
        )
        volunteer_skill = Volunteer_User_Add_Ons.objects.get(skills=skill)
        self.assertEquals(volunteer_skill.user.username, "volunteer_admin")
        self.assertEquals(response.status_code, 200)

    def test_volunteer_create_interests(self):
        """
        The volunteer can add a list of interests in the volunteer form
        :return:
        """

        interest = Interest(name='Education')
        interest.save()
        import json
        interests = json.dumps([{"label": interest.name, "value": interest.name}])
        user = User.objects.get(username="volunteer_admin")
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user)
        response = self.client.post(
            reverse('createSkill', kwargs={'volunteer_id': volunteer.id}),
            data={
                "interests": [interests]
            }
        )
        volunteer_interest = Volunteer_User_Add_Ons.objects.get(interests=interest)
        self.assertEquals(volunteer_interest.user.username, "volunteer_admin")
        self.assertEquals(response.status_code, 200)

    def test_volunteer_edit_interests(self):
        """
        When a volunteer edits their profile, the volunteer can edit the interests in the system
        :return:
        """
        interest = Interest(name='Software')
        interest.save()
        import json
        interests = json.dumps([{"label": interest.name, "value": interest.name}])
        user = User.objects.get(username="volunteer_admin")
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user)
        response = self.client.post(
            reverse('editSkill', kwargs={'volunteer_id': volunteer.id}),
            data={
                "interests": [interests]
            }
        )
        volunteer_interest = Volunteer_User_Add_Ons.objects.get(interests=interest)
        self.assertEquals(volunteer_interest.user.username, "volunteer_admin")
        self.assertEquals(response.status_code, 200)



    def test_volunteer_edit_skills(self):
        """
        When a volunteer edits their profile, the volunteer can edit the skills in the system
        :return:
        """

        skill = Skill(name='numerical')
        skill.save()
        import json
        skills = json.dumps([{"label": skill.name, "value": skill.name}])
        user = User.objects.get(username="volunteer_admin")
        volunteer = Volunteer_User_Add_Ons.objects.get(user=user)
        response = self.client.post(
            reverse('editSkill', kwargs={'volunteer_id': volunteer.id}),
            data={
                "skills": [skills]
            }
        )
        volunteer_skill = Volunteer_User_Add_Ons.objects.get(skills=skill)
        self.assertEquals(volunteer_skill.user.username, "volunteer_admin")
        self.assertEquals(response.status_code, 200)
