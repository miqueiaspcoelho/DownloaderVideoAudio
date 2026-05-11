Com base na **Constituição Técnica**, na **Memória Persistente** e na **Especificação**, elaborei o plano de ação estruturado para o desenvolvimento do **YouTube Media Downloader**.

O foco será garantir a separação entre a lógica de download (serviços) e a interface (PySide6), mantendo o sistema responsivo via threads.

---

## 🚀 Plano de Ação: YouTube Media Downloader

### Fase 1: Setup e Infraestrutura (Fundação)

O objetivo aqui é garantir que o ambiente siga as regras inegociáveis de isolamento e tipagem.

1. **Ambiente Virtual:** Criar `.venv` e instalar dependências fixas (`yt-dlp`, `PySide6`, `pillow`, `ruff`, `black`, `mypy`).
2. **Estrutura de Diretórios:** Montar a árvore `src/` conforme a Constituição (core, services, ui, workers, models).
3. **Configuração de Qualidade:** Inicializar o `pyproject.toml` com as regras do Ruff e Black.
4. **Sistema de Logs:** Implementar o módulo de logging centralizado gravando em `logs/`.

### Fase 2: Camada de Domínio e Serviços (O Motor)

Desenvolvimento da lógica de negócio pura, sem interferência da UI.

1. **FileSystemService:** Criar lógica para gerenciar `~/Downloads/audio`, `video` e `.thumbnails`.
2. **DownloadService:**
* Integrar `yt-dlp` para extração de metadados.
* Implementar lógica de download para MP4 (melhor qualidade) e MP3 (via FFmpeg).


3. **ThumbnailService:** Implementar download e processamento de miniaturas via `Pillow`.
4. **PersistenceService:** Criar o gerenciador de JSON local para o histórico de arquivos.

### Fase 3: Concorrência e Workers (A Fluidez)

Garantir o requisito crítico: a interface não pode travar.

1. **DownloadWorker:** Criar classe herdando de `QRunnable` ou `QThread`.
2. **Sinais (Signals):** Definir sinais para reportar progresso (`percentage`), status (`state`) e finalização ou erro para a UI.

### Fase 4: Interface Gráfica - UI (A Experiência)

Construção visual com PySide6 seguindo a estética de cores pastéis e bordas arredondadas.

1. **MainWindow:** Implementar a janela principal (1200x800, centralizada).
2. **Navegação por Abas:** Criar as abas "Downloads", "Áudios" e "Vídeos".
3. **Custom Widgets:**
* **ProgressCircle:** Componente circular animado para o progresso.
* **MediaCard:** Widget para exibir thumbnail, título e metadados.


4. **Aba de Input:** Campo de URL, Radio Buttons (Áudio/Vídeo) e Checkbox de Playlist.

### Fase 5: Integração e Biblioteca (O Fechamento)

Unir o motor à carcaça e validar o fluxo do usuário.

1. **Auto-Scan:** Implementar a função que lê as pastas de download ao iniciar e popula as abas.
2. **Fluxo de Update:** Garantir que, ao finalizar um download, o novo `MediaCard` apareça instantaneamente na aba correta.
3. **Tratamento de Erros:** Validar URLs e exibir mensagens amigáveis em caso de falha de conexão ou conversão.

---

## 🛠️ Regras de Implementação Imediata

* **Nomenclatura:** Funções em `camelCase`, variáveis em `snake_case`, classes em `PascalCase`.
* **Tipagem:** Uso obrigatório de `Type Hints` em todas as novas funções.
* **Commits:** Seguir o padrão semântico (ex: `feat:`, `fix:`, `refactor:`).