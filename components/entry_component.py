import customtkinter as ctk
class EntryComponent:
    @staticmethod
    def show(app: object,placeholder_text: str = '', width: int = 200) -> object:
        """
        Cria e retorna um campo de entrada (input) do CustomTkinter (CTkEntry).

        Este método simplifica a criação de campos de entrada na interface,
        permitindo definir um texto placeholder e a largura do campo.

        Args:
            app (object): O widget pai (geralmente um CTkFrame ou CTk).
            placeholder_text (str, optional): Texto que aparece como placeholder
                                              no campo de entrada. O padrão é ''.
            width (int, optional): Largura do campo de entrada em pixels. O padrão é 200.

        Returns:
            ctk.CTkEntry: O objeto de entrada criado, que pode ser posicionado
                          com pack(), grid() ou place().
        """
        field_entry = ctk.CTkEntry(
            app,
            placeholder_text=placeholder_text,
            width=width
        )
        return field_entry
