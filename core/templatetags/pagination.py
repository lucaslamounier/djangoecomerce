# coding=utf-8

from django.template import Library

register = Library()

'''
    Páginação de objetos
'''
@register.inclusion_tag('pagination.html')
def pagination(request, paginator, page_obj):
    context = dict()
    context['paginator'] = paginator
    context['request'] = request
    context['page_obj'] = page_obj
    getvars = request.GET.copy()
    if 'page' in getvars:
        del getvars['page']
    if len(getvars) > 0:
        context['getvars'] = '&{0}'.format(getvars.urlencode())
    else:
        context['getvars'] = ''
    return context
