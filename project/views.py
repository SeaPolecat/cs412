# File: project/views.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 12/08/2025
# Description: Contains views classes that render templates,
# pass in context variables, and handle form submissions.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import random


## MIXINS ############################################################################################


class MyLoginRequiredMixin(LoginRequiredMixin):
    """My own subclass of the LoginRequiredMixin, which implements
    some useful features.
    """

    def get_login_url(self):
        """Return the URL for this app's login page."""

        return reverse('login')
    
    def get_logged_in_player(self):
        """Return the Profile corresponding to the logged in User."""

        return Player.objects.get(user=self.request.user)


## GENERIC CRUD VIEWS ############################################################################################


class PlayerListView(ListView):
    """View to show a list of all Players."""

    model = Player
    template_name = 'project/show_all_players.html'
    context_object_name = 'players'

    def get_queryset(self):
        """Order the Players by latest join date first."""

        return Player.objects.all().order_by('-date_joined')


class PlayerDetailView(DetailView):
    """View to show a single Player."""

    model = Player
    template_name = 'project/show_player.html'
    context_object_name = 'player'
    

class MyPlayerDetailView(MyLoginRequiredMixin, DetailView):
    """View to show the logged in Player."""

    model = Player
    template_name = 'project/show_player.html'
    context_object_name = 'player'

    def get_object(self):
        """Get the logged in Player via MyLoginRequiredMixin."""

        return self.get_logged_in_player()


class ShowCollectionDetailView(DetailView):
    """View to show all of a Player's OwnedItems."""

    model = Player
    template_name = 'project/show_collection.html'
    context_object_name = 'player'


class ShowTradesDetailView(MyLoginRequiredMixin, DetailView):
    """View to show the logged in Player's incoming and outgoing Trades."""

    model = Player
    template_name = 'project/show_trades.html'
    context_object_name = 'player'

    def get_object(self):
        """Get the logged in Player via MyLoginRequiredMixin."""

        return self.get_logged_in_player()


class BoxListView(MyLoginRequiredMixin, ListView):
    """View to show a list of Boxes that the logged in Player has created."""

    model = Box
    template_name = 'project/show_all_boxes.html'
    context_object_name = 'boxes'

    def get_queryset(self):
        """Get the logged in Player and their Boxes."""

        player = self.get_logged_in_player()
        
        return player.get_all_boxes()


class BoxDetailView(MyLoginRequiredMixin, DetailView):
    """View to show a single Box that the logged in Player has created,
    along with all the Items in the Box.
    """

    model = Box
    template_name = 'project/show_box.html'
    context_object_name = 'box'

    def get_context_data(self, **kwargs):
        """Add possible state messages to the context."""

        context = super().get_context_data(**kwargs)

        # different states are passed in through the URL
        success = self.request.GET.get('success')
        failure = self.request.GET.get('failure')

        # if there is no state, just display the page
        if not success and not failure:
            return super().get_context_data(**kwargs)

        # success means a Player successfully published their Box to the shop;
        # add "success" to the context to let the template know
        elif success:
            context['success'] = success
        
        # failure means a Player encountered an error while trying to publish a Box;
        # add "failure" to the context to let the template know
        elif failure:
            context['failure'] = failure

        return context
    

class ShopBoxListView(ListView):
    """View to show a list of published Boxes in the shop."""
    
    model = Box
    template_name = 'project/show_all_shop_boxes.html'
    context_object_name = 'boxes'

    def get_queryset(self):
        """Only query Boxes that have been published."""

        return Box.objects.filter(published=True)


class ShopBoxDetailView(DetailView):
    """View to show a single published Box, along with all its Items."""
    
    model = Box
    template_name = 'project/show_shop_box.html'
    context_object_name = 'box'

    def dispatch(self, request, *args, **kwargs):
        """Redirect back to the main shop page if the Box isn't published."""

        pk = self.kwargs['pk'] # Box PK
        box = Box.objects.get(pk=pk)

        if not box.published:
            return redirect('show_all_shop_boxes')

        return super().dispatch(request, *args, **kwargs)


class CreateBoxView(MyLoginRequiredMixin, CreateView):
    """View to create a new Box."""
    
    model = Box
    form_class = CreateUpdateBoxForm
    template_name = 'project/create_box.html'
    
    def form_valid(self, form):
        """Attach the logged in Player as a FK to the newly created Box."""

        player = self.get_logged_in_player()

        box = form.instance
        box.player = player

        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the Box's page after successful creation."""

        pk = self.object.pk # Box PK

        return reverse('show_box', kwargs={'pk': pk})
    

