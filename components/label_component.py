import customtkinter as ctk
class LabelComponent:
    @staticmethod
    def show(app: object, text: str) -> object:
        """
        Cria e retorna um label do CustomTkinter (CTkLabel).

        Este método simplifica a criação de labels na interface,
        permitindo definir o texto exibido.

        Args:
            app (object): O widget pai (geralmente um CTkFrame ou CTk).
            text (str): O texto que será exibido no label.

        Returns:
            ctk.CTkLabel: O objeto label criado, que pode ser posicionado
                          com pack(), grid() ou place().
        """
        field_label = ctk.CTkLabel(
            app, 
            text = text
        )
        return field_label
