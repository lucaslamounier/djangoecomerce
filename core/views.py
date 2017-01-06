# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	texts = ['lorem ipsum', 'consectetur adipisicing elit',
			'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.']
	context = {
		'title': 'Django e-commerce',
		'texts': texts,
	}
	return render(request, 'index.html', context)
