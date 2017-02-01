import os
import psycopg2
from django.db import connection
from django.http import JsonResponse
cursor = connection.cursor()
from django.db import connection
from datetime import datetime
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.static import serve
from django.http import HttpResponseRedirect
from foraliving.models import Interview_Question_Map, Question, Video, Question_Video_Map, Interview_Question_Video_Map, \
    User_Add_Ons


@login_required(login_url='/account/login/')
def protected_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)


class RecordingType(LoginRequiredMixin, generic.View):
    """Generic view to display the recording page,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL

    recording_view = 'recording/recording_type.html'

    def get(self, request, interview_id):
        return render(request, self.recording_view, {'interview': interview_id})


class RecordingSetupMicrophone(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (microphone),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup_microphone.html'

    def get(self, request, interview_id):
        return render(request, self.setup_view, {'interview': interview_id})


class RecordingSetupFace(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (face),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup_face.html'

    def get(self, request, interview_id, camera_id):
        return render(
            request,
            self.setup_view,
            {
                'interview': interview_id,
                'camera_id': camera_id
            }
        )


class RecordingSetupBattery(LoginRequiredMixin, generic.View):
    """Generic view to display the recording setup (battery),
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/setup_battery.html'

    def get(self, request, interview_id):
        return render(request, self.setup_view, {'interview': interview_id})


class QuestionInterview(LoginRequiredMixin, generic.View):
    """Generic view to display the question of the interview,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'recording/questions.html'

    def get(self, request, interview_id):
        general_videos = []
        practice_question = Question.objects.get(
            name="What is your favorite book and why? (student practice question)")
        questions = Interview_Question_Map.objects.filter(interview=interview_id)
        question_default = Interview_Question_Map.objects.filter(question_id=practice_question.id,
                                                                 interview_id=interview_id)
        if not questions:
            new_data = Interview_Question_Map(interview_id=interview_id, question_id=practice_question.id)
            new_data.save()

        interview_question_map = Interview_Question_Map.objects.filter(interview=interview_id)

        cursor_q = connection.cursor()
        cursor_q.execute("""SELECT * FROM foraliving_interview_question_map as IQ inner join foraliving_question as Q on
        IQ.question_id=Q.id WHERE interview_id=(%s) AND IQ.id NOT IN ( SELECT interview_question_id FROM foraliving_interview_question_video_map)""", (interview_id,))
        questions = cursor_q.fetchall()
        cursor_q.close()

        cursor_v = connection.cursor()
        cursor_v.execute(
            """SELECT Q.name, IQ.id, count(*) from foraliving_interview_question_map as IQ  inner join
foraliving_interview_question_video_map as IQV  on IQV.interview_question_id =IQ.id  inner join foraliving_question as Q
on Q.id=IQ.question_id where IQ.interview_id=(%s) group by Q.name, IQ.id""", (interview_id,))
        results = cursor_v.fetchall()
        for result in results:
            all = []
            all.append(result[0])
            all.append(result[1])
            all.append(result[2])
            all.append("")
            for interview in interview_question_map:
                if result[1] == interview.id:
                    question_video = Interview_Question_Video_Map.objects.filter(interview_question=interview.id).first()
                    all[3] = question_video.video.url
            general_videos.append(all)

        return render(request, self.question_view,
                      {'questions': questions, 'interview': interview_id, 'results': general_videos})


class Recording(LoginRequiredMixin, generic.View):
    """Generic view to display the recording interface,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    question_view = 'recording/recording.html'

    def get(self, request, question_id):
        questions = Interview_Question_Map.objects.get(pk=question_id)
        return render(request, self.question_view, {'questions': questions, 'question_name': questions.question.name})


class Orientation(LoginRequiredMixin, generic.View):
    """Generic view to display the orientation page,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/orientation.html'

    def get(self, request, interview_id):
        return render(request, self.setup_view, {'interview': interview_id})


class SaveRecording(LoginRequiredMixin, generic.View):
    """Generic view to save the video in the server,
    this will be shown after login success"""
    login_url = settings.LOGIN_URL
    setup_view = 'recording/assignment.html'

    def post(self, request):
        today = datetime.today()
        today = str(today.isoformat())
        file = request.FILES['data']
        media_root = settings.MEDIA_ROOT
        interview_question = Interview_Question_Map.objects.get(pk=request.POST.get("interview_question"))

        path = "videos/" + "_iq" + str(interview_question.id) + "_q" + str(interview_question.question.id) + "date_" + (
            today.replace(' ', '')) + ".webm"
        # #create video
        user_add = User_Add_Ons.objects.get(user=request.user.id)
        video = Video(name=interview_question.question.name, url=path, tags="student", created_by=user_add,
                      creation_date=today, status="new")
        video.save()

        # #create question_video
        question_video = Question_Video_Map(question=interview_question.question, video=video)
        question_video.save()

        # create interview_question_video
        interview_question_video = Interview_Question_Video_Map(interview_question=interview_question, video=video)
        interview_question_video.save()

        # save the video
        path = default_storage.save(path, ContentFile(file.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        return JsonResponse("Done", safe=False)