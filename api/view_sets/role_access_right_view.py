from .viewset_includes import *


class RoleAccessRightViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = RoleAccessRight.objects.all()

    def get_object(self, pk=None):
        try:
            return RoleAccessRight.objects.get(pk=pk)
        except RoleAccessRight.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_role_access_rights', request)
        instance = LoggedUser.get_instance(request.user.id)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(
            self.queryset.filter(instance_id=instance), request)
        serializer = RoleAccessRightSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_role_access_right', request)
        instance = LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        serializer = RoleAccessRightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_role_access_right', request)
        role_access_right = self.get_object(pk)
        request.data['instance_id'] = role_access_right.instance_id_id
        serializer = RoleAccessRightSerializer(
            role_access_right, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, role_access_right.instance_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_role_access_right', request)
        role_access_right = self.get_object(pk)
        serializer = RoleAccessRightSerializer(role_access_right)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_role_access_right', request)
        instance = LoggedUser.get_instance(request.user.id)
        role_access_right = self.get_object(pk)
        role_access_right.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
