# coding=utf-8

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from model_mommy import mommy
from django.conf import settings

User = get_user_model()


class LoginViewTestCase(TestCase):

    def setUp(self):
        '''' Executado quando inicia cada teste '''
        self.client = Client()
        self.url = reverse('login')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_login_ok(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        data = {'username': self.user.username, 'password': '123'}
        response = self.client.post(self.url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, redirect_url, status_code=302)
        self.assertTrue(response.wsgi_request.user.is_authenticated())

    def test_login_error(self):
        data = {'username': self.user.username, 'password': '1234'}
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        error_msg = ('Por favor, entre com um Apelido / Usuário  e senha corretos. Note que ambos os campos diferenciam maiúsculas e minúsculas.')
        self.assertFormError(response, 'form', None, error_msg)


class RegisterViewTestCase(TestCase):

    def setUp(self):
        '''' Executado quando inicia cada teste '''
        self.client = Client()
        self.url = reverse('accounts:register')

    def test_register_ok(self):
        data = {'username': 'lucas', 'password1': 'teste123',
                'password2': 'teste123', 'email': 'test@test.com'}
        response = self.client.post(self.url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEquals(User.objects.count(), 1)

    def test_register_error(self):
        data = {'username': 'lucas', 'password1': 'teste123',
                'password2': 'teste123'}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdateUserTestCase(TestCase):

        def setUp(self):
            '''' Executado quando inicia cada teste '''
            self.client = Client()
            self.url = reverse('accounts:update_user')
            self.user = mommy.prepare(settings.AUTH_USER_MODEL)
            self.user.set_password('123')
            self.user.save()

        def tearDown(self):
            self.user.delete()

        def test_update_user_ok(self):
            data = {'name': 'test', 'email': 'test@test.com'}
            response = self.client.get(self.url)
            self.assertEquals(response.status_code, 302)
            self.client.login(username=self.user.username, password='123')
            response = self.client.post(self.url, data)
            accounts_index_url = reverse('accounts:index')
            self.assertRedirects(response, accounts_index_url)
            self.user.refresh_from_db()
            self.assertEquals(self.user.email, 'test@test.com')
            self.assertEquals(self.user.name, 'test')


        def test_update_user_error(self):
            data = {}
            self.client.login(username=self.user.username, password='123')
            response = self.client.post(self.url, data)
            self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdatePasswordTestCase(TestCase):

        def setUp(self):
            '''' Executado quando inicia cada teste '''
            self.client = Client()
            self.url = reverse('accounts:update_password')
            self.user = mommy.prepare(settings.AUTH_USER_MODEL)
            self.user.set_password('123')
            self.user.save()

        def tearDown(self):
            self.user.delete()

        def test_update_password_ok(self):
            data = {
                'old_password': '123', 'new_password1': 'teste123', 'new_password2': 'teste123'
            }
            self.client.login(username=self.user.username, password='123')
            response = self.client.post(self.url, data)
            self.user.refresh_from_db()
            self.assertTrue(self.user.check_password('teste123'))
