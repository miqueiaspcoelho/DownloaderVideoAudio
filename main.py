# main.py
from downloader import YoutubeDownloader


def main():
    print("YouTube Downloader (yt_dlp)\n")

    url = input("Cole a URL do video: ").strip()

    print("\nPlaylist?")
    print("1 - Sim")
    print("2 - Nao")

    playlist_input = input("Digite 1 ou 2: ").strip()

    if playlist_input == "1":
        playlist = True
    elif playlist_input == "2":
        playlist = False
    else:
        print("Opcao invalida")
        return

    downloader = YoutubeDownloader(url, playlist)

    print("\nO que deseja baixar?")
    print("1 - Video")
    print("2 - Musica (MP3)")

    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == "1":
        downloader.videoDownload()
    elif escolha == "2":
        downloader.audioDownload()
    else:
        print("Opcao invalida.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuario.")