from django.shortcuts import render


def game(request):
    list = range(0,6)
    l = len(list)
    width = 300/l
    return render(request, 'ttt/board.html', {'size': list, 's': l - 1, 'width':width})