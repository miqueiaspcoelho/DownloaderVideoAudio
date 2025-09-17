# Youtube Donwloader (Video & Audio)

Ferramenta via cli para download de vídeos e/ou audios do youtube utilizando a lib yt_dlp

## Instalação
Necessário possuir interpretador python instalado
[python 3.8+](https://www.python.org/downloads/). Bem como pacote [ffmeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) para trabalhar com audio dos vídeos.

### Adicionar ffmeg ao path (windows)
- Extraia em uma pasta
- Dentro da pasta extraída, vá até:
    `` C:\ffmpeg\ffmpeg-<versao>\bin\ ``
- Copie esse caminho e adicione no PATH do sistema:
- Vá em: Painel de Controle → Sistema → Avançado → Variáveis de ambiente
- Em "Path", clique em editar e adicione:  `` C:\ffmpeg\ffmpeg-<versao>\bin\ ``

### Instalando Biblioteca yt_dlp
Considerando a correta instalação do python e gerenciador pip e adição ao PATH do sistema, rode no terminal o seguinte comando:
```bash
    pip install yt_dlp
```
    
## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/miqueiaspcoelho/DownloaderVideoAudio.git
```

Entre no diretório do projeto

```bash
  cd my-project
```

Rode o script

```bash
  python main.py
```


## Funcionalidades

- Donwload de Vídeos do youtube
- Donwload de Audios do youtube
- Definição se será baixado playlist ou vídeo/audio único
- Execução via linha de comando


## Documentação

O projeto está definido em dois arquivos:
- downloader.py 
    ``instancia a classe YoutubeDownloader que contem os métodos para download de video ou audio mediante uma url do youtube válida.``
- main.py 
    ``define a lógica principal do sistema, servindo de interface para adição dos parâmetros por meio do usuário``

Os arquivos são salvos automaticamente no diretório Downloads do computador do usário em duas subpastas (*Vídeos* => **Downloads/videos**; *Audio* => **Downloads/audios**)


## Melhorias

Posteriormente será lançado versão para destopk com interface gráfica para melhor experiência de usuário.

