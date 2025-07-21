from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.gold_online_store.models.gold import GoldPrice

from apps.core.models import CustomUser


class GoldTransaction(models.Model):
    """
    Abstract base model for gold-related transactions (sale or purchase).
    """
    STATUS_CHOICES = (
        ('ACCEPTED', _('Accepted')),
        ('WAITING', _('Waiting')),
        ('REJECTED', _('Rejected')),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='%(class)s_transactions',
        verbose_name=_('user'),
        help_text=_('The user who initiated the transaction.')
    )
    create_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('create date'),
        help_text=_('The date and time the transaction was initiated.')
    )
    money_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0,
        verbose_name=_('money amount'),
        help_text=_('The amount of money involved in the transaction (in $).')
    )
    gold_amount = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=0.0,
        verbose_name=_('gold amount'),
        help_text=_('The amount of gold involved in the transaction (in grams).')
    )
    gold_price = models.ForeignKey(
        GoldPrice,
        on_delete=models.PROTECT,
        related_name='%(class)s_transactions',
        verbose_name=_('gold price'),
        help_text=_('The gold price record associated with this transaction.')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='WAITING',
        verbose_name=_('status'),
        help_text=_('The current status of the transaction.')
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['create_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.__class__.__name__} {self.id} ({self.get_status_display()}) for {self.user.username}"

    def clean(self):
        """
        Validate that money_amount and gold_amount are positive.
        """
        if self.money_amount < 0:
            raise models.ValidationError(_('Money amount cannot be negative.'))
        if self.gold_amount < 0:
            raise models.ValidationError(_('Gold amount cannot be negative.'))

    def save(self, *args, **kwargs):
        """
        Ensure transaction_date is set to current time if not provided.
        """
        if not self.create_date:
            self.create_date = timezone.now()
        super().save(*args, **kwargs)


class GoldSaleTransaction(GoldTransaction):
    """
    Represents a transaction for selling gold by a user.
    """
    class Meta:
        verbose_name = _('gold sale transaction')
        verbose_name_plural = _('gold sale transactions')


class GoldPurchaseTransaction(GoldTransaction):
    """
    Represents a transaction for purchasing gold by a user.
    """
    class Meta:
        verbose_name = _('gold purchase transaction')
        verbose_name_plural = _('gold purchase transactions')