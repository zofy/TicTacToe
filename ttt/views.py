from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import Score, Player


def home(request):
    return render(request, 'ttt/board.html', {'size': [0] * 3})


def game(request, size):
    listSize = range(0, int(size) ** 2)
    return render(request, 'ttt/board.html',
                  {'size': listSize, 'width': 90.0 / int(size), 'margin': 10.0 / (int(size) * 2)})


def show_scores(request):
    scores = Score.objects.order_by('-vs_player')[:10]
    return render(request, 'ttt/scores.html', {'scores': scores})


def login(request):
    return render(request, 'ttt/login.html')


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    try:
        user = Player.objects.get(name=username, password=password)
    except:
        user = None

    if user is not None:
        return HttpResponseRedirect('/ttt/3/')
    else:
        return HttpResponseRedirect('/ttt/invalid/')


def invalid(request):
    return render(request, 'ttt/login.html', {'appendix': 'Invalid input, try again!'})
