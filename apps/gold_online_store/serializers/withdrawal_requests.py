from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.core.serializers import CustomUserSerializer
from apps.gold_online_store.models.withdrawal_requests import MoneyWithdrawalRequest, GoldWithdrawalRequest


class WithdrawalRequestSerializer(serializers.ModelSerializer):
    """
    Base serializer for withdrawal requests (money or gold).
    """
    user = CustomUserSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True,
        help_text=_('Human-readable status of the withdrawal request.')
    )

    class Meta:
        model = None  # Abstract, will be set in subclasses
        fields = [
            'id',
            'user',
            'create_date',
            'status',
            'status_display',
        ]
        read_only_fields = ['id', 'user', 'create_date', 'status_display']

    def validate(self, attrs):
        """
        Ensure that status is valid.
        """
        status = attrs.get('status', None)
        if status and status not in dict(self.Meta.model.STATUS_CHOICES).keys():
            raise serializers.ValidationError(_('Invalid status value.'))
        return attrs

    def create(self, validated_data):
        """
        Ensure create_date is set to current time if not provided.
        """
        if 'create_date' not in validated_data:
            validated_data['create_date'] = timezone.now()
        return super().create(validated_data)


class MoneyWithdrawalRequestSerializer(WithdrawalRequestSerializer):
    """
    Serializer for MoneyWithdrawalRequest model to handle money withdrawal requests.
    """
    class Meta(WithdrawalRequestSerializer.Meta):
        model = MoneyWithdrawalRequest
        fields = WithdrawalRequestSerializer.Meta.fields + ['money_amount']
        read_only_fields = WithdrawalRequestSerializer.Meta.read_only_fields

    def validate(self, attrs):
        """
        Ensure that money_amount is non-negative and within reasonable limits.
        """
        attrs = super().validate(attrs)
        money_amount = attrs.get('money_amount', 0)
        if money_amount < 0:
            raise serializers.ValidationError(_('Money amount cannot be negative.'))
        if money_amount > 10**12:  # Arbitrary limit for sanity check
            raise serializers.ValidationError(_('Money amount exceeds maximum allowed value.'))
        return attrs


class GoldWithdrawalRequestSerializer(WithdrawalRequestSerializer):
    """
    Serializer for GoldWithdrawalRequest model to handle gold withdrawal requests.
    """
    class Meta(WithdrawalRequestSerializer.Meta):
        model = GoldWithdrawalRequest
        fields = WithdrawalRequestSerializer.Meta.fields + ['gold_amount']
        read_only_fields = WithdrawalRequestSerializer.Meta.read_only_fields

    def validate(self, attrs):
        """
        Ensure that gold_amount is non-negative and within reasonable limits.
        """
        attrs = super().validate(attrs)
        gold_amount = attrs.get('gold_amount', 0)
        if gold_amount < 0:
            raise serializers.ValidationError(_('Gold amount cannot be negative.'))
        if gold_amount > 10**6:  # Arbitrary limit for sanity check
            raise serializers.ValidationError(_('Gold amount exceeds maximum allowed value.'))
        return attrs