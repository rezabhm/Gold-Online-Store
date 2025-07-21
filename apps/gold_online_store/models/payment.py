from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.core.models import CustomUser


class PaymentTransaction(models.Model):
    """
    Represents a payment transaction associated with a user.
    """
    STATUS_CHOICES = (
        ('PENDING', _('Pending Payment')),
        ('SUCCESS', _('Successful Payment')),
        ('FAILED', _('Failed Payment')),
    )

    payment_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('payment date'),
        help_text=_('The date and time of the payment transaction.')
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='payment_transactions',
        verbose_name=_('user'),
        help_text=_('The user associated with this payment transaction.')
    )
    money_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0,
        verbose_name=_('money amount'),
        help_text=_('The amount of money involved in the transaction (in $).')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name=_('status'),
        help_text=_('The status of the payment transaction.')
    )

    class Meta:
        verbose_name = _('payment transaction')
        verbose_name_plural = _('payment transactions')
        indexes = [
            models.Index(fields=['payment_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Payment {self.pk} ({self.get_status_display()})"
