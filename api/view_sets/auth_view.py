from .data_object import *
from api.view_sets import data_object
from .viewset_includes import *
from api import helper
from django.contrib.auth.hashers import make_password


class LoginViewSet(viewsets.ViewSet):
    queryset = Client.objects.all().order_by('client_id')

    def get_object(self, pk=None):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get_user_object(self, pk=None):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_clients', request)
        paginator = ResponsePaginationHelper()
        instance = helper.LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(
            self.queryset.filter(instance_id=instance), request)
        serializer = ClientSerializer(results, many=True)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
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

            client_data = data_object.DataObjects.client_data(request.data)
            client_data['user_id'] = user.id
            client_data['instance_id'] = instance
            serializer = ClientSerializer(data=client_data)
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
        Security.secureAccess(self, 'change_client', request)
        instance = LoggedUser.get_instance(request.user.id)
        client = self.get_object(pk)
        user = self.get_user_object(client.user_id.id)

        user_data = data_object.UserObjects.user_data(request.data)
        user_data['username'] = request.data['email']
        user_serializer = UserSerializer(user, data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            request.data['user_id'] = user.id
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)

        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            UserLogHelper.create_log(
                user_data, request.method, request.user.id, instance)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_client', request)
        instance = LoggedUser.get_instance(request.user.id)
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_client', request)
        instance = LoggedUser.get_instance(request.user.id)
        client = self.get_object(pk)
        client.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Client.objects.all().order_by('client_id')

    def get_object(self, pk=None):
        try:
            return Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            raise Http404

    def get_user_object(self, pk=None):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_clients', request)
        paginator = ResponsePaginationHelper()
        instance = helper.LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(
            self.queryset.filter(instance_id=instance), request)
        serializer = ClientSerializer(results, many=True)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
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

            client_data = data_object.DataObjects.client_data(request.data)
            client_data['user_id'] = user.id
            client_data['instance_id'] = instance
            serializer = ClientSerializer(data=client_data)
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
        Security.secureAccess(self, 'change_client', request)
        instance = LoggedUser.get_instance(request.user.id)
        client = self.get_object(pk)
        user = self.get_user_object(client.user_id.id)

        user_data = data_object.UserObjects.user_data(request.data)
        user_data['username'] = request.data['email']
        user_serializer = UserSerializer(user, data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            request.data['user_id'] = user.id
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)

        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            UserLogHelper.create_log(
                user_data, request.method, request.user.id, instance)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_client', request)
        instance = LoggedUser.get_instance(request.user.id)
        client = self.get_object(pk)
        serializer = ClientSerializer(client)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_client', request)
        instance = LoggedUser.get_instance(request.user.id)
        client = self.get_object(pk)
        client.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
