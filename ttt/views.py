from django.shortcuts import render
from models import Score


def home(request):
    return render(request, 'ttt/board.html', {'size': [0]*3, 's': 2, 'width': 100})


def game(request, size):
    size = int(size)
    list = range(0, size)
    width = 300/size
    return render(request, 'ttt/board.html', {'size': list, 's': size - 1, 'width': width})


def show_scores(request):
    scores = Score.objects.all()
    return render(request, 'ttt/scores.html', {'scores': scores})