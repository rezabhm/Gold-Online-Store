import pytest
from django.utils import timezone
from django.db import models
from decimal import Decimal
import factory
from faker import Faker
from apps.core.models import CustomUser
from apps.gold_online_store.models.gold import Wallet, GoldPrice
from apps.gold_online_store.models.payment import PaymentTransaction
from apps.gold_online_store.models.transaction import GoldSaleTransaction, GoldPurchaseTransaction
from apps.gold_online_store.models.withdrawal_requests import MoneyWithdrawalRequest, GoldWithdrawalRequest

# Factory setup for test data
faker = Faker()

class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.LazyAttribute(lambda _: faker.user_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    password = factory.PostGenerationMethodCall('set_password', 'password123')

class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    user = factory.SubFactory(CustomUserFactory)
    money_stock = Decimal('1000.00')
    gold_stock = Decimal('10.0000')

class GoldPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldPrice

    date = factory.LazyAttribute(lambda _: timezone.now())
    sale_price = Decimal('2500000.00')
    price_difference = Decimal('10000.00')
    total_gold_stock = Decimal('1000.0000')
    stock_status = True
    active = True

class PaymentTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentTransaction

    user = factory.SubFactory(CustomUserFactory)
    payment_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('500.00')
    status = 'PENDING'

class GoldSaleTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldSaleTransaction

    user = factory.SubFactory(CustomUserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('500.00')
    gold_amount = Decimal('10.0000')
    gold_price = factory.SubFactory(GoldPriceFactory)
    status = 'WAITING'

class GoldPurchaseTransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldPurchaseTransaction

    user = factory.SubFactory(CustomUserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('500.00')
    gold_amount = Decimal('10.0000')
    gold_price = factory.SubFactory(GoldPriceFactory)
    status = 'WAITING'

class MoneyWithdrawalRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MoneyWithdrawalRequest

    user = factory.SubFactory(CustomUserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    money_amount = Decimal('200.00')
    status = 'WAITING'

class GoldWithdrawalRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoldWithdrawalRequest

    user = factory.SubFactory(CustomUserFactory)
    create_date = factory.LazyAttribute(lambda _: timezone.now())
    gold_amount = Decimal('5.0000')
    status = 'WAITING'

# Wallet Model Tests
@pytest.mark.django_db
def test_wallet_model_create():
    wallet = WalletFactory()
    assert Wallet.objects.filter(user=wallet.user).exists()
    assert wallet.money_stock == Decimal('1000.00')
    assert wallet.gold_stock == Decimal('10.0000')
    assert wallet.user.username is not None
    assert str(wallet) == f"Wallet of {wallet.user.username}"

@pytest.mark.django_db
def test_wallet_model_total_value_with_gold_price():
    wallet = WalletFactory(money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
    gold_price = GoldPriceFactory(sale_price=Decimal('2500000.00'), active=True)
    total_value = wallet.total_value
    expected_value = Decimal('1000.00') + (Decimal('10.0000') * Decimal('2500000.00'))
    assert total_value == expected_value

@pytest.mark.django_db
def test_wallet_model_total_value_no_gold_price():
    wallet = WalletFactory(money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
    total_value = wallet.total_value
    assert total_value == Decimal('1000.00')

@pytest.mark.django_db
def test_wallet_model_negative_money_stock():
    with pytest.raises(models.ValidationError, match='Money amount cannot be negative'):
        WalletFactory(money_stock=Decimal('-1000.00')).full_clean()

@pytest.mark.django_db
def test_wallet_model_negative_gold_stock():
    with pytest.raises(models.ValidationError, match='Gold amount cannot be negative'):
        WalletFactory(gold_stock=Decimal('-10.0000')).full_clean()

@pytest.mark.django_db
def test_wallet_model_one_to_one_user():
    user = CustomUserFactory()
    WalletFactory(user=user)
    with pytest.raises(models.IntegrityError):
        WalletFactory(user=user)  # Should fail due to OneToOne constraint

# GoldPrice Model Tests
@pytest.mark.django_db
def test_gold_price_model_create():
    gold_price = GoldPriceFactory()
    assert GoldPrice.objects.filter(id=gold_price.id).exists()
    assert gold_price.sale_price == Decimal('2500000.00')
    assert gold_price.price_difference == Decimal('10000.00')
    assert gold_price.total_gold_stock == Decimal('1000.0000')
    assert gold_price.stock_status is True
    assert gold_price.active is True
    assert str(gold_price).startswith("Gold Price on")

@pytest.mark.django_db
def test_gold_price_model_active_unique():
    GoldPriceFactory(active=True)
    gold_price = GoldPriceFactory(active=True)
    assert GoldPrice.objects.filter(active=True).count() == 1
    assert GoldPrice.objects.get(id=gold_price.id).active is True

@pytest.mark.django_db
def test_gold_price_model_negative_sale_price():
    with pytest.raises(models.ValidationError, match='Sale price cannot be negative'):
        GoldPriceFactory(sale_price=Decimal('-2500000.00')).full_clean()

@pytest.mark.django_db
def test_gold_price_model_negative_price_difference():
    with pytest.raises(models.ValidationError, match='Price difference cannot be negative'):
        GoldPriceFactory(price_difference=Decimal('-10000.00')).full_clean()

@pytest.mark.django_db
def test_gold_price_model_negative_total_gold_stock():
    with pytest.raises(models.ValidationError, match='Total gold stock cannot be negative'):
        GoldPriceFactory(total_gold_stock=Decimal('-1000.0000')).full_clean()

@pytest.mark.django_db
def test_gold_price_model_index_on_date_and_active():
    gold_price = GoldPriceFactory()
    assert 'date' in [index.fields[0] for index in GoldPrice._meta.indexes]
    assert 'active' in [index.fields[0] for index in GoldPrice._meta.indexes]

# PaymentTransaction Model Tests
@pytest.mark.django_db
def test_payment_transaction_model_create():
    payment = PaymentTransactionFactory()
    assert PaymentTransaction.objects.filter(id=payment.id).exists()
    assert payment.money_amount == Decimal('500.00')
    assert payment.status == 'PENDING'
    assert payment.payment_date is not None
    assert str(payment).startswith(f"Payment {payment.pk}")

@pytest.mark.django_db
def test_payment_transaction_model_negative_money_amount():
    with pytest.raises(models.ValidationError, match='Money amount cannot be negative'):
        PaymentTransactionFactory(money_amount=Decimal('-500.00')).full_clean()

@pytest.mark.django_db
def test_payment_transaction_model_invalid_status():
    with pytest.raises(models.ValidationError, match='is not a valid choice'):
        PaymentTransactionFactory(status='INVALID').full_clean()

@pytest.mark.django_db
def test_payment_transaction_model_index_on_payment_date_and_status():
    payment = PaymentTransactionFactory()
    assert 'payment_date' in [index.fields[0] for index in PaymentTransaction._meta.indexes]
    assert 'status' in [index.fields[0] for index in PaymentTransaction._meta.indexes]

# GoldSaleTransaction Model Tests
@pytest.mark.django_db
def test_gold_sale_transaction_model_create():
    transaction = GoldSaleTransactionFactory()
    assert GoldSaleTransaction.objects.filter(id=transaction.id).exists()
    assert transaction.money_amount == Decimal('500.00')
    assert transaction.gold_amount == Decimal('10.0000')
    assert transaction.status == 'WAITING'
    assert transaction.create_date is not None
    assert transaction.gold_price is not None
    assert str(transaction).startswith(f"GoldSaleTransaction {transaction.id}")

@pytest.mark.django_db
def test_gold_sale_transaction_model_negative_money_amount():
    with pytest.raises(models.ValidationError, match='Money amount cannot be negative'):
        GoldSaleTransactionFactory(money_amount=Decimal('-500.00')).full_clean()

@pytest.mark.django_db
def test_gold_sale_transaction_model_negative_gold_amount():
    with pytest.raises(models.ValidationError, match='Gold amount cannot be negative'):
        GoldSaleTransactionFactory(gold_amount=Decimal('-10.0000')).full_clean()

@pytest.mark.django_db
def test_gold_sale_transaction_model_invalid_status():
    with pytest.raises(models.ValidationError, match='is not a valid choice'):
        GoldSaleTransactionFactory(status='INVALID').full_clean()

@pytest.mark.django_db
def test_gold_sale_transaction_model_index_on_create_date_and_status():
    transaction = GoldSaleTransactionFactory()
    assert 'create_date' in [index.fields[0] for index in GoldSaleTransaction._meta.indexes]
    assert 'status' in [index.fields[0] for index in GoldSaleTransaction._meta.indexes]

# GoldPurchaseTransaction Model Tests
@pytest.mark.django_db
def test_gold_purchase_transaction_model_create():
    transaction = GoldPurchaseTransactionFactory()
    assert GoldPurchaseTransaction.objects.filter(id=transaction.id).exists()
    assert transaction.money_amount == Decimal('500.00')
    assert transaction.gold_amount == Decimal('10.0000')
    assert transaction.status == 'WAITING'
    assert transaction.create_date is not None
    assert transaction.gold_price is not None
    assert str(transaction).startswith(f"GoldPurchaseTransaction {transaction.id}")

@pytest.mark.django_db
def test_gold_purchase_transaction_model_negative_money_amount():
    with pytest.raises(models.ValidationError, match='Money amount cannot be negative'):
        GoldPurchaseTransactionFactory(money_amount=Decimal('-500.00')).full_clean()

@pytest.mark.django_db
def test_gold_purchase_transaction_model_negative_gold_amount():
    with pytest.raises(models.ValidationError, match='Gold amount cannot be negative'):
        GoldPurchaseTransactionFactory(gold_amount=Decimal('-10.0000')).full_clean()

@pytest.mark.django_db
def test_gold_purchase_transaction_model_invalid_status():
    with pytest.raises(models.ValidationError, match='is not a valid choice'):
        GoldPurchaseTransactionFactory(status='INVALID').full_clean()

@pytest.mark.django_db
def test_gold_purchase_transaction_model_index_on_create_date_and_status():
    transaction = GoldPurchaseTransactionFactory()
    assert 'create_date' in [index.fields[0] for index in GoldPurchaseTransaction._meta.indexes]
    assert 'status' in [index.fields[0] for index in GoldPurchaseTransaction._meta.indexes]

# MoneyWithdrawalRequest Model Tests
@pytest.mark.django_db
def test_money_withdrawal_request_model_create():
    request = MoneyWithdrawalRequestFactory()
    assert MoneyWithdrawalRequest.objects.filter(id=request.id).exists()
    assert request.money_amount == Decimal('200.00')
    assert request.status == 'WAITING'
    assert request.create_date is not None
    assert str(request).startswith(f"MoneyWithdrawalRequest {request.id}")

@pytest.mark.django_db
def test_money_withdrawal_request_model_negative_money_amount():
    with pytest.raises(models.ValidationError, match='Money amount cannot be negative'):
        MoneyWithdrawalRequestFactory(money_amount=Decimal('-200.00')).full_clean()

@pytest.mark.django_db
def test_money_withdrawal_request_model_invalid_status():
    with pytest.raises(models.ValidationError, match='is not a valid choice'):
        MoneyWithdrawalRequestFactory(status='INVALID').full_clean()

@pytest.mark.django_db
def test_money_withdrawal_request_model_index_on_create_date_and_status():
    request = MoneyWithdrawalRequestFactory()
    assert 'create_date' in [index.fields[0] for index in MoneyWithdrawalRequest._meta.indexes]
    assert 'status' in [index.fields[0] for index in MoneyWithdrawalRequest._meta.indexes]

# GoldWithdrawalRequest Model Tests
@pytest.mark.django_db
def test_gold_withdrawal_request_model_create():
    request = GoldWithdrawalRequestFactory()
    assert GoldWithdrawalRequest.objects.filter(id=request.id).exists()
    assert request.gold_amount == Decimal('5.0000')
    assert request.status == 'WAITING'
    assert request.create_date is not None
    assert str(request).startswith(f"GoldWithdrawalRequest {request.id}")

@pytest.mark.django_db
def test_gold_withdrawal_request_model_negative_gold_amount():
    with pytest.raises(models.ValidationError, match='Gold amount cannot be negative'):
        GoldWithdrawalRequestFactory(gold_amount=Decimal('-5.0000')).full_clean()

@pytest.mark.django_db
def test_gold_withdrawal_request_model_invalid_status():
    with pytest.raises(models.ValidationError, match='is not a valid choice'):
        GoldWithdrawalRequestFactory(status='INVALID').full_clean()

@pytest.mark.django_db
def test_gold_withdrawal_request_model_index_on_create_date_and_status():
    request = GoldWithdrawalRequestFactory()
    assert 'create_date' in [index.fields[0] for index in GoldWithdrawalRequest._meta.indexes]
    assert 'status' in [index.fields[0] for index in GoldWithdrawalRequest._meta.indexes]

# Edge Case Tests
@pytest.mark.django_db
def test_wallet_model_zero_values():
    wallet = WalletFactory(money_stock=Decimal('0.00'), gold_stock=Decimal('0.0000'))
    wallet.full_clean()
    assert wallet.money_stock == Decimal('0.00')
    assert wallet.gold_stock == Decimal('0.0000')
    assert wallet.total_value == Decimal('0.00')

@pytest.mark.django_db
def test_gold_price_model_zero_values():
    gold_price = GoldPriceFactory(sale_price=Decimal('0.00'), price_difference=Decimal('0.00'), total_gold_stock=Decimal('0.0000'))
    gold_price.full_clean()
    assert gold_price.sale_price == Decimal('0.00')
    assert gold_price.price_difference == Decimal('0.00')
    assert gold_price.total_gold_stock == Decimal('0.0000')

@pytest.mark.django_db
def test_payment_transaction_model_zero_money_amount():
    payment = PaymentTransactionFactory(money_amount=Decimal('0.00'))
    payment.full_clean()
    assert payment.money_amount == Decimal('0.00')

@pytest.mark.django_db
def test_gold_sale_transaction_model_zero_amounts():
    transaction = GoldSaleTransactionFactory(money_amount=Decimal('0.00'), gold_amount=Decimal('0.0000'))
    transaction.full_clean()
    assert transaction.money_amount == Decimal('0.00')
    assert transaction.gold_amount == Decimal('0.0000')

@pytest.mark.django_db
def test_gold_purchase_transaction_model_zero_amounts():
    transaction = GoldPurchaseTransactionFactory(money_amount=Decimal('0.00'), gold_amount=Decimal('0.0000'))
    transaction.full_clean()
    assert transaction.money_amount == Decimal('0.00')
    assert transaction.gold_amount == Decimal('0.0000')

@pytest.mark.django_db
def test_money_withdrawal_request_model_zero_amount():
    request = MoneyWithdrawalRequestFactory(money_amount=Decimal('0.00'))
    request.full_clean()
    assert request.money_amount == Decimal('0.00')

@pytest.mark.django_db
def test_gold_withdrawal_request_model_zero_amount():
    request = GoldWithdrawalRequestFactory(gold_amount=Decimal('0.0000'))
    request.full_clean()
    assert request.gold_amount == Decimal('0.0000')

@pytest.mark.django_db
def test_wallet_model_max_digits():
    with pytest.raises(models.ValidationError, match='Ensure that there are no more than 15 digits in total'):
        WalletFactory(money_stock=Decimal('1000000000000000.00')).full_clean()

@pytest.mark.django_db
def test_gold_price_model_max_digits():
    with pytest.raises(models.ValidationError, match='Ensure that there are no more than 15 digits in total'):
        GoldPriceFactory(sale_price=Decimal('1000000000000000.00')).full_clean()

@pytest.mark.django_db
def test_payment_transaction_model_max_digits():
    with pytest.raises(models.ValidationError, match='Ensure that there are no more than 15 digits in total'):
        PaymentTransactionFactory(money_amount=Decimal('1000000000000000.00')).full_clean()

@pytest.mark.django_db
def test_gold_sale_transaction_model_max_digits():
    with pytest.raises(models.ValidationError, match='Ensure that there are no more than 15 digits in total'):
        GoldSaleTransactionFactory(money_amount=Decimal('1000000000000000.00')).full_clean()

@pytest.mark.django_db
def test_gold_purchase_transaction_model_max_digits():
    with pytest.raises(models.ValidationError, match='Ensure that there are no more than 15 digits in total'):
        GoldPurchaseTransactionFactory(money_amount=Decimal('1000000000000000.00')).full_clean()

@pytest.mark.django_db
def test_money_withdrawal_request_model_max_digits():
    with pytest.raises(models.ValidationError, match='Ensure that there are no more than 15 digits in total'):
        MoneyWithdrawalRequestFactory(money_amount=Decimal('1000000000000000.00')).full_clean()

@pytest.mark.django_db
def test_gold_withdrawal_request_model_max_digits():
    with pytest.raises(models.ValidationError, match='Ensure that there are no more than 15 digits in total'):
        GoldWithdrawalRequestFactory(gold_amount=Decimal('1000000000000000.0000')).full_clean()