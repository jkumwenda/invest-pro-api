from enum import auto
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Instance(models.Model):
    instance_id = models.AutoField(primary_key=True)
    organisation_name = models.TextField(blank=False, null=False)
    postal_address = models.TextField(blank=False, null=False)
    email_address = models.TextField(blank=True, null=True)
    folder_fs_path = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'instance'


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    phone_number = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'profile'


class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=255, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('role', 'instance_id')]
        db_table = 'role'


class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    role_id = models.ForeignKey(
        Role, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('user_id', 'role_id', 'instance_id')]
        db_table = 'user_role'


class AccessRight(models.Model):
    access_right_id = models.AutoField(primary_key=True)
    access_right = models.CharField(
        max_length=255, unique=True, blank=False, null=False)
    code = models.CharField(max_length=255, unique=True,
                            blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'access_right'


class RoleAccessRight(models.Model):
    role_access_right_id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(
        Role, on_delete=models.CASCADE, blank=True, null=True)
    access_right_id = models.ForeignKey(
        AccessRight, on_delete=models.CASCADE, blank=True, null=True)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('role_id', 'access_right_id', 'instance_id')]
        db_table = 'role_access_right'


class Sector(models.Model):
    sector_id = models.AutoField(primary_key=True)
    sector = models.TextField(blank=False, null=False, max_length=80)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('sector', 'instance_id')]
        db_table = 'sector'


class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company = models.TextField(blank=False, null=False, max_length=80)
    sector_id = models.ForeignKey(
        Sector, on_delete=models.CASCADE, blank=True, null=True)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('company', 'instance_id')]
        db_table = 'company'


class ParameterCategory(models.Model):
    parameter_category_id = models.AutoField(primary_key=True)
    parameter_category = models.TextField(
        blank=False, null=False, max_length=500)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('parameter_category', 'instance_id')]
        db_table = 'parameter_category'


class AnswerType(models.Model):
    answer_type_id = models.AutoField(primary_key=True)
    answer_type = models.TextField(
        blank=False, null=False, max_length=500)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('answer_type', 'instance_id')]
        db_table = 'answer_type'


class AnswerValue(models.Model):
    answer_value_id = models.AutoField(primary_key=True)
    answer_value = models.CharField(blank=False, null=False, max_length=100)
    value = models.IntegerField(blank=True, null=True)
    answer_type_id = models.ForeignKey(
        AnswerType, on_delete=models.CASCADE, blank=False, null=False, related_name='answer_types')
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('answer_value', 'instance_id')]
        db_table = 'answer_value'


class Parameter(models.Model):
    parameter_id = models.AutoField(primary_key=True)
    parameter = models.TextField(
        blank=False, null=False, max_length=500)
    parameter_category_id = models.ForeignKey(
        ParameterCategory, on_delete=models.CASCADE, blank=False, null=False, related_name='parameter_categories')
    answer_type_id = models.ForeignKey(
        AnswerType, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('parameter', 'instance_id')]
        db_table = 'parameter'


class ParameterGroup(models.Model):
    parameter_group_id = models.AutoField(primary_key=True)
    parameter_group = models.TextField(
        blank=False, null=False, max_length=500)
    parameter_id = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('parameter_group', 'instance_id')]
        db_table = 'parameter_group'


class AnalysisPortfolio(models.Model):
    analysis_portfolio_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(
        Company, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    analysis_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('parameter_group', 'instance_id')]
        db_table = 'analysis_portfolio'


class AnalysisPortfolioCategory(models.Model):
    analysis_portfolio_category_id = models.AutoField(primary_key=True)
    parameter_category_id = models.ForeignKey(
        ParameterCategory, on_delete=models.CASCADE, blank=False, null=False)
    analysis_portfolio_id = models.ForeignKey(
        AnalysisPortfolio, on_delete=models.CASCADE, blank=False, null=False, related_name='analysis_portfolios')
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('parameter_group', 'instance_id')]
        db_table = 'analysis_portfolio_category'


class AnalysisParameter(models.Model):
    analysis_parameter_id = models.AutoField(primary_key=True)
    analysis_portfolio_category_id = models.ForeignKey(
        AnalysisPortfolioCategory, on_delete=models.CASCADE, blank=False, null=False, related_name='analysis_portfolio_category')
    parameter_id = models.ForeignKey(
        Parameter, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('parameter_group', 'instance_id')]
        db_table = 'analysis_parameter'


class AnalysisValue(models.Model):
    analysis_value_id = models.AutoField(primary_key=True)
    analysis_parameter_id = models.ForeignKey(
        AnalysisParameter, on_delete=models.CASCADE, blank=False, null=False, related_name='analysis_parameter_value')
    answer_value_id = models.ForeignKey(
        AnswerValue, on_delete=models.CASCADE, blank=False, null=False, related_name='answer_values')
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        # unique_together = [('parameter_group', 'instance_id')]
        db_table = 'analysis_value'


class UserLog(models.Model):
    user_log_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    log = models.TextField()
    tag = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'user_log'
