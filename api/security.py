from django.contrib.auth.models import User
from django.http.response import JsonResponse
from .serializers import RoleAccessRightSerializer
from django.http import Http404
from django.core.exceptions import PermissionDenied


class Security():
    def secureAccess(self, codename, request):
        userId = request.user.id
        queryset = User.objects.get(pk=userId)
        serializer = RoleAccessRightSerializer(queryset)
        return True  # Comment it out in production
        for groups in serializer.data['groups']:
            for permission in groups['permissions']:
                if permission['codename'] == codename:
                    return True
        raise PermissionDenied()
