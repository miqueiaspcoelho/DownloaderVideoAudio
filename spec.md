# Especificação Técnica Objetiva — YouTube Media Downloader

# 1. Objetivo

Desenvolver um software desktop em Python 3.14+ para download de vídeos e músicas do YouTube utilizando a biblioteca yt-dlp.

O sistema deve permitir:

* Download de vídeos
* Download de áudios
* Download individual
* Download de playlists
* Visualização dos arquivos baixados
* Interface gráfica moderna e responsiva
* Execução assíncrona sem travar a interface

---

# 2. Stack Tecnológica

## Linguagem

* Python 3.14+

---

## Interface Gráfica

### Biblioteca escolhida:

* PySide6

### Motivos:

* Interface moderna
* Excelente responsividade
* Fácil criação de abas, cards e animações
* Suporte robusto a threads
* Boa estilização visual

---

## Download

### Biblioteca:

* yt-dlp

---

## Conversão de mídia

### Biblioteca:

* FFmpeg

---

## Imagens e thumbnails

### Biblioteca:

* Pillow

---

# 3. Estrutura de Pastas

## Diretórios do projeto

```text id="r2mxw3"
project_root/
│
├── src/
├── tests/
├── assets/
├── logs/
├── .venv/
├── pyproject.toml
└── README.md
```

---

# 4. Diretórios de Download

## Regra obrigatória

Os downloads DEVEM utilizar a pasta padrão do sistema operacional do usuário.

---

## Caminhos obrigatórios

### Áudios

```text id="g6u3j6"
~/Downloads/audio/
```

---

### Vídeos

```text id="zyw6c4"
~/Downloads/video/
```

---

## Regras

* Caso as pastas não existam, o sistema deve criá-las automaticamente.
* O caminho deve funcionar tanto em Windows quanto Linux.
* Utilizar `Path.home()` + `Downloads`.

---

# 5. Funcionalidades Principais

# 5.1 Download

O usuário deve poder:

* Inserir URL
* Escolher:

  * áudio
  * vídeo
* Selecionar:

  * playlist
  * conteúdo único

---

# 5.2 Download de Áudio

## Regras

* Converter automaticamente para MP3
* Melhor qualidade disponível
* Salvar em:

```text id="huc4z2"
Downloads/audio/
```

---

# 5.3 Download de Vídeo

## Regras

* Preferência por MP4
* Melhor qualidade disponível
* Salvar em:

```text id="8q3i0d"
Downloads/video/
```

---

# 6. Interface Gráfica

# 6.1 Janela Principal

## Requisitos

* NÃO abrir em tela cheia
* Deve abrir centralizada
* Deve ser redimensionável
* Interface responsiva

---

## Tamanho inicial sugerido

```text id="yjlwm4"
1200x800
```

---

# 6.2 Visual

## Requisitos UX/UI

* Layout moderno
* Visual limpo
* Sem excesso de informação
* Navegação intuitiva

---

## Estilo visual

* Cores pastéis
* Bordas arredondadas
* Sombras suaves
* Espaçamentos consistentes
* Ícones claros

---

# 6.3 Navegação

## Abas obrigatórias

### Aba 1

```text id="6bj5go"
Downloads
```

### Aba 2

```text id="r8mvf6"
Áudios
```

### Aba 3

```text id="aq9p5l"
Vídeos
```

---

# 7. Área de Download

# Componentes obrigatórios

## Campo URL

* Input único
* Placeholder explicativo

Exemplo:

```text id="2f9yqm"
Cole aqui o link do YouTube
```

---

## Tipo de Download

### Radio buttons

* Áudio
* Vídeo

---

## Playlist

### Checkbox

* É playlist?

---

## Botão principal

### Texto:

```text id="1f00y5"
Baixar
```

---

## Regras UX

* Botão grande
* Fácil identificação
* Hover effect
* Sem ambiguidade

---

# 8. Sistema Assíncrono

# Requisito crítico

A interface NÃO pode travar durante downloads.

---

# Implementação obrigatória

Utilizar:

* QThread
  OU
* QRunnable + QThreadPool

---

# 9. Barra de Progresso

# Requisitos

* Formato circular
* Atualização em tempo real
* Animação suave

---

## Informações exibidas

