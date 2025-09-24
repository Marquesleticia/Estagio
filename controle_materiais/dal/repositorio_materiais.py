import sqlite3
import os

class RepositorioMateriais:
    def __init__(self, db_name="database/estoque.db"):
        
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        project_dir = os.path.abspath(os.path.join(base_dir, ".."))  
        db_path = os.path.join(project_dir, db_name)

       
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        
        self.conn = sqlite3.connect(db_path)
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS materiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                descricao TEXT
            )
        ''')
        self.conn.commit()

    def inserir_material(self, nome, categoria, quantidade, descricao):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO materiais (nome, categoria, quantidade, descricao)
            VALUES (?, ?, ?, ?)
        ''', (nome, categoria, quantidade, descricao))
        self.conn.commit()

    def listar_materiais(self, filtro_nome="", filtro_categoria=""):
        cursor = self.conn.cursor()
        query = "SELECT * FROM materiais WHERE nome LIKE ? AND categoria LIKE ? ORDER BY nome"
        cursor.execute(query, (f"%{filtro_nome}%", f"%{filtro_categoria}%"))
        return cursor.fetchall()

    def atualizar_material(self, id_, nome, categoria, quantidade, descricao):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE materiais
            SET nome = ?, categoria = ?, quantidade = ?, descricao = ?
            WHERE id = ?
        ''', (nome, categoria, quantidade, descricao, id_))
        self.conn.commit()

    def remover_material(self, id_):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM materiais WHERE id = ?', (id_,))
        self.conn.commit()
