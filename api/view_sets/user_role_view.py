from .viewset_includes import *


class UserRoleViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserRole.objects.all()

    def get_object(self, pk=None):
        try:
            return UserRole.objects.get(pk=pk)
        except UserRole.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_user_roles', request)
        instance = LoggedUser.get_instance(request.user.id)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(
            self.queryset.filter(instance_id=instance), request)
        serializer = UserRoleSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_user_role', request)
        instance = LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        serializer = UserRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_user_role', request)
        user_role = self.get_object(pk)
        request.data['instance_id'] = user_role.instance_id_id
        serializer = UserRoleSerializer(
            user_role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, user_role.instance_id_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_user_role', request)
        user_role = self.get_object(pk)
        serializer = UserRoleSerializer(user_role)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_user_role', request)
        instance = LoggedUser.get_instance(request.user.id)
        user_role = self.get_object(pk)
        user_role.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
