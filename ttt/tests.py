from django.core.urlresolvers import reverse
from django.test import TestCase

from ttt.models import Player, LoggedUser


class PlayerTest(TestCase):
    def create_player(self, name='Bambo', password='bubu'):
        return Player.objects.create(name=name, password=password, vs_player=0, vs_comp=0)

    def test_player_creation(self):
        p = self.create_player()
        self.assertTrue(isinstance(p, Player))
        self.assertEqual(p.name + ', ' + p.password, p.__str__())

    def test_authenticate(self):
        p = self.create_player()
        self.assertEqual(p, Player.objects.get(name=p.name, password=p.password))

    def test_login(self):
        resp = self.client.get(reverse('ttt:login'))
        self.assertEqual(resp.status_code, 200)

    def test_auth_view(self):
        p = self.create_player()

        # login with created user
        url = reverse('ttt:authentication')
        resp = self.client.post(url, {'username': p.name, 'password': p.password})
        session = self.client.session

        # test whether user is in the session and whether page is redirected
        self.assertIn('user', session)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('ttt:menu'))

        session.delete()  # we have delete session in order to obtain new one after next login

        # login with empty data
        resp = self.client.post(url, {})

        # user should not be in the session and should be redirected to ttt:invalid
        self.assertNotIn('user', self.client.session)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('ttt:invalidLogin'))

    def test_get_user(self):
        # login
        p = self.create_player()
        url = reverse('ttt:authentication')
        self.client.post(url, {'username': p.name, 'password': p.password})

        # test whether I 'm in session
        resp = self.client.get(reverse('ttt:getUser'))
        self.assertEqual(p.name, resp.json()['name'])


class LoggedUserTest(TestCase):
    def create_loggedUser(self, name='Novy'):
        return LoggedUser.objects.create(name=name)

    def test_loggedUser_creation(self):
        u = self.create_loggedUser()
        self.assertTrue(isinstance(u, LoggedUser))

    def test_search_player(self):
        # login
        p = Player.objects.create(name='Bubak', password='bubu', vs_player=0, vs_comp=0)
        self.client.post(reverse('ttt:authentication'), {'username': p.name, 'password': p.password})
        u1 = self.create_loggedUser(name=p.name)
        u2 = self.create_loggedUser(name='Matt')
        u3 = self.create_loggedUser(name='Mathew')

        # get all logged users apart from 'me' - so to speak u1
        resp = self.client.get(reverse('ttt:search'))

        self.assertEqual([u2.name, u3.name], resp.json()['names'])

        # now get only searched player (logged user)
        resp = self.client.post(reverse('ttt:search'), {'player': u3.name})
        self.assertEqual([u3.name], resp.json()['names'])
