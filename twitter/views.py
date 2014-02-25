from twitter.models import Poll
from django.views import generic


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'results.html'
