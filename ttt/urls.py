from django.conf.urls import url
from . import views

app_name = 'ttt'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^scores/$', views.show_scores, name='scores'),
    url(r'^(?P<size>[0-9]+)/$', views.game, name='game'),
    url(r'^login/$', views.get_name, name='login'),
]