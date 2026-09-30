import os
import shutil
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from pathlib import Path
from motor_creator import criar_projeto
from modelos_creator import listar_modelos, obter_modelo
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

        self.pasta_projetos = (
            Path(App.get_running_app().user_data_dir)
            / "projetos_criados"
        )
        self.pasta_projetos.mkdir(
            parents=True,
            exist_ok=True
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
        caixa = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(10)
        )

        caixa.add_widget(
            Label(
                text="Escolha o tipo de aplicativo",
                size_hint_y=None,
                height=dp(34),
                font_size="16sp"
            )
        )

        scroll = ScrollView()

        lista = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        popup = Popup(
            title="Novo Projeto - Escolher Modelo",
            content=caixa,
            size_hint=(0.96, 0.96),
            auto_dismiss=False
        )

        def escolher_modelo(nome_modelo):
            popup.dismiss()
            self.modelo_em_criacao = nome_modelo
            self.formulario_novo_projeto(
                nome_modelo
            )

        for nome_modelo in listar_modelos():
            modelo = obter_modelo(nome_modelo)

            botao = Button(
                text=(
                    nome_modelo
                    + "\n"
                    + modelo["descricao"]
                ),
                size_hint_y=None,
                height=dp(52),
                font_size="13sp"
            )

            botao.bind(
                on_release=lambda _botao, nome=nome_modelo:
                escolher_modelo(nome)
            )

            lista.add_widget(botao)

        scroll.add_widget(lista)
        caixa.add_widget(scroll)

        cancelar = Button(
            text="CANCELAR",
            size_hint_y=None,
            height=dp(44)
        )

        cancelar.bind(
            on_release=popup.dismiss
        )

        caixa.add_widget(cancelar)

        popup.open()

    def formulario_novo_projeto(
        self,
        modelo_escolhido,
        *_
    ):
        caixa = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(12)
        )

        nome = TextInput(
            hint_text="Nome do aplicativo",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        pacote = TextInput(
            hint_text="Pacote: exemplo cursomusica",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        categorias = TextInput(
            hint_text="Categorias: Violão, Teclado, Harmonia",
            multiline=False,
            size_hint_y=None,
            height=dp(50)
        )

        aviso = Label(
            text="",
            size_hint_y=None,
            height=dp(45)
        )

        caixa.add_widget(Label(
            text="Nome do aplicativo",
            size_hint_y=None,
            height=dp(28)
        ))
        caixa.add_widget(nome)

        caixa.add_widget(Label(
            text="Nome do pacote",
            size_hint_y=None,
            height=dp(28)
        ))
        caixa.add_widget(pacote)

        caixa.add_widget(Label(
            text="Categorias",
            size_hint_y=None,
            height=dp(28)
        ))
        caixa.add_widget(categorias)

        caixa.add_widget(aviso)

        linha = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(55)
        )

        cancelar = Button(text="CANCELAR")
        criar = Button(text="CRIAR")

        linha.add_widget(cancelar)
        linha.add_widget(criar)
        caixa.add_widget(linha)

        popup = Popup(
            title=f"Novo Projeto - {modelo_escolhido}",
            content=caixa,
            size_hint=(0.92, 0.85),
            auto_dismiss=False
        )

        cancelar.bind(on_release=popup.dismiss)

        def confirmar(*_args):
            lista = [
                item.strip()
                for item in categorias.text.split(",")
                if item.strip()
            ]

            try:
                resultado = criar_projeto(
                    self.pasta_projetos,
                    nome.text,
                    pacote.text,
                    lista,
                    modelo_escolhido
                )

                popup.dismiss()

                self.status.text = (
                    "Criado: "
                    + resultado["nome"]
                )

            except Exception as erro:
                aviso.text = str(erro)

        criar.bind(on_release=confirmar)

        popup.open()

    def meus_projetos(self, *_):
        projetos = sorted(
            [
                p for p in self.pasta_projetos.iterdir()
                if p.is_dir()
            ],
            key=lambda p: p.name.lower()
        )

        if not projetos:
            self.status.text = "Nenhum projeto criado."
            return

        caixa = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(10)
        )

        scroll = ScrollView()

        lista = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        popup = Popup(
            title="Meus Projetos",
            content=caixa,
            size_hint=(0.97, 0.88),
            auto_dismiss=False
        )

        for projeto in projetos:
            linha = BoxLayout(
                spacing=dp(6),
                size_hint_y=None,
                height=dp(60)
            )

            nome = projeto.name.replace("_", " ")

            label = Label(
                text=nome,
                halign="left",
                valign="middle"
            )

            label.bind(
                size=lambda instancia, tamanho:
                setattr(instancia, "text_size", tamanho)
            )

            detalhes = Button(
                text="DETALHES",
                size_hint_x=None,
                width=dp(105)
            )

            excluir = Button(
                text="EXCLUIR",
                size_hint_x=None,
                width=dp(95)
            )

            detalhes.bind(
                on_release=lambda _botao, p=projeto:
                self.abrir_detalhes(p)
            )

            excluir.bind(
                on_release=lambda _botao, p=projeto:
                self.confirmar_exclusao(p, popup)
            )

            linha.add_widget(label)
            linha.add_widget(detalhes)
            linha.add_widget(excluir)

            lista.add_widget(linha)

        scroll.add_widget(lista)
        caixa.add_widget(scroll)

        fechar = Button(
            text="FECHAR",
            size_hint_y=None,
            height=dp(55)
        )

        fechar.bind(on_release=popup.dismiss)

        caixa.add_widget(fechar)

        popup.open()

    def abrir_detalhes(self, projeto):
        nome = projeto.name.replace("_", " ")
        pacote = "Não identificado"
        categorias = []

        leia_me = projeto / "LEIA-ME.txt"

        if leia_me.exists():
            linhas = leia_me.read_text(
                encoding="utf-8"
            ).splitlines()

            lendo_categorias = False

            for linha in linhas:
                if linha.startswith("PACOTE:"):
                    pacote = linha.split(":", 1)[1].strip()

                elif linha.strip() == "CATEGORIAS:":
                    lendo_categorias = True

                elif lendo_categorias and linha.startswith("- "):
                    categorias.append(
                        linha[2:].strip()
                    )

        categorias_texto = (
            "\n".join("- " + item for item in categorias)
            if categorias
            else "- Nenhuma"
        )

        caixa = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )

        info = Label(
            text=(
                f"[b]{nome}[/b]\n\n"
                f"Pacote:\n{pacote}\n\n"
                f"Categorias:\n{categorias_texto}"
            ),
            markup=True,
            halign="left",
            valign="top"
        )

        info.bind(
            size=lambda instancia, tamanho:
            setattr(instancia, "text_size", tamanho)
        )

        resultado = Label(
            text="",
            size_hint_y=None,
            height=dp(60)
        )

        linha = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(58)
        )

        gerar = Button(text="GERAR ZIP")
        exportar = Button(text="EXPORTAR")
        fechar = Button(text="FECHAR")

        linha.add_widget(gerar)
        linha.add_widget(exportar)
        linha.add_widget(fechar)

        caixa.add_widget(info)
        caixa.add_widget(resultado)
        caixa.add_widget(linha)

        popup = Popup(
            title="Detalhes do Projeto",
            content=caixa,
            size_hint=(0.93, 0.82),
            auto_dismiss=False
        )

        gerar.bind(
            on_release=lambda *_:
            self.gerar_zip(projeto, resultado)
        )

        exportar.bind(
            on_release=lambda *_:
            self.exportar_downloads(
                projeto,
                resultado
            )
        )

        fechar.bind(on_release=popup.dismiss)

        popup.open()

    def gerar_zip(self, projeto, resultado_label):
        try:
            pasta_exportacao = (
                self.pasta_projetos.parent
                / "exports"
            )

            pasta_exportacao.mkdir(
                parents=True,
                exist_ok=True
            )

            destino_base = (
                pasta_exportacao
                / projeto.name
            )

            zip_existente = Path(
                str(destino_base) + ".zip"
            )

            if zip_existente.exists():
                zip_existente.unlink()

            for cache in projeto.rglob("__pycache__"):
                if cache.is_dir():
                    shutil.rmtree(cache)

            for pyc in projeto.rglob("*.pyc"):
                if pyc.is_file():
                    pyc.unlink()

            arquivo_zip = shutil.make_archive(
                str(destino_base),
                "zip",
                root_dir=str(projeto.parent),
                base_dir=projeto.name
            )

            resultado_label.text = (
                "ZIP criado com sucesso:\n"
                + Path(arquivo_zip).name
            )

            self.status.text = (
                "ZIP criado: "
                + Path(arquivo_zip).name
            )

        except Exception as erro:
            resultado_label.text = (
                "Erro ao gerar ZIP:\n"
                + str(erro)
            )

    def exportar_downloads(
        self,
        projeto,
        resultado_label
    ):
        try:
            candidatos = [
                Path("/sdcard/Download"),
                Path("/storage/emulated/0/Download"),
                Path(
                    "/data/data/com.termux/files/"
                    "home/storage/downloads"
                ),
            ]

            pasta_download = None

            for candidato in candidatos:
                if (
                    candidato.is_dir()
                    and os.access(
                        candidato,
                        os.W_OK
                    )
                ):
                    pasta_download = candidato
                    break

            if pasta_download is None:
                raise RuntimeError(
                    "Nenhuma pasta Downloads gravável encontrada."
                )

            destino_android = (
                pasta_download
                / "Croger Creator"
            )

            destino_android.mkdir(
                parents=True,
                exist_ok=True
            )

            for cache in projeto.rglob(
                "__pycache__"
            ):
                if cache.is_dir():
                    shutil.rmtree(cache)

            for pyc in projeto.rglob(
                "*.pyc"
            ):
                if pyc.is_file():
                    pyc.unlink()

            pasta_interna = (
                self.pasta_projetos.parent
                / "exports"
            )

            pasta_interna.mkdir(
                parents=True,
                exist_ok=True
            )

            base_zip = (
                pasta_interna
                / projeto.name
            )

            zip_interno = Path(
                str(base_zip) + ".zip"
            )

            if zip_interno.exists():
                zip_interno.unlink()

            arquivo_zip = shutil.make_archive(
                str(base_zip),
                "zip",
                root_dir=str(projeto.parent),
                base_dir=projeto.name
            )

            destino_final = (
                destino_android
                / Path(arquivo_zip).name
            )

            shutil.copy2(
                arquivo_zip,
                destino_final
            )

            resultado_label.text = (
                "Exportado para Downloads: "
                + destino_final.name
            )

            self.status.text = (
                "Exportado: "
                + destino_final.name
            )

        except Exception as erro:
            resultado_label.text = (
                "Erro ao exportar: "
                + str(erro)
            )

    def confirmar_exclusao(
        self,
        projeto,
        popup_lista
    ):
        caixa = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )

        nome = projeto.name.replace("_", " ")

        caixa.add_widget(
            Label(
                text=(
                    "Excluir este projeto?\n\n"
                    + nome
                )
            )
        )

        linha = BoxLayout(
            spacing=dp(10),
            size_hint_y=None,
            height=dp(55)
        )

        cancelar = Button(text="CANCELAR")
        excluir = Button(text="EXCLUIR")

        linha.add_widget(cancelar)
        linha.add_widget(excluir)
        caixa.add_widget(linha)

        confirmacao = Popup(
            title="Confirmar exclusão",
            content=caixa,
            size_hint=(0.85, 0.50),
            auto_dismiss=False
        )

        cancelar.bind(
            on_release=confirmacao.dismiss
        )

        def apagar(*_args):
            try:
                shutil.rmtree(projeto)

                confirmacao.dismiss()
                popup_lista.dismiss()

                self.status.text = (
                    "Projeto excluído: "
                    + nome
                )

                self.meus_projetos()

            except Exception as erro:
                self.status.text = (
                    "Erro ao excluir: "
                    + str(erro)
                )

        excluir.bind(
            on_release=apagar
        )

        confirmacao.open()

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
