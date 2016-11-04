from django.conf.urls import include, url

from django.contrib import admin
from . import views
from foraliving.recording import RecordingType, RecordingSetup, RecordingSetup2, RecordingSetup3, QuestionInterview, Recording

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
    url(r'^setup/$', RecordingSetup.as_view(), name='recording_setup'),
    url(r'^setup2/$', RecordingSetup2.as_view(), name='recording_setup2'),
    url(r'^setup3/$', RecordingSetup3.as_view(), name='recording_setup3'),
    url(r'^question_interview/$', QuestionInterview.as_view(), name='question_interview'),
    url(r'^recording/(?P<question_id>\d+)/$', Recording.as_view(), name='recording'),
]