class CreateItemView(MyLoginRequiredMixin, CreateView):
    """View to create a new Item for a Box."""

    model = Item
    form_class = CreateUpdateItemForm
    template_name = 'project/create_item.html'

    def get_context_data(self, **kwargs):
        """Add the Box this Item belongs to into the context."""

        pk = self.kwargs['pk'] # Box PK
        box = Box.objects.get(pk=pk)

        context = super().get_context_data(**kwargs)
        context['box'] = box

        return context
    
    def form_valid(self, form):
        """Attach the Box as a FK to the newly created Item."""

        pk = self.kwargs['pk'] # Box PK
        box = Box.objects.get(pk=pk)

        item = form.instance
        item.box = box

        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the Box's page after successful creation."""

        pk = self.kwargs['pk'] # Box PK

        return reverse('show_box', kwargs={'pk': pk})
    

class CreatePlayerView(CreateView):
    """View to create a new Player through signing up."""

    model = Player
    form_class = CreateUpdatePlayerForm
    template_name = 'project/create_player.html'

    def get_context_data(self, **kwargs):
        """Add Django's user creation form into the context."""

        context = super().get_context_data()
        context['django_form'] = UserCreationForm

        return context
    
    def form_valid(self, form):
        """Handles the form submission and saves the new object 
        to the Django database.
        """

        # rebuild Django's user creation form
        django_form = UserCreationForm(self.request.POST)

        # print any validation errors
        if not django_form.is_valid():
            print(django_form.errors)

        # save the new user to the db, and log them in
        user = django_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        # attach the given username and user to the newly created Player
        profile = form.instance
        profile.username = user.username
        profile.user = user

        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the logged in Player's page after successful creation."""

        return reverse('show_my_player')
    

class UpdateBoxView(MyLoginRequiredMixin, UpdateView):
    """View to update a Box."""

    model = Box
    form_class = CreateUpdateBoxForm
    template_name = 'project/update_box.html'
    
    def get_success_url(self):
        """Redirect to the Box's page after successful update."""

        pk = self.kwargs['pk'] # Box PK

        return reverse('show_box', kwargs={'pk': pk})
    

class UpdateItemView(MyLoginRequiredMixin, UpdateView):
    """View to update an Item."""

    model = Item
    form_class = CreateUpdateItemForm
    template_name = 'project/update_item.html'

    def get_context_data(self, **kwargs):
        """Add the Box this Item belongs to into the context."""

        pk = self.kwargs['pk'] # Item PK

        # find the Item and its corresponding Box
        item = Item.objects.get(pk=pk)
        box = item.box

        # add Box to context
        context = super().get_context_data(**kwargs)
        context['box'] = box

        return context
    
    def get_success_url(self):
        """Redirect to the Box's page after successful update."""

        pk = self.kwargs['pk'] # Item PK

        # find the Item and its corresponding Box
        item = Item.objects.get(pk=pk)
        box = item.box

        return reverse('show_box', kwargs={'pk': box.pk})
    

class UpdatePlayerView(MyLoginRequiredMixin, UpdateView):
    """View to update the logged in Player."""

    model = Player
    form_class = CreateUpdatePlayerForm
    template_name = 'project/update_player.html'

    def get_object(self):
        """Get the logged in Player via MyLoginRequiredMixin."""

        return self.get_logged_in_player()

    def get_success_url(self):
        """Redirect to the logged in Player's page after successful update."""

        return reverse('show_my_player')
    

class DeleteBoxView(MyLoginRequiredMixin, DeleteView):
    """View to delete a Box."""

    model = Box
    template_name = 'project/delete_box.html'

    def get_success_url(self):
        """Redirect to the page with all Boxes after successful deletion."""

        return reverse('show_all_boxes')
    

class DeleteItemView(MyLoginRequiredMixin, DeleteView):
    """View to delete an Item."""

    model = Item
    template_name = 'project/delete_item.html'

    def get_context_data(self, **kwargs):
        """Add the Box this Item belongs to into the context."""

        pk = self.kwargs['pk'] # Item PK

        # find the Item and its corresponding Box
        item = Item.objects.get(pk=pk)
        box = item.box

        # add Box to context
        context = super().get_context_data(**kwargs)
        context['box'] = box

        return context

    def get_success_url(self):
        """Redirect to the Box's page after successful deletion."""

        pk = self.kwargs['pk'] # Item PK

        # find the Item and its corresponding Box
        item = Item.objects.get(pk=pk)
        box = item.box

        return reverse('show_box', kwargs={'pk': box.pk})
    

## CUSTOM VIEWS ############################################################################################


