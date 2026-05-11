"""
MainWindow - Janela principal da aplicação.

Interface gráfica com abas para downloads, áudios e vídeos.
"""

from datetime import datetime
from pathlib import Path

from PySide6.QtGui import QCloseEvent, QFont
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import get_logger
from src.models import DownloadStatus, DownloadTask, Media, MediaMetadata, MediaType
from src.services import (
    DownloadService,
    FileSystemService,
    PersistenceService,
    ThumbnailService,
)
from src.ui.widgets import MediaCard, ProgressCircle
from src.workers import DownloadThread, DownloadWorker

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """Janela principal da aplicação."""

    def __init__(self) -> None:
        """Inicializa a janela principal."""
        super().__init__()
        self.setWindowTitle("YouTube Media Downloader")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self._get_stylesheet())

        # Inicializa serviços
        self.fs_service = FileSystemService()
        self.download_service = DownloadService(self.fs_service)
        self.thumbnail_service = ThumbnailService(self.fs_service)
        self.persistence_service = PersistenceService()

        # Inicializa worker
        self.download_worker = DownloadWorker(
            self.fs_service,
            self.download_service,
            self.thumbnail_service,
            self.persistence_service,
        )
        self.download_worker.progress_updated.connect(self._on_progress_updated)
        self.download_worker.download_completed.connect(self._on_download_completed)
        self.download_worker.download_failed.connect(self._on_download_failed)

        # Estado da aplicação
        self.active_downloads: dict[str, DownloadTask] = {}
        self.download_progress_circles: dict[str, ProgressCircle] = {}
        self.download_status_labels: dict[str, QLabel] = {}
        self.media_list: list[Media] = []
        self.audio_cards: list[MediaCard] = []
        self.video_cards: list[MediaCard] = []
        self.active_threads: list[DownloadThread] = []

        # Constrói a UI
        self._build_ui()
        self._load_media_library()

    def _build_ui(self) -> None:
        """Constrói a interface gráfica."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título
        title = QLabel("YouTube Media Downloader")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        layout.addWidget(title)

        # Painel de entrada
        self._build_input_panel(layout)

        # Abas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #f5f5fa;
                border: none;
                padding: 8px 20px;
                margin-right: 2px;
                border-radius: 8px 8px 0px 0px;
                color: #000000;

            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #403AED;
                color: #000000;
            }
        """)

        # Aba de Downloads
        self.downloads_tab = QWidget()
        self.tabs.addTab(self.downloads_tab, "Downloads")

        self._build_downloads_tab()

        # Aba de Áudios
        self.audios_tab = QWidget()
        self.tabs.addTab(self.audios_tab, "Áudios")
        self._build_audios_tab()

        # Aba de Vídeos
        self.videos_tab = QWidget()
        self.tabs.addTab(self.videos_tab, "Vídeos")
        self._build_videos_tab()

        layout.addWidget(self.tabs)

    def _build_input_panel(self, layout: QVBoxLayout) -> None:
        """Constrói o painel de entrada."""
        panel = QWidget()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)

        radio_style = """
            QRadioButton {
                color: #000000;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border-radius: 7px;
                border: 1px solid #403AED;
                background-color: transparent;
            }
            QRadioButton::indicator:checked {
                background-color: #3A6FED;
                border: 1px solid #403AED;
            }
            QRadioButton::indicator:unchecked {
                background-color: transparent;
                border: 1px solid #403AED;
            }
        """

        checkbox_style = """
            QCheckBox {
                color: #000000;
                font-size: 10pt;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1px solid #403AED;
                border-radius: 4px;
                background-color: transparent;
                color: #000000;
            }
            QCheckBox::indicator:checked {
                background-color: #3A6FED;
                border: 1px solid #403AED;
            }
        """
        # URL input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        url_label.setFont(QFont("Arial", 10))
        url_layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole a URL do YouTube aqui...")
        self.url_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
                font-size: 10pt;
                color: #000000;
            }
        """)
        url_layout.addWidget(self.url_input)
        panel_layout.addLayout(url_layout)

        # Opções
        options_layout = QHBoxLayout()

        # Tipo de mídia
        type_group = QWidget()
        type_layout = QHBoxLayout(type_group)
        type_layout.setContentsMargins(0, 0, 0, 0)

        type_label = QLabel("Tipo:")
        type_layout.addWidget(type_label)

        self.audio_radio = QRadioButton("Áudio (MP3)")
        self.audio_radio.setStyleSheet(radio_style)

        self.audio_radio.setChecked(True)
        type_layout.addWidget(self.audio_radio)

        self.video_radio = QRadioButton("Vídeo (MP4)")
        self.video_radio.setStyleSheet(radio_style)
        type_layout.addWidget(self.video_radio)

        options_layout.addWidget(type_group)

        # Playlist
        self.playlist_checkbox = QCheckBox("Playlist")
        self.playlist_checkbox.setStyleSheet(checkbox_style)
        options_layout.addWidget(self.playlist_checkbox)

        # Botão de download
        self.download_button = QPushButton("Baixar")
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #3A6FED;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #403AED;
            }
            QPushButton:pressed {
                background-color: #7C3AED;
            }
        """)
        self.download_button.clicked.connect(self._on_download_clicked)
        options_layout.addWidget(self.download_button)

        panel_layout.addLayout(options_layout)
        layout.addWidget(panel)

    def _build_downloads_tab(self) -> None:
        """Constrói a aba de downloads."""
        layout = QVBoxLayout(self.downloads_tab)

        # Status de downloads ativos
        status_label = QLabel("Downloads Ativos:")
        status_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(status_label)

        self.downloads_scroll = QScrollArea()
        self.downloads_scroll.setWidgetResizable(True)
        self.downloads_scroll.setStyleSheet("QScrollArea { border: none; }")

        self.downloads_container = QWidget()
        self.downloads_layout = QVBoxLayout(self.downloads_container)
        self.downloads_layout.addStretch()

        self.downloads_scroll.setWidget(self.downloads_container)
        layout.addWidget(self.downloads_scroll)

    def _build_audios_tab(self) -> None:
        """Constrói a aba de áudios."""
        layout = QVBoxLayout(self.audios_tab)

        # Título
        title = QLabel("Seus Áudios")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Grid de cards
        self.audios_scroll = QScrollArea()
        self.audios_scroll.setWidgetResizable(True)
        self.audios_scroll.setStyleSheet("QScrollArea { border: none; }")

        self.audios_container = QWidget()
        self.audios_layout = QVBoxLayout(self.audios_container)
        self.audios_layout.setSpacing(10)
        self.audios_layout.addStretch()

        self.audios_scroll.setWidget(self.audios_container)
        layout.addWidget(self.audios_scroll)

    def _build_videos_tab(self) -> None:
        """Constrói a aba de vídeos."""
        layout = QVBoxLayout(self.videos_tab)

        # Título
        title = QLabel("Seus Vídeos")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)

        # Grid de cards
        self.videos_scroll = QScrollArea()
        self.videos_scroll.setWidgetResizable(True)
        self.videos_scroll.setStyleSheet("QScrollArea { border: none; }")

        self.videos_container = QWidget()
        self.videos_layout = QVBoxLayout(self.videos_container)
        self.videos_layout.setSpacing(10)
        self.videos_layout.addStretch()

        self.videos_scroll.setWidget(self.videos_container)
        layout.addWidget(self.videos_scroll)

    def _on_download_clicked(self) -> None:
        """Callback do botão de download."""
        url = self.url_input.text().strip()

        if not url:
            logger.warning("URL vazia fornecida")
            return

        if not self._is_valid_url(url):
            logger.error(f"URL inválida: {url}")
            return

        media_type = MediaType.AUDIO if self.audio_radio.isChecked() else MediaType.VIDEO
        task = DownloadTask(url=url, media_type=media_type)
        task.status = DownloadStatus.DOWNLOADING
        self._add_download_progress(task)

        # Inicia o download em thread
        thread = DownloadThread(self.download_worker, url, media_type)
        thread.finished.connect(lambda: self._on_download_thread_finished(thread))
        self.active_threads.append(thread)
        thread.start()

        self.url_input.clear()
        self.download_button.setEnabled(False)
        logger.info(f"Download iniciado: {url} ({media_type.value})")

    def _on_progress_updated(self, task: DownloadTask) -> None:
        """Callback de atualização de progresso."""
        if task.url not in self.download_progress_circles:
            self._add_download_progress(task)

        progress_circle = self.download_progress_circles[task.url]
        status_label = self.download_status_labels[task.url]
        progress_circle.set_progress(task.progress_percentage)
        status_label.setText(f"Baixando... {task.progress_percentage:.1f}%")
        logger.info(f"Progresso: {task.progress_percentage:.1f}%")

    def _on_download_completed(self, media: Media) -> None:
        """Callback de download completo."""
        logger.info(f"Download concluído: {media.metadata.title}")
        self.media_list.append(media)
        self._add_media_card(media)
        self._mark_last_download_finished("Finalizado")
        self.download_button.setEnabled(True)

    def _on_download_failed(self, url: str, error: Exception) -> None:
        """Callback de falha no download."""
        logger.error(f"Falha no download: {error}")
        if url in self.download_status_labels:
            self.download_status_labels[url].setText(f"Erro: {error}")
        self.download_button.setEnabled(True)

    def _on_download_thread_finished(self, thread: DownloadThread) -> None:
        """Callback quando thread de download termina."""
        if thread in self.active_threads:
            self.active_threads.remove(thread)
        logger.debug("Thread de download finalizada")

    def _add_download_progress(self, task: DownloadTask) -> None:
        """Adiciona um item visual para o progresso do download."""
        item = QWidget()
        item.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #eeeeee;
            }
        """)

        item_layout = QHBoxLayout(item)
        item_layout.setContentsMargins(12, 12, 12, 12)
        item_layout.setSpacing(12)

        progress_circle = ProgressCircle()
        status_label = QLabel(f"Preparando {task.media_type.value}...")
        status_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        status_label.setWordWrap(True)

        item_layout.addWidget(progress_circle)
        item_layout.addWidget(status_label, stretch=1)

        self.active_downloads[task.url] = task
        self.download_progress_circles[task.url] = progress_circle
        self.download_status_labels[task.url] = status_label
        self.downloads_layout.insertWidget(self.downloads_layout.count() - 1, item)

    def _mark_last_download_finished(self, status: str) -> None:
        """Marca o ultimo download ativo como concluido na UI."""
        if not self.download_status_labels:
            return

        last_url = next(reversed(self.download_status_labels))
        self.download_progress_circles[last_url].set_progress(100.0)
        self.download_status_labels[last_url].setText(status)

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Trata o fechamento da janela.

        Aguarda todas as threads terminarem antes de fechar.
        """
        logger.info("Fechando aplicação...")

        # Aguarda todas as threads terminarem
        for thread in self.active_threads:
            if thread.isRunning():
                logger.info("Aguardando threads...")
                thread.quit()
                thread.wait(timeout=5000)  # Aguarda 5 segundos

        # Limpa a lista
        self.active_threads.clear()

        # Aceita o evento de fechamento
        event.accept()
        logger.info("Aplicação finalizada")

    def _is_valid_url(self, url: str) -> bool:
        """
        Valida se a URL é válida (contém youtube.com ou youtu.be).

        Args:
            url: URL a validar.

        Returns:
            True se for uma URL válida do YouTube.
        """
        return "youtube.com" in url or "youtu.be" in url

    def _load_media_library(self) -> None:
        """Carrega a biblioteca de mídias já baixadas."""
        history_media = self.persistence_service.load_history()
        scanned_media = self._scan_download_folders(history_media)
        self.media_list = history_media + scanned_media

        for media in self.media_list:
            self._add_media_card(media)

    def _scan_download_folders(self, existing_media: list[Media]) -> list[Media]:
        """Le arquivos locais das pastas de download que ainda nao estao no historico."""
        known_paths = {
            media.file_path.resolve() for media in existing_media if media.file_path.exists()
        }
        scanned_media = []

        for audio_path in self.fs_service.list_audio_files():
            if audio_path.resolve() not in known_paths:
                scanned_media.append(self._create_local_media(audio_path, MediaType.AUDIO))

        for video_path in self.fs_service.list_video_files():
            if video_path.resolve() not in known_paths:
                scanned_media.append(self._create_local_media(video_path, MediaType.VIDEO))

        return scanned_media

    def _create_local_media(self, file_path: Path, media_type: MediaType) -> Media:
        """Cria uma midia local a partir de arquivo encontrado no disco."""
        metadata = MediaMetadata(
            title=file_path.stem,
            duration=0,
            uploader="Arquivo local",
            upload_date=None,
            thumbnail_url="",
            video_id=file_path.stem,
        )
        downloaded_at = datetime.fromtimestamp(file_path.stat().st_mtime)

        return Media(
            file_path=file_path,
            media_type=media_type,
            metadata=metadata,
            file_size=self.fs_service.get_file_size(file_path),
            downloaded_at=downloaded_at,
            thumbnail_path=None,
        )

    def _add_media_card(self, media: Media) -> None:
        """Adiciona um card de mídia à interface."""
        card = MediaCard()
        card.set_title(media.metadata.title)
        card.set_metadata(media.metadata.uploader, media.metadata.duration)
        card.set_thumbnail(media.thumbnail_path)

        if media.media_type == MediaType.AUDIO:
            self.audio_cards.append(card)
            self.audios_layout.insertWidget(self.audios_layout.count() - 1, card)
        else:
            self.video_cards.append(card)
            self.videos_layout.insertWidget(self.videos_layout.count() - 1, card)

    def _get_stylesheet(self) -> str:
        """Retorna o stylesheet da aplicação."""
        return """
            QMainWindow {
                background-color: #f5f5fa;
            }
            QWidget {
                background-color: #f5f5fa;
            }
            QLabel {
                color: #333333;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton {
                background-color: #c896dc;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b87acc;
            }
        """
