from .viewset_includes import *
from api import helper
from rest_framework.exceptions import APIException


class AnalysisParameterViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = AnalysisParameter.objects.all().order_by('analysis_parameter_id')

    def get_object(self, pk=None):
        try:
            return AnalysisParameter.objects.get(pk=pk)
        except AnalysisParameter.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_analysis_parameters', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(self.queryset.filter(
            instance_id=instance), request)
        serializer = AnalysisParameterSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_analysis_parameter', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        serializer = AnalysisParameterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            parameters = Parameter.objects.all().order_by('parameter_id')

            analysis_parameter = {}
            analysis_parameter['analysis_parameter_id'] = serializer.data['analysis_parameter_id']
            analysis_parameter['instance_id'] = instance

            for parameter in parameters:
                analysis_parameter['parameter_id'] = parameter.parameter_id
                parameter_serializer = AnalysisParameterSerializer(
                    data=analysis_parameter)
                if parameter_serializer.is_valid():
                    parameter_serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_analysis_parameter', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_parameter = self.get_object(pk)
        request.data['instance_id'] = analysis_parameter.instance_id_id
        serializer = AnalysisParameterSerializer(
            analysis_parameter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_analysis_parameter', request)
        instance = self.get_object(pk)
        serializer = AnalysisParameterSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_analysis_parameter', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_parameter = self.get_object(pk)
        analysis_parameter.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
