from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from foraliving.general import Videos
from foraliving.recording import RecordingType, RecordingSetupMicrophone, RecordingSetupFace, RecordingSetupBattery, \
    QuestionInterview, Recording, Orientation, SaveRecording, protected_serve
from foraliving.student import CompleteVideo, StudentAssignment, ConductVideo, SelectQuestion, SelectQuestionEdit, \
    SendEmail, AssignmentList, delete_video
from foraliving.teacher import TeacherStudentT1, TeacherVolunteerT6, TeacherVideosT8, asignment_list, \
    student_list, list_student_group, AssignGroup, uniqueGroup, TeacherVolunteerT6a, AssignVolunteer, list_groups, \
    TeacherVolunteerT9, groupList, studentList, CreateInterview, GroupInterface, update_video, delete_interview, \
    delete_class, AddClass, AddClassAssignment, DownloadTemplate, studentPersonalInfo, delete_student, delete_group, \
    group_members, student_without_group, uniqueGroupEdit, AssignGroupEdit
from foraliving.volunteer import VolunteerProfile, VolunteerEdit
from foraliving.general import Videos
from foraliving.volunteer import Contact, editSkill, GetInterviewed, InterviewQuestionsView, JoinInterviewView, \
    GetQuestionFromInterviewQuestion

from . import views

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    # url(r"^$", views.index, name="home"),
    # url(r"^setup/", views.interviewSetup, name="setup"),
    url(r"^record/", views.record, name="record"),
    url(r"^theme/", views.sitetheme, name='theme'),

    # recording urls
    url(r'^recording_type/(?P<interview_id>\d+)/$', RecordingType.as_view(), name='recording_type'),
    url(r'^setup_microphone/(?P<interview_id>\d+)/$', RecordingSetupMicrophone.as_view(),
        name='recording_setup_microphone'),
    url(r'^setup_face/(?P<interview_id>\d+)/(?P<camera_id>\d+)/$', RecordingSetupFace.as_view(),
        name='recording_setup_face'),
    url(
        r'^setup_battery/(?P<interview_id>\d+)/(?P<camera_id>\d+)/$',
        RecordingSetupBattery.as_view(),
        name='recording_setup_battery'
    ),
    url(
        r'^question_interview/(?P<interview_id>\d+)/(?P<camera_id>\d+)/$',
        QuestionInterview.as_view(),
        name='question_interview'
    ),
    url(r'^recording/(?P<question_id>\d+)/(?P<camera_id>\d+)/$', Recording.as_view(), name='recording'),
    url(r'^orientation/(?P<interview_id>\d+)/$', Orientation.as_view(), name='orientation'),

    # student urls
    url(r'^complete_video/(?P<interview_id>\d+)/$', CompleteVideo.as_view(), name='complete_video'),
    url(r'^assignment/(?P<interview_id>\d+)/$', StudentAssignment.as_view(), name='assignment'),
    url(r'^conduct_video/(?P<interview_id>\d+)/$', ConductVideo.as_view(), name='conduct_video'),
    url(r'^select_question/(?P<interview_id>\d+)/$', SelectQuestion.as_view(), name='select_question'),
    url(r'^select_question_edit/(?P<interview_id>\d+)/$', SelectQuestionEdit.as_view(), name='select_question_edit'),
    url(r'^send_video/(?P<video_id>\d+)/$', SendEmail.as_view(), name='send_email'),
    url(r'^video/save/$', SaveRecording.as_view(), name='save_recording'),
    url(r'^assignment-list/$', AssignmentList.as_view(), name='assignment_list'),
    url(r'^video/delete/$', delete_video, name='delete_video'),

    # volunteer uls
    url(r'^volunteer/profile/(?P<user_id>\d+)/(?P<interview_id>\d+)$', VolunteerProfile.as_view(),
        name='volunteer_profile'),
    url(r'^volunteer/profile/edit/(?P<user_id>\d+)/$', VolunteerEdit.as_view(), name='volunteer_profile_edit'),
    url(r'^edit-skills/(?P<volunteer_id>\d+)/$', editSkill, name='editSkill'),
    url(
        r'^volunteer/get_interviewed$',
        GetInterviewed.as_view(),
        name='volunteer_get_interviewed'
    ),
    url(
        r'^volunteer/interview/(?P<interview_id>\d+)/questions$',
        InterviewQuestionsView.as_view(),
        name='volunteer_interview_questions'
    ),
    url(
        r'^volunteer/interview/(?P<interview_id>\d+)/join$',
        JoinInterviewView.as_view(),
        name='volunteer_join_interview'
    ),
    url(
        r'^volunteer/interview/question/(?P<question_id>[0-9]+)/$',
        GetQuestionFromInterviewQuestion.as_view(),
        name='interview_question_show'
    ),

    # general
    url(r"^$", Videos.as_view(), name='videos'),
    url(r"^contact/", Contact.as_view(), name='contact'),

    # teacher
    url(r"^teacher/class/$", TeacherStudentT1.as_view(), name='teacher_class'),
    url(r"^teacher/volunteer/list/$", TeacherVolunteerT6.as_view(), name='teacher_volunteer'),
    url(r"^teacher/interview-volunteer/create/$", CreateInterview.as_view(), name='create_interview_volunteer'),
    url(r"teacher/interview/create/(?P<user_id>\d+)/$", TeacherVolunteerT9.as_view(), name='create_interview'),
    url(r"^teacher/volunteer/assign/(?P<user_id>\d+)/(?P<assignment_id>\d+)/$", TeacherVolunteerT6a.as_view(),
        name='teacher_volunteer_assign'),
    url(r"^teacher/videos/$", TeacherVideosT8.as_view(), name='teacher_videos'),
    url(r"^assign_group/$", AssignGroup.as_view(), name='assign_group'),
    url(r"^assign/volunteer/(?P<volunteer_id>\d+)/(?P<assignment_id>\d+)/(?P<user_id>\d+)/$",
        AssignVolunteer.as_view(), name='assign_volunteer'),
    url(r"^teacher/class/new/$", AddClass.as_view(), name='teacher_add_class'),
    url(r"^teacher/class/(?P<class_id>\d+)/new/assignment/$", AddClassAssignment.as_view(), name='t_new_assignment'),
    url(r"^teacher/class/new/download/template$", DownloadTemplate.as_view(), name='download_template'),

    url(r"^groups/$", list_groups, name='list_groups'),
    url(r"^unique-group/$", uniqueGroup, name='uniqueGroup'),
    url(r"^get/student-group/(?P<assignment_id>\d+)/$", groupList, name='group_list'),
    url(r"^get/student-list/(?P<assignment_id>\d+)/$", studentList, name='student_list'),
    url(r"^get-assignment/(?P<class_id>\d+)/$", asignment_list, name='assignment_list'),
    url(r"^student-list/(?P<class_id>\d+)/(?P<assignment_id>\d+)/$", student_list, name='class_student_list'),
    url(r"list-student-group", list_student_group, name='list-student_group'),
    url(r"teacher/group/(?P<class_id>\d+)/(?P<assignment_id>\d+)/(?P<group_id>\d+)/$", GroupInterface.as_view(),
        name='group_info'),
    url(r"^video/update/(?P<video_id>\d+)/(?P<flag_id>\d+)/$", update_video, name='update_video'),
    url(r"^interview/delete/$", delete_interview, name='delete_interview'),
    url(r"^class/delete/$", delete_class, name='delete_class'),
    url(r"^student-info/(?P<class_id>\d+)/$", studentPersonalInfo, name='studentPersonalInfo'),
    url(r"^student/delete/$", delete_student, name='delete_student'),
    url(r"^group/delete/$", delete_group, name='delete_group'),
    url(r"^group/members/$", group_members, name='list-group_members'),
    url(r"^class/members/$", student_without_group, name='student_without_group'),
    url(r"^unique-group-edit/$", uniqueGroupEdit, name='uniqueGroupEdit'),
    url(r"^assign_group/edit/$", AssignGroupEdit.as_view(), name='assign_group_edit'),

]

urlpatterns += [
               ] + static(settings.MEDIA_URL, protected_serve, document_root=settings.MEDIA_ROOT)
