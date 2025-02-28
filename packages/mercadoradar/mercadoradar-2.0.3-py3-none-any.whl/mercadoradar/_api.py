import os
from json import JSONDecodeError

from dotenv import load_dotenv
from requests import request

from src import mercadoradar
from src.mercadoradar import api_token

load_dotenv()
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

mercadoradar.api_token = api_token


class MercadoRadarAPI:
    BASE_URL = 'https://api-pricing.mercadoradar.com.br' if not DEBUG else 'http://localhost:8000'

    def _make_request(self, method: str,
                      path: str,
                      params: dict = None,
                      data: dict = None) -> list | dict | bytes:
        headers = {
            'Authorization': f'Token {mercadoradar.api_token}',
            'Content-Type': 'application/json',
        }
        url = f'{self.BASE_URL}{path}'

        if url[-1] != '/':
            url = f'{url}/'

        response = request(method, url, headers=headers, params=params, json=data)

        if response.status_code // 100 != 2:
            try:
                response_content = response.json()
            except JSONDecodeError:
                response_content = response.content or response.text

            raise Exception(f'[HTTP {response.status_code}] {response_content}')

        if response.headers.get('Content-Type') == 'text/csv':
            return response.content

        return response.json()

    def create_request(self, path: str, data: list | dict) -> dict:
        return self._make_request(method='POST', path=path, data=data)

    def list_request(self, path: str, limit: int = 100, offset: int = 0, params: dict = None) -> list:
        params = self._set_pagination(limit, offset, params)
        return self._make_request(method='GET', path=path, params=params)

    @staticmethod
    def _set_pagination(limit, offset, params):
        if not params:
            params = dict()
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset
        return params

    def retrieve_request(self, path, id):
        path = f'{path}{id}/'
        return self._make_request(method='GET', path=path)

    def update_request(self, path, id, data):
        path = f'{path}{id}/'
        return self._make_request(method='PUT', path=path, data=data)

    def delete_request(self, path, id):
        path = f'{path}{id}/'
        return self._make_request(method='DELETE', path=path)

    def action_request(self, path: str, action: str, id: int, limit: int = 100, offset: int = 0,
                       params: dict = None) -> list | dict:
        path = f'{path}{id}/{action}'
        params = self._set_pagination(limit, offset, params)
        return self._make_request(method='GET', path=path, params=params)
