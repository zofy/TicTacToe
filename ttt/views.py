from django.shortcuts import render
from models import Score


def home(request):
    return render(request, 'ttt/board.html', {'size': [0]*3})


def game(request, size):
    size = int(size)
    list = range(0, size**2)
    return render(request, 'ttt/board.html', {'size': list})


def show_scores(request):
    scores = Score.objects.order_by('-vs_player')[:10]
    return render(request, 'ttt/scores.html', {'scores': scores})