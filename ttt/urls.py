from django.conf.urls import url

from . import views

app_name = 'ttt'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^scores/$', views.show_scores, name='scores'),
    url(r'^(?P<size>[3-9]+)/$', views.game, name='game'),
    url(r'^comp/(?P<size>[3-9]+)/$', views.game_vs_comp, name='gameVsComp'),

    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view, name='authentication'),
    url(r'^invalid/$', views.invalid, name='invalidLogin'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^menu/$', views.menu, name='menu'),
    url(r'^menu/searchPlayer/$', views.search_player, name='search'),
    url(r'^getUser/$', views.get_user, name='getUser'),

    url(r'^menu/createConnection/$', views.create_connection, name='createConnection'),
    url(r'^menu/dropConnection/$', views.drop_connection, name='dropConnection'),
    url(r'^menu/sendMsg/$', views.send_message, name='sendMsg'),
]
