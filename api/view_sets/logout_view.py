from .viewset_includes import *


class LogoutViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def get_object(self, pk=None):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def list(self, request):
        self.get_object(request.user.id)
        request.user.auth_token.delete()
        return Response({"success": ("Successfully logged out.")}, status=status.HTTP_200_OK)
