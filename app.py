#imports
import customtkinter as ctk
from components import LabelComponent, EntryComponent, ButtonComponent, CheckboxComponent, RadioButtonComponent
from downloader import YoutubeDownloader
from functions import utils

#definições globais
ctk.set_appearance_mode('dark')
app = ctk.CTk()
app.title('Audio e Video Downloader')
app.geometry('600x300')

#FUNÇÃO PARA DOWNLOAD
def function_download()->None:
    """
    Cria, com base em verificações, um objeto para download de audio ou música
    com base em argumentos recebidos do frontend

        Args:
           None

        Returns:
            None
    """
    downloader = ''
    url = utils.function_get_url(entry_url)
    is_playlist = not utils.function_get_checkbox_playlist(checkbox_var_playlist)
    type_definition = utils.function_get_radiobutton_type(type_download)
    try:
        if len(url) > 0:
            utils.function_update_status(show_label, 'Iniciando Download')
            downloader = YoutubeDownloader(url, is_playlist)
            exit
            if type_definition == 'M':
                downloader.audioDownload()
                utils.function_update_status(show_label, 'Download de música concluído.')
            if type_definition == 'V':
                downloader.videoDownload()
                utils.function_update_status(show_label, 'Download de vídeo concluído.')
        else:
            utils.function_update_status(show_label, 'Digite uma url válida')
            return 
    except Exception as e:
        utils.function_update_status(show_label, f'Erro: {e}')

#DEFININDO FRAME MASTER
frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="x")

# FRAME URL
frame_url = ctk.CTkFrame(frame, fg_color="transparent")
frame_url.pack(fill="x", pady=(0, 10))

label_url = LabelComponent.show(frame_url, "URL")
entry_url = EntryComponent.show(frame_url, "Cole a URL do vídeo")

label_url.grid(row=0, column=0, padx=(0, 10), sticky="w")
entry_url.grid(row=0, column=1, sticky="ew")

frame_url.grid_columnconfigure(1, weight=1)

# FRAME É PLAYLIST
frame_options = ctk.CTkFrame(frame, fg_color="transparent")
frame_options.pack(fill="x", pady=(0, 15))

checkbox_var_playlist = ctk.BooleanVar(value=False)
checkbox = CheckboxComponent.show(
    frame_options,
    "É playlist?",
    checkbox_var_playlist
)

checkbox.pack(anchor="w")

# FRAME OPÇÕES VIDEO OU MÚSICA
frame_options = ctk.CTkFrame(frame, fg_color="transparent")
frame_options.pack(fill="x", pady=(0, 15))

type_download = ctk.StringVar(value='M')
radiobutton_is_music = RadioButtonComponent.show(
    frame_options,
    "Música",
    type_download,
    'M'
)
radiobutton_is_music.pack(anchor="w")

radiobutton_is_video = RadioButtonComponent.show(
    frame_options,
    "Vídeo",
    type_download,
    'V'
)
radiobutton_is_video.pack(anchor="w")

# FRAME BOTÃO DOWNLOAD
frame_action = ctk.CTkFrame(frame, fg_color="transparent")
frame_action.pack(fill="x", pady=(0, 10))

button_download = ButtonComponent.show(
    frame_action,
    "Download",
    function_download
)

button_download.pack(pady=5)

# LABEL STATUS
show_label = LabelComponent.show(frame, "")
show_label.pack(pady=(10, 0))

# INICIA APP
app.mainloop()