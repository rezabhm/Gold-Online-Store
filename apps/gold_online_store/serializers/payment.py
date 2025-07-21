from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.core.serializers import CustomUserSerializer
from apps.gold_online_store.models.payment import PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentTransaction model to handle payment transaction data.
    """
    user = CustomUserSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
        help_text=_('Human-readable status of the payment transaction.')
    )

    class Meta:
        model = PaymentTransaction
        fields = [
            'id',
            'user',
            'payment_date',
            'money_amount',
            'status',
            'status_display',
        ]
        read_only_fields = ['id', 'user', 'payment_date', 'status_display']

    def validate(self, attrs):
        """
        Ensure that money_amount is non-negative and within reasonable limits.
        """
        money_amount = attrs.get('money_amount', 0)
        if money_amount < 0:
            raise serializers.ValidationError(_('Money amount cannot be negative.'))
        if money_amount > 10**12:  # Arbitrary limit for sanity check
            raise serializers.ValidationError(_('Money amount exceeds maximum allowed value.'))
        return attrs

    def create(self, validated_data):
        """
        Ensure payment_date is set to current time if not provided.
        """
        if 'payment_date' not in validated_data:
            validated_data['payment_date'] = timezone.now()
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Customize the output to include additional context if needed.
        """
        representation = super().to_representation(instance)
        return representation