* Porcentagem aproximada
* Estado atual do download

---

## Exemplos

```text id="5hgw12"
Baixando...
42%
```

---

# 10. Estados do Download

## Estados obrigatórios

* Preparando
* Baixando
* Convertendo
* Finalizado
* Erro

---

# 11. Mensagens do Sistema

# 11.1 Sucesso

## Exemplo

```text id="n4v8a8"
Download concluído com sucesso.
```

---

# 11.2 Erros

## Obrigatório

Mensagens claras e explicativas.

---

## Proibido

```text id="3o1h6r"
Erro desconhecido
```

---

## Exemplos válidos

```text id="2glr4e"
Não foi possível acessar o vídeo.
```

```text id="7lq8fw"
URL inválida.
```

```text id="q91f20"
Falha ao converter o áudio.
```

---

# 12. Biblioteca de Arquivos Baixados

# 12.1 Verificação Automática

O sistema deve:

* Ler automaticamente:

  * `Downloads/audio`
  * `Downloads/video`

---

## Atualizações automáticas

* Ao iniciar o sistema
* Após concluir downloads
* Após remoções de arquivos

---

# 12.2 Exibição dos Arquivos

## Formato

* Cards estilo YouTube
* Grid responsivo
* Scroll suave

---

## Cards de vídeo

Devem mostrar:

* Thumbnail
* Nome
* Resolução
* Data do download

---

## Cards de áudio

Devem mostrar:

* Thumbnail
* Nome
* Duração
* Data do download

---

# 13. Miniaturas

# Requisitos

* Baixar thumbnail automaticamente
* Armazenar localmente
* Associar thumbnail ao arquivo

---

## Diretório sugerido

```text id="cix6mj"
Downloads/.thumbnails/
```

---

# 14. Persistência de Dados

## Solução recomendada

* JSON local simples

---

## Estrutura recomendada

```json id="n83q8t"
{
  "title": "",
  "type": "",
  "file_path": "",
  "thumbnail_path": "",
  "download_date": ""
}
```

---

# 15. Arquitetura

# Separação obrigatória

## UI

Responsável apenas pela interface.

---

## Services

Responsável por:

* yt-dlp
* ffmpeg
* thumbnails
* gerenciamento de arquivos

---

## Workers

Responsável por:

* downloads assíncronos
* threads

---

## Models

Responsável por:

* entidades
* estruturas de dados

---

# 16. Logging

# Obrigatório

* Utilizar módulo `logging`
* Salvar logs localmente

---

## Diretório

```text id="18ckw0"
logs/
```

---

# 17. Ambiente Virtual

# Obrigatório

```bash id="v4k3zf"
python -m venv .venv
```

---

# Instalação

```bash id="u9trvx"
pip install -r requirements/dev.txt
```

---

# 18. Dependências Principais

```text id="wj7b8u"
yt-dlp
PySide6
pillow
ffmpeg-python
ruff
black
mypy
```

---

# 19. Testes

## Estratégia

Aplicar apenas testes essenciais.

---

## Testes recomendados

* validação de URL
* criação automática de diretórios
* serviços de download

---

## Não obrigatório

* testes complexos de interface
* cobertura extensa

---

# 20. Compatibilidade

## Sistemas suportados

* Windows
* Linux

---

# 21. Fluxo do Usuário

## Fluxo esperado

1. Usuário cola URL
2. Seleciona:

   * áudio ou vídeo
3. Marca:

   * playlist ou não
4. Clica em baixar
5. Download inicia em thread separada
6. Barra circular atualiza progresso
7. Download finaliza
8. Sistema atualiza automaticamente:

   * aba de vídeos
   * aba de áudios
9. Usuário visualiza o conteúdo baixado

---

# 22. Requisitos Inegociáveis

## O sistema NÃO pode:

* Travar durante downloads
* Exibir erros genéricos
* Misturar UI com lógica de negócio
* Utilizar downloads fora da pasta Downloads do usuário
* Fazer instalação global de dependências

---

# 23. Critérios de Qualidade

O projeto deve priorizar:

1. Simplicidade
2. UX intuitiva
3. Responsividade
4. Clareza visual
5. Código modular
6. Facilidade de manutenção
7. Escalabilidade futura
