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


class BuildingType(models.Model):
    building_type_id = models.AutoField(primary_key=True)
    building_type = models.TextField(blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('building_type', 'instance_id')]
        db_table = 'building_type'


class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    postal_address = models.TextField(blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    user_id = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('user_id', 'instance_id')]
        db_table = 'client'


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, null=False)
    instance_id = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('status', 'instance_id')]
        db_table = 'status'


class District(models.Model):
    district_id = models.AutoField(primary_key=True)
    district = models.CharField(
        max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'district'


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location = models.CharField(
        max_length=255, unique=False, null=False)
    district_id = models.ForeignKey(
        District, on_delete=models.CASCADE, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('location', 'district_id', 'instance_id')]
        db_table = 'location'


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.TextField(blank=False, null=False)
    project_manager = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    client_id = models.ForeignKey(
        Client, on_delete=models.CASCADE, blank=False, null=False)
    building_type_id = models.ForeignKey(
        BuildingType, on_delete=models.CASCADE, blank=False, null=False)
    location_id = models.ForeignKey(
        Location, on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    status_id = models.ForeignKey(
        Status, on_delete=models.CASCADE, blank=True, null=True)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'project'


class Space(models.Model):
    space_id = models.AutoField(primary_key=True)
    space = models.CharField(max_length=255, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('space', 'instance_id')]
        db_table = 'space'


class ProjectSpace(models.Model):
    project_space_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=True, null=True)
    space_id = models.ForeignKey(
        Space, on_delete=models.CASCADE, blank=True, null=True)
    size = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'project_space'


class Phase(models.Model):
    phase_id = models.AutoField(primary_key=True)
    phase = models.CharField(max_length=255, blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [('phase', 'instance_id')]
        db_table = 'phase'


class ProjectFlow(models.Model):
    project_flow_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=False, null=False)
    phase_id = models.ForeignKey(
        Phase, on_delete=models.CASCADE, blank=False, null=False)
    flow_number = models.IntegerField(blank=False, null=False)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        unique_together = [
            ('project_id', 'phase_id', 'instance_id', 'flow_number')]
        db_table = 'project_flow'


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    project_flow_id = models.ForeignKey(
        ProjectFlow, on_delete=models.CASCADE, blank=True, null=True)
    note = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'note'


class PublishedFile(models.Model):
    published_file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255, blank=False, null=False)
    project_id = models.ForeignKey(
        Project, on_delete=models.CASCADE, blank=False, null=False)
    file_path = models.TextField(blank=False, null=False)
    instance_id = models.ForeignKey(
        Instance, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'published_file'


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
