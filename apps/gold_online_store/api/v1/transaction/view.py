from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.gold_online_store.models.transaction import GoldSaleTransaction, GoldPurchaseTransaction
from apps.gold_online_store.serializers.transaction import GoldSaleTransactionSerializer, GoldPurchaseTransactionSerializer
from apps.gold_online_store.api.v1.transaction.swagger_decorator import (
    admin_create_gold_sale_transaction_swagger,
    admin_retrieve_gold_sale_transaction_swagger,
    admin_update_gold_sale_transaction_swagger,
    admin_partial_update_gold_sale_transaction_swagger,
    admin_destroy_gold_sale_transaction_swagger,
    admin_list_gold_sale_transaction_swagger,
    user_create_gold_sale_transaction_swagger,
    user_retrieve_gold_sale_transaction_swagger,
    user_update_gold_sale_transaction_swagger,
    user_partial_update_gold_sale_transaction_swagger,
    user_destroy_gold_sale_transaction_swagger,
    user_list_gold_sale_transaction_swagger,
    admin_create_gold_purchase_transaction_swagger,
    admin_retrieve_gold_purchase_transaction_swagger,
    admin_update_gold_purchase_transaction_swagger,
    admin_partial_update_gold_purchase_transaction_swagger,
    admin_destroy_gold_purchase_transaction_swagger,
    admin_list_gold_purchase_transaction_swagger,
    user_create_gold_purchase_transaction_swagger,
    user_retrieve_gold_purchase_transaction_swagger,
    user_update_gold_purchase_transaction_swagger,
    user_partial_update_gold_purchase_transaction_swagger,
    user_destroy_gold_purchase_transaction_swagger,
    user_list_gold_purchase_transaction_swagger,
)


@method_decorator(name='create', decorator=admin_create_gold_sale_transaction_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_gold_sale_transaction_swagger)
@method_decorator(name='update', decorator=admin_update_gold_sale_transaction_swagger)
@method_decorator(name='partial_update', decorator=admin_partial_update_gold_sale_transaction_swagger)
@method_decorator(name='destroy', decorator=admin_destroy_gold_sale_transaction_swagger)
@method_decorator(name='list', decorator=admin_list_gold_sale_transaction_swagger)
class GoldSaleTransactionAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing gold sale transaction records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = GoldSaleTransactionSerializer
    lookup_field = 'id'
    queryset = GoldSaleTransaction.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'status']


@method_decorator(name='create', decorator=user_create_gold_sale_transaction_swagger)
@method_decorator(name='retrieve', decorator=user_retrieve_gold_sale_transaction_swagger)
@method_decorator(name='update', decorator=user_update_gold_sale_transaction_swagger)
@method_decorator(name='partial_update', decorator=user_partial_update_gold_sale_transaction_swagger)
@method_decorator(name='destroy', decorator=user_destroy_gold_sale_transaction_swagger)
@method_decorator(name='list', decorator=user_list_gold_sale_transaction_swagger)
class GoldSaleTransactionAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Authenticated user API ViewSet for managing own gold sale transaction records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GoldSaleTransactionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        Restrict queryset to the authenticated user's gold sale transactions.
        """
        return GoldSaleTransaction.objects.filter(user__username=self.request.user.username)

    def create(self, request, *args, **kwargs):
        """
        Set user to authenticated user and prevent modification of user field.
        """
        if 'user' in request.data:
            raise ValidationError(_('User field cannot be set manually.'))
        request.data['user'] = self.request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Ensure the user can only update their own gold sale transaction and prevent user field modification.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only update your own gold sale transaction.'))
        if 'user' in request.data:
            raise ValidationError(_('User field cannot be modified.'))
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Ensure the user can only partially update their own gold sale transaction and prevent user field modification.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only update your own gold sale transaction.'))
        if 'user' in request.data:
            raise ValidationError(_('User field cannot be modified.'))
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Ensure the user can only delete their own gold sale transaction.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only delete your own gold sale transaction.'))
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Ensure the user can only retrieve their own gold sale transaction.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only access your own gold sale transaction.'))
        return super().retrieve(request, *args, **kwargs)


@method_decorator(name='create', decorator=admin_create_gold_purchase_transaction_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_gold_purchase_transaction_swagger)
@method_decorator(name='update', decorator=admin_update_gold_purchase_transaction_swagger)
@method_decorator(name='partial_update', decorator=admin_partial_update_gold_purchase_transaction_swagger)
@method_decorator(name='destroy', decorator=admin_destroy_gold_purchase_transaction_swagger)
@method_decorator(name='list', decorator=admin_list_gold_purchase_transaction_swagger)
class GoldPurchaseTransactionAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing gold purchase transaction records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = GoldPurchaseTransactionSerializer
    lookup_field = 'id'
    queryset = GoldPurchaseTransaction.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'status']


@method_decorator(name='create', decorator=user_create_gold_purchase_transaction_swagger)
@method_decorator(name='retrieve', decorator=user_retrieve_gold_purchase_transaction_swagger)
@method_decorator(name='update', decorator=user_update_gold_purchase_transaction_swagger)
@method_decorator(name='partial_update', decorator=user_partial_update_gold_purchase_transaction_swagger)
@method_decorator(name='destroy', decorator=user_destroy_gold_purchase_transaction_swagger)
@method_decorator(name='list', decorator=user_list_gold_purchase_transaction_swagger)
class GoldPurchaseTransactionAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Authenticated user API ViewSet for managing own gold purchase transaction records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = GoldPurchaseTransactionSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        Restrict queryset to the authenticated user's gold purchase transactions.
        """
        return GoldPurchaseTransaction.objects.filter(user__username=self.request.user.username)

    def create(self, request, *args, **kwargs):
        """
        Set user to authenticated user and prevent modification of user field.
        """
        if 'user' in request.data:
            raise ValidationError(_('User field cannot be set manually.'))
        request.data['user'] = self.request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Ensure the user can only update their own gold purchase transaction and prevent user field modification.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only update your own gold purchase transaction.'))
        if 'user' in request.data:
            raise ValidationError(_('User field cannot be modified.'))
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Ensure the user can only partially update their own gold purchase transaction and prevent user field modification.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only update your own gold purchase transaction.'))
        if 'user' in request.data:
            raise ValidationError(_('User field cannot be modified.'))
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Ensure the user can only delete their own gold purchase transaction.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only delete your own gold purchase transaction.'))
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Ensure the user can only retrieve their own gold purchase transaction.
        """
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied(_('You can only access your own gold purchase transaction.'))
        return super().retrieve(request, *args, **kwargs)