from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.core.api.v1.user.view import UserRegisterAPIView, UserAPIView, UserAdminAPIView

router = DefaultRouter()

router.register('core/a/user/', UserAdminAPIView, basename='user-admin')
router.register('core/l/user/', UserAPIView, basename='authenticated-user')
router.register('core/p/user/', UserRegisterAPIView, basename='register-user')


urlpatterns = [

    path('accounts/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('accounts/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),

]

urlpatterns += router.urls
