from django.urls import path
from .views import Register, UserProfile

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('user-profile/', UserProfile.as_view(), name='user-profile'),
    # simple_jwt_urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