class PublishBoxView(MyLoginRequiredMixin, View):
    """View to publish a Box to the shop."""

    def get(self, request, *args, **kwargs):
        """Publish the Box if it's ready, and send an error message otherwise."""

        pk = kwargs['pk'] # Box PK
        box = Box.objects.get(pk=pk)

        # URL to redirect to after completion
        url = reverse('show_box', kwargs={'pk': pk})

        # if the Box contains least 1 Item of each rarity, publish it
        if box.contains_every_rarity():
            box.published = True
            box.save()

            # display the Box's creator page with the success state
            return redirect(f'{url}?success=1')
        
        # otherwise, display the Box's creator page with the failure state
        return redirect(f'{url}?failure=1')


class UnpublishBoxView(MyLoginRequiredMixin, View):
    """View to unpublish (remove) a Box from the shop."""

    def get(self, request, *args, **kwargs):
        """Unpublish the Box and save to the db."""

        pk = kwargs['pk'] # Box PK

        # find the Box and unpublish it
        box = Box.objects.get(pk=pk)
        box.published = False
        box.save()

        # display the Box's creator page
        return redirect('show_box', pk)


class OpenBoxView(MyLoginRequiredMixin, View):
    """View to open a Box from the shop."""

    def get(self, request, *args, **kwargs):
        """Draw a random Item from the Box and add it to 
        the Player's OwnedItems.
        """

        pk = kwargs['pk'] # Box PK
        box = Box.objects.get(pk=pk)

        # if the Box is not published, redirect back to the main shop page
        if not box.published:
            return redirect('show_all_shop_boxes')

        # draw a random Item from the Box (with respect to different rarity probabilities)
        item = box.draw_random_item()

        # get the logged in Player
        player = self.get_logged_in_player()

        # if the Player already owns the Item, increment its quantity
        try:
            owned_item = OwnedItem.objects.get(player=player, item=item)
            owned_item.quantity += 1

        # otherwise, create a new OwnedItem
        except:
            owned_item = OwnedItem(player=player, item=item)

        # save the OwnedItem to db
        owned_item.save()

        # increment the Player's boxes_opened stat, and save to db
        player.boxes_opened += 1
        player.save()

        template_name = 'project/open_box.html'

        # add the Box and Item to the context and render the template above
        context = {
            'box': box,
            'item': item,
        }
        return render(request, template_name, context)
    

class DisplayCollectionView(MyLoginRequiredMixin, View):
    """View to display an OwnedItem (i.e. create a DisplayItem) 
    in one of the Player's display slots.
    """

    def get(self, request, *args, **kwargs):
        """Collect info about which slot to display in, and render a 
        form for the Player to choose which OwnedItem to display.
        """

        slot = self.kwargs['slot'] # the display slot the Player chose

        # get the logged in Player and their OwnedItems
        player = self.get_logged_in_player()
        owned_items = player.get_all_owned_items()

        template_name = 'project/display_collection.html'

        # add the slot and list of OwnedItems to the context,
        # and render the template above
        context = {
            'slot': slot,
            'owned_items': owned_items,
        }
        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        """Collect info about which OwnedItem the Player wants to display,
        and display it in the appropriate slot."""

        print(request.POST)

        slot = self.kwargs['slot'] # the display slot the Player chose

        # get the logged in Player
        player = self.get_logged_in_player()

        # if POST contains "delete", the Player chose to remove their 
        # OwnedItem from the display slot
        if request.POST.get('delete'):

            # find the corresponding DisplayItem and delete it
            try:
                display_item = DisplayItem.objects.get(owned_item__player=player, display_slot=slot)
                display_item.delete()
            except:
                pass

        # otherwise, check if the display slot is between 0 and 8
        # (each Player only gets 9 display slots on their profile)
        elif slot >= 0 and slot <= 8:
            oi_pk = request.POST['oi_pk'] # OwnedItem PK passed in through POST

            # get the chosen OwnedItem
            owned_item = OwnedItem.objects.get(pk=oi_pk)

            # if a DisplayItem with the chosen slot already exists, update it
            try:
                display_item = DisplayItem.objects.get(owned_item__player=player, display_slot=slot)
                display_item.owned_item = owned_item

            # otherwise, create a new DisplayItem with the chosen OwnedItem and slot
            except:
                display_item = DisplayItem(owned_item=owned_item, display_slot=slot)

            # save the DisplayItem to db
            display_item.save()

            # if the same OwnedItem exists in another slot, delete it, because each
            # unique OwnedItem can only be displayed in 1 slot at a time
            try:
                existing = DisplayItem.objects.exclude(display_slot=slot).get(owned_item=owned_item)
                existing.delete()
            except:
                pass

        # redirect to the logged in Player's profile page
        return redirect('show_player', pk=player.pk)
    

