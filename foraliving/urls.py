from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from foraliving.recording import RecordingType, RecordingSetupMicrophone, RecordingSetupFace, RecordingSetupBattery, \
    QuestionInterview, Recording, Orientation, SaveRecording, protected_serve
from foraliving.student import CompleteVideo, StudentAssignment, ConductVideo, SelectQuestion, SelectQuestionEdit, \
    SendEmail
from foraliving.volunteer import VolunteerProfile
from foraliving.general import Videos
from foraliving.volunteer import Contact

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
    url(r'^setup_face/(?P<interview_id>\d+)/$', RecordingSetupFace.as_view(), name='recording_setup_face'),
    url(r'^setup_battery/(?P<interview_id>\d+)/$', RecordingSetupBattery.as_view(), name='recording_setup_battery'),
    url(r'^question_interview/(?P<interview_id>\d+)/$', QuestionInterview.as_view(), name='question_interview'),
    url(r'^recording/(?P<question_id>\d+)/$', Recording.as_view(), name='recording'),
    url(r'^orientation/(?P<interview_id>\d+)/$', Orientation.as_view(), name='orientation'),

    # student urls
    url(r'^complete_video/(?P<interview_id>\d+)/$', CompleteVideo.as_view(), name='complete_video'),
    url(r'^assignment/(?P<interview_id>\d+)/$', StudentAssignment.as_view(), name='assignment'),
    url(r'^conduct_video/(?P<interview_id>\d+)/$', ConductVideo.as_view(), name='conduct_video'),
    url(r'^select_question/(?P<interview_id>\d+)/$', SelectQuestion.as_view(), name='select_question'),
    url(r'^select_question_edit/(?P<interview_id>\d+)/$', SelectQuestionEdit.as_view(), name='select_question_edit'),
    url(r'^send_video/(?P<video_id>\d+)/$', SendEmail.as_view(), name='send_email'),
    url(r'^video/save/$', SaveRecording.as_view(), name='save_recording'),

    # volunteer uls
    url(r'^volunteer/profile/(?P<user_id>\d+)/(?P<interview_id>\d+)$', VolunteerProfile.as_view(), name='volunteer_profile'),

    # general
    url(r"^$", Videos.as_view(), name='videos'),
    url(r"^contact/", Contact.as_view(), name='contact')

]

urlpatterns += [
               ] + static(settings.MEDIA_URL, protected_serve, document_root=settings.MEDIA_ROOT)
