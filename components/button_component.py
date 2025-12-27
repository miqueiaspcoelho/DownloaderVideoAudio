import customtkinter as ctk
class ButtonComponent:
    @staticmethod
    def show(app: object,text: str, command: function = '') -> object:
        """
        Cria e retorna um botão do CustomTkinter (CTkButton).

        Este método simplifica a criação de botões dentro da interface
        utilizando CustomTkinter, permitindo definir o texto exibido
        e a função que será executada ao clicar no botão.

        Args:
            app (object): O widget pai (geralmente um CTkFrame ou CTk).
            text (str): O texto exibido no botão.
            command (callable, optional): Função a ser executada ao clicar no botão.
                                          O padrão é None.

        Returns:
            ctk.CTkButton: O objeto botão criado, que pode ser posicionado
                           com pack(), grid() ou place().
        """
        field_button = ctk.CTkButton(
            app, 
            text= text, 
            command= command
        )
        return field_button
