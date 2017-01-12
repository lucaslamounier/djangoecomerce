# coding=utf-8

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from model_mommy import mommy
from catalog.models import Product, Category


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
        self.products = mommy.make('catalog.Product', _quantity=10)

    def tearDown(self):
        Product.objects.all().delete()

    def test_view_ok(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list.html')

    def test_context(self):
        response = self.client.get(self.url)
        self.assertTrue('product_list' in response.context)
        product_list = response.context['product_list']
        self.assertEquals(product_list.count(), 10)
