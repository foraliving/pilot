"""foraliving_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from foraliving import views
from foraliving.views import VolunteerForm
from foraliving.parent import AccountSetup

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^foraliving/', include('foraliving.urls')),
    url(r"^account/", include("account.urls")),
    url(r"^$", views.index, name="home"),
    url(r"^theme/", views.sitetheme, name='theme'),
    url(r"^volunteer/create/", VolunteerForm.as_view(), name='vSignup'),
    url(r"^account/setup/", AccountSetup.as_view(), name='accountSetup'),
    url(r"^create-skills/(?P<volunteer_id>\d+)/$", views.createSkill, name='createSkill'),
    url(r"^unique-email/", views.uniqueEmail, name='uniqueEmail'),
    url(r"^unique-username/", views.uniqueUsername, name='uniqueUsername'),
    url(r"^categories/", views.categories, name='Categories'),
    url(r"^interests/", views.interests, name='Interests'),

]
