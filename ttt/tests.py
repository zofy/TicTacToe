from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver

from ttt.models import Player, MenuUser


class PlayerTest(TestCase):
    def create_player(self, name='Bambo', password='bububu'):
        return Player.objects.create(name=name, password=password)

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
        url = reverse('ttt:login')
        resp = self.client.post(url, {'name': p.name, 'password': p.password})
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
        url = reverse('ttt:login')
        self.client.post(url, {'name': p.name, 'password': p.password})

        # test whether I 'm in session
        resp = self.client.get(reverse('ttt:getUser'))
        self.assertEqual(p.name, resp.json()['name'])

    def test_logout(self):
        # login user
        p = self.create_player()
        self.client.post(reverse('ttt:login'), {'name': p.name, 'password': p.password})
        self.assertIn('user', self.client.session)

        # log him out
        resp = self.client.get(reverse('ttt:logout'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('You have been successfully logged out.', resp.content)
        self.assertNotIn('user', self.client.session)

    def test_game_vs_comp(self):
        # login user and let him play
        p = self.create_player()
        self.client.post(reverse('ttt:login'), {'name': p.name, 'password': p.password})

        resp = self.client.get(reverse('ttt:gameVsComp', args=[3]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(3 ** 2, len(resp.context['size']))


class LoggedUserTest(TestCase):
    def create_loggedUser(self, name='Novy'):
        return MenuUser.objects.create(name=name)

    def test_loggedUser_creation(self):
        u = self.create_loggedUser()
        self.assertTrue(isinstance(u, MenuUser))

    def test_search_player(self):
        # login
        p = Player.objects.create(name='Bubak', password='bububu')
        self.client.post(reverse('ttt:login'), {'name': p.name, 'password': p.password})

        u1 = self.create_loggedUser(name=p.name)
        u2 = self.create_loggedUser(name='Matt')
        u3 = self.create_loggedUser(name='Mathew')

        # get all logged users apart from 'me' - so to speak u1
        resp = self.client.get(reverse('ttt:searchPlayer'))

        self.assertEqual([u2.name, u3.name], resp.json()['names'])

        # now get only searched player (logged user)
        resp = self.client.post(reverse('ttt:searchPlayer'), {'player': u3.name})
        self.assertEqual([u3.name], resp.json()['names'])

        # but cannot get me
        resp = self.client.post(reverse('ttt:searchPlayer'), {'player': u1.name})
        self.assertNotIn(u1.name, resp.json()['names'])


# Selenium tests
class SeleniumTestCase(LiveServerTestCase):
    def open(self, url):
        self.wd.get("%s%s" % (self.live_server_url, url))

    def setUp(self):
        # setUp is where you setup call fixture creation scripts
        # and instantiate the WebDriver, which in turns loads up the browser.
        # User.objects.create_superuser(username='admin',
        #                               password='pw',
        #                               email='info@lincolnloop.com')

        # Instantiating the WebDriver will load your browser
        self.wd = webdriver.Firefox()

    def tearDown(self):
        # Don't forget to call quit on your webdriver, so that
        # the browser is closed after the tests are ran
        self.wd.quit()

    def test_login(self):
        self.open(reverse('ttt:login'))
        b = self.wd.find_element_by_tag_name('button')
