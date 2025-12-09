# File: project/models.py
# Author: Yi Ji (Wayne) Wang (waynew@bu.edu), 12/08/2025
# Description: Defines what attributes that models in the database should have.

from django.db import models
from django.contrib.auth.models import User
import random


## CONSTANTS ############################################################################################


# Django shorthand representations of different Item rarities
COMMON = 'C'
UNCOMMON = 'U'
RARE = 'R'
SUPER_RARE = 'SR'
SECRET = 'SE'

# rarities and their full names
RARITY_CHOICES = {
    (COMMON, 'Common'),
    (UNCOMMON, 'Uncommon'),
    (RARE, 'Rare'),
    (SUPER_RARE, 'Super Rare'),
    (SECRET, 'Secret'),
}

# colours that represent each rarity, in hexadecimal format
RARITY_COLOURS = {
    COMMON: '#8a8a8a',
    UNCOMMON: '#5ead57',
    RARE: '#598eff',
    SUPER_RARE: '#c95cff',
    SECRET: '#f0a226',
}

# Cumulative Density Function of X, where X = rarity of Item drawn from a Box;
# Pr(X <= COMMON) = 0.4, Pr(X <= UNCOMMON) = 0.7, etc.
RARITY_CDF = {         # PDF
    COMMON: 0.4,       # 0.4
    UNCOMMON: 0.7,     # 0.3
    RARE: 0.9,         # 0.2
    SUPER_RARE: 0.99,  # 0.09
    SECRET: 1,         # 0.01
}

# the order that items should appear in, based on rarity
RARITY_ORDER = {COMMON: 1, UNCOMMON: 2, RARE: 3, SUPER_RARE: 4, SECRET: 5}


## MODELS ############################################################################################


class Player(models.Model):
    """Encapsulate the data of a Player who opens blindboxes."""

    username = models.TextField(blank=False) # the Player's name
    profile_image = models.ImageField(blank=True) # the Player's profile image
    boxes_opened = models.IntegerField(default=0) # the number of blindboxes that the Player has opened
    date_joined = models.DateTimeField(auto_now_add=True) # the date when the Player joined
    user = models.OneToOneField(User, on_delete=models.CASCADE) # the Django user tied to the Player via a 1-to-1 relationship

    def __str__(self):
        """Return a string representation of this Player."""

        return f'{self.username}'
    
    def get_all_owned_items(self):
        """Get all the OwnedItems that this Player owns."""

        owned_items = list(OwnedItem.objects.filter(player=self))

        # sort the OwnedItems by increasing rarity
        owned_items.sort(key=lambda oi: RARITY_ORDER[oi.item.rarity])

        return owned_items
    
    def get_all_boxes(self):
        """Get all the Boxes that this Player created."""

        return Box.objects.filter(player=self).order_by('-date_created')
    
    def get_incoming_trades(self):
        """Get all incoming Trades (where another Player requested a 
        trade with this Player).
        """

        return Trade.objects.filter(tradee_item__player=self)
    
    def get_outgoing_trades(self):
        """Get all outgoing Trades (where this Player requested a 
        trade with another Player).
        """

        return Trade.objects.filter(trader_item__player=self)
    
    def get_slots(self):
        """Get a list representing the display slots on this Player's profile."""

        # query all DisplayItems corresponding to this Player
        display_items = DisplayItem.objects.filter(owned_item__player=self)

        # a Player has 9 slots to display items
        slots = [0] * 9

        # fill the slots with the DisplayItems that this Player chose to display;
        # a slot with 0 means that no item should be displayed there
        for i in range(len(slots)):
            try:
                slots[i] = display_items.get(display_slot=i)
            except:
                pass

        return slots


