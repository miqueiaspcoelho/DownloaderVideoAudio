"""
FileSystemService - Gerenciamento de sistemas de arquivos.

Responsável por criar e gerenciar os diretórios de download.
"""

from pathlib import Path

from src.core import get_logger

logger = get_logger(__name__)

AUDIO_EXTENSIONS = ("*.mp3", "*.m4a", "*.webm", "*.opus", "*.wav")
VIDEO_EXTENSIONS = ("*.mp4", "*.mkv", "*.webm", "*.mov")


class FileSystemService:
    """Serviço de gerenciamento do sistema de arquivos."""

    def __init__(self) -> None:
        """Inicializa o serviço com os caminhos padrão."""
        self._downloads_base = Path.home() / "Downloads"
        self.audio_dir = self._downloads_base / "audio"
        self.video_dir = self._downloads_base / "video"
        self.thumbnails_dir = self._downloads_base / ".thumbnails"

        self._ensure_directories_exist()

    def _ensure_directories_exist(self) -> None:
        """Cria os diretórios de download se não existirem."""
        for directory in [self.audio_dir, self.video_dir, self.thumbnails_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório verificado/criado: {directory}")

    def get_audio_path(self, filename: str) -> Path:
        """
        Retorna o caminho completo para um arquivo de áudio.

        Args:
            filename: Nome do arquivo.

        Returns:
            Path completo para o arquivo.
        """
        return self.audio_dir / filename

    def get_video_path(self, filename: str) -> Path:
        """
        Retorna o caminho completo para um arquivo de vídeo.

        Args:
            filename: Nome do arquivo.

        Returns:
            Path completo para o arquivo.
        """
        return self.video_dir / filename

    def get_thumbnail_path(self, video_id: str) -> Path:
        """
        Retorna o caminho completo para uma miniatura.

        Args:
            video_id: ID do vídeo no YouTube.

        Returns:
            Path para o arquivo da miniatura.
        """
        return self.thumbnails_dir / f"{video_id}.jpg"

    def file_exists(self, file_path: Path) -> bool:
        """
        Verifica se um arquivo existe.

        Args:
            file_path: Caminho do arquivo.

        Returns:
            True se o arquivo existe, False caso contrário.
        """
        return file_path.exists() and file_path.is_file()

    def get_file_size(self, file_path: Path) -> int:
        """
        Obtém o tamanho de um arquivo em bytes.

        Args:
            file_path: Caminho do arquivo.

        Returns:
            Tamanho em bytes, ou 0 se o arquivo não existe.
        """
        if self.file_exists(file_path):
            return file_path.stat().st_size
        return 0

    def list_audio_files(self) -> list[Path]:
        """
        Lista todos os arquivos de áudio.

        Returns:
            Lista de Paths dos arquivos de áudio.
        """
        audio_files = []
        for pattern in AUDIO_EXTENSIONS:
            audio_files.extend(self.audio_dir.glob(pattern))
        return audio_files

    def list_video_files(self) -> list[Path]:
        """
        Lista todos os arquivos de vídeo.

        Returns:
            Lista de Paths dos arquivos de vídeo.
        """
        video_files = []
        for pattern in VIDEO_EXTENSIONS:
            video_files.extend(self.video_dir.glob(pattern))
        return video_files

    def delete_file(self, file_path: Path) -> bool:
        """
        Deleta um arquivo.

        Args:
            file_path: Caminho do arquivo.

        Returns:
            True se deletado com sucesso, False caso contrário.
        """
        try:
            if self.file_exists(file_path):
                file_path.unlink()
                logger.info(f"Arquivo deletado: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao deletar arquivo {file_path}: {e}")
            return False

    def get_downloads_base_path(self) -> Path:
        """
        Retorna o caminho base dos downloads.

        Returns:
            Path para o diretório base de downloads.
        """
        return self._downloads_base
