from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


## CONSTANTS ############################################################################################


COMMON = 'C'
UNCOMMON = 'U'
RARE = 'R'
SUPER_RARE = 'SR'
SECRET = 'SE'

RARITY_ORDER = {COMMON: 1, UNCOMMON: 2, RARE: 3, SUPER_RARE: 4, SECRET: 5}


class Player(models.Model):

    username = models.TextField(blank=False)
    profile_image = models.ImageField(blank=True)
    boxes_opened = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username}'
    
    def get_all_owned_items(self):
        owned_items = list(OwnedItem.objects.filter(player=self))

        owned_items.sort(key=lambda oi: RARITY_ORDER[oi.item.rarity])

        return owned_items
    
    def get_all_boxes(self):
        return Box.objects.filter(player=self).order_by('-date_created')
    
    def get_incoming_trades(self):
        return Trade.objects.filter(tradee_item__player=self)
    
    def get_outgoing_trades(self):
        return Trade.objects.filter(trader_item__player=self)
    
    def get_slots(self):
        display_items = DisplayItem.objects.filter(owned_item__player=self)
        slots = [0] * 9

        for i in range(len(slots)):
            try:
                slots[i] = display_items.get(display_slot=i)
            except:
                pass

        return slots


class Box(models.Model):
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    cover_image = models.ImageField(blank=False)
    published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.player}, {self.published})'
    
    # make more of these methods to use directly in views/templates lol
    def get_all_items(self):
        items = list(Item.objects.filter(box=self))

        items.sort(key=lambda item: RARITY_ORDER[item.rarity])

        return items


class Item(models.Model):

    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    image = models.ImageField(blank=False)

    RARITY_CHOICES = {
        COMMON: 'Common',
        UNCOMMON: 'Uncommon',
        RARE: 'Rare',
        SUPER_RARE: 'Super Rare',
        SECRET: 'Secret',
    }

    rarity = models.CharField(
        max_length=2,
        choices=RARITY_CHOICES,
        default=COMMON,
    )

    def __str__(self):
        return f'{self.name} ({self.rarity}) --> {self.box}'
    
    def get_number_in_existence(self):
        owned_items = OwnedItem.objects.filter(item=self)
        num = 0

        for oi in owned_items:
            num += oi.quantity

        return num
    
    def get_rarity_color(self):
        RARITY_COLORS = {
            COMMON: 'gray',
            UNCOMMON: 'green',
            RARE: 'blue',
            SUPER_RARE: 'purple',
            SECRET: 'yellow',
        }
        return RARITY_COLORS[self.rarity]


class OwnedItem(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_owned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.item} || owned by {self.player} (x {self.quantity})'


class DisplayItem(models.Model):

    owned_item = models.ForeignKey(OwnedItem, on_delete=models.CASCADE)
    display_slot = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.owned_item} || display slot {self.display_slot}'


class Trade(models.Model):

    trader_item = models.ForeignKey(OwnedItem, related_name='trader_item',  on_delete=models.CASCADE)
    tradee_item = models.ForeignKey(OwnedItem, related_name='tradee_item', on_delete=models.CASCADE)
    trader_confirmed = models.BooleanField(default=False)
    tradee_confirmed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.trader_item} <==> {self.tradee_item}'