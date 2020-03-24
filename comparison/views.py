from django.http import HttpResponse
from django.template import loader
from .tables import PaymentSystemTable
from .models import PaymentSystem


def index(request):
    template = loader.get_template('comparison/index.html')
    context = { }
    return HttpResponse(template.render(context, request))

# views.py
# def payment_systems_list(request):
#     table = PaymentSystemTable(PaymentSystem.objects.all())

#     return loader.render(request, "person_list.html", {
#         "table": table
#     })