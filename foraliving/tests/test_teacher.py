from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from foraliving.models import Volunteer_User_Add_Ons, Class, Assignment, Interview, User_Add_Ons, Student_Class, \
    Interview_Question_Map, Interview, \
    Interview_Question_Video_Map, Question, Video


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

    def test_group_interviewee_name(self):
        """
        Test to display the interviewee information from t4
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        group = Group.objects.get(user=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        interview = Interview.objects.get(assignment=assignment, group=group)
        response = self.client.get(reverse('group_info', kwargs={'class_id': student_class.falClass.id,
                                                                 'assignment_id': assignment.id, 'group_id': group.id}))
        self.assertContains(response, interview.interviewee.first_name)
        self.assertContains(response, interview.interviewee.last_name)

    def test_student_info(self):
        """
        Test to display the student information from t1
        :return:
        """
        user = User.objects.get(pk=6)
        student_class = Student_Class.objects.get(student=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        response = self.client.get(reverse('studentPersonalInfo', kwargs={'class_id': student_class.falClass.id}))
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.username)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_display_number_videos(self):
        """
        Test to display the number of videos approval from t4
        :return:
        """
        file = open('examples/test.webm', 'r', encoding='utf-8', errors='ignore')
        question = Question.objects.get(pk=23)
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        group = Group.objects.get(user=user)
        assignment = Assignment.objects.get(falClass=student_class.falClass)
        interview = Interview.objects.get(assignment=assignment, group=group)
        interview_question = Interview_Question_Map(interview=interview, question=question)
        interview_question.save()
        response_save = self.client.post(
            reverse('save_recording'), data={'data': file, 'interview_question': interview_question.id})
        self.assertEqual(response_save.status_code, 200)
        self.assertContains(response_save, "Done")
        interview_question_video = Interview_Question_Video_Map.objects.get(interview_question=interview_question)
        video_old = Video.objects.get(pk=interview_question_video.video.id)
        response = self.client.get(reverse('update_video', kwargs={'video_id': video_old.id, 'flag_id': 1}))

        response = self.client.get(reverse('group_info', kwargs={'class_id': student_class.falClass.id,
                                                                 'assignment_id': assignment.id, 'group_id': group.id}))
        self.assertContains(response, "You have 1 video(s) waiting to be approved")

    def test_approval_videos_group(self):
        """
        Test to verify when a teacher will change the video status
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

        video_old = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_old.status, "new")
        response = self.client.get(reverse('update_video', kwargs={'video_id': video_old.id, 'flag_id': 0}))
        video_new = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_new.status, "approved")

    def test_not_approval_videos_group(self):
        """
        Test to verify when a teacher will change the video status
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

        video_old = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_old.status, "new")
        response = self.client.get(reverse('update_video', kwargs={'video_id': video_old.id, 'flag_id': 0}))
        video_new = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_new.status, "approved")

        response = self.client.get(reverse('update_video', kwargs={'video_id': video_new.id, 'flag_id': 1}))
        video_new = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_new.status, "pending")

    def test_remove_student(self):
        """
        Test when a teacher delete a student of a class
        :return:
        """
        user = User.objects.get(pk=6)
        response = self.client.post(
            reverse('delete_student'), data={'user_id': user.id})
        self.assertEqual(response.status_code, 200)

    def test_create_assignment(self):
        """
        Test to create a new assignment
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        response = self.client.post(reverse('t_new_assignment', kwargs={'class_id': student_class.falClass.id}),
                                    data={'assignment_name': 'New Assignment',
                                          'description': 'this is a test to create a new assignment'})
        self.assertContains(response, "Assignment added successfully")

    def test_assignment_error_title(self):
        """
        Test to create a new assignment
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        response = self.client.post(reverse('t_new_assignment', kwargs={'class_id': student_class.falClass.id}),
                                    data={'assignment_name': '',
                                          'description': 'this is a test to create a new assignment'})
        self.assertContains(response, "Assignment not added")

    def test_delete_class(self):
        """
        Test to verify when a teacher delete a class
        :return:
        """
        user = User.objects.get(pk=2)
        student_class = Student_Class.objects.get(student=user)
        response = self.client.post(
            reverse('delete_class'), data={'class_id': student_class.falClass.id})
        self.assertEqual(response.status_code, 200)


    def test_edit_group_name_without_student(self):
        """
        Test to verify when a teacher edit a group
        :return:
        """
        group = Group.objects.get(name="Sports")
        response = self.client.post(reverse("assign_group_edit"), data={'group_id': group.id, 'group_name': "Sports Update", 'students[]': [""]})
        self.assertContains(response, "true")
        self.assertEqual(response.status_code, 200)

    def test_edit_group_with_student(self):
        """
        Test to verify when a teacher edit a group
        :return:
        """
        group = Group.objects.get(name="Sports")
        student_group = User.objects.filter(groups__name="Sports").values_list('id', flat=True)
        test = list(student_group)
        response = self.client.post(reverse("assign_group_edit"),
                                    data={'group_id': group.id, 'group_name': "Sports Update", 'students[]': test})
        self.assertContains(response, "true")
        self.assertEqual(response.status_code, 200)

    def test_delete_group(self):
        """
        Test to verify when a teacher delete a class
        :return:
        """
        group = Group.objects.get(pk=1)
        response = self.client.post(
            reverse('delete_group'), data={'group_id': group.id})

        self.assertEqual(response.status_code, 200)


    def test_display_teacherVideos__without_videos(self):
        """
        Test to verify when a teacher to use the videos interface and not exist videos
        :return:
        """
        response = self.client.get(
            reverse('teacher_videos'))
        self.assertContains(response, "There are no videos for this class")

    def test_display_teacherVideos__with_videos(self):
        """
        Test to verify when a teacher to use the videos interface
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
        video_old = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_old.status, "new")
        response = self.client.get(reverse('update_video', kwargs={'video_id': video_old.id, 'flag_id': 0}))
        video_new = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_new.status, "approved")
        response_videos = self.client.get(
            reverse('teacher_videos'))
        self.assertEqual(response_videos.status_code, 200)
        self.assertContains(response_videos, video_new.url)

    def test_display_teacherVideos__with_class(self):
        """
        Test to verify when a teacher to use the videos interface and select one class
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
        video_old = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_old.status, "new")
        response = self.client.get(reverse('update_video', kwargs={'video_id': video_old.id, 'flag_id': 0}))
        video_new = Video.objects.get(pk=interview_question_video.video.id)
        self.assertEqual(video_new.status, "approved")
        response_videos = self.client.get(
            reverse('teacher_videos' )+ "?class=1")
        self.assertEqual(response_videos.status_code, 200)
        self.assertContains(response_videos, video_new.url)










