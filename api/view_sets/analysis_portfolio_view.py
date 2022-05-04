from .viewset_includes import *
from api import helper
from rest_framework.exceptions import APIException


class AnalysisPortfolioViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = AnalysisPortfolio.objects.all().order_by('analysis_portfolio_id')

    def get_object(self, pk=None):
        try:
            return AnalysisPortfolio.objects.get(pk=pk)
        except AnalysisPortfolio.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_analysis_portfolios', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(self.queryset.filter(
            instance_id=instance), request)
        serializer = AnalysisPortfolioSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_analysis_portfolio', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        serializer = AnalysisPortfolioSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            parameter_categories = ParameterCategory.objects.all().order_by('parameter_category_id')

            analysis_portfolio_category = {}
            analysis_portfolio_category['analysis_portfolio_id'] = serializer.data['analysis_portfolio_id']
            analysis_portfolio_category['instance_id'] = instance

            for parameter_category in parameter_categories:
                analysis_portfolio_category['parameter_category_id'] = parameter_category.parameter_category_id
                analysis_portfolio_category_serializer = AnalysisPortfolioCategorySerializer(
                    data=analysis_portfolio_category)

                if analysis_portfolio_category_serializer.is_valid():
                    analysis_portfolio_category_serializer.save()

                    parameters = Parameter.objects.filter(
                        parameter_category_id=parameter_category.parameter_category_id).order_by('parameter_id')
                    analysis_parameter = {}
                    analysis_parameter['analysis_portfolio_category_id'] = analysis_portfolio_category_serializer.data['analysis_portfolio_category_id']
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
        Security.secureAccess(self, 'change_analysis_portfolio', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_portfolio = self.get_object(pk)
        request.data['instance_id'] = analysis_portfolio.instance_id_id
        serializer = AnalysisPortfolioSerializer(
            analysis_portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_analysis_portfolio', request)
        instance = self.get_object(pk)
        serializer = AnalysisPortfolioSerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_analysis_portfolio', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_portfolio = self.get_object(pk)
        analysis_portfolio.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
