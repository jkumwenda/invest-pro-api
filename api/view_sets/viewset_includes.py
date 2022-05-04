from django.contrib.auth import authenticate
from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import *
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from ..helper import *
from rest_framework.exceptions import APIException
from ..security import Security
