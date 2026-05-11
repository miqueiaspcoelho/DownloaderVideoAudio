"""
Custom Widgets - Componentes visuais customizados.

ProgressCircle e MediaCard para exibição de mídia e progresso.
"""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ProgressCircle(QWidget):
    """Widget circular animado para exibir progresso."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inicializa o widget de progresso."""
        super().__init__(parent)
        self.progress = 0.0
        self.setMinimumSize(120, 120)
        self.setMaximumSize(120, 120)

        # Cores pastéis
        self.background_color = QColor(245, 245, 250)
        self.progress_color = QColor(200, 150, 220)  # Lilás suave
        self.text_color = QColor(100, 100, 120)

    def set_progress(self, value: float) -> None:
        """
        Define o progresso (0-100).

        Args:
            value: Percentual de progresso.
        """
        self.progress = min(100.0, max(0.0, value))
        self.update()

    def paintEvent(self, event) -> None:
        """Desenha o widget."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        center_x = width / 2
        center_y = height / 2
        radius = min(width, height) / 2 - 5

        # Fundo
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        # Círculo de fundo
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.background_color)
        painter.drawEllipse(
            int(center_x - radius), int(center_y - radius), int(radius * 2), int(radius * 2)
        )

        # Círculo de progresso
        painter.setPen(QPen(self.progress_color, 8, Qt.PenStyle.SolidLine))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        start_angle = 90 * 16
        span_angle = int(-(self.progress / 100.0) * 360 * 16)

        painter.drawArc(
            int(center_x - radius),
            int(center_y - radius),
            int(radius * 2),
            int(radius * 2),
            start_angle,
            span_angle,
        )

        # Texto de percentual
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self.text_color)

        text = f"{int(self.progress)}%"
        fm = painter.fontMetrics()
        text_width = fm.horizontalAdvance(text)
        text_height = fm.height()

        painter.drawText(
            int(center_x - text_width / 2),
            int(center_y + text_height / 4),
            text,
        )


class MediaCard(QWidget):
    """Card para exibir informações de mídia."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inicializa o card de mídia."""
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #f0f0f5;
            }
        """)
        self.setMinimumHeight(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Thumbnail
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setMinimumSize(170, 96)
        self.thumbnail_label.setStyleSheet("border-radius: 8px;")
        layout.addWidget(self.thumbnail_label)

        # Título
        self.title_label = QLabel()
        self.title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)

        # Metadados
        self.metadata_label = QLabel()
        self.metadata_label.setFont(QFont("Arial", 9))
        self.metadata_label.setStyleSheet("color: #888888;")
        layout.addWidget(self.metadata_label)

        layout.addStretch()

    def set_thumbnail(self, image_path: Path | None) -> None:
        """
        Define a imagem de thumbnail.

        Args:
            image_path: Caminho para a imagem.
        """
        if image_path and image_path.exists():
            pixmap = QPixmap(str(image_path))
            pixmap = pixmap.scaledToWidth(170, Qt.TransformationMode.SmoothTransformation)
            self.thumbnail_label.setPixmap(pixmap)
        else:
            self.thumbnail_label.setStyleSheet("background-color: #f0f0f5; border-radius: 8px;")
            self.thumbnail_label.setText("Sem imagem")

    def set_title(self, title: str) -> None:
        """
        Define o título.

        Args:
            title: Título da mídia.
        """
        self.title_label.setText(title)

    def set_metadata(self, uploader: str, duration: int) -> None:
        """
        Define os metadados.

        Args:
            uploader: Nome do criador.
            duration: Duração em segundos.
        """
        minutes = duration // 60
        seconds = duration % 60
        self.metadata_label.setText(f"{uploader} • {minutes}:{seconds:02d}")
