"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo implementa a autenticação de usuários no sistema SAGACE utilizando uma API externa.
A classe `AuthenticationAPI` herda de `AuthenticationRepository`, garantindo a conformidade com o princípio de **Dependency Inversion** (D do SOLID),
permitindo a substituição da implementação sem afetar os consumidores da interface.

Principais funcionalidades:

- Realiza autenticação via API externa.
- Armazena o token JWT utilizando `TokenStorage`.
- Lança exceções apropriadas em caso de falha.

Classes:

- ``AuthenticationAPI``: Implementação do repositório de autenticação via API.

Exemplo de uso:

.. code-block:: python

    from sagace.infrastructure import AuthenticationAPI
    from sagace.core import TokenStorage

    auth_api = AuthenticationAPI()
    token_storage = TokenStorage()
    token = auth_api.authenticate("https://api.sagace.online", "usuario", "senha", "app_token", token_storage)
    print(token)


Autor: Diego Yosiura
Última Atualização: 27/02/2025 15:31
Criado em: 27/02/2025 15:31
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""

import requests
from ..domain import AuthenticationRepository
from ...core import TokenStorage, Token
from ...exceptions.domain import APIRequestError
from ...exceptions.infrastructure import AuthenticationFailedError


class AuthenticationAPI(AuthenticationRepository):
    """
    Implementação da autenticação via API externa.

    Esta classe implementa `AuthenticationRepository`, garantindo que qualquer mudança na forma
    de autenticação possa ser feita sem impactar os consumidores desta interface.

    Princípios utilizados:
    - **Dependency Inversion (D - SOLID)**: Utiliza uma abstração (`AuthenticationRepository`) para evitar dependências diretas.
    - **Single Responsibility (S - SOLID)**: Responsável exclusivamente por autenticação via API.
    - **Clean Architecture**: Implementação no nível de infraestrutura, garantindo separação entre domínio e serviços externos.
    """

    BASE_URL = "https://demo.sagace.online/"
    AUTH_URL = "auth/base/login/"

    def authenticate(self, base_url: str, username: str, password: str, token: str,
                     token_storage: TokenStorage) -> Token:
        """
        Autentica um usuário via API e retorna um token JWT.

        :param base_url: URL base da API de autenticação.
        :type base_url: str
        :param username: Nome de usuário para autenticação.
        :type username: str
        :param password: Senha do usuário.
        :type password: str
        :param token: Token da aplicação para autenticação.
        :type token: str
        :param token_storage: Instância responsável por armazenar o token JWT.
        :type token_storage: TokenStorage
        :return: Token JWT retornado pela API.
        :rtype: Token
        :raises APIRequestError: Se a API retornar um erro na requisição.
        :raises AuthenticationFailedError: Se os dados esperados não estiverem presentes na resposta.
        """

        # Constrói a URL completa garantindo que a barra não seja duplicada ou omitida
        full_url = f"{base_url.rstrip('/')}/{self.AUTH_URL.lstrip('/')}"

        # Envia uma requisição HTTP POST para a API de autenticação
        response = requests.post(
            url=full_url,
            json={"username": username, "password": password},
            headers={"Authorization": token}
        )

        try:
            # Garante que a resposta HTTP não contenha erros (4xx ou 5xx)
            response.raise_for_status()
        except Exception:
            # Lança uma exceção caso a requisição falhe
            raise APIRequestError(response.status_code, response.text)

        data = response.json()

        # Verifica se a chave 'data' está presente na resposta
        if 'data' not in data:
            raise AuthenticationFailedError()

        # Garante que os campos essenciais existam antes de criar o token
        required_fields = ['ds_application_name', 'ds_description', 'authorization_token']
        if not all(field in data['data'] for field in required_fields):
            raise AuthenticationFailedError()

        # Cria um objeto Token com os dados retornados pela API
        token = Token(
            base_url=base_url,
            application_name=data['data']["ds_application_name"],
            description=data['data']["ds_description"],
            access_token=data['data']["authorization_token"]
        )

        # Salva o token no armazenamento definido
        token_storage.save_token(token)
        return token
