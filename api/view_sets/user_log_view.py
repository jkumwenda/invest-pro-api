from .viewset_includes import *
from api import helper


class UserLogViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserLog.objects.all()

    def get_object(self, pk=None):
        try:
            return UserLog.objects.get(pk=pk)
        except UserLog.DoesNotExist:
            raise Http404

    def list(self, request):
        Security.secureAccess(self, 'viw_user_logs', request)
        instance = helper.LoggedUser.get_instance(request.user.id)
        paginator = ResponsePaginationHelper()
        results = paginator.paginate_queryset(
            self.queryset.filter(instance_id=instance), request)
        serializer = UserLogSerializer(results, many=True)
        UserLogHelper.create_log(
            request, request.method, request.user.id, instance)
        return paginator.get_paginated_response(serializer.data)
