from .viewset_includes import *


class AnswerTypeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, DjangoModelPermissions)
    queryset = AnswerType.objects.all()

    def get_object(self, pk=None):
        try:
            return AnswerType.objects.get(pk=pk)
        except AnswerType.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'view_answer_types', request)
        instance = LoggedUser.get_instance(request.user.id)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(self.queryset, request)
        serializer = AnswerTypeSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        Security.secureAccess(self, 'add_answer_type', request)
        instance = LoggedUser.get_instance(request.user.id)
        instance = LoggedUser.get_instance(request.user.id)
        request.data['instance_id'] = instance

        serializer = AnswerTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        Security.secureAccess(self, 'change_answer_type', request)
        instance = LoggedUser.get_instance(request.user.id)
        answer_type = self.get_object(pk)
        request.data['instance_id'] = answer_type.instance_id.pk

        serializer = AnswerTypeSerializer(answer_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            UserLogHelper.create_log(
                request.data, request.method, request.user.id, instance)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        Security.secureAccess(self, 'view_answer_type', request)
        instance = LoggedUser.get_instance(request.user.id)
        answer_type = self.get_object(pk)
        serializer = AnswerTypeSerializer(answer_type)
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        Security.secureAccess(self, 'delete_answer_type', request)
        instance = LoggedUser.get_instance(request.user.id)
        answer_type = self.get_object(pk)
        answer_type.delete()
        UserLogHelper.create_log(
            request.data, request.method, request.user.id, instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
