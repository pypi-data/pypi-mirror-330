"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo fornece uma implementação concreta de um cliente HTTP autenticado dentro do sistema SAGACE.
A classe `HTTPAPIClient` herda de `APIClient`, garantindo que todas as requisições sejam autenticadas e sigam
um contrato unificado.

Principais funcionalidades:

- Realiza requisições HTTP autenticadas (GET, POST, PUT, DELETE).
- Gerencia o armazenamento e recuperação do token JWT.
- Lança exceções adequadas em caso de erro na API.

Classes:

- ``HTTPAPIClient``: Implementação concreta de `APIClient` utilizando `requests`.

Exemplo de uso:

.. code-block:: python

    from sagace.infrastructure.http_api_client import HTTPAPIClient
    from sagace.core import TokenStorage

    api_client = HTTPAPIClient("https://api.sagace.online", TokenStorage())
    response = api_client.get("/usuario/dados")
    print(response)

Autor: Diego Yosiura
Última Atualização: 27/02/2025 16:30
Criado em: 27/02/2025 16:30
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

import requests
from . import APIClient
from ..exceptions.domain import PermissionDeniedError, TokenExpiredError, APIRequestError


class HTTPAPIClient(APIClient):
    """
    Implementação concreta de `APIClient` utilizando `requests`.

    Esta classe fornece uma implementação real para comunicação com APIs via HTTP,
    garantindo que todas as requisições sejam autenticadas.

    Princípios aplicados:
    - **Liskov Substitution (L - SOLID)**: `HTTPAPIClient` pode ser utilizada no lugar de `APIClient` sem alterar o comportamento esperado.
    - **Open/Closed (O - SOLID)**: A classe pode ser estendida para novos métodos HTTP sem modificação do código existente.
    """

    def request(self, method: str, endpoint: str, **kwargs):
        """
        Método genérico para requisições HTTP autenticadas.

        :param method: Método HTTP a ser utilizado (GET, POST, PUT, DELETE).
        :type method: str
        :param endpoint: Caminho relativo dentro da API.
        :type endpoint: str
        :param kwargs: Parâmetros adicionais para `requests.request()`.
        :return: Resposta JSON da API.
        :rtype: dict
        :raises TokenExpiredError: Se o token estiver expirado.
        :raises PermissionDeniedError: Se o usuário não tiver permissão para acessar o recurso.
        :raises APIRequestError: Para quaisquer outros erros da API.
        """

        # Constrói a URL completa garantindo que não haja barras duplicadas
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self._get_headers()

        # Mescla headers passados como argumento com os padrões
        if "headers" in kwargs:
            kwargs["headers"].update(headers)
        else:
            kwargs["headers"] = headers

        # Executa a requisição HTTP
        response = requests.request(method, url, **kwargs)

        # Tratamento de erros comuns da API
        if response.status_code == 401:
            raise TokenExpiredError()
        elif response.status_code == 403:
            raise PermissionDeniedError()
        elif not response.ok:
            raise APIRequestError(response.status_code, response.text)

        return response.json()

    def _get_headers(self) -> dict:
        """
        Retorna os headers padrão com autenticação JWT.

        :return: Dicionário de headers HTTP contendo o token JWT.
        :rtype: dict
        """
        return {"Authorization": f"JWT {self.token_storage.get_token().access_token}"}

    def get(self, endpoint: str, **kwargs):
        """
        Método GET autenticado.

        :param endpoint: Caminho relativo dentro da API.
        :type endpoint: str
        :param kwargs: Parâmetros adicionais para a requisição.
        :return: Resposta JSON da API.
        :rtype: dict
        """
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        """
        Método POST autenticado.

        :param endpoint: Caminho relativo dentro da API.
        :type endpoint: str
        :param kwargs: Parâmetros adicionais para a requisição.
        :return: Resposta JSON da API.
        :rtype: dict
        """
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs):
        """
        Método PUT autenticado.

        :param endpoint: Caminho relativo dentro da API.
        :type endpoint: str
        :param kwargs: Parâmetros adicionais para a requisição.
        :return: Resposta JSON da API.
        :rtype: dict
        """
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        """
        Método DELETE autenticado.

        :param endpoint: Caminho relativo dentro da API.
        :type endpoint: str
        :param kwargs: Parâmetros adicionais para a requisição.
        :return: Resposta JSON da API.
        :rtype: dict
        """
        return self.request("DELETE", endpoint, **kwargs)
