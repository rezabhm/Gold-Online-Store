from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.core.serializers import CustomUserSerializer
from apps.gold_online_store.models.gold import Wallet, GoldPrice


class GoldPriceSerializer(serializers.ModelSerializer):
    """
    Serializer for GoldPrice model to handle gold price data.
    """
    class Meta:
        model = GoldPrice
        fields = [
            'id',
            'date',
            'sale_price',
            'price_difference',
            'total_gold_stock',
            'stock_status',
            'active',
        ]
        read_only_fields = ['id', 'date']

    def validate(self, attrs):
        """
        Ensure that sale_price, price_difference, and total_gold_stock are non-negative.
        """
        if attrs.get('sale_price', 0) < 0:
            raise serializers.ValidationError(_('Sale price cannot be negative.'))
        if attrs.get('price_difference', 0) < 0:
            raise serializers.ValidationError(_('Price difference cannot be negative.'))
        if attrs.get('total_gold_stock', 0) < 0:
            raise serializers.ValidationError(_('Total gold stock cannot be negative.'))
        return attrs

    def create(self, validated_data):
        """
        Set active=True for new GoldPrice instances and ensure only one is active.
        """
        instance = super().create(validated_data)
        if instance.active:
            GoldPrice.objects.filter(active=True).exclude(pk=instance.pk).update(active=False)
        return instance


class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for Wallet model to handle wallet data and related user information.
    """
    user = CustomUserSerializer(read_only=True)
    total_value = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True,
        help_text=_('The total value of the wallet (money + gold value in USD).')
    )

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'money_stock', 'gold_stock', 'total_value']
        read_only_fields = ['id', 'user', 'total_value']

    def validate(self, attrs):
        """
        Ensure that money_stock and gold_stock are non-negative and within reasonable limits.
        """
        money_stock = attrs.get('money_stock', 0)
        gold_stock = attrs.get('gold_stock', 0)

        if money_stock < 0:
            raise serializers.ValidationError(_('Money stock cannot be negative.'))
        if gold_stock < 0:
            raise serializers.ValidationError(_('Gold stock cannot be negative.'))
        if money_stock > 10**12:  # Arbitrary limit for sanity check
            raise serializers.ValidationError(_('Money stock exceeds maximum allowed value.'))
        if gold_stock > 10**6:  # Arbitrary limit for sanity check
            raise serializers.ValidationError(_('Gold stock exceeds maximum allowed value.'))
        return attrs

    def to_representation(self, instance):
        """
        Include the latest active gold price in the wallet representation for context.
        """
        representation = super().to_representation(instance)
        latest_gold_price = GoldPrice.objects.filter(active=True).order_by('-date').first()
        representation['latest_gold_price'] = (
            GoldPriceSerializer(latest_gold_price).data if latest_gold_price else None
        )
        return representation