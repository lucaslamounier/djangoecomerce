# coding=utf-8

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from model_mommy import mommy
from catalog.models import Product, Category
from django.conf import settings

User = get_user_model()


class  IndextViewTestCase(TestCase):

    def setUp(self):
        ''' Executado quando inicia cada teste '''
        self.client = Client()
        self.url = reverse('index')

    def tearDown(self):
        ''' Executado quando acaba cada teste '''
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')


class ProductListTestCase(TestCase):

    def setUp(self):
        '''' Executado quando inicia cada teste '''
        self.url = reverse('catalog:product_list')
        # cria 10 produtos automaticamente para o teste
        self.products = mommy.make('catalog.Product', _quantity=10)

    def tearDown(self):
        Product.objects.all().delete()

    def test_view_ok(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list.html')

    def test_context(self):
        response = self.client.get(self.url)
        self.assertTrue('products' in response.context)
        product_list = response.context['products']
        self.assertEquals(product_list.count(), 3)
        paginator = response.context['paginator']
        self.assertEquals(paginator.num_pages, 4)

    def test_page_not_found(self):
        response = self.client.get('{}?page=5'.format(self.url))
        self.assertEquals(response.status_code, 404)


class ContactViewTestCase(TestCase):

    def setUp(self):
        '''' Executado quando inicia cada teste '''
        self.client = Client()
        self.url = reverse('contact')

    def test_view_ok(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_form_error(self):
        ''' Testa se há erro no formulário de contato '''
        data = {'name': '', 'message': '', 'email': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_form_ok(self):
            ''' Testa se o formulário de contato foi enviado com sucesso '''
            data = {'name': 'test', 'message': 'test', 'email': 'test@test.com'}
            response = self.client.post(self.url, data)
            self.assertTrue(response.context['success'])
            self.assertEquals(len(mail.outbox), 1)
            self.assertEquals(mail.outbox[0].subject, 'Contato do Django E-Commerce')
