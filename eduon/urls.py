# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!!!!! Dear developer, write clean code !!!!!! #
# !!!!!!!!!! Don't make us scold you !!!!!!!!!!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test

from decorator_include import decorator_include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view



from home.click import TestView
from home.views import Page404
from home.viewset import DidUserBuy
from rest_framework.authtoken import views
from rest_framework import permissions
from simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from . import router


handler404 = Page404

schema_view = get_schema_view(
    openapi.Info(
        title="eduon.uz API",
        default_version='v1.0',
        description="EduOn backend",
        terms_of_service="https://eduon.uz/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),

    path('backoffice/', include('backoffice.urls')),
    # path('backoffice/', decorator_include(user_passes_test(lambda user: user.is_authenticated and user.admin_set.count() > 0), 'backoffice.urls')),

    path('api1234/', include(router.router.urls)),
    path('api/did-user-buy/', DidUserBuy.as_view(), name="is-user-bought"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/paycom/', include('paycom.urls')),
    path('api/uniredpay/', include('uniredpay.urls')),
    path('click/transaction/', TestView.as_view()),
    # path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)