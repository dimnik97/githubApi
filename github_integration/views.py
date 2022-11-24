import json
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .BaseApiUser import BaseApiUser
from django.conf import settings


class ApiUserData(APIView, BaseApiUser):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        self.user = self.get_user_info(request.user)
        headers = self.get_request_headers()
        api_address = self.generate_user_address()
        user_data = self.execute_api_get_request(headers, api_address)
        response = Response(user_data)
        return response

    @staticmethod
    def generate_user_address():
        return f"{BaseApiUser.api_base_address}/user"


class ApiProjectsData(APIView, BaseApiUser):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    def get(self, request, format=None):
        self.user = self.get_user_info(request.user)
        headers = self.get_request_headers()
        api_address = self.generate_projects_address()
        user_projects = self.execute_api_get_request(headers, api_address)
        response = JsonResponse(user_projects, safe=False)
        return response

    @staticmethod
    def generate_projects_address():
        return f"{BaseApiUser.api_base_address}/user/repos"


class ApiLinkAuthorization(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        client_id = settings.SOCIAL_AUTH_GITHUB_KEY
        response = {
            'api_link': self.generate_auth_link(client_id)
        }
        return JsonResponse(response)

    @staticmethod
    def generate_auth_link(client_id):
        return f"{BaseApiUser.base_address}/login/oauth/authorize?client_id={client_id}"


class ApiUserAccessToken(APIView, BaseApiUser):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        code = request.query_params['code']
        headers = {'Accept': 'application/vnd.github+json'}
        api_address = self.generate_access_token_link()
        params = {
            "client_id": settings.SOCIAL_AUTH_GITHUB_KEY,
            "client_secret": settings.SOCIAL_AUTH_GITHUB_SECRET,
            "code": code
        }
        response = self.execute_api_post_request(headers, api_address, params)
        if not response.get('error'):
            access_token_github = response['access_token']
        else:
            return JsonResponse({'Error': response['error']})

        headers = {'Content-type': 'application/json'}
        api_address = f"http://127.0.0.1:8000/auth/convert-token/"
        params = {
            "grant_type": "convert_token",
            "client_id": settings.CLIENT_ID_APPLICATION,
            "client_secret": settings.CLIENT_SECRET_APPLICATION,
            "token": access_token_github,
            "backend": "github"
        }
        response = self.execute_api_post_request(headers, api_address, params)
        access_token = response.get('access_token')
        return JsonResponse({'access_token': access_token})

    @staticmethod
    def generate_access_token_link():
        return f"{BaseApiUser.base_address}/login/oauth/access_token"


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # simply delete the token to force a login
        try:
            request.user.auth_token.delete()
        except:
            print('logged out')
        return Response(status=status.HTTP_200_OK)
