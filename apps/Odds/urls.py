from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^show_odds/(?P<id>\d+)$', views.show_odds, name="show_odds"),
    url(r'^create_bets/(?P<id>\d+)$', views.create_bets, name="create_bets"),
    url(r'^login_index$', views.login_index, name='login_index'),
    url(r'^login$', views.login),
    url(r'^registrate$', views.registrate),
    url(r'^register$', views.register, name = 'register'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^success$', views.success),
    url(r'^validate_proposition/(?P<id>\d+)$', views.validate_proposition, name = "validate_proposition"),
    url(r'^show_other_bets/(?P<id>\d+)$', views.show_other_bets, name = "show_other_bets"),
    url(r'^take_other_side/(?P<id>\d+)$',views.take_other_side, name = 'take_other_side'),
]
