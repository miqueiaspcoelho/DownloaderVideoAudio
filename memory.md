# Memória Persistente do Projeto — YouTube Media Downloader

## Objetivo

Este documento funciona como uma janela de contexto persistente para agentes de IA e LLMs utilizados dentro da IDE.

Sua finalidade é:

* Evitar releitura completa do projeto
* Reduzir consumo de tokens
* Preservar decisões arquiteturais
* Garantir consistência técnica
* Manter padrões de desenvolvimento
* Servir como cache semântico do projeto

O modelo deve consultar esta memória antes de analisar arquivos do projeto.

---

# Identidade do Projeto

## Nome

YouTube Media Downloader

---

## Objetivo Principal

Software desktop em Python 3.14+ para download de vídeos e músicas do YouTube utilizando yt-dlp.

O sistema deve:

* baixar vídeos
* baixar áudios
* suportar playlists
* possuir interface moderna
* não travar durante downloads
* mostrar biblioteca local de mídias

---

# Stack Oficial

## Linguagem

* Python 3.14+

## UI

* PySide6

## Download

* yt-dlp

## Conversão de mídia

* FFmpeg

## Imagens

* Pillow

---

# Regras Arquiteturais

## Obrigatório

* arquitetura modular
* separação de responsabilidades
* código coeso
* baixo acoplamento
* funções pequenas
* tipagem estática
* uso de classes
* uso de serviços
* uso de workers para tarefas assíncronas

---

# Convenções de Código

## Variáveis

Sempre usar:

snake_case

Exemplo:

* video_path
* download_progress

---

## Funções

Sempre usar: camelCase (internamente) ou snake_case (em Python)

Exemplo:
* def download_video()
* def get_thumbnail()

---

# Status de Implementação

## ✅ Completo (Fase 1 - Setup)

- [x] Estrutura de diretórios criada (src/, tests/, assets/, logs/)
- [x] Dependências instaladas (yt-dlp, PySide6, Pillow, FFmpeg, ruff, black, mypy)
- [x] pyproject.toml configurado com regras de lint/format
- [x] Logger centralizado (src/core/logger.py)

## ✅ Completo (Fase 2 - Serviços)

- [x] FileSystemService: gerencia ~/Downloads/audio, ~/Downloads/video, ~/.thumbnails
- [x] DownloadService: integração yt-dlp com metadados e progresso
- [x] ThumbnailService: download e processamento com Pillow
- [x] PersistenceService: histórico em JSON (.data/download_history.json)

## ✅ Completo (Fase 3 - Workers)

- [x] DownloadWorker: QObject para execução assíncrona
- [x] DownloadThread: QThread para download sem travar UI
- [x] Sinais: progress_updated, download_completed, download_failed

## ✅ Completo (Fase 4 - UI)