class Box(models.Model):
    """Encapsulate the data of a blind Box."""
    
    player = models.ForeignKey(Player, on_delete=models.CASCADE) # the Player who created this Box
    name = models.TextField(blank=False) # the name of this Box
    cover_image = models.ImageField(blank=False) # the cover image of this Box
    published = models.BooleanField(default=False) # whether or not this Box is published to the shop
    date_created = models.DateTimeField(auto_now_add=True) # the date when this Box was created

    def __str__(self):
        """Return a string representation of this Box."""

        return f'{self.name} ({self.player}, {self.published})'
    
    def get_all_items(self):
        """Get all the Items that can be obtained from this Box."""

        items = list(Item.objects.filter(box=self))

        # sort the Items by increasing rarity
        items.sort(key=lambda item: RARITY_ORDER[item.rarity])

        return items
    
    def draw_random_item(self):
        """Draw a random Item from this Box (with respect to different rarity probabilities)."""
    
        # generate a random float uniformly distributed along the interval [0.0, 1.0]
        rand = random.uniform(0.0, 1.0)

        # check which interval of RARITY_CDF that rand belongs to,
        # and query a list of Items of the appropriate rarity

        if rand <= RARITY_CDF[COMMON]:
            items = Item.objects.filter(box=self, rarity=COMMON)

        elif rand > RARITY_CDF[COMMON] and rand <= RARITY_CDF[UNCOMMON]:
            items = Item.objects.filter(box=self, rarity=UNCOMMON)

        elif rand > RARITY_CDF[UNCOMMON] and rand <= RARITY_CDF[RARE]:
            items = Item.objects.filter(box=self, rarity=RARE)

        elif rand > RARITY_CDF[RARE] and rand <= RARITY_CDF[SUPER_RARE]:
            items = Item.objects.filter(box=self, rarity=SUPER_RARE)

        else:
            items = Item.objects.filter(box=self, rarity=SECRET)

        # choose a random item from the resulting list of Items
        return random.choice(items)
    
    def contains_every_rarity(self):
        """Check whether this Box contains at least 1 Item of each rarity."""

        # get all the Items in this Box and extract their rarities into a list
        items = Item.objects.filter(box=self)
        rarities = items.values_list('rarity', flat=True)

        # check if the rarities list contains every rarity
        if (COMMON in rarities
            and UNCOMMON in rarities
            and RARE in rarities
            and SUPER_RARE in rarities
            and SECRET in rarities):

            return True
        
        return False


class Item(models.Model):
    """Encapsulate the data of an Item that can be obtained from a Box."""

    box = models.ForeignKey(Box, on_delete=models.CASCADE) # the Box that this Item belongs to
    name = models.TextField(blank=False) # this Item's name
    image = models.ImageField(blank=False) # this Item's image

    # this Item's rarity level (rarer == smaller chance of obtaining it from a Box)
    rarity = models.CharField(max_length=2, choices=RARITY_CHOICES, default=COMMON)

    def __str__(self):
        """Return a string representation of this Item."""

        return f'{self.name} ({self.rarity}) --> {self.box}'
    
    def get_number_in_existence(self):
        """Get the total number of instances of this Item that 
        Players have obtained."""

        # query all OwnedItems corresponding to this Item
        owned_items = OwnedItem.objects.filter(item=self)
        num = 0

        # sum all the OwnedItems' quantities 
        for oi in owned_items:
            num += oi.quantity

        return num
    
    def get_rarity_color(self):
        """Return the colour that an Item's rarity should have,
        in hexadecimal format.
        """

        return RARITY_COLOURS[self.rarity]


class OwnedItem(models.Model):
    """Encapsulate the data of an Item owned by a Player."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE) # the Player who owns this OwnedItem
    item = models.ForeignKey(Item, on_delete=models.CASCADE) # the Item corresponding to this OwnedItem
    quantity = models.IntegerField(default=1) # how many of this OwnedItem the Player owns
    date_owned = models.DateTimeField(auto_now_add=True) # the date when the first instance of this OwnedItem was obtained

    def __str__(self):
        """Return a string representation of this OwnedItem."""

        return f'{self.item} || owned by {self.player} (x {self.quantity})'


class DisplayItem(models.Model):
    """Encapsulate the data of an Item that a Player has displayed on their Profile."""

    owned_item = models.ForeignKey(OwnedItem, on_delete=models.CASCADE) # the OwnedItem to be displayed
    display_slot = models.IntegerField(default=1) # the display slot that this DisplayItem is placed in

    def __str__(self):
        """Return a string representation of this DisplayItem."""

        return f'{self.owned_item} || display slot {self.display_slot}'


class Trade(models.Model):
    """Encapsulate the data of a Trade of Items between 2 Players."""

    # the OwnedItem offered by this Trade's instigator
    trader_item = models.ForeignKey(OwnedItem, related_name='trader_item',  on_delete=models.CASCADE)

    # the OwnedItem that this Trade's instigator wants to have in exchange
    tradee_item = models.ForeignKey(OwnedItem, related_name='tradee_item', on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True) # the date when this Trade was created

    def __str__(self):
        """Return a string representation of this Trade."""

        return f'{self.trader_item} <==> {self.tradee_item}'