from dal.repositorio_materiais import RepositorioMateriais

class GerenciadorDeEstoque:
    def __init__(self):
        self.repo = RepositorioMateriais()

    def cadastrar_material(self, nome, categoria, quantidade, descricao):
        if not nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        if not categoria.strip():
            raise ValueError("Categoria não pode ser vazia.")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
        self.repo.inserir_material(nome, categoria, quantidade, descricao)

    def obter_materiais(self, filtro_nome="", filtro_categoria=""):
        return self.repo.listar_materiais(filtro_nome, filtro_categoria)

    def editar_material(self, id_, nome, categoria, quantidade, descricao):
        if not nome.strip():
            raise ValueError("Nome não pode ser vazio.")
        if not categoria.strip():
            raise ValueError("Categoria não pode ser vazia.")
        if quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa.")
        self.repo.atualizar_material(id_, nome, categoria, quantidade, descricao)

    def excluir_material(self, id_):
        self.repo.remover_material(id_)