from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import CustomUser


class Wallet(models.Model):
    """
    Represents a user's wallet with money and gold stock balances.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='wallet',
        verbose_name=_('user'),
        help_text=_('The user associated with this wallet.')
    )
    money_stock = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0,
        verbose_name=_('money stock'),
        help_text=_('The amount of money in the wallet (in $).')
    )
    gold_stock = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=0.0,
        verbose_name=_('gold stock'),
        help_text=_('The amount of gold in the wallet (in grams).')
    )

    class Meta:
        verbose_name = _('wallet')
        verbose_name_plural = _('wallets')

    def __str__(self):
        return f"Wallet of {self.user.username}"

    @property
    def total_value(self):
        """
        Calculate the total value of the wallet based on current gold price.
        """
        latest_gold_price = GoldPrice.objects.filter(active=True).order_by('-date').first()
        if latest_gold_price:
            return self.money_stock + (self.gold_stock * latest_gold_price.sale_price)
        return self.money_stock


class GoldPrice(models.Model):
    """
    Stores gold price information with timestamp and stock status.
    """
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('date'),
        help_text=_('The date and time of the price record.')
    )
    sale_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=2500000.00,
        verbose_name=_('sale price'),
        help_text=_('The sale price of gold per unit (in IRR).')
    )
    price_difference = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=10000.00,
        verbose_name=_('price difference'),
        help_text=_('The difference between buy and sell prices (in $).')
    )
    total_gold_stock = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=0.0,
        verbose_name=_('total gold stock'),
        help_text=_('Total gold stock available (in grams).')
    )
    stock_status = models.BooleanField(
        default=True,
        verbose_name=_('stock status'),
        help_text=_('Indicates if gold stock is available.')
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_('active'),
        help_text=_('Indicates if this price record is currently active.')
    )

    class Meta:
        verbose_name = _('gold price')
        verbose_name_plural = _('gold prices')
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['active']),
        ]

    def __str__(self):
        return f"Gold Price on {self.date.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        """
        Ensure only one GoldPrice instance is active at a time.
        """
        if self.active:
            GoldPrice.objects.filter(active=True).exclude(pk=self.pk).update(active=False)
        super().save(*args, **kwargs)