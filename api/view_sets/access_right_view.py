from .viewset_includes import *


class AccessRightViewSet(viewsets.ViewSet):
    access_right_classes = (IsAuthenticated,)
    queryset = AccessRight.objects.all()

    def get_object(self, pk=None):
        try:
            return AccessRight.objects.get(pk=pk)
        except AccessRight.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_access_rights', request)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = AccessRightSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_access_right', request)
        serializer = AccessRightSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_access_right', request)
        access_right = self.get_object(pk)
        serializer = AccessRightSerializer(access_right, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_access_right', request)
        access_right = self.get_object(pk)
        serializer = AccessRightSerializer(access_right)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_access_right', request)
        access_right = self.get_object(pk)
        access_right.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
