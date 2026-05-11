# YouTube Media Downloader

Aplicacao desktop em Python para baixar videos e audios do YouTube com interface grafica em PySide6, downloads assincronos e biblioteca local de midias.

## Funcionalidades

- Download de videos em MP4 usando yt-dlp.
- Download de audios com conversao para MP3 quando FFmpeg esta disponivel.
- Fallback para formatos ja baixados pelo yt-dlp quando FFmpeg nao esta acessivel ao processo.
- Barra circular de progresso na aba Downloads.
- Interface desktop com abas: Downloads, Audios e Videos.
- Biblioteca local com cards para arquivos baixados e arquivos adicionados manualmente nas pastas.
- Scan automatico de `~/Downloads/audio` e `~/Downloads/video` ao iniciar.
- Miniaturas baixadas e armazenadas localmente quando disponiveis.
- Historico persistente em JSON.
- Logs centralizados em `logs/app.log`.
- Campo de URL, escolha Audio/Video e checkbox de Playlist na interface.

## Stack

- Python 3.14+
- PySide6
- yt-dlp
- FFmpeg
- Pillow
- requests
- JSON local
- Ruff, Black, MyPy e pytest

## Estrutura

```text
.
+-- app.py
+-- main.py
+-- pyproject.toml
+-- pytest.ini
+-- README.md
+-- .data/
|   +-- download_history.json
+-- logs/
|   +-- app.log
+-- src/
|   +-- core/
|   |   +-- logger.py
|   +-- models/
|   |   +-- media.py
|   +-- services/
|   |   +-- download.py
|   |   +-- filesystem.py
|   |   +-- persistence.py
|   |   +-- thumbnail.py
|   +-- ui/
|   |   +-- main_window.py
|   |   +-- widgets.py
|   +-- workers/
|       +-- download_worker.py
+-- tests/
    +-- test_services.py
```

## Instalacao

Crie e use o ambiente virtual do projeto:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

O projeto exige FFmpeg para mesclar video+audio e converter audio para MP3. No Windows, o app tenta localizar automaticamente:

- `FFMPEG_LOCATION`
- `FFMPEG_BINARY`
- `ffmpeg` no `PATH`
- `C:/ffmpeg*/bin`

Exemplo opcional:

```powershell
$env:FFMPEG_LOCATION="C:\ffmpeg-8.1.1-essentials_build\bin"
```

## Executar

```powershell
.venv\Scripts\python.exe main.py
```

## Como Usar

1. Cole uma URL do YouTube.
2. Escolha `Audio (MP3)` ou `Video (MP4)`.
3. Marque `Playlist` se aplicavel.
4. Clique em `Baixar`.
5. Acompanhe o progresso na aba Downloads.
6. Veja os arquivos nas abas Audios e Videos.

## Diretorios

Os downloads usam a pasta padrao do usuario:

```text
~/Downloads/audio/
~/Downloads/video/
~/Downloads/.thumbnails/
```

Dados internos do app:

```text
.data/download_history.json
.data/metadata_cache.json
logs/app.log
```

Formatos escaneados pela biblioteca:

- Audios: `.mp3`, `.m4a`, `.webm`, `.opus`, `.wav`
- Videos: `.mp4`, `.mkv`, `.webm`, `.mov`

## Arquitetura

- `src/services`: regras de negocio, yt-dlp, FFmpeg, arquivos, thumbnails e persistencia.
- `src/workers`: execucao em `QThread` para nao travar a interface.
- `src/ui`: janela principal e widgets visuais.
- `src/models`: dataclasses e enums de dominio.
- `src/core`: logging centralizado.

## FFmpeg e Fallback

Quando FFmpeg e encontrado, o download de video usa melhor video + melhor audio e mescla em MP4.

Quando FFmpeg nao e encontrado pelo processo Python, o app evita o erro de merge do yt-dlp usando um formato unico (`b[ext=mp4]/best`). Para audio, a conversao para MP3 depende do FFmpeg; sem ele, o arquivo baixado pode permanecer em outro formato suportado pela biblioteca local.

## Testes e Qualidade

```powershell
.venv\Scripts\python.exe -m pytest --basetemp .pytest_tmp -o cache_dir=.pytest_cache_run
.venv\Scripts\python.exe -m ruff check src tests
.venv\Scripts\python.exe -m black --check src tests
```

Status atual: 13 testes passando.

Em alguns ambientes Windows, o pytest pode nao conseguir criar temporarios em `AppData\Local\Temp`; por isso o comando acima usa `--basetemp .pytest_tmp`.

## Desenvolvimento

Formatar:

```powershell
.venv\Scripts\python.exe -m black src tests
```

Lint:

```powershell
.venv\Scripts\python.exe -m ruff check src tests
```

Type check:

```powershell
.venv\Scripts\python.exe -m mypy src
```

## Licenca

MIT
