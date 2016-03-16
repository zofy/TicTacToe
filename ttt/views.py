from Crypto.Cipher import AES
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render

from models import Player, LoggedUser
from ttt.forms import RegisterForm


def authenticate(username, password):
    try:
        return Player.objects.get(name=username, password=password)
    except:
        return None


def check_session(func):
    def wraper(request, *args, **kwargs):
        if 'user' not in request.session:
            return HttpResponseRedirect('/ttt/login/')
        else:
            return func(request, *args, **kwargs)

    return wraper


def home(request):
    return render(request, 'ttt/board.html', {'size': [0] * 3})


@check_session
def game(request, size):
    listSize = range(0, int(size) ** 2)
    return render(request, 'ttt/board.html',
                  {'size': listSize, 'width': 90.0 / int(size), 'margin': 10.0 / (int(size) * 2)})


@check_session
def game_vs_comp(request, size):
    listSize = range(0, int(size) ** 2)
    return render(request, 'ttt/board.html',
                  {'size': listSize, 'width': 90.0 / int(size), 'margin': 10.0 / (int(size) * 2)})


def show_scores(request):
    # scores = Score.objects.order_by('-vs_player')[:10]
    return render(request, 'ttt/scores.html', {'scores': []})


def login(request):
    form = RegisterForm()
    return render(request, 'ttt/login.html', {'form': form})


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username, password)

    # user = User.objects.create_user(username, password)
    # user.save()
    # return HttpResponseRedirect('/ttt/3/')

    if user is not None:
        request.session['user'] = user.name
        request.session.set_expiry(0)
        return HttpResponseRedirect('/ttt/menu/')
    else:
        return HttpResponseRedirect('/ttt/invalid/')


def invalid(request):
    # here comes invalid message
    messages.error(request, 'Invalid input, try again!')
    return render(request, 'ttt/login.html')


def logout(request):
    try:
        for session in Session.objects.all():
            if session.get_decoded().get('user') == request.session['user']:
                session.delete()
        del request.session['user']
    except KeyError:
        pass
    # here comes successful logout message
    messages.info(request, 'You have been successfully logged out.')
    return render(request, 'ttt/login.html')


@check_session
def menu(request):
    return render(request, 'ttt/menu.html')


def search_player(request):
    # names of logged users
    if request.method == 'GET':
        players = LoggedUser.objects.exclude(name=request.session['user'])
        # data = Session.objects.all()
        # return JsonResponse({'names': [session.get_decoded().get('user') for session in data]})

    # get particular logged user
    if request.method == 'POST':
        searched_player = request.POST['player']
        players = LoggedUser.objects.filter(name__contains=searched_player).exclude(name=request.session['user'])

    return JsonResponse({'names': [p.name for p in players]})


def get_user(request):
    return JsonResponse({'name': request.session['user']})


def send_message(request):
    if request.method == 'POST':
        # secret_key = 'key123' potom mozme pouzit
        cipher_text = '{"status": 0, "name": ' + request.POST['user'] + '}'

    if request.method == 'GET':
        cipher_text = 'Hello everybody!'

    return JsonResponse({'msg': cipher_text})

