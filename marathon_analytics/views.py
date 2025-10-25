# marathon_analytics/views.py

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Result

# import plotly library for graphing
import plotly
import plotly.graph_objects as go

# Create your views here.

class ResultsListView(ListView):
    """View to display marathon results."""

    model = Result
    template_name = 'marathon_analytics/results.html'
    context_object_name = 'results'

    # how many records per page (add /?page=2 at the end of the URL to specify a page)
    paginate_by = 25

    def get_queryset(self):
        """Limit the result queryset (for now)."""

        # get all the results
        results = super().get_queryset()

        # slice to only return first 25 records
        # return results[:25]

        # look for URL parameters to filter by:
        if 'city' in self.request.GET:
            city = self.request.GET['city']

            if city:
                results = results.filter(city=city)

        return results
    

class ResultDetailView(DetailView):
    """Display results for a single runner."""

    model = Result
    template_name = 'marathon_analytics/result_detail.html'
    context_object_name = 'r' # short for Result

    def get_context_data(self, **kwargs):
        """Provide context variables for use in the template."""

        context = super().get_context_data(**kwargs)

        r = context['r'] # Result for one runner

        # create a graph of first half / second half time as pie chart
        first_half_seconds = (r.time_half1.hour * 60 + r.time_half1.minute) * 60 + r.time_half1.second
        second_half_seconds = (r.time_half2.hour * 60 + r.time_half2.minute) * 60 + r.time_half2.second

        print(f'r={r}; first_half_seconds={first_half_seconds}; second_half_seconds={second_half_seconds}')

        # create the plotly graph object:
        labels = ['first_half_seconds', 'second_half_seconds']
        values = [first_half_seconds, second_half_seconds]

        # generate the Pie chart:
        fig = go.Pie(labels=labels, values=values)
        title_text = 'Half Marathon Splits (seconds)'

        # obtain the graph as an HTML div (returns a string containing HTML code)
        graph_div_splits = plotly.offline.plot(
            {
                'data': [fig],
                'layout_title_text': title_text,
            },
            auto_open=False,
            output_type='div',
        )

        # add pie chart to context
        context['graph_div_splits'] = graph_div_splits

        # create a bar chart with count of runners passed/passed by
        x = [
            f'Runners Passed by {r.first_name}',
            f'Runners who Passed {r.first_name}',
        ]
        y = [
            r.get_runners_passed(),
            r.get_runners_passed_by(),
        ]

        fig = go.Bar(x=x, y=y)
        title_text = 'Runners Passed/Passed By'

        graph_div_passed = plotly.offline.plot(
            {
                'data': fig,
                'layout_title_text': title_text,
            },
            auto_open=False,
            output_type='div',
        )

        # add bar chart to context
        context['graph_div_passed'] = graph_div_passed

        return context