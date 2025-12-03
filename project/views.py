from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import *
from django.shortcuts import render, redirect
from django.urls import reverse
import random


COMMON = 'C'
UNCOMMON = 'U'
RARE = 'R'
SUPER_RARE = 'SR'
SECRET = 'SE'


class PlayerListView(ListView):

    model = Player
    template_name = 'project/show_all_players.html'
    context_object_name = 'players'


class PlayerDetailView(DetailView):

    model = Player
    template_name = 'project/show_player.html'
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        queryset = DisplayItem.objects.filter(owned_item__player=pk)
        display_items = [0] * 9

        for i in range(len(display_items)):
            try:
                display_items[i] = queryset.get(display_slot=i)
            except:
                pass

        context['display_items'] = display_items

        return context


class OwnedItemListView(ListView):

    model = OwnedItem
    template_name = 'project/show_all_owned_items.html'
    context_object_name = 'owned_items'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = OwnedItem.objects.filter(player=pk)
        owned_items = []

        owned_items += queryset.filter(item__rarity=COMMON)
        owned_items += queryset.filter(item__rarity=UNCOMMON)
        owned_items += queryset.filter(item__rarity=RARE)
        owned_items += queryset.filter(item__rarity=SUPER_RARE)
        owned_items += queryset.filter(item__rarity=SECRET)

        return owned_items
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        context['player'] = player

        return context


class BoxListView(ListView):

    model = Box
    template_name = 'project/show_all_boxes.html'
    context_object_name = 'boxes'


class BoxDetailView(DetailView):

    model = Box
    template_name = 'project/show_box.html'
    context_object_name = 'box'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = context['box']
        queryset = Item.objects.filter(box=pk)
        items = []

        items += queryset.filter(rarity=COMMON)
        items += queryset.filter(rarity=UNCOMMON)
        items += queryset.filter(rarity=RARE)
        items += queryset.filter(rarity=SUPER_RARE)
        items += queryset.filter(rarity=SECRET)

        context['items'] = items

        return context
    

class OpenBoxView(DetailView):

    model = OwnedItem
    template_name = 'project/open_box.html'
    context_object_name = 'oi'
    
    def get_object(self):
        ITEM_CHANCES = {
            COMMON: 40,     # 40%
            UNCOMMON: 70,   # 30%
            RARE: 90,       # 20%
            SUPER_RARE: 99, # 9%
            SECRET: 100,    # 1%
        }
        
        rand = random.uniform(1.0, 100.0)
        player = Player.objects.get(pk=1)
        pk = self.kwargs['pk']
        queryset = Item.objects.filter(box=pk)

        if rand <= ITEM_CHANCES[COMMON]:
            items = queryset.filter(rarity=COMMON)

        elif rand > ITEM_CHANCES[COMMON] and rand <= ITEM_CHANCES[UNCOMMON]:
            items = queryset.filter(rarity=UNCOMMON)

        elif rand > ITEM_CHANCES[UNCOMMON] and rand <= ITEM_CHANCES[RARE]:
            items = queryset.filter(rarity=RARE)

        elif rand > ITEM_CHANCES[RARE] and rand <= ITEM_CHANCES[SUPER_RARE]:
            items = queryset.filter(rarity=SUPER_RARE)

        else:
            items = queryset.filter(rarity=SECRET)

        item = random.choice(items)

        try:
            owned_item = OwnedItem.objects.get(player=player, item=item)
            owned_item.quantity += 1
        except:
            owned_item = OwnedItem(player=player, item=item)

        owned_item.save()

        return owned_item
    

def choose_display_item(request, pk, slot):

    if request.POST:
        print(request.POST)

        if request.POST.get('delete'):
            try:
                display_item = DisplayItem.objects.get(owned_item__player=pk, display_slot=slot)
                display_item.delete()
            except:
                pass

        elif slot >= 0 and slot <= 9:
            oi_pk = request.POST['oi_pk']
            owned_item = OwnedItem.objects.get(pk=oi_pk)

            # insert into slot
            try:
                display_item = DisplayItem.objects.get(owned_item__player=pk, display_slot=slot)
                display_item.owned_item = owned_item
            except:
                display_item = DisplayItem(owned_item=owned_item, display_slot=slot)

            display_item.save()

            # delete existing elsewhere
            try:
                existing = DisplayItem.objects.filter(owned_item__player=pk)
                existing = existing.exclude(display_slot=slot).get(owned_item=oi_pk)
                existing.delete()
            except:
                pass

        return redirect('show_player', pk=pk)
    
    player = Player.objects.get(pk=pk)
    queryset = OwnedItem.objects.filter(player=pk)
    owned_items = []

    owned_items += queryset.filter(item__rarity=COMMON)
    owned_items += queryset.filter(item__rarity=UNCOMMON)
    owned_items += queryset.filter(item__rarity=RARE)
    owned_items += queryset.filter(item__rarity=SUPER_RARE)
    owned_items += queryset.filter(item__rarity=SECRET)

    template_name = 'project/choose_display_item.html'
    context = {
        'player': player,
        'slot': slot,
        'owned_items': owned_items,
    }
    return render(request, template_name, context)