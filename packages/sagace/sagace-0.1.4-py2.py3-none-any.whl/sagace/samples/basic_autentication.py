# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------------------------------------------

Module: Authentication Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo realiza a autenticação no sistema SAGACE utilizando a classe `AuthenticationService`.
Ele faz uso do armazenamento em memória para tokens e protege a senha do usuário utilizando
hash SHA-512 antes do envio.

Obs.:

- **Princípios SOLID e Clean Architecture**:
  - **Single Responsibility Principle (SRP)**: Cada classe utilizada no código tem uma única responsabilidade,
    como armazenamento de token e autenticação.
  - **Dependency Inversion Principle (DIP)**: A autenticação depende de uma interface (`AuthenticationService`),
    permitindo diferentes implementações.

Author:           @diego.yosiura
Last Update:      27/02/2025 15:33
Created:          27/02/2025 15:33
Copyright:        (c) Ampere Consultoria Ltda
Original Project: sagace-v2-package
IDE:              PyCharm
"""

import os  # Importa módulo para acessar variáveis de ambiente
from hashlib import sha512  # Importa SHA-512 para hash seguro da senha

# Importa classes necessárias do projeto SAGACE
from sagace.core.storage import MemoryTokenStorage  # Armazena tokens temporariamente na memória

from sagace.auth.interfaces.authentication_service import AuthenticationService  # Serviço de autenticação

# Inicializa o serviço de autenticação
auth_service = AuthenticationService()

# Define a URL base para o sistema de autenticação
base_url = "https://demo.sagace.online"

# Obtém credenciais e token da aplicação a partir das variáveis de ambiente
username = os.getenv('SAGACE_USERNAME')  # Usuário definido nas variáveis de ambiente
password = os.getenv('SAGACE_PASSWORD')  # Senha do usuário (não deve ser armazenada em texto plano)
application_token = os.getenv('SAGACE_TOKEN')  # Token de aplicação para acesso

# Garante que a senha não seja nula antes de calcular o hash
if password:
    password = sha512(password.encode('utf-8')).hexdigest()  # Aplica hash SHA-512 à senha
else:
    raise ValueError("A variável de ambiente 'SAGACE_PASSWORD' não foi definida.")

# Instancia o armazenamento de token em memória
token_storage = MemoryTokenStorage()

try:
    # Realiza o login e armazena o token JWT recebido
    token = auth_service.login(base_url, username, password, application_token, token_storage)

    # Exibe o token JWT recebido para fins de debug
    print(f"Token JWT recebido: {token}")

except Exception as e:
    # Captura e exibe erros de autenticação
    print(f"Erro ao autenticar: {e}")
