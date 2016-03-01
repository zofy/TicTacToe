from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import Score, Player
from .forms import LoginForm


def home(request):
    return render(request, 'ttt/board.html', {'size': [0]*3})


def game(request, size):
    listSize = range(0, int(size)**2)
    return render(request, 'ttt/board.html', {'size': listSize, 'width': 90.0/int(size), 'margin': 10.0/(int(size)*2)})


def show_scores(request):
    scores = Score.objects.order_by('-vs_player')[:10]
    return render(request, 'ttt/scores.html', {'scores': scores})


def login(request):
    access = 'false'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            p_name = form.cleaned_data['name']
            p_passw = form.cleaned_data['password']

            # overim hraca

            player = Player.objects.filter(name=p_name)
            if player and player[0].password == p_passw:
                access = 'true'
            # redirect to a new URL:
            return render(request, 'ttt/index.html', {'form': form, 'access': access})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'ttt/index.html', {'form': form, 'access': access})