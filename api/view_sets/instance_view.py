from .viewset_includes import *


class InstanceViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Instance.objects.all()

    def get_object(self, pk=None):
        try:
            return Instance.objects.get(pk=pk)
        except Instance.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_instance', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = InstanceSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_instance', request)
        serializer = InstanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_instance', request)
        instance = self.get_object(pk)
        serializer = InstanceSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_instance', request)
        instance = self.get_object(pk)
        serializer = InstanceSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_instance', request)
        instance = self.get_object(pk)
        instance.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
