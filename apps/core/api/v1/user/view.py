from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, filters
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.models import CustomUser
from apps.core.serializers import CustomUserSerializer
from apps.core.api.v1.user.swagger_decorator import (
    admin_create_user_swagger,
    admin_retrieve_user_swagger,
    admin_update_user_swagger,
    admin_partial_update_user_swagger,
    admin_destroy_user_swagger,
    admin_list_user_swagger,
    user_retrieve_user_swagger,
    user_update_user_swagger,
    user_partial_update_user_swagger,
    register_create_user_swagger,
)


@method_decorator(name='create', decorator=admin_create_user_swagger)
@method_decorator(name='retrieve', decorator=admin_retrieve_user_swagger)
@method_decorator(name='update', decorator=admin_update_user_swagger)
@method_decorator(name='partial_update', decorator=admin_partial_update_user_swagger)
@method_decorator(name='destroy', decorator=admin_destroy_user_swagger)
@method_decorator(name='list', decorator=admin_list_user_swagger)
class UserAdminAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """
    Admin-only API ViewSet for managing user records.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


@method_decorator(name='retrieve', decorator=user_retrieve_user_swagger)
@method_decorator(name='update', decorator=user_update_user_swagger)
@method_decorator(name='partial_update', decorator=user_partial_update_user_swagger)
class UserAPIView(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """
    Authenticated user API ViewSet for viewing and updating own user record.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """
        Restrict queryset to the authenticated user's record.
        """
        return CustomUser.objects.filter(username=self.request.user.username)

    def update(self, request, *args, **kwargs):
        """
        Prevent non-admin users from changing user_role to admin.
        """
        if not request.user.is_staff and 'user_role' in request.data and request.data['user_role'] == 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(_('Non-admin users cannot set user_role to admin.'))
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Prevent non-admin users from changing user_role to admin.
        """
        if not request.user.is_staff and 'user_role' in request.data and request.data['user_role'] == 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(_('Non-admin users cannot set user_role to admin.'))
        return super().partial_update(request, *args, **kwargs)


@method_decorator(name='create', decorator=register_create_user_swagger)
class UserRegisterAPIView(
    GenericViewSet,
    mixins.CreateModelMixin,
):
    """
    Public API ViewSet for registering new users.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Ensure user_role is set to 'customer' for new registrations.
        """
        if 'user_role' in request.data and request.data['user_role'] != 'customer':
            from rest_framework.exceptions import ValidationError
            raise ValidationError(_('User role must be "customer" for registration.'))
        return super().create(request, *args, **kwargs)