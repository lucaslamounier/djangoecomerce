# coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^carrinho/adicionar/(?P<slug>[\w_-]+)/$', views.create_cart_item, name='create_cartitem'),
    url(regex=r'^carrinho/$', view=views.cart_item, name='cart_item'),
]