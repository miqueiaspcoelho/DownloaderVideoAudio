import customtkinter as ctk
class CheckboxComponent:
    @staticmethod
    def show(app: object,text: str, variable: vars, command: function = None) -> object:
        """
        Cria e retorna um checkbox do CustomTkinter (CTkCheckBox).

        Este método simplifica a criação de checkboxes dentro da interface,
        permitindo definir o texto exibido, a variável associada e a função
        a ser chamada quando o estado do checkbox mudar.

        Args:
            app (object): O widget pai (geralmente um CTkFrame ou CTk).
            text (str): O texto exibido ao lado do checkbox.
            variable (ctk.Variable): Variável do tipo BooleanVar associada ao checkbox
                                     para rastrear o estado (True/False).
            command (callable, optional): Função a ser executada ao mudar o estado
                                          do checkbox. O padrão é None.

        Returns:
            ctk.CTkCheckBox: O objeto checkbox criado, que pode ser posicionado
                             com pack(), grid() ou place().
        """
        field_checkbox = ctk.CTkCheckBox(
            app, 
            text= text, 
            command=command,
            variable=variable, 
            onvalue=True, 
            offvalue=False
        )
        return field_checkbox
