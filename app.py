"""
Aplicação Principal - YouTube Media Downloader.

Ponto de entrada da aplicação que inicializa a UI e inicia o loop de eventos.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from PySide6.QtWidgets import QApplication

from src.core import get_logger
from src.ui import MainWindow

logger = get_logger(__name__)


def main() -> int:
    """
    Função principal da aplicação.

    Returns:
        Código de saída da aplicação.
    """
    try:
        logger.info("Iniciando YouTube Media Downloader...")

        app = QApplication(sys.argv)
        app.setApplicationName("YouTube Media Downloader")

        window = MainWindow()
        window.show()

        logger.info("Aplicação iniciada com sucesso")
        return app.exec()

    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
