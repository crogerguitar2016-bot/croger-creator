from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp


class CrogerCreator(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            **kwargs
        )

        titulo = Label(
            text="CROGER CREATOR",
            font_size="26sp",
            size_hint_y=None,
            height=dp(60)
        )

        subtitulo = Label(
            text="Criador de Aplicativos",
            font_size="18sp",
            size_hint_y=None,
            height=dp(45)
        )

        self.add_widget(titulo)
        self.add_widget(subtitulo)

        scroll = ScrollView()

        botoes = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            padding=[0, dp(10)]
        )

        botoes.bind(
            minimum_height=botoes.setter("height")
        )

        opcoes = [
            ("NOVO PROJETO", self.novo_projeto),
            ("MEUS PROJETOS", self.meus_projetos),
            ("MODELOS", self.modelos),
            ("RECURSOS", self.recursos),
            ("CONFIGURAÇÕES", self.configuracoes),
        ]

        for texto, funcao in opcoes:
            botao = Button(
                text=texto,
                size_hint_y=None,
                height=dp(65),
                font_size="18sp"
            )

            botao.bind(
                on_release=funcao
            )

            botoes.add_widget(botao)

        scroll.add_widget(botoes)

        self.add_widget(scroll)

        self.status = Label(
            text="Croger Creator pronto.",
            size_hint_y=None,
            height=dp(50)
        )

        self.add_widget(self.status)

    def novo_projeto(self, *_):
        self.status.text = "Novo Projeto selecionado."

    def meus_projetos(self, *_):
        self.status.text = "Meus Projetos selecionado."

    def modelos(self, *_):
        self.status.text = "Modelos selecionado."

    def recursos(self, *_):
        self.status.text = "Recursos selecionado."

    def configuracoes(self, *_):
        self.status.text = "Configurações selecionado."


class CrogerCreatorApp(App):

    def build(self):
        self.title = "Croger Creator"
        return CrogerCreator()


if __name__ == "__main__":
    CrogerCreatorApp().run()
