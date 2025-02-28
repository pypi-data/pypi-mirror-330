# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 16:30
    Created:          27/02/2025 16:30
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
import requests
from . import APIClient
from ..exceptions.domain import PermissionDeniedError, TokenExpiredError, APIRequestError

class HTTPAPIClient(APIClient):
    """Implementação concreta do APIClient utilizando requests."""

    def request(self, method: str, endpoint: str, **kwargs):
        """
        Método genérico para requisições HTTP autenticadas.
        :param method: Método HTTP (GET, POST, PUT, DELETE).
        :param endpoint: Endpoint relativo à `base_url`.
        :param kwargs: Parâmetros adicionais para `requests.request()`.
        :return: Resposta JSON da API.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()

        # Mescla os headers com os que podem ter sido passados nos kwargs
        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        # Faz a requisição HTTP
        response = requests.request(method, url, **kwargs)

        # Tratamento de erros comuns
        if response.status_code == 401:
            raise TokenExpiredError()
        elif response.status_code == 403:
            raise PermissionDeniedError()
        elif not response.ok:
            raise APIRequestError(response.status_code, response.text)

        return response.json()

    def _get_headers(self) -> dict:
        """Retorna os headers padrão com autenticação JWT."""
        return {"Authorization": f"JWT {self.token_storage.get_token().access_token}"}

    def get(self, endpoint: str, **kwargs):
        """Método GET autenticado."""
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        """Método POST autenticado."""
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        """Método PUT autenticado."""
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        """Método DELETE autenticado."""
        return self.request("DELETE", endpoint, **kwargs)