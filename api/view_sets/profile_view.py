from .data_object import *
from .viewset_includes import *
from api import helper
from django.contrib.auth.hashers import make_password

from api.view_sets import data_object


class ProfileViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all().order_by('profile_id')

    def get_object(self, pk=None):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get_user_object(self, pk=None):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_profile', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = ProfileSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_client', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        user_data = data_object.DataObjects.user_data(request.data)

        password = helper.GeneratePassword.random_password()
        user_data['password'] = make_password(password)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            UserLogHelper.create_log(
                user_data, request.method, request.user.id, instance)

            profile_data = data_object.DataObjects.profile_data(request.data)
            profile_data['user_id'] = user.id
            profile_data['instance_id'] = instance
            serializer = ProfileSerializer(data=profile_data)
            if serializer.is_valid():
                serializer.save()
                helper.SendEmail.new_user(user_data, password)
                UserLogHelper.create_log(
                    request.data, request.method, request.user.id, instance)
                return Response(serializer.data)

            user = self.get_user_object(user.id)
            user.delete()
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_profile', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        Profile = self.get_object(pk)

        user_data = data_object.DataObjects.user_data(request.data)
        user = User.objects.filter(pk=Profile.user_id.pk).update(**user_data)

        request.data['user_id'] = Profile.user_id.pk
        request.data['instance_id'] = Profile.instance_id_id

        serializer = ProfileSerializer(Profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_profile', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        Profile = self.get_object(pk)
        serializer = ProfileSerializer(Profile)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_profile', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        Profile = self.get_object(pk)
        Profile.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
