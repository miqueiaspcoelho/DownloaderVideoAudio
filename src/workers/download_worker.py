"""
DownloadWorker - Worker para downloads assíncronos.

Executa downloads em thread separada para manter a UI responsiva.
"""

from datetime import datetime

from PySide6.QtCore import QObject, QThread, Signal

from src.core import get_logger
from src.models import DownloadStatus, DownloadTask, Media, MediaType
from src.services import (
    DownloadService,
    FileSystemService,
    PersistenceService,
    ThumbnailService,
)

logger = get_logger(__name__)


class DownloadWorker(QObject):
    """Worker para executar downloads em thread separada."""

    # Sinais
    progress_updated = Signal(DownloadTask)
    download_completed = Signal(Media)
    download_failed = Signal(str, Exception)

    def __init__(
        self,
        fs_service: FileSystemService,
        download_service: DownloadService,
        thumbnail_service: ThumbnailService,
        persistence_service: PersistenceService,
    ) -> None:
        """
        Inicializa o worker.

        Args:
            fs_service: Serviço de sistema de arquivos.
            download_service: Serviço de download.
            thumbnail_service: Serviço de miniaturas.
            persistence_service: Serviço de persistência.
        """
        super().__init__()
        self.fs_service = fs_service
        self.download_service = download_service
        self.thumbnail_service = thumbnail_service
        self.persistence_service = persistence_service

        # Define o callback de progresso
        self.download_service.set_progress_callback(self._on_progress)

    def download(self, url: str, media_type: MediaType) -> None:
        """
        Inicia um download.

        Args:
            url: URL do vídeo.
            media_type: Tipo de mídia (áudio ou vídeo).
        """
        task = DownloadTask(url=url, media_type=media_type)
        task.status = DownloadStatus.DOWNLOADING

        try:
            logger.info(f"Iniciando download: {url} ({media_type.value})")

            # Extrai metadados
            metadata = self.download_service.extract_metadata(url)
            if not metadata:
                raise ValueError("Falha ao extrair metadados")

            # Faz o download
            file_path = (
                self.download_service.download_audio(url, task)
                if media_type == MediaType.AUDIO
                else self.download_service.download_video(url, task)
            )

            if not file_path:
                raise ValueError("Falha ao baixar arquivo")

            # Baixa thumbnail
            thumbnail_path = self.thumbnail_service.download_thumbnail(
                metadata.video_id, metadata.thumbnail_url
            )

            # Cria objeto Media
            media = Media(
                file_path=file_path,
                media_type=media_type,
                metadata=metadata,
                file_size=self.fs_service.get_file_size(file_path),
                downloaded_at=datetime.now(),
                thumbnail_path=thumbnail_path,
            )

            # Persiste o download
            self.persistence_service.save_media(media)

            task.status = DownloadStatus.COMPLETED
            task.progress_percentage = 100.0
            task.downloaded_media = media

            self.download_completed.emit(media)
            logger.info(f"Download concluído: {media.metadata.title}")

        except Exception as e:
            task.status = DownloadStatus.FAILED
            task.error_message = str(e)
            self.download_failed.emit(url, e)
            logger.error(f"Erro ao fazer download: {e}")

    def _on_progress(self, task: DownloadTask) -> None:
        """
        Callback de progresso do serviço de download.

        Args:
            task: DownloadTask com informações de progresso.
        """
        self.progress_updated.emit(task)


class DownloadThread(QThread):
    """Thread para executar downloads."""

    def __init__(self, worker: DownloadWorker, url: str, media_type: MediaType) -> None:
        """
        Inicializa a thread.

        Args:
            worker: DownloadWorker.
            url: URL a fazer download.
            media_type: Tipo de mídia.
        """
        super().__init__()
        self.worker = worker
        self.url = url
        self.media_type = media_type

    def run(self) -> None:
        """Executa o download."""
        self.worker.download(self.url, self.media_type)
