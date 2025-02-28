"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define classes de exceções para tratamento de erros na camada de domínio do sistema SAGACE.
A classe `DomainError` serve como exceção base para erros relacionados ao domínio da aplicação,
permitindo a criação de exceções especializadas de forma estruturada.

Principais funcionalidades:

- Define uma exceção base para o domínio da aplicação.
- Pode ser herdada por outras exceções específicas do domínio.

Princípios de Design Aplicados:

- **Single Responsibility Principle (SRP - SOLID)**: Cada classe tem uma única responsabilidade clara.
- **Open/Closed Principle (OCP - SOLID)**: `DomainError` pode ser estendida sem modificar seu código-fonte.
- **Encapsulamento**: Centraliza a manipulação de mensagens de erro dentro da exceção base.

Classes:

- ``DomainError``: Exceção base para erros no domínio.

Exemplo de uso:

.. code-block:: python

    from sagace.exceptions import DomainError

    class CustomDomainError(DomainError):
        # Exceção específica do domínio da aplicação.
        pass

    try:
        raise CustomDomainError("Erro específico no domínio.")
    except DomainError as e:
        print(f"Erro capturado: {e}")

Autor: Diego Yosiura
Última Atualização: 27/02/2025 16:05
Criado em: 27/02/2025 16:05
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""


class DomainError(Exception):
    """
    Exceção base para erros no domínio.

    Esta classe deve ser utilizada como base para definir novas exceções específicas do domínio.

    Princípios aplicados:
    - **Single Responsibility Principle (S - SOLID)**: Representa exclusivamente erros do domínio.
    - **Open/Closed Principle (O - SOLID)**: Pode ser estendida para criar novas exceções sem modificar seu código-fonte.
    """
    pass
