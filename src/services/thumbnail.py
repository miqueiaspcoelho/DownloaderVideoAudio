"""
ThumbnailService - Gerenciamento de miniaturas.

Responsável por fazer download e processar miniaturas de vídeos.
"""

import io
from pathlib import Path

import requests
from PIL import Image

from src.core import get_logger
from src.services.filesystem import FileSystemService

logger = get_logger(__name__)


class ThumbnailService:
    """Serviço de gerenciamento de miniaturas."""

    def __init__(self, fs_service: FileSystemService) -> None:
        """
        Inicializa o serviço de miniaturas.

        Args:
            fs_service: Instância de FileSystemService.
        """
        self.fs_service = fs_service
        self.thumbnail_size = (320, 180)  # Tamanho padrão de miniaturas

    def download_thumbnail(self, video_id: str, thumbnail_url: str) -> Path | None:
        """
        Baixa e processa uma miniatura.

        Args:
            video_id: ID do vídeo no YouTube.
            thumbnail_url: URL da miniatura.

        Returns:
            Path para o arquivo salvo, ou None se falhar.
        """
        try:
            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()

            image = Image.open(io.BytesIO(response.content))
            image = self._resize_thumbnail(image)

            thumbnail_path = self.fs_service.get_thumbnail_path(video_id)
            image.save(thumbnail_path, quality=85)

            logger.info(f"Miniatura salva: {thumbnail_path}")
            return thumbnail_path

        except requests.RequestException as e:
            logger.error(f"Erro ao baixar miniatura de {video_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro ao processar miniatura de {video_id}: {e}")
            return None

    def _resize_thumbnail(self, image: Image.Image) -> Image.Image:
        """
        Redimensiona uma miniatura.

        Args:
            image: Imagem PIL.

        Returns:
            Imagem redimensionada.
        """
        return image.resize(self.thumbnail_size, Image.Resampling.LANCZOS)

    def get_thumbnail(self, video_id: str) -> Path | None:
        """
        Obtém o caminho de uma miniatura baixada.

        Args:
            video_id: ID do vídeo.

        Returns:
            Path se existir, None caso contrário.
        """
        thumbnail_path = self.fs_service.get_thumbnail_path(video_id)
        if self.fs_service.file_exists(thumbnail_path):
            return thumbnail_path
        return None

    def delete_thumbnail(self, video_id: str) -> bool:
        """
        Deleta uma miniatura.

        Args:
            video_id: ID do vídeo.

        Returns:
            True se deletado com sucesso.
        """
        thumbnail_path = self.fs_service.get_thumbnail_path(video_id)
        return self.fs_service.delete_file(thumbnail_path)
