from django.conf.urls import url
from . import views

app_name = 'ttt'
urlpatterns = [
    url(r'^$', views.game, name='game')
]