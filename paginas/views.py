from django.views.generic import TemplateView

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

class TableView(TemplateView):
    template_name = "table.html"
