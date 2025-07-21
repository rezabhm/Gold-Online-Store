from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.models import CustomUser
from apps.gold_online_store.models.gold import Wallet, GoldPrice
from apps.gold_online_store.models.payment import PaymentTransaction
from apps.gold_online_store.models.transaction import GoldSaleTransaction, GoldPurchaseTransaction
from apps.gold_online_store.models.withdrawal_requests import MoneyWithdrawalRequest, GoldWithdrawalRequest
from decimal import Decimal

class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        self.regular_user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='user123'
        )
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token
        self.user_token = RefreshToken.for_user(self.regular_user).access_token
        self.gold_price = GoldPrice.objects.create(
            date=timezone.now(),
            sale_price=Decimal('2500000.00'),
            price_difference=Decimal('10000.00'),
            total_gold_stock=Decimal('1000.0000'),
            stock_status=True,
            active=True
        )

    def authenticate_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

    def authenticate_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

    def clear_credentials(self):
        self.client.credentials()

# WalletAdminAPIView Tests
class WalletAdminAPIViewTests(BaseTestCase):
    def test_wallet_admin_list(self):
        self.authenticate_admin()
        Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        Wallet.objects.create(user=CustomUser.objects.create_user(username='user2', password='pass123'), money_stock=Decimal('2000.00'), gold_stock=Decimal('20.0000'))
        response = self.client.get(reverse('admin-wallet-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_wallet_admin_list_search(self):
        self.authenticate_admin()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.get(reverse('admin-wallet-list'), {'search': self.regular_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_wallet_admin_create(self):
        self.authenticate_admin()
        new_user = CustomUser.objects.create_user(username='newuser', password='pass123')
        data = {'user': new_user.id, 'money_stock': '1500.00', 'gold_stock': '15.0000'}
        response = self.client.post(reverse('admin-wallet-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Wallet.objects.filter(user=new_user, money_stock=Decimal('1500.00'), gold_stock=Decimal('15.0000')).exists())

    def test_wallet_admin_retrieve(self):
        self.authenticate_admin()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.get(reverse('admin-wallet-detail', kwargs={'pk': wallet.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], wallet.id)

    def test_wallet_admin_update(self):
        self.authenticate_admin()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        data = {'user': self.regular_user.id, 'money_stock': '2000.00', 'gold_stock': '20.0000'}
        response = self.client.put(reverse('admin-wallet-detail', kwargs={'pk': wallet.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallet.refresh_from_db()
        self.assertEqual(wallet.money_stock, Decimal('2000.00'))
        self.assertEqual(wallet.gold_stock, Decimal('20.0000'))

    def test_wallet_admin_partial_update(self):
        self.authenticate_admin()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        data = {'money_stock': '1500.00'}
        response = self.client.patch(reverse('admin-wallet-detail', kwargs={'pk': wallet.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallet.refresh_from_db()
        self.assertEqual(wallet.money_stock, Decimal('1500.00'))

    def test_wallet_admin_destroy(self):
        self.authenticate_admin()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.delete(reverse('admin-wallet-detail', kwargs={'pk': wallet.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Wallet.objects.filter(id=wallet.id).exists())

    def test_wallet_admin_unauthorized(self):
        self.authenticate_user()
        response = self.client.get(reverse('admin-wallet-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# WalletAPIView Tests
class WalletAPIViewTests(BaseTestCase):
    def test_wallet_user_list(self):
        self.authenticate_user()
        Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.get(reverse('wallet-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_wallet_user_create(self):
        self.authenticate_user()
        data = {'money_stock': '1000.00', 'gold_stock': '10.0000'}
        response = self.client.post(reverse('wallet-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Wallet.objects.filter(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000')).exists())

    def test_wallet_user_create_user_field_protected(self):
        self.authenticate_user()
        data = {'user': 999, 'money_stock': '1000.00', 'gold_stock': '10.0000'}
        response = self.client.post(reverse('wallet-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_wallet_user_retrieve(self):
        self.authenticate_user()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.get(reverse('wallet-detail', kwargs={'pk': wallet.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], wallet.id)

    def test_wallet_user_retrieve_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        wallet = Wallet.objects.create(user=other_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.get(reverse('wallet-detail', kwargs={'pk': wallet.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wallet_user_update(self):
        self.authenticate_user()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        data = {'money_stock': '2000.00', 'gold_stock': '20.0000'}
        response = self.client.put(reverse('wallet-detail', kwargs={'pk': wallet.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallet.refresh_from_db()
        self.assertEqual(wallet.money_stock, Decimal('2000.00'))
        self.assertEqual(wallet.gold_stock, Decimal('20.0000'))

    def test_wallet_user_update_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        wallet = Wallet.objects.create(user=other_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        data = {'money_stock': '2000.00', 'gold_stock': '20.0000'}
        response = self.client.put(reverse('wallet-detail', kwargs={'pk': wallet.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wallet_user_partial_update(self):
        self.authenticate_user()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        data = {'money_stock': '1500.00'}
        response = self.client.patch(reverse('wallet-detail', kwargs={'pk': wallet.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallet.refresh_from_db()
        self.assertEqual(wallet.money_stock, Decimal('1500.00'))

    def test_wallet_user_destroy(self):
        self.authenticate_user()
        wallet = Wallet.objects.create(user=self.regular_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.delete(reverse('wallet-detail', kwargs={'pk': wallet.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Wallet.objects.filter(id=wallet.id).exists())

    def test_wallet_user_destroy_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        wallet = Wallet.objects.create(user=other_user, money_stock=Decimal('1000.00'), gold_stock=Decimal('10.0000'))
        response = self.client.delete(reverse('wallet-detail', kwargs={'pk': wallet.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# GoldPriceAdminAPIView Tests
class GoldPriceAdminAPIViewTests(BaseTestCase):
    def test_gold_price_admin_list(self):
        self.authenticate_admin()
        GoldPrice.objects.create(date=timezone.now(), sale_price=Decimal('2500000.00'), price_difference=Decimal('10000.00'), total_gold_stock=Decimal('1000.0000'), stock_status=True, active=True)
        response = self.client.get(reverse('admin-gold-price-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_gold_price_admin_list_search(self):
        self.authenticate_admin()
        gold_price = GoldPrice.objects.create(date=timezone.now(), sale_price=Decimal('2500000.00'), price_difference=Decimal('10000.00'), total_gold_stock=Decimal('1000.0000'), stock_status=True, active=True)
        response = self.client.get(reverse('admin-gold-price-list'), {'search': str(gold_price.date.date())})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_gold_price_admin_create(self):
        self.authenticate_admin()
        data = {
            'date': timezone.now().isoformat(),
            'sale_price': '2600000.00',
            'price_difference': '15000.00',
            'total_gold_stock': '2000.0000',
            'stock_status': True,
            'active': True
        }
        response = self.client.post(reverse('admin-gold-price-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GoldPrice.objects.filter(sale_price=Decimal('2600000.00'), total_gold_stock=Decimal('2000.0000')).exists())

    def test_gold_price_admin_retrieve(self):
        self.authenticate_admin()
        gold_price = GoldPrice.objects.create(date=timezone.now(), sale_price=Decimal('2500000.00'), price_difference=Decimal('10000.00'), total_gold_stock=Decimal('1000.0000'), stock_status=True, active=True)
        response = self.client.get(reverse('admin-gold-price-detail', kwargs={'pk': gold_price.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], gold_price.id)

    def test_gold_price_admin_update(self):
        self.authenticate_admin()
        gold_price = GoldPrice.objects.create(date=timezone.now(), sale_price=Decimal('2500000.00'), price_difference=Decimal('10000.00'), total_gold_stock=Decimal('1000.0000'), stock_status=True, active=True)
        data = {
            'date': timezone.now().isoformat(),
            'sale_price': '2700000.00',
            'price_difference': '12000.00',
            'total_gold_stock': '1500.0000',
            'stock_status': True,
            'active': True
        }
        response = self.client.put(reverse('admin-gold-price-detail', kwargs={'pk': gold_price.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gold_price.refresh_from_db()
        self.assertEqual(gold_price.sale_price, Decimal('2700000.00'))
        self.assertEqual(gold_price.total_gold_stock, Decimal('1500.0000'))

    def test_gold_price_admin_partial_update(self):
        self.authenticate_admin()
        gold_price = GoldPrice.objects.create(date=timezone.now(), sale_price=Decimal('2500000.00'), price_difference=Decimal('10000.00'), total_gold_stock=Decimal('1000.0000'), stock_status=True, active=True)
        data = {'sale_price': '2600000.00'}
        response = self.client.patch(reverse('admin-gold-price-detail', kwargs={'pk': gold_price.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        gold_price.refresh_from_db()
        self.assertEqual(gold_price.sale_price, Decimal('2600000.00'))

    def test_gold_price_admin_destroy(self):
        self.authenticate_admin()
        gold_price = GoldPrice.objects.create(date=timezone.now(), sale_price=Decimal('2500000.00'), price_difference=Decimal('10000.00'), total_gold_stock=Decimal('1000.0000'), stock_status=True, active=True)
        response = self.client.delete(reverse('admin-gold-price-detail', kwargs={'pk': gold_price.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GoldPrice.objects.filter(id=gold_price.id).exists())

    def test_gold_price_admin_unauthorized(self):
        self.authenticate_user()
        response = self.client.get(reverse('admin-gold-price-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# PaymentTransactionAdminAPIView Tests
class PaymentTransactionAdminAPIViewTests(BaseTestCase):
    def test_payment_transaction_admin_list(self):
        self.authenticate_admin()
        PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.get(reverse('admin-payment-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_payment_transaction_admin_list_search(self):
        self.authenticate_admin()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.get(reverse('admin-payment-transaction-list'), {'search': self.regular_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_payment_transaction_admin_create(self):
        self.authenticate_admin()
        data = {'user': self.regular_user.id, 'money_amount': '600.00', 'status': 'PENDING'}
        response = self.client.post(reverse('admin-payment-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PaymentTransaction.objects.filter(user=self.regular_user, money_amount=Decimal('600.00')).exists())

    def test_payment_transaction_admin_retrieve(self):
        self.authenticate_admin()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.get(reverse('admin-payment-transaction-detail', kwargs={'pk': payment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], payment.id)

    def test_payment_transaction_admin_update(self):
        self.authenticate_admin()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        data = {'user': self.regular_user.id, 'money_amount': '700.00', 'status': 'SUCCESS'}
        response = self.client.put(reverse('admin-payment-transaction-detail', kwargs={'pk': payment.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        self.assertEqual(payment.money_amount, Decimal('700.00'))
        self.assertEqual(payment.status, 'SUCCESS')

    def test_payment_transaction_admin_partial_update(self):
        self.authenticate_admin()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        data = {'status': 'SUCCESS'}
        response = self.client.patch(reverse('admin-payment-transaction-detail', kwargs={'pk': payment.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        self.assertEqual(payment.status, 'SUCCESS')

    def test_payment_transaction_admin_destroy(self):
        self.authenticate_admin()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.delete(reverse('admin-payment-transaction-detail', kwargs={'pk': payment.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PaymentTransaction.objects.filter(id=payment.id).exists())

    def test_payment_transaction_admin_unauthorized(self):
        self.authenticate_user()
        response = self.client.get(reverse('admin-payment-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# PaymentTransactionAPIView Tests
class PaymentTransactionAPIViewTests(BaseTestCase):
    def test_payment_transaction_user_list(self):
        self.authenticate_user()
        PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.get(reverse('payment-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_payment_transaction_user_create(self):
        self.authenticate_user()
        data = {'money_amount': '600.00', 'status': 'PENDING'}
        response = self.client.post(reverse('payment-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PaymentTransaction.objects.filter(user=self.regular_user, money_amount=Decimal('600.00')).exists())

    def test_payment_transaction_user_create_user_field_protected(self):
        self.authenticate_user()
        data = {'user': 999, 'money_amount': '600.00', 'status': 'PENDING'}
        response = self.client.post(reverse('payment-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_payment_transaction_user_retrieve(self):
        self.authenticate_user()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.get(reverse('payment-transaction-detail', kwargs={'pk': payment.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], payment.id)

    def test_payment_transaction_user_retrieve_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        payment = PaymentTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.get(reverse('payment-transaction-detail', kwargs={'pk': payment.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_payment_transaction_user_update(self):
        self.authenticate_user()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        data = {'money_amount': '600.00', 'status': 'SUCCESS'}
        response = self.client.put(reverse('payment-transaction-detail', kwargs={'pk': payment.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        self.assertEqual(payment.money_amount, Decimal('600.00'))
        self.assertEqual(payment.status, 'SUCCESS')

    def test_payment_transaction_user_destroy(self):
        self.authenticate_user()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.delete(reverse('payment-transaction-detail', kwargs={'pk': payment.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PaymentTransaction.objects.filter(id=payment.id).exists())

    def test_payment_transaction_user_destroy_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        payment = PaymentTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), status='PENDING')
        response = self.client.delete(reverse('payment-transaction-detail', kwargs={'pk': payment.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# GoldSaleTransactionAdminAPIView Tests
class GoldSaleTransactionAdminAPIViewTests(BaseTestCase):
    def test_gold_sale_transaction_admin_list(self):
        self.authenticate_admin()
        GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('admin-gold-sale-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_gold_sale_transaction_admin_list_search(self):
        self.authenticate_admin()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('admin-gold-sale-transaction-list'), {'search': self.regular_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_gold_sale_transaction_admin_create(self):
        self.authenticate_admin()
        data = {
            'user': self.regular_user.id,
            'money_amount': '600.00',
            'gold_amount': '10.0000',
            'gold_price': self.gold_price.id,
            'status': 'WAITING'
        }
        response = self.client.post(reverse('admin-gold-sale-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GoldSaleTransaction.objects.filter(user=self.regular_user, money_amount=Decimal('600.00'), gold_amount=Decimal('10.0000')).exists())

    def test_gold_sale_transaction_admin_retrieve(self):
        self.authenticate_admin()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('admin-gold-sale-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], transaction.id)

    def test_gold_sale_transaction_admin_update(self):
        self.authenticate_admin()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {
            'user': self.regular_user.id,
            'money_amount': '700.00',
            'gold_amount': '15.0000',
            'gold_price': self.gold_price.id,
            'status': 'ACCEPTED'
        }
        response = self.client.put(reverse('admin-gold-sale-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.money_amount, Decimal('700.00'))
        self.assertEqual(transaction.gold_amount, Decimal('15.0000'))
        self.assertEqual(transaction.status, 'ACCEPTED')

    def test_gold_sale_transaction_admin_partial_update(self):
        self.authenticate_admin()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'status': 'ACCEPTED'}
        response = self.client.patch(reverse('admin-gold-sale-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'ACCEPTED')

    def test_gold_sale_transaction_admin_destroy(self):
        self.authenticate_admin()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.delete(reverse('admin-gold-sale-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GoldSaleTransaction.objects.filter(id=transaction.id).exists())

    def test_gold_sale_transaction_admin_unauthorized(self):
        self.authenticate_user()
        response = self.client.get(reverse('admin-gold-sale-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# GoldSaleTransactionAPIView Tests
class GoldSaleTransactionAPIViewTests(BaseTestCase):
    def test_gold_sale_transaction_user_list(self):
        self.authenticate_user()
        GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('gold-sale-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_gold_sale_transaction_user_create(self):
        self.authenticate_user()
        data = {'money_amount': '600.00', 'gold_amount': '10.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.post(reverse('gold-sale-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GoldSaleTransaction.objects.filter(user=self.regular_user, money_amount=Decimal('600.00'), gold_amount=Decimal('10.0000')).exists())

    def test_gold_sale_transaction_user_create_user_field_protected(self):
        self.authenticate_user()
        data = {'user': 999, 'money_amount': '600.00', 'gold_amount': '10.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.post(reverse('gold-sale-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_gold_sale_transaction_user_retrieve(self):
        self.authenticate_user()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('gold-sale-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], transaction.id)

    def test_gold_sale_transaction_user_retrieve_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        transaction = GoldSaleTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('gold-sale-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gold_sale_transaction_user_update(self):
        self.authenticate_user()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'money_amount': '700.00', 'gold_amount': '15.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.put(reverse('gold-sale-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.money_amount, Decimal('700.00'))
        self.assertEqual(transaction.gold_amount, Decimal('15.0000'))

    def test_gold_sale_transaction_user_update_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        transaction = GoldSaleTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'money_amount': '700.00', 'gold_amount': '15.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.put(reverse('gold-sale-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gold_sale_transaction_user_partial_update(self):
        self.authenticate_user()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'gold_amount': '15.0000'}
        response = self.client.patch(reverse('gold-sale-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.gold_amount, Decimal('15.0000'))

    def test_gold_sale_transaction_user_destroy(self):
        self.authenticate_user()
        transaction = GoldSaleTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.delete(reverse('gold-sale-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GoldSaleTransaction.objects.filter(id=transaction.id).exists())

    def test_gold_sale_transaction_user_destroy_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        transaction = GoldSaleTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.delete(reverse('gold-sale-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# GoldPurchaseTransactionAdminAPIView Tests
class GoldPurchaseTransactionAdminAPIViewTests(BaseTestCase):
    def test_gold_purchase_transaction_admin_list(self):
        self.authenticate_admin()
        GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('admin-gold-purchase-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_gold_purchase_transaction_admin_list_search(self):
        self.authenticate_admin()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('admin-gold-purchase-transaction-list'), {'search': self.regular_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_gold_purchase_transaction_admin_create(self):
        self.authenticate_admin()
        data = {
            'user': self.regular_user.id,
            'money_amount': '600.00',
            'gold_amount': '10.0000',
            'gold_price': self.gold_price.id,
            'status': 'WAITING'
        }
        response = self.client.post(reverse('admin-gold-purchase-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GoldPurchaseTransaction.objects.filter(user=self.regular_user, money_amount=Decimal('600.00'), gold_amount=Decimal('10.0000')).exists())

    def test_gold_purchase_transaction_admin_retrieve(self):
        self.authenticate_admin()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('admin-gold-purchase-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], transaction.id)

    def test_gold_purchase_transaction_admin_update(self):
        self.authenticate_admin()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {
            'user': self.regular_user.id,
            'money_amount': '700.00',
            'gold_amount': '15.0000',
            'gold_price': self.gold_price.id,
            'status': 'ACCEPTED'
        }
        response = self.client.put(reverse('admin-gold-purchase-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.money_amount, Decimal('700.00'))
        self.assertEqual(transaction.gold_amount, Decimal('15.0000'))
        self.assertEqual(transaction.status, 'ACCEPTED')

    def test_gold_purchase_transaction_admin_partial_update(self):
        self.authenticate_admin()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'status': 'ACCEPTED'}
        response = self.client.patch(reverse('admin-gold-purchase-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'ACCEPTED')

    def test_gold_purchase_transaction_admin_destroy(self):
        self.authenticate_admin()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.delete(reverse('admin-gold-purchase-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GoldPurchaseTransaction.objects.filter(id=transaction.id).exists())

    def test_gold_purchase_transaction_admin_unauthorized(self):
        self.authenticate_user()
        response = self.client.get(reverse('admin-gold-purchase-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# GoldPurchaseTransactionAPIView Tests
class GoldPurchaseTransactionAPIViewTests(BaseTestCase):
    def test_gold_purchase_transaction_user_list(self):
        self.authenticate_user()
        GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('gold-purchase-transaction-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_gold_purchase_transaction_user_create(self):
        self.authenticate_user()
        data = {'money_amount': '600.00', 'gold_amount': '10.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.post(reverse('gold-purchase-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GoldPurchaseTransaction.objects.filter(user=self.regular_user, money_amount=Decimal('600.00'), gold_amount=Decimal('10.0000')).exists())

    def test_gold_purchase_transaction_user_create_user_field_protected(self):
        self.authenticate_user()
        data = {'user': 999, 'money_amount': '600.00', 'gold_amount': '10.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.post(reverse('gold-purchase-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_gold_purchase_transaction_user_retrieve(self):
        self.authenticate_user()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('gold-purchase-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], transaction.id)

    def test_gold_purchase_transaction_user_retrieve_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        transaction = GoldPurchaseTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.get(reverse('gold-purchase-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gold_purchase_transaction_user_update(self):
        self.authenticate_user()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'money_amount': '700.00', 'gold_amount': '15.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.put(reverse('gold-purchase-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.money_amount, Decimal('700.00'))
        self.assertEqual(transaction.gold_amount, Decimal('15.0000'))

    def test_gold_purchase_transaction_user_update_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        transaction = GoldPurchaseTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'money_amount': '700.00', 'gold_amount': '15.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.put(reverse('gold-purchase-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gold_purchase_transaction_user_partial_update(self):
        self.authenticate_user()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        data = {'gold_amount': '15.0000'}
        response = self.client.patch(reverse('gold-purchase-transaction-detail', kwargs={'pk': transaction.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.gold_amount, Decimal('15.0000'))

    def test_gold_purchase_transaction_user_destroy(self):
        self.authenticate_user()
        transaction = GoldPurchaseTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.delete(reverse('gold-purchase-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GoldPurchaseTransaction.objects.filter(id=transaction.id).exists())

    def test_gold_purchase_transaction_user_destroy_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        transaction = GoldPurchaseTransaction.objects.create(user=other_user, money_amount=Decimal('500.00'), gold_amount=Decimal('10.0000'), gold_price=self.gold_price, status='WAITING')
        response = self.client.delete(reverse('gold-purchase-transaction-detail', kwargs={'pk': transaction.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# MoneyWithdrawalRequestAdminAPIView Tests
class MoneyWithdrawalRequestAdminAPIViewTests(BaseTestCase):
    def test_money_withdrawal_request_admin_list(self):
        self.authenticate_admin()
        MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.get(reverse('admin-money-withdrawal-request-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_money_withdrawal_request_admin_list_search(self):
        self.authenticate_admin()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.get(reverse('admin-money-withdrawal-request-list'), {'search': self.regular_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_money_withdrawal_request_admin_create(self):
        self.authenticate_admin()
        data = {'user': self.regular_user.id, 'money_amount': '300.00', 'status': 'WAITING'}
        response = self.client.post(reverse('admin-money-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MoneyWithdrawalRequest.objects.filter(user=self.regular_user, money_amount=Decimal('300.00')).exists())

    def test_money_withdrawal_request_admin_retrieve(self):
        self.authenticate_admin()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.get(reverse('admin-money-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], request.id)

    def test_money_withdrawal_request_admin_update(self):
        self.authenticate_admin()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        data = {'user': self.regular_user.id, 'money_amount': '400.00', 'status': 'ACCEPTED'}
        response = self.client.put(reverse('admin-money-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.money_amount, Decimal('400.00'))
        self.assertEqual(request.status, 'ACCEPTED')

    def test_money_withdrawal_request_admin_partial_update(self):
        self.authenticate_admin()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        data = {'status': 'ACCEPTED'}
        response = self.client.patch(reverse('admin-money-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.status, 'ACCEPTED')

    def test_money_withdrawal_request_admin_destroy(self):
        self.authenticate_admin()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.delete(reverse('admin-money-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MoneyWithdrawalRequest.objects.filter(id=request.id).exists())

    def test_money_withdrawal_request_admin_unauthorized(self):
        self.authenticate_user()
        response = self.client.get(reverse('admin-money-withdrawal-request-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# MoneyWithdrawalRequestAPIView Tests
class MoneyWithdrawalRequestAPIViewTests(BaseTestCase):
    def test_money_withdrawal_request_user_list(self):
        self.authenticate_user()
        MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.get(reverse('money-withdrawal-request-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_money_withdrawal_request_user_create(self):
        self.authenticate_user()
        data = {'money_amount': '300.00', 'status': 'WAITING'}
        response = self.client.post(reverse('money-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MoneyWithdrawalRequest.objects.filter(user=self.regular_user, money_amount=Decimal('300.00')).exists())

    def test_money_withdrawal_request_user_create_user_field_protected(self):
        self.authenticate_user()
        data = {'user': 999, 'money_amount': '300.00', 'status': 'WAITING'}
        response = self.client.post(reverse('money-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_money_withdrawal_request_user_retrieve(self):
        self.authenticate_user()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.get(reverse('money-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], request.id)

    def test_money_withdrawal_request_user_retrieve_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        request = MoneyWithdrawalRequest.objects.create(user=other_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.get(reverse('money-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_money_withdrawal_request_user_update(self):
        self.authenticate_user()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        data = {'money_amount': '400.00', 'status': 'WAITING'}
        response = self.client.put(reverse('money-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.money_amount, Decimal('400.00'))

    def test_money_withdrawal_request_user_update_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        request = MoneyWithdrawalRequest.objects.create(user=other_user, money_amount=Decimal('200.00'), status='WAITING')
        data = {'money_amount': '400.00', 'status': 'WAITING'}
        response = self.client.put(reverse('money-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_money_withdrawal_request_user_partial_update(self):
        self.authenticate_user()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        data = {'money_amount': '300.00'}
        response = self.client.patch(reverse('money-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.money_amount, Decimal('300.00'))

    def test_money_withdrawal_request_user_destroy(self):
        self.authenticate_user()
        request = MoneyWithdrawalRequest.objects.create(user=self.regular_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.delete(reverse('money-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MoneyWithdrawalRequest.objects.filter(id=request.id).exists())

    def test_money_withdrawal_request_user_destroy_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        request = MoneyWithdrawalRequest.objects.create(user=other_user, money_amount=Decimal('200.00'), status='WAITING')
        response = self.client.delete(reverse('money-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# GoldWithdrawalRequestAdminAPIView Tests
class GoldWithdrawalRequestAdminAPIViewTests(BaseTestCase):
    def test_gold_withdrawal_request_admin_list(self):
        self.authenticate_admin()
        GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.get(reverse('admin-gold-withdrawal-request-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_gold_withdrawal_request_admin_list_search(self):
        self.authenticate_admin()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.get(reverse('admin-gold-withdrawal-request-list'), {'search': self.regular_user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_gold_withdrawal_request_admin_create(self):
        self.authenticate_admin()
        data = {'user': self.regular_user.id, 'gold_amount': '10.0000', 'status': 'WAITING'}
        response = self.client.post(reverse('admin-gold-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GoldWithdrawalRequest.objects.filter(user=self.regular_user, gold_amount=Decimal('10.0000')).exists())

    def test_gold_withdrawal_request_admin_retrieve(self):
        self.authenticate_admin()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.get(reverse('admin-gold-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], request.id)

    def test_gold_withdrawal_request_admin_update(self):
        self.authenticate_admin()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        data = {'user': self.regular_user.id, 'gold_amount': '15.0000', 'status': 'ACCEPTED'}
        response = self.client.put(reverse('admin-gold-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.gold_amount, Decimal('15.0000'))
        self.assertEqual(request.status, 'ACCEPTED')

    def test_gold_withdrawal_request_admin_partial_update(self):
        self.authenticate_admin()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        data = {'status': 'ACCEPTED'}
        response = self.client.patch(reverse('admin-gold-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.status, 'ACCEPTED')

    def test_gold_withdrawal_request_admin_destroy(self):
        self.authenticate_admin()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.delete(reverse('admin-gold-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GoldWithdrawalRequest.objects.filter(id=request.id).exists())

    def test_gold_withdrawal_request_admin_unauthorized(self):
        self.authenticate_user()
        response = self.client.get(reverse('admin-gold-withdrawal-request-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# GoldWithdrawalRequestAPIView Tests
class GoldWithdrawalRequestAPIViewTests(BaseTestCase):
    def test_gold_withdrawal_request_user_list(self):
        self.authenticate_user()
        GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.get(reverse('gold-withdrawal-request-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user']['username'], self.regular_user.username)

    def test_gold_withdrawal_request_user_create(self):
        self.authenticate_user()
        data = {'gold_amount': '10.0000', 'status': 'WAITING'}
        response = self.client.post(reverse('gold-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(GoldWithdrawalRequest.objects.filter(user=self.regular_user, gold_amount=Decimal('10.0000')).exists())

    def test_gold_withdrawal_request_user_create_user_field_protected(self):
        self.authenticate_user()
        data = {'user': 999, 'gold_amount': '10.0000', 'status': 'WAITING'}
        response = self.client.post(reverse('gold-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_gold_withdrawal_request_user_retrieve(self):
        self.authenticate_user()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.get(reverse('gold-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], request.id)

    def test_gold_withdrawal_request_user_retrieve_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        request = GoldWithdrawalRequest.objects.create(user=other_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.get(reverse('gold-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gold_withdrawal_request_user_update(self):
        self.authenticate_user()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        data = {'gold_amount': '10.0000', 'status': 'WAITING'}
        response = self.client.put(reverse('gold-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.gold_amount, Decimal('10.0000'))

    def test_gold_withdrawal_request_user_update_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        request = GoldWithdrawalRequest.objects.create(user=other_user, gold_amount=Decimal('5.0000'), status='WAITING')
        data = {'gold_amount': '10.0000', 'status': 'WAITING'}
        response = self.client.put(reverse('gold-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_gold_withdrawal_request_user_partial_update(self):
        self.authenticate_user()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        data = {'gold_amount': '10.0000'}
        response = self.client.patch(reverse('gold-withdrawal-request-detail', kwargs={'pk': request.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        request.refresh_from_db()
        self.assertEqual(request.gold_amount, Decimal('10.0000'))

    def test_gold_withdrawal_request_user_destroy(self):
        self.authenticate_user()
        request = GoldWithdrawalRequest.objects.create(user=self.regular_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.delete(reverse('gold-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(GoldWithdrawalRequest.objects.filter(id=request.id).exists())

    def test_gold_withdrawal_request_user_destroy_unauthorized(self):
        self.authenticate_user()
        other_user = CustomUser.objects.create_user(username='otheruser', password='pass123')
        request = GoldWithdrawalRequest.objects.create(user=other_user, gold_amount=Decimal('5.0000'), status='WAITING')
        response = self.client.delete(reverse('gold-withdrawal-request-detail', kwargs={'pk': request.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# Edge Case Tests
class EdgeCaseTests(BaseTestCase):
    def test_wallet_admin_create_invalid_data(self):
        self.authenticate_admin()
        data = {'user': 999, 'money_stock': 'invalid'}
        response = self.client.post(reverse('admin-wallet-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('money_stock', response.data)

    def test_gold_price_admin_create_invalid_date(self):
        self.authenticate_admin()
        data = {'date': 'invalid-date', 'sale_price': '2500000.00', 'price_difference': '10000.00', 'total_gold_stock': '1000.0000'}
        response = self.client.post(reverse('admin-gold-price-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date', response.data)

    def test_payment_transaction_user_update_user_field(self):
        self.authenticate_user()
        payment = PaymentTransaction.objects.create(user=self.regular_user, money_amount=Decimal('500.00'), status='PENDING')
        data = {'user': 999, 'money_amount': '600.00', 'status': 'SUCCESS'}
        response = self.client.put(reverse('payment-transaction-detail', kwargs={'pk': payment.id}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('user', response.data)

    def test_gold_sale_transaction_negative_amount(self):
        self.authenticate_admin()
        data = {'user': self.regular_user.id, 'money_amount': '-500.00', 'gold_amount': '10.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.post(reverse('admin-gold-sale-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('money_amount', response.data)

    def test_gold_purchase_transaction_negative_amount(self):
        self.authenticate_admin()
        data = {'user': self.regular_user.id, 'money_amount': '500.00', 'gold_amount': '-10.0000', 'gold_price': self.gold_price.id, 'status': 'WAITING'}
        response = self.client.post(reverse('admin-gold-purchase-transaction-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gold_amount', response.data)

    def test_money_withdrawal_request_negative_amount(self):
        self.authenticate_admin()
        data = {'user': self.regular_user.id, 'money_amount': '-200.00', 'status': 'WAITING'}
        response = self.client.post(reverse('admin-money-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('money_amount', response.data)

    def test_gold_withdrawal_request_negative_amount(self):
        self.authenticate_user()
        data = {'gold_amount': '-5.0000', 'status': 'WAITING'}
        response = self.client.post(reverse('gold-withdrawal-request-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('gold_amount', response.data)