- [x] ProgressCircle: widget circular animado com percentual
- [x] MediaCard: card com thumbnail, título, metadados
- [x] MainWindow: 1200x800, centrada, pastéis (lilás #c896dc)
- [x] Abas: Downloads (ativos), Áudios, Vídeos
- [x] Input: URL field, radio (Áudio/Vídeo), checkbox (Playlist)

## ✅ Completo (Fase 5 - Integração)

- [x] Validação de URLs (youtube.com / youtu.be)
- [x] Tratamento robusto de erros com logging
- [x] Testes unitários (✅ 13 testes passando)
  - FileSystemService (4 testes)
  - DownloadService (2 testes)  
  - ThumbnailService (2 testes)
  - PersistenceService (3 testes)
  - DownloadTask (2 testes)
- [x] Documentação completa (README.md)
- [x] Carregamento automático de histórico ao iniciar
- [x] Fluxo de update dinâmico (novo card na aba)
- [x] pytest.ini e estrutura de testes

---

# Bug Fixes

## ✅ Progress UI, FFmpeg e Auto-Scan da Biblioteca

**Problemas corrigidos**:
- Progresso de download era emitido pelo worker, mas a UI apenas registrava logs.
- Download de video podia falhar alegando FFmpeg ausente quando o processo Python nao recebia a localizacao explicitamente.
- Arquivos adicionados manualmente em `~/Downloads/video` ou `~/Downloads/audio` nao apareciam como cards porque a UI lia apenas o historico JSON.
- Cards de audio quebravam por typo (`audios_cards` inexistente).

**Solucoes implementadas**:
1. `src/ui/main_window.py` agora cria item visual na aba Downloads ao iniciar e atualiza `ProgressCircle` por sinal de progresso.
2. `src/services/download.py` localiza `ffmpeg` com `FFMPEG_LOCATION`, `FFMPEG_BINARY`, `shutil.which()` e fallback para instalacoes comuns em `C:/ffmpeg*/bin`; passa `ffmpeg_location` ao yt-dlp quando encontrado.
3. Download de video usa formato preferencial MP4 compativel: `bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/best` e `merge_output_format="mp4"`.
4. `src/ui/main_window.py` combina historico persistido com scan das pastas locais ao iniciar.
5. `src/services/filesystem.py` lista audios locais com extensoes `mp3`, `m4a`, `webm`, `opus` e `wav`, e videos locais com extensoes `mp4`, `mkv`, `webm` e `mov`.
6. Se FFmpeg nao for localizado, download de video usa fallback de formato unico (`b[ext=mp4]/best`) para evitar erro de merge; com FFmpeg localizado, mantem melhor video+audio.

**Validacao**:
- `pytest --basetemp .pytest_tmp -o cache_dir=.pytest_cache_run`: 13 testes passando.
- `ruff check src tests`: OK.
- `black --check src tests`: OK.

**Observacao**: em sandbox Windows, o pytest pode falhar ao usar `AppData\\Local\\Temp`; usar `--basetemp .pytest_tmp` evita o problema.

## ✅ Thread Cleanup - "destroyed while thread is still running"

**Problema**: Ao fechar a aplicação enquanto downloads estavam rodando, PySide6 geraria erro de thread destruída enquanto rodava.

**Solução implementada** em `src/ui/main_window.py`:
1. Adicionado `self.active_threads: list[DownloadThread]` para rastrear threads ativas
2. Armazenar referência da thread ao criar: `self.active_threads.append(thread)`
3. Remover da lista quando terminar: `_on_download_thread_finished(thread)`
4. Implementado `closeEvent()` que:
   - Aguarda todas as threads rodando com `thread.wait(timeout=5000)`
   - Chama `thread.quit()` para parar gracefully
   - Limpa lista de threads antes de fechar

**Status**: ✅ Resolvido - A aplicação agora fecha corretamente sem warnings

---

# Status Geral

## ✅ 100% Completo

Todas as 5 fases do plano foram implementadas com sucesso.

**Arquivos criados**: 18  
**Linhas de código**: ~2000+  
**Testes**: 13 (todos passando)  
**Documentação**: Completa  
**Bug Fixes**: 1 (Thread cleanup)

# Arquitetura de Pastas

```
src/
├── core/                 # Logger centralizado
│   ├── __init__.py
│   └── logger.py
├── models/              # Estruturas de dados
│   ├── __init__.py
│   └── media.py
├── services/            # Lógica de negócio
│   ├── __init__.py
│   ├── filesystem.py
│   ├── download.py
│   ├── thumbnail.py
│   └── persistence.py
├── workers/             # Concorrência (PySide6 threads)
│   ├── __init__.py
│   └── download_worker.py
├── ui/                  # Interface gráfica
│   ├── __init__.py
│   ├── widgets.py
│   └── main_window.py
└── __init__.py

app.py                   # Ponto de entrada (PySide6)
main.py                  # Wrapper para executar
```

---

# Pontos-Chave de Implementação

## FileSystemService
- Cria automaticamente ~/Downloads/{audio, video, .thumbnails}
- Métodos: get_audio_path(), get_video_path(), list_audio_files(), list_video_files()

## DownloadService
- yt-dlp integrado com hooks de progresso
- Suporta MP3 (com FFmpeg) e MP4 (melhor qualidade)
- Extrai metadados antes de download

## DownloadWorker/Thread
- Download ocorre fora da main thread
- Sinais PySide6 para atualizar UI (thread-safe)
- Progress: progress_updated → 0-100%

## MainWindow
- Estilo pastél (fundo #f5f5fa, botão lilás #c896dc)
- Abas:
  - Downloads: mostra tasks ativas com ProgressCircle
  - Áudios: MediaCards de MP3s
  - Vídeos: MediaCards de MP4s
- Input panel: URL + radio (áudio/vídeo) + checkbox (playlist)

## PersistenceService
- Histórico salvo em .data/download_history.json
- Cache de metadados em .data/metadata_cache.json
- Load automático ao iniciar app

camelCase iniciando com letra minúscula

Exemplo:

* startDownload()
* validateUrl()
* loadLibrary()

---

## Classes

Sempre usar:

PascalCase

Exemplo:

* DownloadService
* VideoCardWidget
* DownloadWorker

---

## Constantes

Sempre usar:

UPPER_SNAKE_CASE

Exemplo:

* DEFAULT_WINDOW_WIDTH
* MAX_RETRIES

---

# Diretórios de Download

## Obrigatório

Usar SEMPRE a pasta Downloads do usuário.

### Áudios

~/Downloads/audio/

### Vídeos

~/Downloads/video/

---

# Regras de UI

## Interface

* moderna
* minimalista
* responsiva
* agradável visualmente
* cores pastéis
* botões claros
* UX intuitiva

---

## Janela

* NÃO fullscreen
* redimensionável
* iniciar centralizada
* tamanho inicial sugerido: 1200x800

---

## Abas obrigatórias

* Downloads
* Áudios
* Vídeos

---

# Downloads Assíncronos

## Regra crítica

A interface NÃO pode travar.

---

## Implementação obrigatória

Usar:

* QThread
  OU
* QRunnable + QThreadPool

---

# Barra de Progresso

## Requisitos

* circular
* animada
* atualização em tempo real
* mostrar porcentagem aproximada

---

# Biblioteca de Mídias

## Requisitos

O sistema deve:

* ler automaticamente arquivos locais
* atualizar biblioteca após download
* exibir cards estilo YouTube
* usar thumbnails

---

# Cards

## Vídeos

Devem exibir:

* thumbnail
* nome
* resolução
* data

## Áudios

Devem exibir:

* thumbnail
* nome
* duração
* data

---

# Tratamento de Erros

## Proibido

* erros genéricos
* except vazio
* falhas silenciosas

---

## Obrigatório

Mensagens claras.

Exemplos:

* URL inválida
* Falha ao converter áudio
* Não foi possível acessar o vídeo

---

# Logging

## Obrigatório

* usar logging
* salvar logs localmente
* evitar print()

---

# Ambiente Virtual

## Obrigatório

Toda dependência deve ser instalada em:

```bash
python -m venv .venv
```

---

# Dependências Oficiais

* yt-dlp
* PySide6
* pillow
* ffmpeg-python
* ruff
* black
* mypy

---

# Qualidade de Código

## Obrigatório

* SOLID
* DRY
* KISS
* YAGNI

---

# Proibições

## Nunca fazer

* lógica de negócio na UI
* funções gigantes
* arquivos monolíticos
* código duplicado
* dependências circulares
* instalação global de pacotes
* travar interface principal

---

# Estratégia de Leitura para LLM

Antes de analisar qualquer arquivo:

1. Ler esta memória
2. Inferir arquitetura atual
3. Consultar apenas arquivos necessários
4. Evitar releitura completa do projeto
5. Preservar padrões já definidos

---

# Estratégia de Geração de Código

Todo código novo deve:

* respeitar arquitetura existente
* ser modular
* possuir nomes claros
* ser desacoplado
* possuir responsabilidade única
* evitar complexidade desnecessária

---

# Estratégia de Evolução

Novas funcionalidades devem:

* ser implementadas em novos módulos
* evitar alterar módulos estáveis
* preservar compatibilidade visual
* manter UX consistente
* reutilizar componentes existentes

---

# Regra Suprema

Se existir conflito entre implementação rápida e qualidade arquitetural:

A qualidade arquitetural deve prevalecer.
