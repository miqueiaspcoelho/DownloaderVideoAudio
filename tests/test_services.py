"""
Testes unitários básicos para os serviços.

Use: pytest tests/test_services.py -v
"""

from pathlib import Path

import pytest

from src.core import get_logger
from src.models import DownloadStatus, DownloadTask, MediaType
from src.services import (
    DownloadService,
    FileSystemService,
    PersistenceService,
    ThumbnailService,
)

logger = get_logger(__name__)


@pytest.fixture
def fs_service() -> FileSystemService:
    """Fixture para FileSystemService."""
    return FileSystemService()


@pytest.fixture
def download_service(fs_service: FileSystemService) -> DownloadService:
    """Fixture para DownloadService."""
    return DownloadService(fs_service)


@pytest.fixture
def thumbnail_service(fs_service: FileSystemService) -> ThumbnailService:
    """Fixture para ThumbnailService."""
    return ThumbnailService(fs_service)


@pytest.fixture
def persistence_service(tmp_path: Path) -> PersistenceService:
    """Fixture para PersistenceService com diretório temporário."""
    return PersistenceService(data_dir=tmp_path / ".data")


class TestFileSystemService:
    """Testes para FileSystemService."""

    def test_initialization(self, fs_service: FileSystemService) -> None:
        """Testa inicialização e criação de diretórios."""
        assert fs_service.audio_dir.exists()
        assert fs_service.video_dir.exists()
        assert fs_service.thumbnails_dir.exists()

    def test_get_audio_path(self, fs_service: FileSystemService) -> None:
        """Testa geração de path para áudio."""
        path = fs_service.get_audio_path("test.mp3")
        assert path.name == "test.mp3"
        assert path.parent == fs_service.audio_dir

    def test_get_video_path(self, fs_service: FileSystemService) -> None:
        """Testa geração de path para vídeo."""
        path = fs_service.get_video_path("test.mp4")
        assert path.name == "test.mp4"
        assert path.parent == fs_service.video_dir

    def test_list_files_empty(self, fs_service: FileSystemService) -> None:
        """Testa listagem de arquivos em diretórios vazios."""
        audios = fs_service.list_audio_files()
        videos = fs_service.list_video_files()

        assert isinstance(audios, list)
        assert isinstance(videos, list)


class TestDownloadService:
    """Testes para DownloadService."""

    def test_initialization(self, download_service: DownloadService) -> None:
        """Testa inicialização."""
        assert download_service.fs_service is not None
        assert callable(download_service.extract_metadata)

    def test_progress_callback(self, download_service: DownloadService) -> None:
        """Testa definição de callback de progresso."""

        def dummy_callback(task: DownloadTask) -> None:
            pass

        download_service.set_progress_callback(dummy_callback)
        assert download_service.progress_callback is dummy_callback


class TestThumbnailService:
    """Testes para ThumbnailService."""

    def test_initialization(self, thumbnail_service: ThumbnailService) -> None:
        """Testa inicialização."""
        assert thumbnail_service.fs_service is not None
        assert thumbnail_service.thumbnail_size == (320, 180)

    def test_get_nonexistent_thumbnail(self, thumbnail_service: ThumbnailService) -> None:
        """Testa obtenção de thumbnail inexistente."""
        path = thumbnail_service.get_thumbnail("nonexistent_id")
        assert path is None


class TestPersistenceService:
    """Testes para PersistenceService."""

    def test_initialization(self, persistence_service: PersistenceService) -> None:
        """Testa inicialização."""
        assert persistence_service.data_dir.exists()
        assert persistence_service.history_file is not None
        assert persistence_service.metadata_cache is not None

    def test_load_empty_history(self, persistence_service: PersistenceService) -> None:
        """Testa carregamento de histórico vazio."""
        history = persistence_service.load_history()
        assert isinstance(history, list)
        assert len(history) == 0

    def test_save_and_load_history(
        self,
        persistence_service: PersistenceService,
    ) -> None:
        """Testa salvar e carregar histórico."""
        from datetime import datetime

        from src.models import Media, MediaMetadata

        metadata = MediaMetadata(
            title="Test Video",
            duration=300,
            uploader="Test User",
            upload_date="2024-01-01",
            thumbnail_url="http://example.com/thumb.jpg",
            video_id="test_id",
        )

        media = Media(
            file_path=Path("/tmp/test.mp3"),
            media_type=MediaType.AUDIO,
            metadata=metadata,
            file_size=5000000,
            downloaded_at=datetime.now(),
        )

        assert persistence_service.save_media(media)

        history = persistence_service.load_history()
        assert len(history) == 1
        assert history[0].metadata.title == "Test Video"


class TestDownloadTask:
    """Testes para DownloadTask."""

    def test_creation(self) -> None:
        """Testa criação de DownloadTask."""
        task = DownloadTask(
            url="https://youtube.com/watch?v=test",
            media_type=MediaType.AUDIO,
        )

        assert task.url == "https://youtube.com/watch?v=test"
        assert task.media_type == MediaType.AUDIO
        assert task.status == DownloadStatus.PENDING
        assert task.progress_percentage == 0.0

    def test_progress_update(self) -> None:
        """Testa atualização de progresso."""
        task = DownloadTask(
            url="https://youtube.com/watch?v=test",
            media_type=MediaType.VIDEO,
        )

        task.progress_percentage = 50.0
        task.current_file_size = 50_000_000
        task.total_file_size = 100_000_000

        assert task.progress_percentage == 50.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
