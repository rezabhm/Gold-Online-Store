import pytest
from django.utils import timezone
from decimal import Decimal
import factory
from faker import Faker
from django.contrib.auth.models import User
from apps.gold_online_store.models.gold import Wallet, GoldPrice
from apps.gold_online_store.models.payment import PaymentTransaction
from apps.gold_online_store.models.transaction import GoldSaleTransaction, GoldPurchaseTransaction
from apps.gold_online_store.models.withdrawal_requests import MoneyWithdrawalRequest, GoldWithdrawalRequest
from apps.gold_online_store.serializers.gold import WalletSerializer, GoldPriceSerializer
from apps.gold_online_store.serializers.payment import PaymentTransactionSerializer
from apps.gold_online_store.serializers.transaction import GoldSaleTransactionSerializer, GoldPurchaseTransactionSerializer
from apps.gold_online_store.serializers.withdrawal_requests import MoneyWithdrawalRequestSerializer, GoldWithdrawalRequestSerializer

# Factory setup for test data
faker = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.user_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    user = factory.SubFactory(UserFactory)
    money_stock = Decimal('1000.00')
    gold_stock = Decimal('10.00')

class GoldPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldPrice

    date = factory.LazyAttribute(lambda _: timezone.now().date())
    sale_price = Decimal('50.00')
    price_difference = Decimal('5.00')
    total_gold_stock = Decimal('1000.00')
    stock_status = 'available'
    active = True

class PaymentTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentTransaction

    user = factory.SubFactory(UserFactory)
    payment_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('500.00')
    status = 'pending'

class GoldSaleTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldSaleTransaction

    user = factory.SubFactory(UserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('500.00')
    gold_amount = Decimal('10.00')
    gold_price = factory.SubFactory(GoldPriceFactory)
    status = 'pending'

class GoldPurchaseTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldPurchaseTransaction

    user = factory.SubFactory(UserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('500.00')
    gold_amount = Decimal('10.00')
    gold_price = factory.SubFactory(GoldPriceFactory)
    status = 'pending'

class MoneyWithdrawalRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MoneyWithdrawalRequest

    user = factory.SubFactory(UserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('200.00')
    status = 'pending'

class GoldWithdrawalRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldWithdrawalRequest

    user = factory.SubFactory(UserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    gold_amount = Decimal('5.00')
    status = 'pending'

# GoldPriceSerializer Tests
@pytest.mark.django_db
def test_gold_price_serializer_valid_data():
    data = {
        'sale_price': '50.00',
        'price_difference': '5.00',
        'total_gold_stock': '1000.00',
        'stock_status': 'available',
        'active': True,
    }
    serializer = GoldPriceSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['sale_price'] == Decimal('50.00')
    assert serializer.validated_data['price_difference'] == Decimal('5.00')
    assert serializer.validated_data['total_gold_stock'] == Decimal('1000.00')

@pytest.mark.django_db
def test_gold_price_serializer_create():
    data = {
        'sale_price': '50.00',
        'price_difference': '5.00',
        'total_gold_stock': '1000.00',
        'stock_status': 'available',
        'active': True,
    }
    serializer = GoldPriceSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.active is True
    assert GoldPrice.objects.filter(active=True).count() == 1

@pytest.mark.django_db
def test_gold_price_serializer_create_deactivates_others():
    GoldPriceFactory(active=True)
    data = {
        'sale_price': '60.00',
        'price_difference': '6.00',
        'total_gold_stock': '1000.00',
        'stock_status': 'available',
        'active': True,
    }
    serializer = GoldPriceSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save()
    assert GoldPrice.objects.filter(active=True).count() == 1
    assert GoldPrice.objects.get(id=instance.id).active is True

@pytest.mark.django_db
def test_gold_price_serializer_negative_sale_price():
    data = {
        'sale_price': '-50.00',
        'price_difference': '5.00',
        'total_gold_stock': '1000.00',
        'stock_status': 'available',
        'active': True,
    }
    serializer = GoldPriceSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Sale price cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_price_serializer_negative_price_difference():
    data = {
        'sale_price': '50.00',
        'price_difference': '-5.00',
        'total_gold_stock': '1000.00',
        'stock_status': 'available',
        'active': True,
    }
    serializer = GoldPriceSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Price difference cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_price_serializer_negative_total_gold_stock():
    data = {
        'sale_price': '50.00',
        'price_difference': '5.00',
        'total_gold_stock': '-1000.00',
        'stock_status': 'available',
        'active': True,
    }
    serializer = GoldPriceSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Total gold stock cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_price_serializer_read_only_fields():
    data = {
        'id': 999,
        'date': '2025-01-01',
        'sale_price': '50.00',
        'price_difference': '5.00',
        'total_gold_stock': '1000.00',
        'stock_status': 'available',
        'active': True,
    }
    serializer = GoldPriceSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.id != 999
    assert instance.date != '2025-01-01'

# WalletSerializer Tests
@pytest.mark.django_db
def test_wallet_serializer_valid_data():
    data = {
        'money_stock': '1000.00',
        'gold_stock': '10.00',
    }
    serializer = WalletSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_stock'] == Decimal('1000.00')
    assert serializer.validated_data['gold_stock'] == Decimal('10.00')

@pytest.mark.django_db
def test_wallet_serializer_create():
    user = UserFactory()
    data = {
        'money_stock': '1000.00',
        'gold_stock': '10.00',
    }
    serializer = WalletSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert serializer.is_valid()
    instance = serializer.save(user=user)
    assert instance.money_stock == Decimal('1000.00')
    assert instance.gold_stock == Decimal('10.00')
    assert instance.user == user

@pytest.mark.django_db
def test_wallet_serializer_negative_money_stock():
    data = {
        'money_stock': '-1000.00',
        'gold_stock': '10.00',
    }
    serializer = WalletSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money stock cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_wallet_serializer_negative_gold_stock():
    data = {
        'money_stock': '1000.00',
        'gold_stock': '-10.00',
    }
    serializer = WalletSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold stock cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_wallet_serializer_exceeds_money_stock_limit():
    data = {
        'money_stock': '1000000000001.00',
        'gold_stock': '10.00',
    }
    serializer = WalletSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money stock exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_wallet_serializer_exceeds_gold_stock_limit():
    data = {
        'money_stock': '1000.00',
        'gold_stock': '1000001.00',
    }
    serializer = WalletSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold stock exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_wallet_serializer_to_representation():
    wallet = WalletFactory()
    GoldPriceFactory(active=True)
    serializer = WalletSerializer(instance=wallet)
    representation = serializer.data
    assert 'latest_gold_price' in representation
    assert representation['latest_gold_price']['active'] is True
    assert 'total_value' in representation
    assert 'user' in representation

@pytest.mark.django_db
def test_wallet_serializer_read_only_fields():
    data = {
        'id': 999,
        'user': {'username': 'testuser'},
        'money_stock': '1000.00',
        'gold_stock': '10.00',
        'total_value': '1500.00',
    }
    serializer = WalletSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save(user=UserFactory())
    assert instance.id != 999
    assert instance.total_value != Decimal('1500.00')

# PaymentTransactionSerializer Tests
@pytest.mark.django_db
def test_payment_transaction_serializer_valid_data():
    data = {
        'money_amount': '500.00',
        'status': 'pending',
    }
    serializer = PaymentTransactionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('500.00')
    assert serializer.validated_data['status'] == 'pending'

@pytest.mark.django_db
def test_payment_transaction_serializer_create():
    user = UserFactory()
    data = {
        'money_amount': '500.00',
        'status': 'pending',
    }
    serializer = PaymentTransactionSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert serializer.is_valid()
    instance = serializer.save(user=user)
    assert instance.money_amount == Decimal('500.00')
    assert instance.status == 'pending'
    assert instance.payment_date is not None

@pytest.mark.django_db
def test_payment_transaction_serializer_negative_money_amount():
    data = {
        'money_amount': '-500.00',
        'status': 'pending',
    }
    serializer = PaymentTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_payment_transaction_serializer_exceeds_money_amount_limit():
    data = {
        'money_amount': '1000000000001.00',
        'status': 'pending',
    }
    serializer = PaymentTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_payment_transaction_serializer_read_only_fields():
    data = {
        'id': 999,
        'user': {'username': 'testuser'},
        'payment_date': '2025-01-01T00:00:00Z',
        'money_amount': '500.00',
        'status': 'pending',
        'status_display': 'Pending',
    }
    serializer = PaymentTransactionSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save(user=UserFactory())
    assert instance.id != 999
    assert instance.payment_date != '2025-01-01T00:00:00Z'
    assert instance.status_display == instance.get_status_display()

@pytest.mark.django_db
def test_payment_transaction_serializer_to_representation():
    transaction = PaymentTransactionFactory()
    serializer = PaymentTransactionSerializer(instance=transaction)
    representation = serializer.data
    assert 'status_display' in representation
    assert representation['status_display'] == transaction.get_status_display()
    assert 'user' in representation

# GoldSaleTransactionSerializer Tests
@pytest.mark.django_db
def test_gold_sale_transaction_serializer_valid_data():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('500.00')
    assert serializer.validated_data['gold_amount'] == Decimal('10.00')
    assert serializer.validated_data['gold_price'] == gold_price

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_create():
    user = UserFactory()
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert serializer.is_valid()
    instance = serializer.save(user=user)
    assert instance.money_amount == Decimal('500.00')
    assert instance.gold_amount == Decimal('10.00')
    assert instance.gold_price == gold_price
    assert instance.create_date is not None

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_negative_money_amount():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '-500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_negative_gold_amount():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '-10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold amount cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_exceeds_money_amount_limit():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '1000000000001.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_exceeds_gold_amount_limit():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '1000001.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold amount exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_inactive_gold_price():
    gold_price = GoldPriceFactory(active=False)
    data = {
        'money_amount': '500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Selected gold price must be active' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_to_representation():
    transaction = GoldSaleTransactionFactory()
    serializer = GoldSaleTransactionSerializer(instance=transaction)
    representation = serializer.data
    assert 'status_display' in representation
    assert representation['status_display'] == transaction.get_status_display()
    assert 'gold_price' in representation
    assert 'user' in representation

# GoldPurchaseTransactionSerializer Tests
@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_valid_data():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('500.00')
    assert serializer.validated_data['gold_amount'] == Decimal('10.00')
    assert serializer.validated_data['gold_price'] == gold_price

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_create():
    user = UserFactory()
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert serializer.is_valid()
    instance = serializer.save(user=user)
    assert instance.money_amount == Decimal('500.00')
    assert instance.gold_amount == Decimal('10.00')
    assert instance.gold_price == gold_price
    assert instance.create_date is not None

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_negative_money_amount():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '-500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_negative_gold_amount():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '-10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold amount cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_exceeds_money_amount_limit():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '1000000000001.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_exceeds_gold_amount_limit():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '500.00',
        'gold_amount': '1000001.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold amount exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_inactive_gold_price():
    gold_price = GoldPriceFactory(active=False)
    data = {
        'money_amount': '500.00',
        'gold_amount': '10.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Selected gold price must be active' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_to_representation():
    transaction = GoldPurchaseTransactionFactory()
    serializer = GoldPurchaseTransactionSerializer(instance=transaction)
    representation = serializer.data
    assert 'status_display' in representation
    assert representation['status_display'] == transaction.get_status_display()
    assert 'gold_price' in representation
    assert 'user' in representation

# MoneyWithdrawalRequestSerializer Tests
@pytest.mark.django_db
def test_money_withdrawal_request_serializer_valid_data():
    data = {
        'money_amount': '200.00',
        'status': 'pending',
    }
    serializer = MoneyWithdrawalRequestSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('200.00')
    assert serializer.validated_data['status'] == 'pending'

@pytest.mark.django_db
def test_money_withdrawal_request_serializer_create():
    user = UserFactory()
    data = {
        'money_amount': '200.00',
        'status': 'pending',
    }
    serializer = MoneyWithdrawalRequestSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert serializer.is_valid()
    instance = serializer.save(user=user)
    assert instance.money_amount == Decimal('200.00')
    assert instance.status == 'pending'
    assert instance.create_date is not None

@pytest.mark.django_db
def test_money_withdrawal_request_serializer_negative_money_amount():
    data = {
        'money_amount': '-200.00',
        'status': 'pending',
    }
    serializer = MoneyWithdrawalRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_money_withdrawal_request_serializer_exceeds_money_amount_limit():
    data = {
        'money_amount': '1000000000001.00',
        'status': 'pending',
    }
    serializer = MoneyWithdrawalRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Money amount exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_money_withdrawal_request_serializer_invalid_status():
    data = {
        'money_amount': '200.00',
        'status': 'invalid_status',
    }
    serializer = MoneyWithdrawalRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Invalid status value' in str(serializer.errors)

@pytest.mark.django_db
def test_money_withdrawal_request_serializer_to_representation():
    request = MoneyWithdrawalRequestFactory()
    serializer = MoneyWithdrawalRequestSerializer(instance=request)
    representation = serializer.data
    assert 'status_display' in representation
    assert representation['status_display'] == request.get_status_display()
    assert 'user' in representation

@pytest.mark.django_db
def test_money_withdrawal_request_serializer_read_only_fields():
    data = {
        'id': 999,
        'user': {'username': 'testuser'},
        'create_date': '2025-01-01T00:00:00Z',
        'money_amount': '200.00',
        'status': 'pending',
        'status_display': 'Pending',
    }
    serializer = MoneyWithdrawalRequestSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save(user=UserFactory())
    assert instance.id != 999
    assert instance.create_date != '2025-01-01T00:00:00Z'

# GoldWithdrawalRequestSerializer Tests
@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_valid_data():
    data = {
        'gold_amount': '5.00',
        'status': 'pending',
    }
    serializer = GoldWithdrawalRequestSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['gold_amount'] == Decimal('5.00')
    assert serializer.validated_data['status'] == 'pending'

@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_create():
    user = UserFactory()
    data = {
        'gold_amount': '5.00',
        'status': 'pending',
    }
    serializer = GoldWithdrawalRequestSerializer(data=data, context={'request': type('Request', (), {'user': user})()})
    assert serializer.is_valid()
    instance = serializer.save(user=user)
    assert instance.gold_amount == Decimal('5.00')
    assert instance.status == 'pending'
    assert instance.create_date is not None

@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_negative_gold_amount():
    data = {
        'gold_amount': '-5.00',
        'status': 'pending',
    }
    serializer = GoldWithdrawalRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold amount cannot be negative' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_exceeds_gold_amount_limit():
    data = {
        'gold_amount': '1000001.00',
        'status': 'pending',
    }
    serializer = GoldWithdrawalRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Gold amount exceeds maximum allowed value' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_invalid_status():
    data = {
        'gold_amount': '5.00',
        'status': 'invalid_status',
    }
    serializer = GoldWithdrawalRequestSerializer(data=data)
    assert not serializer.is_valid()
    assert 'Invalid status value' in str(serializer.errors)

@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_to_representation():
    request = GoldWithdrawalRequestFactory()
    serializer = GoldWithdrawalRequestSerializer(instance=request)
    representation = serializer.data
    assert 'status_display' in representation
    assert representation['status_display'] == request.get_status_display()
    assert 'user' in representation

@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_read_only_fields():
    data = {
        'id': 999,
        'user': {'username': 'testuser'},
        'create_date': '2025-01-01T00:00:00Z',
        'gold_amount': '5.00',
        'status': 'pending',
        'status_display': 'Pending',
    }
    serializer = GoldWithdrawalRequestSerializer(data=data)
    assert serializer.is_valid()
    instance = serializer.save(user=UserFactory())
    assert instance.id != 999
    assert instance.create_date != '2025-01-01T00:00:00Z'

# Edge Case Tests
@pytest.mark.django_db
def test_gold_price_serializer_empty_data():
    serializer = GoldPriceSerializer(data={})
    assert not serializer.is_valid()
    assert 'sale_price' in serializer.errors
    assert 'total_gold_stock' in serializer.errors

@pytest.mark.django_db
def test_wallet_serializer_zero_values():
    data = {
        'money_stock': '0.00',
        'gold_stock': '0.00',
    }
    serializer = WalletSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_stock'] == Decimal('0.00')
    assert serializer.validated_data['gold_stock'] == Decimal('0.00')

@pytest.mark.django_db
def test_payment_transaction_serializer_zero_money_amount():
    data = {
        'money_amount': '0.00',
        'status': 'pending',
    }
    serializer = PaymentTransactionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('0.00')

@pytest.mark.django_db
def test_gold_sale_transaction_serializer_zero_amounts():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '0.00',
        'gold_amount': '0.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldSaleTransactionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('0.00')
    assert serializer.validated_data['gold_amount'] == Decimal('0.00')

@pytest.mark.django_db
def test_gold_purchase_transaction_serializer_zero_amounts():
    gold_price = GoldPriceFactory(active=True)
    data = {
        'money_amount': '0.00',
        'gold_amount': '0.00',
        'gold_price': gold_price.id,
        'status': 'pending',
    }
    serializer = GoldPurchaseTransactionSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('0.00')
    assert serializer.validated_data['gold_amount'] == Decimal('0.00')

@pytest.mark.django_db
def test_money_withdrawal_request_serializer_zero_amount():
    data = {
        'money_amount': '0.00',
        'status': 'pending',
    }
    serializer = MoneyWithdrawalRequestSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['money_amount'] == Decimal('0.00')

@pytest.mark.django_db
def test_gold_withdrawal_request_serializer_zero_amount():
    data = {
        'gold_amount': '0.00',
        'status': 'pending',
    }
    serializer = GoldWithdrawalRequestSerializer(data=data)
    assert serializer.is_valid()
    assert serializer.validated_data['gold_amount'] == Decimal('0.00')