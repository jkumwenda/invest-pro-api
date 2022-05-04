from .viewset_includes import *


class RoleViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = Role.objects.all().order_by('role_id')

    def get_object(self, pk=None):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_roles', request)
        instance = LoggedUser.get_instance(request.user.id)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = RoleSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_role', request)
        instance = LoggedUser.get_instance(request.user.id)
        instance = LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance

        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_role', request)
        instance = LoggedUser.get_instance(request.user.id)
        role = self.get_object(pk)
        request.data['instance_id'] = role.instance_id.pk

        serializer = RoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_role', request)
        instance = LoggedUser.get_instance(request.user.id)
        role = self.get_object(pk)
        serializer = RoleSerializer(role)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_role', request)
        instance = LoggedUser.get_instance(request.user.id)
        role = self.get_object(pk)
        role.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
