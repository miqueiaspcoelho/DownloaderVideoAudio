"""
PersistenceService - Gerenciamento de histórico persistente.

Salva e carrega informações sobre downloads em JSON local.
"""

import json
from datetime import datetime
from pathlib import Path

from src.core import get_logger
from src.models import Media, MediaMetadata, MediaType

logger = get_logger(__name__)


class PersistenceService:
    """Serviço de persistência de dados locais."""

    def __init__(self, data_dir: Path | None = None) -> None:
        """
        Inicializa o serviço de persistência.

        Args:
            data_dir: Diretório para armazenar dados. Se None, usa .data/ do projeto.
        """
        self.data_dir = data_dir or (Path.cwd() / ".data")
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "download_history.json"
        self.metadata_cache = self.data_dir / "metadata_cache.json"

    def save_media(self, media: Media) -> bool:
        """
        Salva informações de uma mídia no histórico.

        Args:
            media: Instância de Media.

        Returns:
            True se salvo com sucesso.
        """
        try:
            history = self._load_history()

            media_dict = {
                "file_path": str(media.file_path),
                "media_type": media.media_type.value,
                "title": media.metadata.title,
                "duration": media.metadata.duration,
                "uploader": media.metadata.uploader,
                "video_id": media.metadata.video_id,
                "file_size": media.file_size,
                "downloaded_at": media.downloaded_at.isoformat(),
                "thumbnail_path": str(media.thumbnail_path) if media.thumbnail_path else None,
            }

            history.append(media_dict)
            self._save_history(history)

            logger.info(f"Mídia salva no histórico: {media.metadata.title}")
            return True

        except Exception as e:
            logger.error(f"Erro ao salvar mídia: {e}")
            return False

    def load_history(self) -> list[Media]:
        """
        Carrega todo o histórico de downloads.

        Returns:
            Lista de Media objetos.
        """
        try:
            history = self._load_history()
            media_list = []

            for item in history:
                media = Media(
                    file_path=Path(item["file_path"]),
                    media_type=MediaType(item["media_type"]),
                    metadata=MediaMetadata(
                        title=item["title"],
                        duration=item["duration"],
                        uploader=item["uploader"],
                        upload_date=None,
                        thumbnail_url="",
                        video_id=item["video_id"],
                    ),
                    file_size=item["file_size"],
                    downloaded_at=datetime.fromisoformat(item["downloaded_at"]),
                    thumbnail_path=(
                        Path(item["thumbnail_path"]) if item.get("thumbnail_path") else None
                    ),
                )
                media_list.append(media)

            return media_list

        except Exception as e:
            logger.error(f"Erro ao carregar histórico: {e}")
            return []

    def cache_metadata(self, url: str, metadata: MediaMetadata) -> bool:
        """
        Cacheia metadados de um vídeo.

        Args:
            url: URL do vídeo.
            metadata: MediaMetadata.

        Returns:
            True se cacheado com sucesso.
        """
        try:
            cache = self._load_cache()

            cache[url] = {
                "title": metadata.title,
                "duration": metadata.duration,
                "uploader": metadata.uploader,
                "video_id": metadata.video_id,
                "thumbnail_url": metadata.thumbnail_url,
                "cached_at": datetime.now().isoformat(),
            }

            self._save_cache(cache)
            return True

        except Exception as e:
            logger.error(f"Erro ao cachear metadados: {e}")
            return False

    def get_cached_metadata(self, url: str) -> MediaMetadata | None:
        """
        Obtém metadados em cache.

        Args:
            url: URL do vídeo.

        Returns:
            MediaMetadata se encontrado, None caso contrário.
        """
        try:
            cache = self._load_cache()

            if url in cache:
                item = cache[url]
                return MediaMetadata(
                    title=item["title"],
                    duration=item["duration"],
                    uploader=item["uploader"],
                    upload_date=None,
                    thumbnail_url=item["thumbnail_url"],
                    video_id=item["video_id"],
                )

            return None

        except Exception:
            return None

    def _load_history(self) -> list[dict]:
        """Carrega o arquivo de histórico."""
        if self.history_file.exists():
            with open(self.history_file, encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_history(self, history: list[dict]) -> None:
        """Salva o arquivo de histórico."""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    def _load_cache(self) -> dict:
        """Carrega o cache de metadados."""
        if self.metadata_cache.exists():
            with open(self.metadata_cache, encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self, cache: dict) -> None:
        """Salva o cache de metadados."""
        with open(self.metadata_cache, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
