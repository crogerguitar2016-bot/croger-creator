from pathlib import Path
import json
import re
import unicodedata
from modelos_creator import obter_modulos


def sem_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def nome_pasta(texto):
    texto = sem_acentos(texto.strip())
    texto = re.sub(r"[^A-Za-z0-9]+", "_", texto)
    return texto.strip("_")


def pacote_valido(pacote):
    return bool(
        re.fullmatch(
            r"[a-z][a-z0-9_]*",
            pacote
        )
    )


def criar_projeto(
    base,
    nome_app,
    pacote,
    categorias,
    modelo="Biblioteca"
):
    nome_app = nome_app.strip()
    pacote = pacote.strip().lower()

    if not nome_app:
        raise ValueError("Digite o nome do aplicativo.")

    if not pacote:
        pacote = sem_acentos(nome_app.lower())
        pacote = re.sub(r"[^a-z0-9]", "", pacote)

    if not pacote_valido(pacote):
        raise ValueError(
            "Pacote inválido. Use letras minúsculas, números e _."
        )

    categorias = [
        item.strip()
        for item in categorias
        if item.strip()
    ]

    if not categorias:
        categorias = ["Principal"]

    modulos = obter_modulos(modelo)

    if not modulos:
        modulos = ["Principal"]

    pasta_nome = nome_pasta(nome_app)

    destino = Path(base) / pasta_nome

    if destino.exists():
        raise FileExistsError(
            "Já existe um projeto com esse nome."
        )

    destino.mkdir(parents=True)

    biblioteca = destino / "biblioteca"
    biblioteca.mkdir()

    for categoria in categorias:
        (biblioteca / categoria).mkdir(
            parents=True,
            exist_ok=True
        )

    (destino / "imagens").mkdir()
    (destino / "dados").mkdir()

    pasta_modulos = destino / "modulos"
    pasta_modulos.mkdir()

    for modulo in modulos:
        (
            pasta_modulos
            / nome_pasta(modulo)
        ).mkdir(
            parents=True,
            exist_ok=True
        )

    main_py = f'''from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

NOME_APP = {nome_app!r}
MODELO = {modelo!r}
MODULOS = {modulos!r}


class TelaPrincipal(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15),
            **kwargs
        )

        self.add_widget(
            Label(
                text=NOME_APP,
                font_size="26sp",
                size_hint_y=None,
                height=dp(70)
            )
        )

        self.add_widget(
            Label(
                text=MODELO,
                font_size="18sp",
                size_hint_y=None,
                height=dp(45)
            )
        )

        lista = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            row_default_height=dp(60),
            row_force_default=True
        )

        lista.bind(
            minimum_height=lista.setter("height")
        )

        for modulo in MODULOS:
            botao = Button(
                text=modulo,
                size_hint_y=None,
                height=dp(60),
                font_size="17sp"
            )

            botao.bind(
                on_release=lambda botao:
                self.selecionar_modulo(botao.text)
            )

            lista.add_widget(botao)

        self.add_widget(lista)

        self.status = Label(
            text="Aplicativo pronto.",
            size_hint_y=None,
            height=dp(50)
        )

        self.add_widget(self.status)

    def selecionar_modulo(self, modulo):
        self.status.text = (
            "Módulo selecionado: "
            + modulo
        )


class AplicativoGerado(App):

    def build(self):
        self.title = NOME_APP
        return TelaPrincipal()


if __name__ == "__main__":
    AplicativoGerado().run()
'''

    templates_por_modelo = {
        "Escola de Música":
            "escola_musica_main.py.txt",
        "Biblioteca":
            "biblioteca_main.py.txt",

        "Estudos/Apostila":
            "estudos_apostila_main.py.txt",

        "Cadastro/Planilha":
            "cadastro_planilha_main.py.txt",

        "Discipulado":
            "discipulado_main.py.txt",

        "Personalizado":
            "personalizado_main.py.txt",
    }

    if modelo in templates_por_modelo:
        template_path = (
            Path(__file__).resolve().parent
            / "templates"
            / templates_por_modelo[modelo]
        )

        if not template_path.exists():
            raise FileNotFoundError(
                "Template não encontrado: "
                + str(template_path)
            )

        main_py = template_path.read_text(
            encoding="utf-8"
        )

        main_py = main_py.replace(
            "@@NOME_APP@@",
            repr(nome_app)
        )

        main_py = main_py.replace(
            "@@MODELO@@",
            repr(modelo)
        )

        main_py = main_py.replace(
            "@@MODULOS@@",
            repr(modulos)
        )

    (destino / "main.py").write_text(
        main_py,
        encoding="utf-8"
    )

    buildozer = "\n".join([
        "[app]",
        "",
        f"title = {nome_app}",
        "",
        f"package.name = {pacote}",
        "package.domain = com.croger",
        "",
        "source.dir = .",
        "source.include_exts = py,png,jpg,jpeg,kv,atlas,txt,json",
        "source.exclude_dirs = .git,.buildozer,bin,__pycache__",
        "",
        "version = 1.0.0",
        "",
        "requirements = python3,kivy",
        "",
        "orientation = portrait",
        "fullscreen = 0",
        "",
        "android.api = 36",
        "android.minapi = 24",
        "android.ndk = 29",
        "android.archs = arm64-v8a",
        "",
        "android.accept_sdk_license = True",
        "",
        "p4a.branch = develop",
        "p4a.source_dir = /home/runner/p4a",
        "",
        "",
        "[buildozer]",
        "",
        "log_level = 2",
        "warn_on_root = 1",
        ""
    ])

    (destino / "buildozer.spec").write_text(
        buildozer,
        encoding="utf-8"
    )

    leia_me = (
        f"APLICATIVO: {nome_app}\n"
        f"PACOTE: com.croger.{pacote}\n\n"
        "CATEGORIAS:\n"
    )

    for categoria in categorias:
        leia_me += f"- {categoria}\n"

    (destino / "LEIA-ME.txt").write_text(
        leia_me,
        encoding="utf-8"
    )

    gitignore = "\n".join([
        "__pycache__/",
        "*.pyc",
        ".buildozer/",
        "bin/",
        ""
    ])

    (destino / ".gitignore").write_text(
        gitignore,
        encoding="utf-8"
    )

    workflow_dir = (
        destino
        / ".github"
        / "workflows"
    )

    workflow_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    workflow = "\n".join([
        f"name: Gerar APK {nome_app}",
        "",
        "on:",
        "  workflow_dispatch:",
        "",
        "jobs:",
        "  build:",
        "    runs-on: ubuntu-22.04",
        "",
        "    steps:",
        "      - name: Baixar projeto",
        "        uses: actions/checkout@v4",
        "",
        "      - name: Configurar Python 3.11",
        "        uses: actions/setup-python@v5",
        "        with:",
        '          python-version: "3.11"',
        "",
        "      - name: Configurar Java 17",
        "        uses: actions/setup-java@v4",
        "        with:",
        "          distribution: temurin",
        '          java-version: "17"',
        "",
        "      - name: Instalar dependências",
        "        run: |",
        "          sudo apt-get update",
        "          sudo apt-get install -y git zip unzip wget curl autoconf automake libtool pkg-config build-essential ccache libffi-dev libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev cmake ninja-build",
        "",
        "      - name: Instalar Rust",
        "        uses: dtolnay/rust-toolchain@stable",
        "",
        "      - name: Instalar ferramentas Python",
        "        run: |",
        "          python -m pip install --upgrade pip",
        '          pip install "cython==0.29.34"',
        "          pip install git+https://github.com/kivy/buildozer.git",
        "",
        "      - name: Instalar Android SDK",
        "        run: |",
        '          mkdir -p "$HOME/android-sdk/cmdline-tools"',
        '          cd "$HOME/android-sdk/cmdline-tools"',
        "          wget -q https://dl.google.com/android/repository/commandlinetools-linux-13114758_latest.zip",
        "          unzip -q commandlinetools-linux-13114758_latest.zip",
        "          mv cmdline-tools latest",
        '          echo "$HOME/android-sdk/cmdline-tools/latest/bin" >> "$GITHUB_PATH"',
        '          echo "$HOME/android-sdk/platform-tools" >> "$GITHUB_PATH"',
        '          yes | "$HOME/android-sdk/cmdline-tools/latest/bin/sdkmanager" --licenses >/dev/null || true',
        '          "$HOME/android-sdk/cmdline-tools/latest/bin/sdkmanager" "platform-tools" "platforms;android-36" "build-tools;37.0.0"',
        "",
        "      - name: Preparar Python-for-Android",
        "        run: |",
        '          git clone --depth 1 --branch develop https://github.com/kivy/python-for-android.git "$HOME/p4a"',
        "",
        "      - name: Compilar APK",
        "        env:",
        "          ANDROIDSDK: /home/runner/android-sdk",
        "          ANDROID_HOME: /home/runner/android-sdk",
        "        run: |",
        "          buildozer -v android debug",
        "",
        "      - name: Publicar APK",
        "        uses: actions/upload-artifact@v4",
        "        with:",
        f"          name: APK-{pacote}",
        "          path: bin/*.apk",
        "          if-no-files-found: error",
        ""
    ])

    (
        workflow_dir
        / "build-apk.yml"
    ).write_text(
        workflow,
        encoding="utf-8"
    )

    configuracao = {
        "nome": nome_app,
        "pacote": f"com.croger.{pacote}",
        "modelo": modelo,
        "modulos": modulos,
        "categorias": categorias,
        "modelo": modelo,
        "modulos": modulos,
    }

    (
        destino
        / "projeto.json"
    ).write_text(
        json.dumps(
            configuracao,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return {
        "nome": nome_app,
        "pacote": f"com.croger.{pacote}",
        "destino": str(destino),
        "categorias": categorias,
        "modelo": modelo,
        "modulos": modulos,
    }
