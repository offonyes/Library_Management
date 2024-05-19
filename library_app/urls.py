from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from library_app.views import (BookViewSet, GenreViewSet, AuthorViewSet,
                               TopBooksView, TopBooksLateReturnsView,
                               TopUsersLateReturnsView, BorrowCountLastYearView, index)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path("index/", index, name='index'),

    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/top/books/', TopBooksView.as_view(), name='topbooks'),
    path('api/top/late/books/', TopBooksLateReturnsView.as_view(), name='toplatebooks'),
    path('api/top/late/users/', TopUsersLateReturnsView.as_view(), name='toplateusers'),
    path('api/last_year_count', BorrowCountLastYearView.as_view(), name='lastyearcount')
]
