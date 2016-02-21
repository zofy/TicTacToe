from django.shortcuts import render
from models import Score


def home(request):
    return render(request, 'ttt/board.html', {'size': [0]*3})


def game(request, size):
    listSize = range(0, int(size)**2)
    return render(request, 'ttt/board.html', {'size': listSize, 'width': 90.0/int(size), 'margin': 10.0/(int(size)*2)})


def show_scores(request):
    scores = Score.objects.order_by('-vs_player')[:10]
    return render(request, 'ttt/scores.html', {'scores': scores})