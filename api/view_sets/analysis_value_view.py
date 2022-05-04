from .viewset_includes import *


class AnalysisValueViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = AnalysisValue.objects.all()

    def get_object(self, pk=None):
        try:
            return AnalysisValue.objects.get(pk=pk)
        except AnalysisValue.DoesNotExist:
            raise Http404

    def get_analysis_parameter(self, analysis_parameter_id=None):
        try:
            return AnalysisValue.objects.get(
                analysis_parameter_id=analysis_parameter_id)
        except AnalysisValue.DoesNotExist:
            return False

    def list(self, request):
        Security.secureAccess(self, 'view_analysis_values', request)
        instance = LoggedUser.get_instance(request.user.id)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = AnalysisValueSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_analysis_value', request)
        instance = LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance

        analysis_parameter = self.get_analysis_parameter(
            request.data['analysis_parameter_id'])
        if analysis_parameter:
            analysis_value = self.get_object(
                analysis_parameter.analysis_value_id)
            serializer = AnalysisValueSerializer(
                analysis_value, data=request.data)
            if serializer.is_valid():
                serializer.save()
                UserLogHelper.create_log(
                    request.data, request.method, request.user.id, instance)
                return Response(serializer.data)
        else:
            serializer = AnalysisValueSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                UserLogHelper.create_log(
                    request.data, request.method, request.user.id, instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_analysis_value', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_value = self.get_object(pk)
        request.data['instance_id'] = analysis_value.instance_id.pk

        serializer = AnalysisValueSerializer(analysis_value, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_analysis_value', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_value = self.get_object(pk)
        serializer = AnalysisValueSerializer(analysis_value)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_analysis_value', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_value = self.get_object(pk)
        analysis_value.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
