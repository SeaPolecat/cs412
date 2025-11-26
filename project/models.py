from django.db import models


class Player(models.Model):

    username = models.TextField(blank=False)
    profile_image = models.ImageField(blank=True)
    coins = models.IntegerField(default=0)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} ({self.coins} coins)'


class Box(models.Model):
    
    name = models.TextField(blank=False)
    cover_image = models.ImageField(blank=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):

    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    name = models.TextField(blank=False)
    image = models.ImageField(blank=False)

    COMMON = 'C'
    UNCOMMON = 'U'
    RARE = 'R'
    SUPER_RARE = 'SR'
    SECRET = 'SE'

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


class OwnedItem(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_owned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""
        {self.item} || owned by {self.player.username} (x {self.quantity})
        """


class DisplayItem(models.Model):

    owned_item = models.ForeignKey(OwnedItem, on_delete=models.CASCADE)
    display_slot = models.IntegerField(default=1)

    def __str__(self):
        return f"""
        {self.owned_item} || display slot {self.display_slot}
        """


class Trade(models.Model):

    trader_item = models.ForeignKey(OwnedItem, related_name='trader_item',  on_delete=models.CASCADE)
    tradee_item = models.ForeignKey(OwnedItem, related_name='tradee_item', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""
        Trader: {self.trader_item.player.username} || {self.trader_item}
        || Tradee: {self.tradee_item.player.username} || {self.tradee_item}
        """