from django import urls
from django.urls import path, include
from api import views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

schema_view = get_schema_view(
    openapi.Info(
        title="DRF BASE API",
        default_version='v1',
        description="DRF Base API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jkumwenda@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('user', views.UserViewSet, basename='User')
router.register('register', views.UserRegistrationViewSet,
                basename='User Registers')
router.register('reset_password', views.PasswordResetViewSet,
                basename='Passwords')
router.register('instance', views.InstanceViewSet,
                basename='Instances')
router.register('profile', views.ProfileViewSet,
                basename='Profiles')
router.register('role', views.RoleViewSet, basename='Roles')
router.register('user_role', views.UserRoleViewSet, basename='User Role')
router.register('access_right', views.AccessRightViewSet,
                basename='Access Right')
router.register('role_access_right', views.RoleAccessRightViewSet,
                basename='Role Access Right')
router.register('company', views.CompanyViewSet,
                basename='Companies')
router.register('sector', views.SectorViewSet,
                basename='Sectors')
router.register('parameter_category', views.ParameterCategoryViewSet,
                basename='Parameter Categories')
router.register('answer_type', views.AnswerTypeViewSet,
                basename='Answer Type')
router.register('answer_value', views.AnswerValueViewSet,
                basename='Answer Value')
router.register('parameter', views.ParameterViewSet,
                basename='Parameter')
router.register('user_log', views.UserLogViewSet, basename='User Log')
router.register('analysis_portfolio', views.AnalysisPortfolioViewSet,
                basename='Analysis Portfolio')
router.register('analysis_parameter', views.AnalysisParameterViewSet,
                basename='Analysis Parameter')
router.register('analysis_portfolio_category', views.AnalysisPortfolioCategoryViewSet,
                basename='Analysis Portfolio Category')
router.register('analysis_value', views.AnalysisValueViewSet,
                basename='Analysis Value')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth-verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
]
