from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import CustomUser


class WithdrawalRequest(models.Model):
    """
    Abstract base model for withdrawal requests (money or gold).
    """
    STATUS_CHOICES = (
        ('ACCEPTED', _('Accepted')),
        ('WAITING', _('Waiting')),
        ('REJECTED', _('Rejected')),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='%(class)s_requests',
        verbose_name=_('user'),
        help_text=_('The user who initiated the withdrawal request.')
    )
    create_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('request date'),
        help_text=_('The date and time the withdrawal request was made.')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='WAITING',
        verbose_name=_('request status'),
        help_text=_('The current status of the withdrawal request.')
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['create_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.__class__.__name__} {self.id} ({self.get_request_status_display()}) for {self.user.username}"

    def save(self, *args, **kwargs):
        """
        Ensure request_date is set to current time if not provided.
        """
        if not self.request_date:
            self.create_date = timezone.now()
        super().save(*args, **kwargs)


class MoneyWithdrawalRequest(WithdrawalRequest):
    """
    Represents a request to withdraw money from a user's wallet.
    """
    money_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0,
        verbose_name=_('money amount'),
        help_text=_('The amount of money to withdraw (in IRR).')
    )

    class Meta:
        verbose_name = _('money withdrawal request')
        verbose_name_plural = _('money withdrawal requests')

    def clean(self):
        """
        Validate that money_amount is positive.
        """
        if self.money_amount < 0:
            raise models.ValidationError(_('Money amount cannot be negative.'))


class GoldWithdrawalRequest(WithdrawalRequest):
    """
    Represents a request to withdraw gold from a user's wallet.
    """
    gold_amount = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        default=0.0,
        verbose_name=_('gold amount'),
        help_text=_('The amount of gold to withdraw (in grams).')
    )

    class Meta:
        verbose_name = _('gold withdrawal request')
        verbose_name_plural = _('gold withdrawal requests')

    def clean(self):
        """
        Validate that gold_amount is positive.
        """
        if self.gold_amount < 0:
            raise models.ValidationError(_('Gold amount cannot be negative.'))