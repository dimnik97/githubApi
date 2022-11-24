import abc
import json
import requests


class BaseApiUser(abc.ABC):
    api_base_address = 'https://api.github.com'
    base_address = 'https://github.com'
    user = None
    headers = None

    @staticmethod
    def get_user_info(user):
        social = user.social_auth.get(provider='github')
        user_info = social.extra_data
        return user_info

    @staticmethod
    def execute_api_get_request(headers, request_address):
        response = requests.get(request_address, headers=headers)
        dict_response = json.loads(response.content)
        return dict_response

    @staticmethod
    def execute_api_post_request(headers, request_address, params):
        response = requests.post(request_address, headers=headers, params=params)
        dict_response = json.loads(response.content)
        return dict_response

    def get_request_headers(self):
        return {'Accept': 'application/vnd.github+json', 'Authorization': f"Bearer {self.user['access_token']}"}
