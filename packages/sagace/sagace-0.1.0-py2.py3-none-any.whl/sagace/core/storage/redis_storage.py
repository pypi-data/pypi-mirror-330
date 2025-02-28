# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.:

    Author:           @diego.yosiura
    Last Update:      27/02/2025 16:24
    Created:          27/02/2025 16:24
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: sagace-v2-package
    IDE:              PyCharm
"""
import redis
from .. import Token
from .. import TokenStorage

class RedisTokenStorage(TokenStorage):
    """Armazena o token no Redis."""

    def __init__(self, redis_url="redis://localhost:6379/0"):
        self.client = redis.StrictRedis.from_url(redis_url, decode_responses=True)

    def save_token(self, token: Token):
        self.client.set("base_url", token.base_url)
        self.client.set("access_token", token.access_token)
        self.client.set("application_name", token.application_name)
        self.client.set("description", token.description)
        self.client.set("token_type", token.token_type)

    def get_token(self) -> Token:
        base_url = self.client.get("base_url")
        access_token = self.client.get("access_token")
        application_name = self.client.get("application_name")
        description = self.client.get("description")
        token_type = self.client.get("token_type")

        if not access_token or not base_url:
            raise ValueError("Token not found in Redis.")
        return Token(
            base_url=base_url,
            access_token=access_token,
            application_name=application_name,
            description=description,
            token_type=token_type
        )