class StartTradeView(MyLoginRequiredMixin, View):
    """View to start a trade with another Player."""

    def get(self, request, *args, **kwargs):
        """Render a form for the trader to choose which OwnedItem 
        they want from the tradee."""

        pk = kwargs['pk'] # tradee Player PK

        # get the tradee Player (the one who is being asked to trade)
        # and their OwnedItems
        tradee: Player = Player.objects.get(pk=pk)
        owned_items = tradee.get_all_owned_items()

        # if the trader is trying to trade with themselves,
        # redirect back to their profile page
        if tradee == self.get_logged_in_player():
            return redirect('show_my_player')

        template_name = 'project/start_trade.html'

        # add the tradee and their OwnedItems to the context,
        # and render the template above
        context = {
            'tradee': tradee,
            'owned_items': owned_items,
        }
        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        """If the trader only submitted 1 form, render another form for them to
        choose which OwnedItem they are offering in exchange. Otherwise, 
        create the Trade.
        """

        print(request.POST)

        # if POST does NOT contain "step2", render another form to let
        # the trader choose which OwnedItem they are offering in exchange
        if not request.POST.get('step2'):

            # PK of the OwnedItem the trader wants from the tradee
            tradee_item_pk = request.POST['tradee_item_pk']

            # save it to the Django session so we can access it after coming
            # back via the 2nd form submission
            request.session['tradee_item_pk'] = tradee_item_pk

            # get the trader Player (the one who is asking to trade)
            # and their OwnedItems
            trader = self.get_logged_in_player()
            owned_items = trader.get_all_owned_items()

            template_name = 'project/start_trade.html'

            # add the trader and their OwnedItems to the context,
            # and render the template above
            context = {
                'trader': trader,
                'owned_items': owned_items,
            }
            return render(request, template_name, context)

        # if POST contains "step2", the trader has submitted both forms,
        # and we can create the Trade

        # PK of the OwnedItem the trader is offering (from POST)
        trader_item_pk = request.POST['trader_item_pk']

        # PK of the OwnedItem the trader wants (from Django session)
        tradee_item_pk = request.session['tradee_item_pk']

        # find the respective OwnedItems
        trader_item = OwnedItem.objects.get(pk=trader_item_pk)
        tradee_item = OwnedItem.objects.get(pk=tradee_item_pk)

        # create the Trade and save to db
        trade = Trade(trader_item=trader_item, tradee_item=tradee_item)
        trade.save()

        # redirect to the page showing all Trades
        return redirect('show_trades')
    

class AcceptTradeView(MyLoginRequiredMixin, View):
    """View to accept a Trade."""

    def get(self, request, *args, **kwargs):
        """Exchange items between the trader and tradee."""

        pk = self.kwargs['pk'] # Trade PK
        trade = Trade.objects.get(pk=pk)

        # get the respective OwnedItems to be exchanged
        trader_item: OwnedItem = trade.trader_item
        tradee_item: OwnedItem = trade.tradee_item

        # get the respective Players involved in the Trade
        trader: Player = trade.trader_item.player
        tradee: Player = trade.tradee_item.player

        ## add OwnedItems that the Players receive

        # if the tradee already has the OwnedItem, increment its quantity
        try:
            owned_item = OwnedItem.objects.get(player=tradee, item=trader_item.item)
            owned_item.quantity += 1

        # otherwise, create a new OwnedItem
        except:
            owned_item = OwnedItem(player=tradee, item=trader_item.item)

        owned_item.save()

        # if the trader already has the OwnedItem, increment its quantity
        try:
            owned_item = OwnedItem.objects.get(player=trader, item=tradee_item.item)
            owned_item.quantity += 1

        # otherwise, create a new OwnedItem
        except:
            owned_item = OwnedItem(player=trader, item=tradee_item.item)

        owned_item.save()

        ## subtract OwnedItems that the Players give away

        # if the trader only has 1 more of the OwnedItem left, delete it
        if trader_item.quantity == 1:
            trader_item.delete()

        # otherwise, decrement its quantity
        else:
            trader_item.quantity -= 1
            trader_item.save()

        # if the tradee only has 1 more of the OwnedItem left, delete it
        if tradee_item.quantity == 1:
            tradee_item.delete()

        # otherwise, decrement its quantity
        else:
            tradee_item.quantity -= 1
            tradee_item.save()

        # delete the Trade (because it's complete)
        trade.delete()

        # redirect to the page showing all Trades
        return redirect('show_trades')


class RejectTradeView(MyLoginRequiredMixin, View):
    """View to reject a Trade."""

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk'] # Trade PK
        trade = Trade.objects.get(pk=pk)

        # delete the trade
        trade.delete()
        
        # redirect to the page showing all Trades
        return redirect('show_trades')