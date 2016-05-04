# from Crypto.Cipher import AES
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render

from models import Player, MenuUser, Score
from ttt.forms import RegisterForm, LoginForm


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
        if MenuUser.objects.filter(name=name).exists():
            return HttpResponseNotFound(
                '<h1>You can maintain only one connection to server!</h1><a href="/ttt/logout/">Logout</a>')
        else:
            return func(request, *args, **kwargs)

    return wraper


def home(request):
    return HttpResponseRedirect('/ttt/menu/')


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
    scores = Score.objects.order_by('-_wins')[:8]
    return render(request, 'ttt/scores.html', {'scores': scores})


def register(request):
    # form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                name = form.cleaned_data['name']
                password = form.cleaned_data['password']
                Player.objects.create_player(name=name, password=password)
                messages.info(request, 'Thanks for signing in!')
                messages.info(request, 'Now you can login.')
                return HttpResponseRedirect('/ttt/login/')
        except IntegrityError:
            messages.error(request, 'Name already exists!')
            messages.error(request, 'Try another one.')
    elif request.method == 'GET':
        form = RegisterForm()

    return render(request, 'ttt/login.html', {'form': form, 'button_name': 'SingUp', 'url': 'ttt:register'})


@already_logged_in
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = None
        if form.is_valid():
            user = form.authenticate()

        if user is not None:
            request.session['user'] = user.name
            request.session.set_expiry(0)
            return HttpResponseRedirect('/ttt/menu/')
        else:
            return HttpResponseRedirect('/ttt/invalid/')

    return render(request, 'ttt/login.html', {'form': form, 'button_name': 'Login', 'url': 'ttt:login'})


def invalid(request):
    form = LoginForm()
    # here comes invalid message
    messages.error(request, 'Invalid input, try again!')
    return render(request, 'ttt/login.html', {'form': form, 'button_name': 'Login', 'url': 'ttt:login'})


@check_session
def logout(request):
    try:
        name = request.session['user']
        if MenuUser.objects.filter(name=name).exists():
            MenuUser.objects.filter(name=name).delete()

        for session in Session.objects.all():
            if session.get_decoded().get('user') == name:
                session.delete()
        del request.session['user']
        del request.session['connection']
        request.session.flush()

    except KeyError:
        pass
    # here comes successful logout message
    messages.info(request, 'You have been successfully logged out.')
    form = LoginForm()
    return render(request, 'ttt/login.html', {'form': form, 'button_name': 'Login', 'url': 'ttt:login'})


@check_session
@check_logged_user
def menu(request):
    return render(request, 'ttt/menu.html')


def search_score(request):
    requested_name = request.POST['player']
    found_scores = Score.objects.filter(player__name__contains=requested_name)
    result = {'scores': []}
    for score in found_scores:
        result['scores'].append([score.player.name, score.wins, score.loses])
    return JsonResponse(result)


def search_player(request):
    # names of logged users
    if request.method == 'GET':
        players = MenuUser.objects.exclude(name=request.session['user'])

    # get particular logged user
    if request.method == 'POST':
        searched_player = request.POST['player']
        players = MenuUser.objects.filter(name__contains=searched_player).exclude(name=request.session['user'])

    return JsonResponse({'names': [p.name for p in players]})


def get_user(request):
    return JsonResponse({'name': request.session.get('user')})


def create_connection(request):
    if request.method == 'POST':
        request.session['connection'] = (request.session['user'], request.POST['player'])
        return JsonResponse({'redirect': '/ttt/9/'})
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


def save_score(request):
    if request.method == 'POST':
        player = Player.objects.get(name=request.POST['name'])
        Score.objects.save_result(player, request.POST['result'])
    return HttpResponse()


def send_message(request):
    if request.method == 'POST':
        # secret_key = 'key123' potom mozme pouzit
        cipher_text = '{"status": 0, "name": ' + '"' + request.POST['user'] + '"' + '}'

    if request.method == 'GET':
        cipher_text = 'huhu'
        # obj = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
        # message = 'The answer is no'
        # cipher_text = obj.encrypt(message).decode('ISO-8859-1').strip()

    return JsonResponse({'msg': cipher_text})
