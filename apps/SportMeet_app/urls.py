from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^loginUser$', views.loginUser),
    url(r'^registerUser$', views.registerUser),
    url(r'^home_page$', views.home_page),
    url(r'^logout$', views.logout),
    url(r'^addTeam$', views.addTeam),
    url(r'^createTeam$', views.createTeam),
    url(r'^viewTeam/(?P<team_id>\d+)$', views.viewTeam),
    url(r'^joinTeam/(?P<team_id>\d+)$', views.joinTeam),
    url(r'^deleteTeam/(?P<team_id>\d+)$', views.deleteTeam),
    url(r'^cancelTeam/(?P<team_id>\d+)$', views.cancelTeam),
]