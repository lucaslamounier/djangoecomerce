# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Category
from .forms import ContactForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View, TemplateView

User = get_user_model()

class IndexView(TemplateView):
	template_name = 'index.html'

index = IndexView.as_view()

def contact(request):
	success = False
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form.send_mail()
		success = True
	context = {
		'form': form,
		'success': success,
	}
	return render(request, 'contact.html', context)
