from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from foraliving.recording import RecordingType, RecordingSetupMicrophone, RecordingSetupFace, RecordingSetupBattery, \
    QuestionInterview, Recording, Orientation, SaveRecording, protected_serve
from foraliving.student import CompleteVideo, StudentAssignment, ConductVideo, SelectQuestion, SelectQuestionEdit, SendEmail
from foraliving.volunteer import VolunteerProfile

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^$", views.index, name="home"),
    # url(r"^setup/", views.interviewSetup, name="setup"),
    url(r"^record/", views.record, name="record"),
    url(r"^theme/", views.sitetheme, name='theme'),
    url(r"^volunteer-signup/", views.volunteerSignup, name='vSignup'),

    # recording urls
    url(r'^recording_type/$', RecordingType.as_view(), name='recording_type'),
    url(r'^setup_microphone/$', RecordingSetupMicrophone.as_view(), name='recording_setup_microphone'),
    url(r'^setup_face/$', RecordingSetupFace.as_view(), name='recording_setup_face'),
    url(r'^setup_battery/$', RecordingSetupBattery.as_view(), name='recording_setup_battery'),
    url(r'^question_interview/(?P<interview_id>\d+)/$', QuestionInterview.as_view(), name='question_interview'),
    url(r'^recording/(?P<question_id>\d+)/$', Recording.as_view(), name='recording'),
    url(r'^orientation/$', Orientation.as_view(), name='orientation'),

    # student urls
    url(r'^complete_video/$', CompleteVideo.as_view(), name='complete_video'),
    url(r'^assignment/$', StudentAssignment.as_view(), name='assignment'),
    url(r'^conduct_video/$', ConductVideo.as_view(), name='conduct_video'),
    url(r'^select_question/(?P<interview_id>\d+)/$', SelectQuestion.as_view(), name='select_question'),
    url(r'^select_question_edit/(?P<interview_id>\d+)/$', SelectQuestionEdit.as_view(), name='select_question_edit'),
    url(r'^send_video/(?P<video_id>\d+)/$', SendEmail.as_view(), name='send_email'),

    # volunteer uls
    url(r'^volunteer/profile/(?P<user_id>\d+)/$', VolunteerProfile.as_view(), name='volunteer_profile'),
    url(r'^video/save/$', SaveRecording.as_view(), name='save_recording')

]

urlpatterns += [
               ] + static(settings.MEDIA_URL, protected_serve, document_root=settings.MEDIA_ROOT)
