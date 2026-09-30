MODELOS = {
    "Biblioteca": {
        "descricao": "Aplicativo para organizar e consultar conteúdos.",
        "modulos": [
            "Categorias",
            "Documentos",
            "PDFs",
            "Imagens",
            "Pesquisa",
            "Favoritos",
        ],
    },

    "Estudos/Apostila": {
        "descricao": "Curso com lições, exercícios e progresso.",
        "modulos": [
            "Apostilas",
            "Lições",
            "Questões",
            "Respostas",
            "Conclusão de estudo",
            "Progresso",
        ],
    },

    "Cadastro/Planilha": {
        "descricao": "Cadastro de pessoas e informações em tabelas.",
        "modulos": [
            "Cadastros",
            "Tabelas",
            "Campos personalizados",
            "Filtros",
            "Relatórios",
            "Exportação",
        ],
    },

    "Escola de Música": {
        "descricao": "Gestão de alunos, aulas, presença e exercícios.",
        "modulos": [
            "Alunos",
            "Instrumentos",
            "Aulas",
            "Presença",
            "Exercícios",
            "Progresso",
            "Repertório",
            "Apostilas",
        ],
    },

    "Discipulado": {
        "descricao": "Acompanhamento de discípulos e estudos.",
        "modulos": [
            "Discípulos",
            "Estudos",
            "Questões",
            "Respostas",
            "Presença",
            "Progresso",
            "Observações",
        ],
    },

    "Personalizado": {
        "descricao": "Permite combinar módulos de vários modelos.",
        "modulos": [
            "Biblioteca",
            "Apostilas",
            "Questões",
            "Cadastros",
            "Planilhas",
            "Presença",
            "Exercícios",
            "Progresso",
            "Relatórios",
        ],
    },
}


def listar_modelos():
    return list(MODELOS.keys())


def obter_modelo(nome):
    return MODELOS.get(nome)


def obter_modulos(nome):
    modelo = obter_modelo(nome)

    if not modelo:
        return []

    return list(modelo["modulos"])


if __name__ == "__main__":
    print("=" * 50)
    print("MODELOS DO CROGER CREATOR")
    print("=" * 50)

    for numero, nome in enumerate(
        listar_modelos(),
        start=1
    ):
        modelo = obter_modelo(nome)

        print()
        print(numero, "-", nome)
        print(modelo["descricao"])

        for modulo in modelo["modulos"]:
            print(" -", modulo)
