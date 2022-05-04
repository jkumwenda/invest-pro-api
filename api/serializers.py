from django.contrib.auth.models import *
from rest_framework import serializers
from .models import *
from rest_framework.exceptions import APIException


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'is_active', ]
        # read_only = ['password']


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class AccessRightSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRight
        fields = '__all__'


class RoleAccessRightSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleAccessRight
        fields = '__all__'


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    sector = SectorSerializer(
        source='sector_id', read_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class ParameterCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterCategory
        fields = '__all__'


class AnswerValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerValue
        fields = '__all__'


class AnswerTypeSerializer(serializers.ModelSerializer):
    answer_types = AnswerValueSerializer(
        read_only=True, many=True)

    class Meta:
        model = AnswerType
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):
    # parameter_category = ParameterCategorySerializer(
    #     source='parameter_category_id', read_only=True)
    answer_type = AnswerTypeSerializer(
        source='answer_type_id', read_only=True)

    class Meta:
        model = Parameter
        fields = '__all__'


class AnalysisValueSerializer(serializers.ModelSerializer):
    answer_value = AnswerValueSerializer(
        source='answer_value_id', read_only=True)

    class Meta:
        model = AnalysisValue
        fields = '__all__'


class AnalysisParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer(
        source='parameter_id', read_only=True)

    analysis_parameter_value = AnalysisValueSerializer(
        read_only=True, many=True)

    class Meta:
        model = AnalysisParameter
        fields = '__all__'


class AnalysisPortfolioCategorySerializer(serializers.ModelSerializer):
    parameter_category = ParameterCategorySerializer(
        source='parameter_category_id', read_only=True)

    analysis_portfolio_category = AnalysisParameterSerializer(
        read_only=True, many=True)

    class Meta:
        model = AnalysisPortfolioCategory
        fields = '__all__'
        # read_only_fields = ['parameter_category']


class AnalysisPortfolioSerializer(serializers.ModelSerializer):
    company = CompanySerializer(
        source='company_id', read_only=True)

    analysis_portfolios = AnalysisPortfolioCategorySerializer(
        read_only=True, many=True)
    parameter_data = serializers.SerializerMethodField('get_parameter_data')

    def get_parameter_data(self, obj):
        total_parameters = AnalysisParameter.objects.filter(
            analysis_portfolio_category_id__analysis_portfolio_id=getattr(obj, 'pk')).count()
        total_values = AnalysisValue.objects.filter(
            analysis_parameter_id__analysis_portfolio_category_id__analysis_portfolio_id=getattr(obj, 'pk')).count()

        data = {'total_parameters': total_parameters,
                'total_values': total_values}
        return data

    class Meta:
        model = AnalysisPortfolio
        fields = '__all__'
