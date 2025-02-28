# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 15:33
    Created:          27/02/2025 15:33
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
import os

from hashlib import sha512
from sagace.core.storage import MemoryTokenStorage
from sagace.auth.interfaces.authentication_service import AuthenticationService

auth_service = AuthenticationService()

base_url = "https://demo.sagace.online"
username = os.getenv('SAGACE_USERNAME')
password = sha512(os.getenv('SAGACE_PASSWORD').encode('utf-8')).hexdigest()
application_token = os.getenv('SAGACE_TOKEN')
token_storage = MemoryTokenStorage()

try:
    token = auth_service.login(base_url, username, password, application_token, token_storage)
    print(f"Token JWT recebido: {token}")
except Exception as e:
    print(f"Erro ao autenticar: {e}")
