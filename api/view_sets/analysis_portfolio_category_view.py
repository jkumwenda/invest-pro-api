from .viewset_includes import *
from api import helper
from rest_framework.exceptions import APIException


class AnalysisPortfolioCategoryViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = AnalysisPortfolioCategory.objects.all().order_by(
        'analysis_portfolio_category_id')

    def get_object(self, pk=None):
        try:
            return AnalysisPortfolioCategory.objects.get(pk=pk)
        except AnalysisPortfolioCategory.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(
            self, 'view_analysis_portfolio_categorys', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(self.queryset.filter(
            instance_id=instance), request)
        serializer = AnalysisPortfolioCategorySerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_analysis_portfolio_category', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        serializer = AnalysisPortfolioCategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(
            self, 'change_analysis_portfolio_category', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_portfolio_category = self.get_object(pk)
        request.data['instance_id'] = analysis_portfolio_category.instance_id_id
        serializer = AnalysisPortfolioCategorySerializer(
            analysis_portfolio_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(
            self, 'view_analysis_portfolio_category', request)
        instance = self.get_object(pk)
        serializer = AnalysisPortfolioCategorySerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(
            self, 'delete_analysis_portfolio_category', request)
        instance = LoggedUser.get_instance(request.user.id)
        analysis_portfolio_category = self.get_object(pk)
        analysis_portfolio_category.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
