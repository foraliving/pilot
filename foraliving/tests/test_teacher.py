from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Volunteer_User_Add_Ons, Class, Assignment, Interview, User_Add_Ons, Student_Class


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
        self.assertContains(response, 'Students')
        self.assertContains(response, 'Volunteers')
        self.assertContains(response, 'Videos')

    def test_verify_teacher_selection_navigation_student(self):
        """
        Test to verify the select options on the menu if the user is teacher
        :return:
        """
        response = self.client.get(
            reverse('teacher_class'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Students')
        self.assertContains(response, 'Volunteers')
        self.assertContains(response, 'Videos')

    def test_verify_teacher_selection_navigation_volunteer(self):
        """
        Test to verify the select options on the menu if the user is teacher
        :return:
        """
        response = self.client.get(
            reverse('teacher_volunteer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Students')
        self.assertContains(response, 'Volunteers')
        self.assertContains(response, 'Videos')

    def test_verify_teacher_selection_navigation_videos(self):
        """
        Test to verify the select options on the menu if the user is teacher
        :return:
        """
        response = self.client.get(
            reverse('teacher_videos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Students')
        self.assertContains(response, 'Volunteers')
        self.assertContains(response, 'Videos')

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

    def test_assignment_list(self):
        """
        Test to verify that the assignment list is displayed with the student info, volunteer and group
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        response = self.client.get(reverse('class_student_list', kwargs={'class_id': student_class.falClass.id,
                                                                         'assignment_id': assignment.id}))
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)

    def test_assignment_list_group(self):
        """
        Test to verify that the assignment list is displayed with the student info, volunteer and group
        :return:
        """
        user = User.objects.get(pk=6)
        group = Group.objects.get(user=user)
        student_class = Student_Class.objects.get(student=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        response = self.client.get(reverse('class_student_list', kwargs={'class_id': student_class.falClass.id,
                                                                         'assignment_id': assignment.id}))
        self.assertContains(response, group)

    def test_assignment_remove_volunteer(self):
        """
        Test to verify when a volunteeer is removed of the system from T3 interface
        :return:
        """
        user = User.objects.get(pk=1)
        response = self.client.get(reverse('delete_interview'), data={'interview_id': user.id})
        self.assertEquals(response.status_code, 200)

    def test_assign_volunter_t3_interface(self):
        """
        Test to assign a volunteer to interview from t3 interface
        :return:
        """
        user = User.objects.get(pk=6)
        group = Group.objects.get(user=user)
        student_class = Student_Class.objects.get(student=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        volunteer = User.objects.get(pk=1)
        response = self.client.get(reverse('assign_volunteer',
                                           kwargs={'volunteer_id': volunteer.id, 'assignment_id': assignment.id,
                                                   'user_id': user.id}))

        redirect_url = '/foraliving/teacher/class/?class=' + str(student_class.falClass.id) + '&assignment=' + str(
            assignment.id)
        self.assertRedirects(response, redirect_url)

    def test_assign_volunter_t6_interface(self):
        """
        Test to assign a volunteer to interview from t9 interface
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        volunteer = User.objects.get(pk=1)
        response = self.client.post(reverse('create_interview_volunteer'),
                                    data={'volunteer_id': volunteer.id, 'assignment': assignment.id,
                                          'new_option': user.id, 'result': 'a'})
        self.assertEquals(response.status_code, 200)

    def test_assign_volunter_t6_interface_with_group(self):
        """
        Test to assign a volunteer to interview from t9 interface
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        volunteer = User.objects.get(pk=1)
        group = Group.objects.get(user=user)
        response = self.client.post(reverse('create_interview_volunteer'),
                                    data={'volunteer_id': volunteer.id, 'assignment': assignment.id,
                                          'new_option': group.id, 'result': 'b'})
        self.assertEquals(response.status_code, 200)

    def test_assign_group_with_new_group(self):
        """
        Assignt students to new group from T3 interface
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        response = self.client.post(reverse('assign_group'),
                                    data={'selected[]': [user.id], 'group': "",
                                          'group_name': "tests", 'class_id': student_class.falClass.id})
        self.assertEquals(response.status_code, 200)

    def test_assign_group_with_existing_group(self):
        """
        Assignt students to new group from T3 interface
        :return:
        """
        user = User.objects.get(pk=7)
        group = Group.objects.get(name="Sports")
        student_class = Student_Class.objects.get(student=user)
        response = self.client.post(reverse('assign_group'),
                                    data={'selected[]': [user.id], 'group': group.id,
                                          'group_name': "", 'class_id': student_class.falClass.id})
        self.assertEquals(response.status_code, 200)


    def test_group_data(self):
        """
        Test to display the group information (name) from t4
        :return:
        """
        user = User.objects.get(pk=6)
        student_class = Student_Class.objects.get(student=user)
        group = Group.objects.get(user=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        response = self.client.get(reverse('group_info', kwargs={'class_id': student_class.falClass.id,
                                                                         'assignment_id': assignment.id, 'group_id': group.id}))
        self.assertContains(response, group.name)

    def test_group_student_list(self):
        """
        Test to display the student list from t4
        :return:
        """
        user = User.objects.get(pk=6)
        student_class = Student_Class.objects.get(student=user)
        group = Group.objects.get(user=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        response = self.client.get(reverse('group_info', kwargs={'class_id': student_class.falClass.id,
                                                                 'assignment_id': assignment.id, 'group_id': group.id}))
        self.assertContains(response, user.first_name + " " + user.last_name + ",")











