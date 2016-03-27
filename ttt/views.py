from Crypto.Cipher import AES
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseNotFound
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


def already_logged_in(func):
    def wraper(request, *args, **kwargs):
        if 'user' in request.session:
            return HttpResponseRedirect('/ttt/menu/')
        else:
            return func(request, *args, **kwargs)

    return wraper


def check_logged_user(func):
    def wraper(request, *args, **kwargs):
        name = request.session['user']
        if LoggedUser.objects.filter(name=name).exists():
            return HttpResponseNotFound('<h1>You can maintain only one connection to server!</h1>')
        else:
            return func(request, *args, **kwargs)

    return wraper


def home(request):
    return render(request, 'ttt/board.html', {'size': [0] * 3})


@check_session
def game(request, size):
    listSize = range(0, int(size) ** 2)
    return render(request, 'ttt/pvp.html',
                  {'size': listSize, 'width': 90.0 / int(size), 'margin': 10.0 / (int(size) * 2)})


@check_session
def game_vs_comp(request, size):
    listSize = range(0, int(size) ** 2)
    return render(request, 'ttt/board.html',
                  {'size': listSize, 'width': 90.0 / int(size), 'margin': 10.0 / (int(size) * 2)})


def show_scores(request):
    # scores = Score.objects.order_by('-vs_player')[:10]
    return render(request, 'ttt/scores.html', {'scores': []})


def register(request):
    form = RegisterForm()
    return render(request, 'ttt/login.html', {'form': form})


@already_logged_in
def login(request):
    return render(request, 'ttt/login.html')


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


def send_request(request):
    if 'connection' in request.session:
        return JsonResponse({"connection": 'true'})
    else:
        return JsonResponse({"connection": 'false'})


def invalid(request):
    # here comes invalid message
    messages.error(request, 'Invalid input, try again!')
    return render(request, 'ttt/login.html')


@check_session
def logout(request):
    try:
        for session in Session.objects.all():
            if session.get_decoded().get('user') == request.session['user']:
                session.delete()
        request.session.flush()
        del request.session['user']
        del request.session['connection']
    except KeyError:
        pass
    # here comes successful logout message
    messages.info(request, 'You have been successfully logged out.')
    return render(request, 'ttt/login.html')


@check_session
@check_logged_user
def menu(request):
    return render(request, 'ttt/menu.html')


def search_player(request):
    # names of logged users
    if request.method == 'GET':
        players = LoggedUser.objects.exclude(name=request.session['user'])

    # get particular logged user
    if request.method == 'POST':
        searched_player = request.POST['player']
        players = LoggedUser.objects.filter(name__contains=searched_player).exclude(name=request.session['user'])

    return JsonResponse({'names': [p.name for p in players]})


def get_user(request):
    return JsonResponse({'name': request.session['user']})


def create_connection(request):
    if request.method == 'POST':
        request.session['connection'] = (request.session['user'], request.POST['player'])
        return JsonResponse({'redirect': '/ttt/4/'})
    if request.method == 'GET':
        if 'connection' in request.session:
            return JsonResponse({'me': request.session['connection'][0], 'opponent': request.session['connection'][1]})
        else:
            return JsonResponse({'none': 1})


def drop_connection(request):
    try:
        del request.session['connection']
    except KeyError:
        pass
    return HttpResponseRedirect('/ttt/menu/')


def send_message(request):
    if request.method == 'POST':
        # secret_key = 'key123' potom mozme pouzit
        cipher_text = '{"status": 0, "name": ' + '"' + request.POST['user'] + '"' + '}'

    if request.method == 'GET':
        obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        message = 'The answer is no'
        cipher_text = obj.encrypt(message).decode('ISO-8859-1').strip()

    return JsonResponse({'msg': cipher_text})

