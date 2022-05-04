from .viewset_includes import *
from api import helper


class SectorViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Sector.objects.all()

    def get_object(self, pk=None):
        try:
            return Sector.objects.get(pk=pk)
        except Sector.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_sectors', request)
        paginator = ResponsePaginationHelper()
        instance = LoggedUser.get_instance(request.user.id)
        results = paginator.paginate_queryset(
            self.queryset.filter(instance_id=instance), request)
        serializer = SectorSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_sector', request)
        instance = LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance

        serializer = SectorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_sector', request)
        sector = self.get_object(pk)
        request.data['instance_id'] = sector.instance_id.pk

        serializer = SectorSerializer(
            sector, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, sector.instance_id.pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_sector', request)
        instance = LoggedUser.get_instance(request.user.id)
        sector = self.get_object(pk)
        serializer = SectorSerializer(sector)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_sector', request)
        instance = LoggedUser.get_instance(request.user.id)
        sector = self.get_object(pk)
        sector.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
