from django.views.generic import ListView, DetailView
from . models import *
import plotly
import plotly.graph_objects as go
from django.db.models import Count


class VotersListView(ListView):
    """View to display every Voter based on filter criteria."""

    model = Voter
    template_name = 'voter_analytics/voters.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the default context dict from the superclass
        context = super().get_context_data(**kwargs)

        # add every unique attribute for some Voter attributes like birth_date, party,
        # so we can use them to generate drop down menus in the template
        context = add_unique_voter_attributes(context)

        # add the filter choices (parameters passed in through the GET request),
        # so we can keep those choices checked after the page reloads
        context = add_filter_choices(self.request, context)

        # get a copy of the GET request's parameters
        params = self.request.GET.copy()

        # remove the page parameter if it already exists;
        # this makes it easier for pagination in the template
        if 'page' in params:
            params.pop('page')
        
        # add the remaining parameters as a string to the context dict
        context['querystring'] = params.urlencode()

        return context
    
    def get_queryset(self):
        """Returns a queryset that gets passed in as a context variable
        and becomes associated with context_object_name.
        """

        # get the default Voters queryset from the superclass
        voters = super().get_queryset()

        # return a subset of the queryset based on filter criteria
        return filter_voters(self.request, voters)
    

class GraphsListView(ListView):
    """View to display graphs of various distributions based on the filtered Voters."""

    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_context_data(self, **kwargs):
        """Return the dictionary of context variables for use in the template."""

        # get the default context dict from the superclass
        context = super().get_context_data(**kwargs)

        # add every unique attribute for some Voter attributes like birth_date, party,
        # so we can use them to generate drop down menus in the template
        context = add_unique_voter_attributes(context)

        # add the filter choices (parameters passed in through the GET request),
        # so we can keep those choices checked after the page reloads
        context = add_filter_choices(self.request, context)

        # get the default Voters queryset from the context dict
        voters = context['voters']

        # filter the voters based on filter criteria
        voters = filter_voters(self.request, voters)

        ################################ BIRTH YEARS BAR GRAPH ################################

        # for each birth year, count the number of Voters who have that birth year;
        # this returns a list of dictionaries of the form {birth_year: count of Voters}
        graph_div_birth_years_data = voters.values('birth_year').annotate(count=Count('pk'))

        print(f'BIRTH YEARS DATA: {graph_div_birth_years_data}')

        # extract the birth years and counts into lists for the x and y axes
        x = [
            d['birth_year'] for d in graph_div_birth_years_data
        ]
        y = [
            d['count'] for d in graph_div_birth_years_data
        ]

        # create the graph and its title text
        fig = go.Bar(x=x, y=y)
        title_text = f'Voter Distribution by Year of Birth (n={len(voters)})'

        # get the graph as an HTML div element
        graph_div_birth_years = plotly.offline.plot(
            {
                'data': [fig],
                'layout_title_text': title_text,
            },
            auto_open=False,
            output_type='div',
        )

        # add graph to context
        context['graph_div_birth_years'] = graph_div_birth_years

        ################################ PARTIES PIE GRAPH ################################

        # for each party, count the number of Voters who are affiliated with that party;
        # this returns a list of dictionaries of the form {party: count of Voters}
        graph_div_parties_data = voters.values('party').annotate(count=Count('pk'))

        print(f'PARTIES DATA: {graph_div_parties_data}')

        # extract the parties and counts into lists for the labels and values
        labels = [
            d['party'] for d in graph_div_parties_data
        ]
        values = [
            d['count'] for d in graph_div_parties_data
        ]

        # create the graph and its title text
        fig = go.Pie(labels=labels, values=values)
        title_text = f'Voter Distribution by Party Affiliation (n={len(voters)})'

        # get the graph as an HTML div element
        graph_div_parties = plotly.offline.plot(
            {
                'data': [fig],
                'layout_title_text': title_text,
            },
            auto_open=False,
            output_type='div',
        )

        # add graph to context
        context['graph_div_parties'] = graph_div_parties

        ################################ ELECTIONS BAR GRAPH ################################

        # for each election, get a subset of the Voters who voted in that election
        graph_div_elections_v20state_data = voters.filter(v20state='TRUE')
        graph_div_elections_v21town_data = voters.filter(v21town='TRUE')
        graph_div_elections_v21primary_data = voters.filter(v21primary='TRUE')
        graph_div_elections_v22general_data = voters.filter(v22general='TRUE')
        graph_div_elections_v23town_data = voters.filter(v23town='TRUE')

        # create the lists for the x and y axes
        x = [
            'v20state',
            'v21town',
            'v21primary',
            'v22general',
            'v23town',
        ]
        y = [
            len(graph_div_elections_v20state_data),
            len(graph_div_elections_v21town_data),
            len(graph_div_elections_v21primary_data),
            len(graph_div_elections_v22general_data),
            len(graph_div_elections_v23town_data),
        ]

        # create the graph and its title text
        fig = go.Bar(x=x, y=y)
        title_text = f'Vote Count by Election n={len(voters)}'

        # get the graph as an HTML div element
        graph_div_elections = plotly.offline.plot(
            {
                'data': [fig],
                'layout_title_text': title_text,
            },
            auto_open=False,
            output_type='div'
        )

        # add graph to context
        context['graph_div_elections'] = graph_div_elections

        return context
    

