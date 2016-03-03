# from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from models import Score, Player


def authenticate(username, password):
    try:
        return Player.objects.get(name=username, password=password)
    except:
        return None


def check_session(request):
    return 'user' not in request.session


def home(request):
    return render(request, 'ttt/board.html', {'size': [0] * 3})


def game(request, size):
    listSize = range(0, int(size) ** 2)

    if check_session(request):
        return HttpResponseRedirect('/ttt/login/')

    return render(request, 'ttt/board.html',
                  {'size': listSize, 'width': 90.0 / int(size), 'margin': 10.0 / (int(size) * 2),
                   'users': request.session['user']})


def show_scores(request):
    scores = Score.objects.order_by('-vs_player')[:10]
    return render(request, 'ttt/scores.html', {'scores': scores})


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
        return HttpResponseRedirect('/ttt/3/')
    else:
        return HttpResponseRedirect('/ttt/invalid/')


def invalid(request):
    return render(request, 'ttt/login.html', {'appendix': 'Invalid input, try again!'})


def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return render(request, 'ttt/login.html', {'appendix': 'You have successfully been logged out!'})


def menu(request):
    pass
