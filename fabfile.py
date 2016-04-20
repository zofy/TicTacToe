from fabric.api import local


def backup():
    local('git pull')
    local('git add .')

    print('enter your commit comment: ')
    comment = raw_input()
    local('git commit -m "%s"' % comment)

    local('git push')
