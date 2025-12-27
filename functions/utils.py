def function_update_status(label: object, text: str) -> None:
    """Atualiza o texto de um label."""
    label.configure(text=text)

def function_get_checkbox_playlist(checkbox_var_playlist: bool) -> bool:
    """Retorna True se o checkbox estiver marcado, False caso contrário."""
    return checkbox_var_playlist.get()

def function_get_radiobutton_type(type_download: str) -> str:
    """Retorna o valor selecionado de um grupo de radiobuttons."""
    return type_download.get()

def function_get_url(entry_url: object) -> str:
    """Retorna o texto digitado no entry, sem espaços extras."""
    return entry_url.get().strip()
