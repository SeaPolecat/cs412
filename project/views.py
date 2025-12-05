from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
import random


## CONSTANTS ############################################################################################


COMMON = 'C'
UNCOMMON = 'U'
RARE = 'R'
SUPER_RARE = 'SR'
SECRET = 'SE'

RARITY_ORDER = {COMMON: 1, UNCOMMON: 2, RARE: 3, SUPER_RARE: 4, SECRET: 5}


# class MyLoginRequiredMixin(LoginRequiredMixin):

#     def get_login_url(self):
#         return reverse('login')
    
#     def get_logged_in_profile(self):
#         return P.objects.get(user=self.request.user)


## CLASS-BASED VIEWS ############################################################################################


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
        owned_items = list(OwnedItem.objects.filter(player=pk))

        owned_items.sort(key=lambda oi: RARITY_ORDER[oi.item.rarity])

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

    def get_queryset(self):
        pk = self.kwargs['pk']
        
        return Box.objects.filter(player=pk).order_by('-date_created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        context['player'] = player

        return context


class BoxDetailView(DetailView):

    model = Box
    template_name = 'project/show_box.html'
    context_object_name = 'box'
    pk_url_kwarg = 'boxpk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        context['player'] = player

        error = self.request.GET.get("error")

        if error:
            context["error"] = error

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


class CreateBoxView(CreateView):
    
    model = Box
    form_class = CreateBoxForm
    template_name = 'project/create_box_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        context['player'] = player

        return context
    
    def form_valid(self, form):
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        box = form.instance
        box.player = player

        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        boxpk = self.object.pk

        return reverse('show_box', kwargs={'pk': pk, 'boxpk': boxpk})
    

class UpdateBoxView(UpdateView):

    model = Box
    form_class = CreateBoxForm
    template_name = 'project/update_box_form.html'
    pk_url_kwarg = 'boxpk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        context['player'] = player

        return context
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        boxpk = self.object.pk

        return reverse('show_box', kwargs={'pk': pk, 'boxpk': boxpk})
    

class DeleteBoxView(DeleteView):

    model = Box
    template_name = 'project/delete_box_form.html'
    pk_url_kwarg = 'boxpk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        context['player'] = player

        return context

    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse('show_all_boxes', kwargs={'pk': pk})
    

class CreateItemView(CreateView):

    form_class = CreateItemForm
    template_name = 'project/create_item_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        player = Player.objects.get(pk=pk)

        boxpk = self.kwargs['boxpk']
        box = Box.objects.get(pk=boxpk)

        context['player'] = player
        context['box'] = box

        return context
    
    def form_valid(self, form):
        boxpk = self.kwargs['boxpk']
        box = Box.objects.get(pk=boxpk)

        item = form.instance
        item.box = box

        return super().form_valid(form)
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        boxpk = self.kwargs['boxpk']

        return reverse('show_box', kwargs={'pk': pk, 'boxpk': boxpk})
    

## FUNCTION-BASED VIEWS ############################################################################################


def open_box(request, pk):
        
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
    player = Player.objects.get(pk=1)

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
    owned_items = list(OwnedItem.objects.filter(player=pk))

    owned_items.sort(key=lambda oi: RARITY_ORDER[oi.item.rarity])

    template_name = 'project/choose_display_item.html'
    context = {
        'player': player,
        'slot': slot,
        'owned_items': owned_items,
    }
    return render(request, template_name, context)
    

def publish_box(request, pk, boxpk):

    box = Box.objects.get(pk=boxpk)
    items = Item.objects.filter(box=boxpk)
    rarities = items.values_list('rarity', flat=True)

    if (COMMON in rarities
        and UNCOMMON in rarities
        and RARE in rarities
        and SUPER_RARE in rarities
        and SECRET in rarities):

        box.published = True
        box.save()

        return redirect('show_box', pk, boxpk)
    
    return redirect(f'/project/player/{pk}/box/{boxpk}?error=1')


def unpublish_box(request, pk, boxpk):

    box = Box.objects.get(pk=boxpk)

    box.published = False
    box.save()

    return redirect('show_box', pk, boxpk)