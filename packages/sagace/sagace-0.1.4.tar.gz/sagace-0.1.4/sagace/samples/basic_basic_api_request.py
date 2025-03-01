# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------------------------

Module: Basic API Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module demonstrates a basic API request using the `HTTPAPIClient` class from the `sagace.core` package.
It performs a request to retrieve all authenticated users and ensures the response contains the expected structure.

Raises:
    APIRequestError: If the response does not contain required fields.

Author:           @diego.yosiura
Last Update:      27/02/2025 15:33
Created:          27/02/2025 15:33
Copyright:        (c) Ampere Consultoria Ltda
Original Project: sagace-v2-package
IDE:              PyCharm
"""

from sagace.exceptions.domain import APIRequestError
from sagace.samples.basic_autentication import token_storage
from sagace.core import HTTPAPIClient

# Instancia o cliente HTTP utilizando o armazenamento de token definido
client = HTTPAPIClient(token_storage)

# Realiza a requisição para obter todos os usuários autenticados
response = client.get('/auth/user/get-all/')

# Valida a presença do campo 'status' na resposta
if 'status' not in response:
    raise APIRequestError(500, "O campo 'status' não está presente na resposta da API.")

# Valida a presença do campo 'data' na resposta
if 'data' not in response:
    raise APIRequestError(500, "O campo 'data' não está presente na resposta da API.")

# Itera sobre os usuários retornados e imprime cada um
for item in response['data']:
    print(item)
