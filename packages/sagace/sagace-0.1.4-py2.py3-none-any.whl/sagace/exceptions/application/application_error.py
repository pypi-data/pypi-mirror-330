"""
--------------------------------------------------------------------------------------------------------------------

Descrição:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Este módulo define uma classe base para exceções na camada de aplicação do sistema SAGACE.
A classe `ApplicationError` serve como a classe pai para todas as exceções relacionadas à aplicação,
fornecendo uma estrutura centralizada para tratamento de erros.

Principais funcionalidades:

- Define uma exceção base para a aplicação.
- Pode ser herdada por outras exceções específicas do domínio.

Princípios de Design Aplicados:

- **Single Responsibility Principle (SRP - SOLID)**: A classe tem a única responsabilidade de representar erros na aplicação.
- **Open/Closed Principle (OCP - SOLID)**: `ApplicationError` pode ser estendida sem modificação do código-fonte existente.

Classes:

- ``ApplicationError``: Exceção base para erros na camada de aplicação.

Exemplo de uso:

.. code-block:: python

    from sagace.exceptions import ApplicationError

    class CustomError(ApplicationError):
        # Exceção específica do domínio da aplicação.
        pass

    try:
        raise CustomError("Ocorreu um erro na aplicação.")
    except ApplicationError as e:
        print(f"Erro capturado: {e}")

Autor: Diego Yosiura
Última Atualização: 27/02/2025 16:05
Criado em: 27/02/2025 16:05
Copyright: (c) Ampere Consultoria Ltda
Projeto Original: sagace-v2-package
IDE: PyCharm
"""


class ApplicationError(Exception):
    """
    Exceção base para erros na camada de aplicação.

    Esta classe deve ser utilizada como classe base para definir novas exceções específicas da aplicação.

    Princípios aplicados:
    - **Single Responsibility Principle (S - SOLID)**: Representa exclusivamente erros da aplicação.
    - **Open/Closed Principle (O - SOLID)**: Pode ser estendida para criar novas exceções sem modificar seu código-fonte.
    """
    pass
