from .viewset_includes import *
from api import helper


class ParameterCategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ParameterCategory.objects.all()

    def get_object(self, pk=None):
        try:
            return ParameterCategory.objects.get(pk=pk)
        except ParameterCategory.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_parameter_categories', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(
            self.queryset.filter(instance_id=instance), request)
        serializer = ParameterCategorySerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_parameter_category', request)
        instance = LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance

        serializer = ParameterCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_parameter_category', request)
        parameter_category = self.get_object(pk)
        request.data['instance_id'] = parameter_category.instance_id.pk

        serializer = ParameterCategorySerializer(
            parameter_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, parameter_category.instance_id.pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_parameter_category', request)
        instance = LoggedUser.get_instance(request.user.id)
        parameter_category = self.get_object(pk)
        serializer = ParameterCategorySerializer(parameter_category)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_parameter_category', request)
        instance = LoggedUser.get_instance(request.user.id)
        parameter_category = self.get_object(pk)
        parameter_category.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
