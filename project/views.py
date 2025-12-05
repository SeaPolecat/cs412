from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import random


## CONSTANTS ############################################################################################


COMMON = 'C'
UNCOMMON = 'U'
RARE = 'R'
SUPER_RARE = 'SR'
SECRET = 'SE'


## MIXINS ############################################################################################


class MyLoginRequiredMixin(LoginRequiredMixin):

    def get_login_url(self):
        return reverse('login')
    
    def get_logged_in_player(self):
        return Player.objects.get(user=self.request.user)


## GENERIC VIEWS ############################################################################################


class PlayerListView(ListView):

    model = Player
    template_name = 'project/show_all_players.html'
    context_object_name = 'players'


class PlayerDetailView(DetailView):

    model = Player
    template_name = 'project/show_player.html'
    context_object_name = 'player'
    

class MyPlayerDetailView(MyLoginRequiredMixin, DetailView):

    model = Player
    template_name = 'project/show_player.html'
    context_object_name = 'player'

    def get_object(self):
        return self.get_logged_in_player()


class ShowItemsDetailView(DetailView):

    model = Player
    template_name = 'project/show_items.html'
    context_object_name = 'player'


class BoxListView(MyLoginRequiredMixin, ListView):

    model = Box
    template_name = 'project/show_all_boxes.html'
    context_object_name = 'boxes'

    def get_queryset(self):
        player = self.get_logged_in_player()
        
        return player.get_all_boxes()


class BoxDetailView(MyLoginRequiredMixin, DetailView):

    model = Box
    template_name = 'project/show_box.html'
    context_object_name = 'box'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        success = self.request.GET.get('success')
        failure = self.request.GET.get('failure')

        if not success and not failure:
            return super().get_context_data(**kwargs)

        elif success:
            context['success'] = success
        
        elif failure:
            context['failure'] = failure

        return context
    

class ShopBoxListView(ListView):
    
    model = Box
    template_name = 'project/show_all_shop_boxes.html'
    context_object_name = 'boxes'

    def get_queryset(self):
        return Box.objects.filter(published=True)


class ShopBoxDetailView(DetailView):
    
    model = Box
    template_name = 'project/show_shop_box.html'
    context_object_name = 'box'

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        box = Box.objects.get(pk=pk)

        if not box.published:
            return redirect('show_all_shop_boxes')

        return super().dispatch(request, *args, **kwargs)


class CreateBoxView(MyLoginRequiredMixin, CreateView):
    
    model = Box
    form_class = CreateBoxForm
    template_name = 'project/create_box_form.html'
    
    def form_valid(self, form):
        player = self.get_logged_in_player()

        box = form.instance
        box.player = player

        return super().form_valid(form)
    

class UpdateBoxView(MyLoginRequiredMixin, UpdateView):

    model = Box
    form_class = CreateBoxForm
    template_name = 'project/update_box_form.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse('show_box', kwargs={'pk': pk})
    

class DeleteBoxView(MyLoginRequiredMixin, DeleteView):

    model = Box
    template_name = 'project/delete_box_form.html'

    def get_success_url(self):
        return reverse('show_all_boxes')
    

class CreateItemView(MyLoginRequiredMixin, CreateView):

    form_class = CreateItemForm
    template_name = 'project/create_item_form.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        box = Box.objects.get(pk=pk)

        context = super().get_context_data(**kwargs)
        context['box'] = box

        return context
    
    def form_valid(self, form):
        pk = self.kwargs['pk']
        box = Box.objects.get(pk=pk)

        item = form.instance
        item.box = box

        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse('show_box', kwargs={'pk': pk})
    

## CUSTOM VIEWS ############################################################################################


class OpenBoxView(MyLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        box = Box.objects.get(pk=pk)

        if not box.published:
            return redirect('show_all_shop_boxes')
        
        ITEM_CHANCES = {
            COMMON: 40,     # 40%
            UNCOMMON: 70,   # 30%
            RARE: 90,       # 20%
            SUPER_RARE: 99, # 9%
            SECRET: 100,    # 1%
        }
        
        rand = random.uniform(1.0, 100.0)
        player = self.get_logged_in_player()

        if rand <= ITEM_CHANCES[COMMON]:
            items = Item.objects.filter(box=pk, rarity=COMMON)

        elif rand > ITEM_CHANCES[COMMON] and rand <= ITEM_CHANCES[UNCOMMON]:
            items = Item.objects.filter(box=pk, rarity=UNCOMMON)

        elif rand > ITEM_CHANCES[UNCOMMON] and rand <= ITEM_CHANCES[RARE]:
            items = Item.objects.filter(box=pk, rarity=RARE)

        elif rand > ITEM_CHANCES[RARE] and rand <= ITEM_CHANCES[SUPER_RARE]:
            items = Item.objects.filter(box=pk, rarity=SUPER_RARE)

        else:
            items = Item.objects.filter(box=pk, rarity=SECRET)

        item = random.choice(items)

        try:
            owned_item = OwnedItem.objects.get(player=player, item=item)
            owned_item.quantity += 1
        except:
            owned_item = OwnedItem(player=player, item=item)

        owned_item.save()

        template_name = 'project/open_box.html'

        context = {
            'item': item
        }
        return render(request, template_name, context)
    

class ItemDisplayView(MyLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        slot = self.kwargs['slot']
        player = self.get_logged_in_player()
        owned_items = player.get_all_owned_items()

        template_name = 'project/item_display.html'
        context = {
            'slot': slot,
            'owned_items': owned_items,
        }
        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        print(request.POST)

        slot = self.kwargs['slot']
        player = self.get_logged_in_player()

        if request.POST.get('delete'):
            try:
                display_item = DisplayItem.objects.get(owned_item__player=player, display_slot=slot)
                display_item.delete()
            except:
                pass

        elif slot >= 0 and slot <= 9:
            oi_pk = request.POST['oi_pk']
            owned_item = OwnedItem.objects.get(pk=oi_pk)

            # insert into slot
            try:
                display_item = DisplayItem.objects.get(owned_item__player=player, display_slot=slot)
                display_item.owned_item = owned_item
            except:
                display_item = DisplayItem(owned_item=owned_item, display_slot=slot)

            display_item.save()

            # delete existing elsewhere
            try:
                existing = (DisplayItem.objects
                            .filter(owned_item__player=player)
                            .exclude(display_slot=slot)
                            .get(owned_item=oi_pk))
                
                existing.delete()
            except:
                pass

        return redirect('show_player', pk=player.pk)
    

class PublishBoxView(MyLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        items = Item.objects.filter(box=pk)
        rarities = items.values_list('rarity', flat=True)

        if (COMMON in rarities
            and UNCOMMON in rarities
            and RARE in rarities
            and SUPER_RARE in rarities
            and SECRET in rarities):

            box = Box.objects.get(pk=pk)

            box.published = True
            box.save()

            return redirect(f'/project/creator/box/{pk}?success=1')
        
        return redirect(f'/project/creator/box/{pk}?failure=1')


class UnpublishBoxView(MyLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        box = Box.objects.get(pk=pk)

        box.published = False
        box.save()

        return redirect('show_box', pk)