#imports
import customtkinter as ctk
import threading
from components import LabelComponent, EntryComponent, ButtonComponent, CheckboxComponent, RadioButtonComponent
from downloader import YoutubeDownloader
from functions import utils


#definições globais
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme("themes/dark_blue.json")
app = ctk.CTk()
app.title('Audio e Video Downloader')
app.geometry('400x320')
app.resizable(False, False)

#USANDP THREADING PARA EVITAR BLOQUEIOS DURANTE DOWNLOAD
def download_worker():
    try:
        url = utils.function_get_url(entry_url)
        is_playlist = not utils.function_get_checkbox_playlist(checkbox_var_playlist)
        type_definition = utils.function_get_radiobutton_type(type_download)
        if not url:
            app.after(0, lambda: show_label.configure(
                text="Digite uma url válida",
                text_color="red"
            ))
            return
        downloader = YoutubeDownloader(url, is_playlist)

        if type_definition == "M":
            downloader.audioDownload()
            app.after(0, lambda: show_label.configure(
                text="Download de música concluído.",
                text_color= "green"
            ))
        else:
            downloader.videoDownload()
            app.after(0, lambda: show_label.configure(
                text="Download de vídeo concluído.",
                text_color= "green"
            ))
    except Exception as e:
        app.after(0, lambda: show_label.configure(
            text=f"Erro: {e}",
            text_color="red"
        ))
    finally:
        app.after(0, function_finish_download)

def function_finish_download():
    progress_bar.stop()
    progress_bar.pack_forget()
    button_download.configure(state="normal")

#FUNÇÃO PARA DOWNLOAD
def function_download()->None:
    button_download.configure(state="disable")
    show_label.configure(text="Download em andamento", text_color="yellow")
    progress_bar.pack(fill="x", padx=20, pady=(5, 10))
    progress_bar.start()  # animação automática
    thread = threading.Thread(
        target=download_worker,
        daemon=True
    )
    thread.start()

#DEFININDO FRAME MASTER
frame = ctk.CTkFrame(app)
frame.pack(padx=20, pady=(20,0), fill="x")

# FRAME URL
frame_url = ctk.CTkFrame(frame, fg_color="transparent")
frame_url.pack(fill="x", padx=(10,10),pady=(10, 10))

label_url = LabelComponent.show(frame_url, "URL")
entry_url = EntryComponent.show(frame_url, "Cole a URL do vídeo")

label_url.grid(row=0, column=0, padx=(10, 10), sticky="w")
entry_url.grid(row=0, column=1, sticky="ew")

frame_url.grid_columnconfigure(1, weight=1)

# FRAME É PLAYLIST
frame_options = ctk.CTkFrame(frame, fg_color="transparent")
frame_options.pack(fill="x", padx=(10,10),pady=(0, 15))

checkbox_var_playlist = ctk.BooleanVar(value=False)
checkbox = CheckboxComponent.show(
    frame_options,
    "É playlist?",
    checkbox_var_playlist
)

checkbox.pack(anchor="w",padx=(10,10),pady=(5, 5))

# FRAME OPÇÕES VIDEO OU MÚSICA
frame_options = ctk.CTkFrame(frame, fg_color="transparent")
frame_options.pack(fill="x", padx=(10,10),pady=(0, 15))

type_download = ctk.StringVar(value='M')
radiobutton_is_music = RadioButtonComponent.show(
    frame_options,
    "Música",
    type_download,
    'M'
)
radiobutton_is_music.pack(anchor="w",padx=(10,10), pady=(10,0))

radiobutton_is_video = RadioButtonComponent.show(
    frame_options,
    "Vídeo",
    type_download,
    'V'
)
radiobutton_is_video.pack(anchor="w",padx=(10,10), pady=(10,0))

# FRAME BOTÃO DOWNLOAD
frame_action = ctk.CTkFrame(frame, fg_color="transparent")
frame_action.pack(fill="x", pady=(0, 10))

#BARRA DE PROGRESSO
progress_bar = ctk.CTkProgressBar(frame_action)
progress_bar.pack(fill="x", padx=20, pady=(5, 10))

progress_bar.set(0)
progress_bar.pack_forget()  # começa escondida

button_download = ButtonComponent.show(
    frame_action,
    "Download",
    function_download
)

button_download.pack(pady=(5,0))

# LABEL STATUS
show_label = LabelComponent.show(frame, "")
show_label.pack(pady=(10, 0))

# INICIA APP
app.mainloop()