from rest_framework.routers import DefaultRouter

from apps.gold_online_store.api.v1.gold.view import WalletAdminAPIView, GoldPriceAdminAPIView, WalletAPIView
from apps.gold_online_store.api.v1.payment.view import PaymentTransactionAdminAPIView, PaymentTransactionAPIView
from apps.gold_online_store.api.v1.transaction.view import GoldSaleTransactionAdminAPIView, \
    GoldPurchaseTransactionAdminAPIView, GoldSaleTransactionAPIView, GoldPurchaseTransactionAPIView
from apps.gold_online_store.api.v1.withdrawal_requests.view import MoneyWithdrawalRequestAdminAPIView, \
    GoldWithdrawalRequestAdminAPIView, MoneyWithdrawalRequestAPIView, GoldWithdrawalRequestAPIView

# Create a router for admin and user endpoints
router = DefaultRouter()

# Admin endpoints
router.register(
    r'admin/payment-transactions',
    PaymentTransactionAdminAPIView,
    basename='admin-payment-transaction'
)
router.register(
    r'admin/wallets',
    WalletAdminAPIView,
    basename='admin-wallet'
)
router.register(
    r'admin/gold-prices',
    GoldPriceAdminAPIView,
    basename='admin-gold-price'
)
router.register(
    r'admin/gold-sale-transactions',
    GoldSaleTransactionAdminAPIView,
    basename='admin-gold-sale-transaction'
)
router.register(
    r'admin/gold-purchase-transactions',
    GoldPurchaseTransactionAdminAPIView,
    basename='admin-gold-purchase-transaction'
)
router.register(
    r'admin/money-withdrawal-requests',
    MoneyWithdrawalRequestAdminAPIView,
    basename='admin-money-withdrawal-request'
)
router.register(
    r'admin/gold-withdrawal-requests',
    GoldWithdrawalRequestAdminAPIView,
    basename='admin-gold-withdrawal-request'
)

# User endpoints
router.register(
    r'payment-transactions',
    PaymentTransactionAPIView,
    basename='payment-transaction'
)
router.register(
    r'wallets',
    WalletAPIView,
    basename='wallet'
)
router.register(
    r'gold-sale-transactions',
    GoldSaleTransactionAPIView,
    basename='gold-sale-transaction'
)
router.register(
    r'gold-purchase-transactions',
    GoldPurchaseTransactionAPIView,
    basename='gold-purchase-transaction'
)
router.register(
    r'money-withdrawal-requests',
    MoneyWithdrawalRequestAPIView,
    basename='money-withdrawal-request'
)
router.register(
    r'gold-withdrawal-requests',
    GoldWithdrawalRequestAPIView,
    basename='gold-withdrawal-request'
)

# URL patterns
urlpatterns = router.urls
