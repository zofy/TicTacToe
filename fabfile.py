from fabric.api import local


def backup():
    local('git pull')
    local('git add .')

    print('enter your commit comment: ')
    comment = raw_input()
    local('git commit -m "%s"' % comment)

    local('git push')


def switch_debug(what_to_change, change_to):
    local('cp TicTacToe/local_settings.py TicTacToe/local_settings.bak')
    sed = "sed 's/^DEBUG = %s$/DEBUG = %s/' TicTacToe/local_settings.bak > TicTacToe/local_settings.py"
    local(sed % (what_to_change, change_to))
    local('rm TicTacToe/local_settings.bak')


def deploy():
    local('pip freeze --local > requirements.txt')
    # local('git pull')
    # local('git add .')
    #
    # print('enter your commit comment: ')
    # comment = raw_input()
    # local('git commit -m "%s"' % comment)
    #
    # local('git push')

    switch_debug('True', 'False')
    local('python manage.py collectstatic')
    switch_debug('False', 'True')

    local('heroku maintenance:on')
    local('git push heroku')
    local('heroku run python manage.py migrate')
    local('heroku maintenance:off')
