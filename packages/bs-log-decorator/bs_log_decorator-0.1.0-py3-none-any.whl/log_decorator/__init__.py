"""
log-decorator: Um decorador de logging flexível para Python que oferece:
- Filtragem hierárquica de logs
- Criação automática de diretório de logs
- Configuração flexível de níveis
- Suporte a console colorido

Author: Bruno Sardou <bruno.sardou@outlook.com>
GitHub: https://github.com/bruno-sardou/log-decorator
"""

from .core import log_decorator, LogLevel

__version__ = "0.1.0"
__all__ = ["log_decorator", "LogLevel"]