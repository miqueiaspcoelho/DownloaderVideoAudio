"""
Módulo centralizado de logging para o YouTube Media Downloader.

Este módulo gerencia todos os logs da aplicação, gravando em arquivo
e exibindo no console com níveis configuráveis.
"""

import logging
import logging.handlers
from pathlib import Path


class LoggerConfig:
    """Configuração centralizada de logging."""

    _instance: LoggerConfig | None = None
    _loggers: dict[str, logging.Logger] = {}

    def __new__(cls) -> LoggerConfig:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Inicializa a configuração de logging."""
        if self._initialized:
            return

        self.logs_dir = Path(__file__).parent.parent.parent / "logs"
        self.logs_dir.mkdir(exist_ok=True)

        self._setup_root_logger()
        self._initialized = True

    def _setup_root_logger(self) -> None:
        """Configura o logger raiz."""
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # Remove handlers existentes
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Formato detalhado
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler para arquivo
        file_handler = logging.handlers.RotatingFileHandler(
            self.logs_dir / "app.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10 MB
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """
        Obtém um logger nomeado.

        Args:
            name: Nome do módulo/logger.

        Returns:
            Logger configurado.
        """
        if name not in self._loggers:
            self._loggers[name] = logging.getLogger(name)

        return self._loggers[name]


def get_logger(name: str) -> logging.Logger:
    """
    Função conveniente para obter um logger.

    Args:
        name: Nome do módulo (tipicamente __name__).

    Returns:
        Logger configurado e pronto para uso.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Iniciando aplicação")
    """
    config = LoggerConfig()
    return config.get_logger(name)
