from .viewset_includes import *
from api import helper


class ParameterViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Parameter.objects.all().order_by('parameter_id')

    def get_object(self, pk=None):
        try:
            return Parameter.objects.get(pk=pk)
        except Parameter.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_parameters', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(self.queryset.filter(
            instance_id=instance), request)
        serializer = ParameterSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_parameter', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        serializer = ParameterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_parameter', request)
        instance = LoggedUser.get_instance(request.user.id)
        building_tye = self.get_object(pk)
        request.data['instance_id'] = building_tye.instance_id_id
        serializer = ParameterSerializer(building_tye, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_parameter', request)
        instance = self.get_object(pk)
        serializer = ParameterSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_parameter', request)
        instance = LoggedUser.get_instance(request.user.id)
        bulding_type = self.get_object(pk)
        bulding_type.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
