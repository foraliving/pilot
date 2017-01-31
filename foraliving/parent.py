from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from foraliving.models import Class, User_Add_Ons


class AccountSetup(LoginRequiredMixin, generic.View):
    """Generic view to setup the student account"""
    login_url = settings.LOGIN_URL
    account_view = 'parent/setup_account.html'

    def get(self, request):
        """
        :param request:
        :return:
        """
        return render(request, self.account_view)