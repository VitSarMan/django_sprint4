from django.shortcuts import render
from django.views.generic import TemplateView


class AboutTemplateView(TemplateView):
    template_name = 'pages/about.html'


class RulesTemplateView(TemplateView):
    template_name = 'pages/rules.html'


#ERROR 403
def custom_403_view(request, exception=None):
    return render(request, 'pages/403csrf.html', status=403)

#ERROR CSRF
def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)

#ERROR 404
def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)

#ERROR 500
def internal_server_error(request):
    return render(request, 'pages/500.html', status=500)