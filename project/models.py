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
    coins = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username} ({self.coins} coins)'


class Box(models.Model):
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    cover_image = models.ImageField(blank=False)
    published = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.player.username}, {self.published})'
    
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
        return f'{self.item} || owned by {self.player.username} (x {self.quantity})'


class DisplayItem(models.Model):

    owned_item = models.ForeignKey(OwnedItem, on_delete=models.CASCADE)
    display_slot = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.owned_item} || display slot {self.display_slot}'


class Trade(models.Model):

    trader_item = models.ForeignKey(OwnedItem, related_name='trader_item',  on_delete=models.CASCADE)
    tradee_item = models.ForeignKey(OwnedItem, related_name='tradee_item', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""
        Trader: {self.trader_item.player.username} || {self.trader_item}
        || Tradee: {self.tradee_item.player.username} || {self.tradee_item}
        """