class VoterDetailView(DetailView):
    """View to display data for a single Voter."""

    model = Voter
    template_name = 'voter_analytics/voter.html'
    context_object_name = 'v'


def add_unique_voter_attributes(context):
    """Helper function to add every unique party, voter score, 
    and birth year to the specified context dictionary.
    """

    context['parties'] = Voter.objects.values_list('party', flat=True).distinct().order_by('party')
    context['scores'] = Voter.objects.values_list('score', flat=True).distinct().order_by('score')
    context['birth_years'] = Voter.objects.values_list('birth_year', flat=True).distinct().order_by('birth_year')

    return context


def add_filter_choices(request, context):
    """Helper function to add the filter choices (parameters passed in 
    through the GET request) to the specified context dictionary.
    """

    context['party_choice'] = request.GET.get('party')
    context['score_choice'] = request.GET.get('score')
    context['min_birth_year_choice'] = request.GET.get('min_birth_year')
    context['max_birth_year_choice'] = request.GET.get('max_birth_year')
    
    # process the list of election filters to add each one
    # to the context dict, if it exists
    if 'elections' in request.GET:
        elections = request.GET.getlist('elections')

        for elec in elections:
            context[f'{elec}_choice'] = True

    return context


def filter_voters(request, voters):
    """Helper function that returns a subset of the Voters queryset based 
    on filter criteria passed in through the GET request.
    """

    # get each filter from the GET request's parameters
    party = request.GET.get('party')
    score = request.GET.get('score')
    min_birth_year = request.GET.get('min_birth_year')
    max_birth_year = request.GET.get('max_birth_year')
    elections = request.GET.getlist('elections')

    # keep on filtering the Voters queryset for each existing filter
    if party:
        voters = voters.filter(party=party)

    if score:
        voters = voters.filter(score=score)

    if min_birth_year:
        voters = voters.filter(birth_year__gte=min_birth_year)

    if max_birth_year:
        voters = voters.filter(birth_year__lte=max_birth_year)

    if elections:
        elections = {elec: True for elec in elections}

        if elections.get('v20state'):
            voters = voters.filter(v20state='TRUE')

        if elections.get('v21town'):
            voters = voters.filter(v21town='TRUE')

        if elections.get('v21primary'):
            voters = voters.filter(v21primary='TRUE')

        if elections.get('v22general'):
            voters = voters.filter(v22general='TRUE')

        if elections.get('v23town'):
            voters = voters.filter(v23town='TRUE')

    return voters