"""
Implementação do decorador de logging flexível para Python.

Author: Bruno Sardou <bruno.sardou@outlook.com>
GitHub: https://github.com/bruno-sardou/log-decorator
"""

import os
import inspect
from loguru import logger
from functools import wraps
from enum import IntEnum
from pathlib import Path
from typing import Union, Callable

# Define uma hierarquia de níveis de log
class LogLevel(IntEnum):
    TRACE = 5
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

# Obtém o usuário do sistema
def get_user():
    try:
        return os.getlogin()  # Nome do usuário logado
    except:
        return "Usuário desconhecido"

# Decorador para logging dinâmico com filtragem hierárquica
def log_decorator(level_or_func: Union[str, Callable] = "INFO") -> Union[Callable, Callable[[Callable], Callable]]:
    """
    Decorator para logging automatizado de funções com filtragem hierárquica.
    Pode ser usado com ou sem parênteses:
        @log_decorator
        def funcao(): ...
        
        @log_decorator()
        def funcao(): ...
        
        @log_decorator(level="DEBUG")
        def funcao(): ...
    
    Parameters:
    level_or_func: Nível mínimo para mostrar logs ou a função a ser decorada
                   Apenas logs deste nível ou superior serão registrados.
    """
    # Verificação para permitir uso com ou sem parênteses
    if callable(level_or_func):
        # Caso 1: @log_decorator sem parênteses
        return _create_wrapper("INFO")(level_or_func)
    
    # Caso 2: @log_decorator() ou @log_decorator(level="DEBUG")
    level = level_or_func
    if isinstance(level, str):
        return _create_wrapper(level)
    else:
        raise TypeError("O argumento level deve ser uma string")

def _create_wrapper(level: str):
    """Função interna que cria o wrapper real"""
    # Verifica se o nível é válido
    valid_levels = ["TRACE", "DEBUG", "INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"]
    if level.upper() not in valid_levels:
        raise ValueError(f"Nível de log inválido: {level}. Use um dos seguintes: {', '.join(valid_levels)}")
    
    # Converte o nível para o valor numérico correspondente
    min_level = getattr(LogLevel, level.upper())
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Cria a pasta de logs se não existir
            log_dir = Path.cwd() / 'logs'
            log_dir.mkdir(exist_ok=True, parents=True)
            
            # Define o caminho do arquivo de log
            # Usa o nome do diretório atual como nome do arquivo
            log_file = log_dir / f'{Path.cwd().name}.log'
            
            # Remove configurações anteriores apenas se necessário
            try:
                logger.remove(wrapper.sink_id)
                logger.remove(wrapper.console_sink_id)
            except (ValueError, AttributeError):
                pass
                
            # Adiciona configuração para o arquivo de log e armazena o ID
            wrapper.sink_id = logger.add(
                str(log_file),  # Converte Path para string para compatibilidade
                format="{time} | {level} | {message} | Usuário: {extra[user]} | Arquivo: {extra[file]}",
                level=level.upper()  # Define o nível mínimo conforme especificado
            )
            
            # Adiciona configuração para exibição no console
            wrapper.console_sink_id = logger.add(
                sink=lambda msg: print(msg),
                format="<level>{level}</level> | {message}",
                level=level.upper(),
                colorize=True  # Adiciona cores para melhor visualização no console
            )
            
            # Obtém o usuário atual
            user = get_user()
            
            # Cria um logger contextualizado com as informações extras
            contextualized_logger = logger.bind(user=user, file=inspect.getfile(func))
            
            # Registra o início da execução se o nível for suficiente
            if LogLevel.INFO >= min_level:
                contextualized_logger.info(f"Executando '{func.__name__}' com args={args}, kwargs={kwargs}")
            
            try:
                result = func(*args, **kwargs)
                # Registra o sucesso se o nível for suficiente
                if LogLevel.SUCCESS >= min_level:
                    contextualized_logger.success(f"Resultado de '{func.__name__}': {result}")
                return result
            except Exception as e:
                # Registra o erro se o nível for suficiente
                error_message = f"Erro na função '{func.__name__}': {type(e).__name__}: {e}"
                if LogLevel.ERROR >= min_level:
                    contextualized_logger.error(error_message)
                raise
            finally:
                # Remover os sinks após o uso para evitar vazamento de recursos
                try:
                    logger.remove(wrapper.sink_id)
                    logger.remove(wrapper.console_sink_id)
                except (ValueError, AttributeError):
                    pass
                
        # Inicializa os atributos de sink
        wrapper.sink_id = None
        wrapper.console_sink_id = None
        return wrapper
    return decorator