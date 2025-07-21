from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.core.serializers import CustomUserSerializer
from apps.gold_online_store.models.transaction import GoldSaleTransaction, GoldPurchaseTransaction
from apps.gold_online_store.serializers.gold import GoldPriceSerializer


class GoldTransactionSerializer(serializers.ModelSerializer):
    """
    Base serializer for gold-related transactions (sale or purchase).
    """
    user = CustomUserSerializer(read_only=True)
    gold_price = GoldPriceSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
        help_text=_('Human-readable status of the transaction.')
    )

    class Meta:
        model = None  # Abstract, will be set in subclasses
        fields = [
            'id',
            'user',
            'create_date',
            'money_amount',
            'gold_amount',
            'gold_price',
            'status',
            'status_display',
        ]
        read_only_fields = ['id', 'user', 'create_date', 'status_display']

    def validate(self, attrs):
        """
        Ensure that money_amount, gold_amount, and gold_price are valid.
        """
        money_amount = attrs.get('money_amount', 0)
        gold_amount = attrs.get('gold_amount', 0)
        gold_price = attrs.get('gold_price', None)

        if money_amount < 0:
            raise serializers.ValidationError(_('Money amount cannot be negative.'))
        if gold_amount < 0:
            raise serializers.ValidationError(_('Gold amount cannot be negative.'))
        if money_amount > 10**12:  # Arbitrary limit for sanity check
            raise serializers.ValidationError(_('Money amount exceeds maximum allowed value.'))
        if gold_amount > 10**6:  # Arbitrary limit for sanity check
            raise serializers.ValidationError(_('Gold amount exceeds maximum allowed value.'))
        if gold_price and not gold_price.active:
            raise serializers.ValidationError(_('Selected gold price must be active.'))
        return attrs

    def create(self, validated_data):
        """
        Ensure create_date is set to current time if not provided.
        """
        if 'create_date' not in validated_data:
            validated_data['create_date'] = timezone.now()
        return super().create(validated_data)


class GoldSaleTransactionSerializer(GoldTransactionSerializer):
    """
    Serializer for GoldSaleTransaction model to handle gold sale transactions.
    """
    class Meta(GoldTransactionSerializer.Meta):
        model = GoldSaleTransaction
        verbose_name = _('gold sale transaction')
        verbose_name_plural = _('gold sale transactions')


class GoldPurchaseTransactionSerializer(GoldTransactionSerializer):
    """
    Serializer for GoldPurchaseTransaction model to handle gold purchase transactions.
    """
    class Meta(GoldTransactionSerializer.Meta):
        model = GoldPurchaseTransaction
        verbose_name = _('gold purchase transaction')
        verbose_name_plural = _('gold purchase transactions')