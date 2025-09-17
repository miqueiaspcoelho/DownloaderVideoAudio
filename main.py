# main.py
from downloader import YoutubeDownloader

def main():
    print("YouTube Downloader (yt_dlp)\n")
    url = input("Cole a URL do video: ").strip()
    print("\nPlaylist ?")
    print("1 - Sim")
    print("2 - Nao")
    playlist = input("Digite 1 ou 2: ").strip()
    if playlist == '1':
        playlist = False
    elif playlist == '2':
        playlist = True
    else:
        print("Opcao invalida")
        exit()

    downloader = YoutubeDownloader(url, playlist)

    print("\nO que deseja baixar?")
    print("1 - Video")
    print("2 - Musica (MP3)")

    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == '1':
        downloader.videoDownload()
    elif escolha == '2':
        downloader.audioDownload()
    else:
        print("Opcaoo invalida.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
