from .viewset_includes import *
from api import helper


class CompanyViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Company.objects.all().order_by('company_id')

    def get_object(self, pk=None):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_companys', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(self.queryset.filter(
            instance_id=instance), request)
        serializer = CompanySerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_company', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_company', request)
        instance = LoggedUser.get_instance(request.user.id)
        company = self.get_object(pk)
        request.data['instance_id'] = company.instance_id_id
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_company', request)
        instance = self.get_object(pk)
        serializer = CompanySerializer(instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_company', request)
        instance = LoggedUser.get_instance(request.user.id)
        company = self.get_object(pk)
        company.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
