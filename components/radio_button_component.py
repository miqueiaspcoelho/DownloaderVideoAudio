import customtkinter as ctk
class RadioButtonComponent:
    @staticmethod
    def show(app: object,text: str, variable: vars, value: any, command: function = None) -> object:
        """
        Cria e retorna um radiobutton do CustomTkinter (CTkRadioButton).

        Este método simplifica a criação de radiobuttons na interface,
        permitindo definir o texto exibido, a variável associada, o valor
        do botão e a função a ser chamada quando selecionado.

        Args:
            app (object): O widget pai (geralmente um CTkFrame ou CTk).
            text (str): O texto exibido ao lado do radiobutton.
            variable (ctk.Variable): Variável associada ao grupo de radiobuttons.
            value (any): Valor atribuído a este radiobutton. Ao ser selecionado,
                         a variável assume este valor.
            command (callable, optional): Função a ser executada ao selecionar o radiobutton.
                                          O padrão é None.

        Returns:
            ctk.CTkRadioButton: O objeto radiobutton criado, que pode ser posicionado
                                com pack(), grid() ou place().
        """
        field_radiobutton = ctk.CTkRadioButton(
            app, 
            text= text, 
            command=command,
            variable=variable, 
            value = value
        )
        return field_radiobutton
