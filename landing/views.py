from django.http import HttpResponse
from django.template import loader
from .tables import PaymentSystemTable
from .models import PaymentSystem


def index(request):
    template = loader.get_template('landing/index.html')
    context = { }
    return HttpResponse(template.render(context, request))