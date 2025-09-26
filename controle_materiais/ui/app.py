import tkinter as tk
from tkinter import ttk, messagebox
from bll.gerenciador_estoque import GerenciadorDeEstoque
from ui.dialogs import MaterialDialog
from PIL import Image, ImageTk 


CATEGORIAS_FIXAS = [
    "Copa e Consumo",
    "Papelaria / Escritório",
    "Higiene e Limpeza"

]
BG_COLOR = "#F0F2F5"          # Fundo cinza muito claro (quase branco)
BTN_PRIMARY = "#1E70E0"       # Azul mais vibrante
BTN_REMOVE = "#DC3545"        # Vermelho mais padrão
BTN_SECONDARY = "#6C757D"     # Cinza mais escuro
HEADER_BG = "#0056B3"         # Azul escuro para cabeçalho
HEADER_FG = "white"
ROW_ALT_BG = "#E9ECEF"        # Cinza claro para linhas alternadas
FONT_FAMILY = "Segoe UI"      
TEXT_COLOR = "#343A40"        # Cor de texto principal

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Estoque")
        self.geometry("1050x800") 

        self.iconbitmap("controle_materiais/ui/logo.ico")
        
        self.configure(bg=BG_COLOR)
        self.gerenciador = GerenciadorDeEstoque()
        self.create_styles()
        self.create_widgets()
        self.atualizar_lista()

    def create_styles(self):
        style = ttk.Style(self)
        style.theme_use("default")

       
        style.configure("Treeview",
                        background=BG_COLOR,
                        foreground=TEXT_COLOR,
                        rowheight=30, # Aumentar altura da linha
                        fieldbackground=BG_COLOR,
                        font=(FONT_FAMILY, 11))
        style.map('Treeview', background=[('selected', BTN_PRIMARY)])

        style.configure("Treeview.Heading",
                        background=HEADER_BG,
                        foreground=HEADER_FG,
                        font=(FONT_FAMILY, 12, "bold"),
                        padding=[5, 10]) 

       
        self.tree_tag_odd = 'oddrow'
        self.tree_tag_even = 'evenrow'
        style.configure(self.tree_tag_odd, background=BG_COLOR)
        style.configure(self.tree_tag_even, background=ROW_ALT_BG)

        
        style.configure("TCombobox",
                        fieldbackground="white",
                        background=BG_COLOR,
                        font=(FONT_FAMILY, 11))
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])


    def create_widgets(self):
      
        header_frame = tk.Frame(self, bg=BG_COLOR)
        header_frame.pack(pady=15, fill=tk.X)

        
        self.logo_image = None
        try:
            original_image = Image.open('controle_materiais/ui/logo.png')
            resized_image = original_image.resize((85, 85), Image.LANCZOS) 
            self.logo_image = ImageTk.PhotoImage(resized_image)
            logo_label = tk.Label(header_frame, image=self.logo_image, bg=BG_COLOR)
            logo_label.pack(side=tk.LEFT, padx=(20, 10))
        except FileNotFoundError:
            print("Logo file 'logo.png' not found. Skipping logo display.")
            

        # Título
        titulo = tk.Label(header_frame, text="Gerenciamento de Estoque Detran",
                          font=(FONT_FAMILY, 25, "bold"),
                          bg=BG_COLOR, fg=TEXT_COLOR)
        titulo.pack(side=tk.LEFT, anchor=tk.W)


        
        filtro_frame = tk.Frame(self, bg=BG_COLOR)
        filtro_frame.pack(pady=15, fill=tk.X, padx=20) 

        # Nome filtro
        tk.Label(filtro_frame, text="Filtro Nome:", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11)).pack(side=tk.LEFT)
        self.filtro_nome = tk.Entry(filtro_frame, width=30, font=(FONT_FAMILY, 11), relief="flat", bd=2, highlightbackground=BTN_SECONDARY, highlightthickness=1)
        self.filtro_nome.pack(side=tk.LEFT, padx=10) 

        # Categoria filtro
        tk.Label(filtro_frame, text="Filtro Categoria:", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_FAMILY, 11)).pack(side=tk.LEFT, padx=(25,0)) # Aumentar padx
        self.filtro_categoria = ttk.Combobox(filtro_frame, values=[""] + CATEGORIAS_FIXAS,
                                             state="readonly", width=28, font=(FONT_FAMILY, 11), style="TCombobox")
        self.filtro_categoria.pack(side=tk.LEFT, padx=10) # Aumentar padx
        self.filtro_categoria.current(0)

        # Botões filtrar e limpar
        btn_filtrar = tk.Button(filtro_frame, text="Consultar", command=self.atualizar_lista,
                               bg=BTN_PRIMARY, fg="white", font=(FONT_FAMILY, 11, "bold"),
                               activebackground="#1A5BBF", activeforeground="white", # Tom mais escuro para active
                               relief="flat", padx=20, pady=8, cursor="hand2", borderwidth=0) # Aumentar padding
        btn_filtrar.pack(side=tk.LEFT, padx=15) # Aumentar padx

        btn_limpar = tk.Button(filtro_frame, text="Limpar", command=self.limpar_filtros,
                              bg=BTN_SECONDARY, fg="white", font=(FONT_FAMILY, 11, "bold"),
                              activebackground="#5A6268", activeforeground="white", # Tom mais escuro para active
                              relief="flat", padx=20, pady=8, cursor="hand2", borderwidth=0) # Aumentar padding
        btn_limpar.pack(side=tk.LEFT)

        # Treeview para lista de materiais
        columns = ("ID", "Nome", "Categoria", "Quantidade", "Descrição")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse",
                                 style="Treeview")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=15) # Aumentar pady

        # Configurar colunas e cabeçalho
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=60, anchor=tk.CENTER) # Ajustar largura
        self.tree.heading("Nome", text="Nome")
        self.tree.column("Nome", width=220) # Ajustar largura
        self.tree.heading("Categoria", text="Categoria")
        self.tree.column("Categoria", width=190) # Ajustar largura
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.column("Quantidade", width=120, anchor=tk.CENTER) # Ajustar largura
        self.tree.heading("Descrição", text="Descrição")
        self.tree.column("Descrição", width=300) # Ajustar largura

        # Frame inferior para botões
        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=20) # Aumentar pady

        # Botões com ícones e estilos
        btn_add = tk.Button(btn_frame, text="➕ Cadastrar", command=self.cadastrar_material,
                            bg=BTN_PRIMARY, fg="white", font=(FONT_FAMILY, 12, "bold"),
                            activebackground="#1A5BBF", activeforeground="white",
                            relief="flat", padx=25, pady=12, cursor="hand2", borderwidth=0) # Aumentar padding
        btn_add.pack(side=tk.LEFT, padx=20, ipadx=10, ipady=5) # Aumentar padx

        btn_edit = tk.Button(btn_frame, text="✏️ Atualizar", command=self.editar_material,
                             bg=BTN_SECONDARY, fg="white", font=(FONT_FAMILY, 12, "bold"),
                             activebackground="#5A6268", activeforeground="white",
                             relief="flat", padx=25, pady=12, cursor="hand2", borderwidth=0) # Aumentar padding
        btn_edit.pack(side=tk.LEFT, padx=20, ipadx=10, ipady=5) # Aumentar padx

        btn_del = tk.Button(btn_frame, text="🗑️ Remover", command=self.remover_material,
                            bg=BTN_REMOVE, fg="white", font=(FONT_FAMILY, 12, "bold"),
                            activebackground="#C82333", activeforeground="white", # Tom mais escuro para active
                            relief="flat", padx=25, pady=12, cursor="hand2", borderwidth=0) # Aumentar padding
        btn_del.pack(side=tk.LEFT, padx=20, ipadx=10, ipady=5) # Aumentar padx

        # Barra de status inferior
        self.status_var = tk.StringVar()
        self.status_var.set("Total de materiais: 0")
        status_bar = tk.Label(self, textvariable=self.status_var, bg=BG_COLOR,
                              fg=TEXT_COLOR, font=(FONT_FAMILY, 11), anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10) # Aumentar pady

        # Label para mensagens de feedback (sucesso/erro)
        self.msg_var = tk.StringVar()
        self.msg_label = tk.Label(self, textvariable=self.msg_var, bg=BG_COLOR,
                                  font=(FONT_FAMILY, 11, "bold"))
        self.msg_label.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0,10)) # Aumentar pady

    def limpar_filtros(self):
        self.filtro_nome.delete(0, tk.END)
        self.filtro_categoria.current(0)
        self.atualizar_lista()
        self.limpar_mensagem()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        filtro_cat = self.filtro_categoria.get()
        if filtro_cat == "":
            filtro_cat = "%"
        materiais = self.gerenciador.obter_materiais(self.filtro_nome.get(), filtro_cat)
        for index, mat in enumerate(materiais):
            tag = self.tree_tag_even if index % 2 == 0 else self.tree_tag_odd
            self.tree.insert("", tk.END, values=mat, tags=(tag,))
        self.status_var.set(f"Total de materiais: {len(materiais)}")
        self.limpar_mensagem()

    def cadastrar_material(self):
        MaterialDialog(self, self.gerenciador, "Cadastrar Material", self.exibir_mensagem)

    def editar_material(self):
        item = self.tree.selection()
        if not item:
            self.exibir_mensagem("Selecione um material para editar.", erro=True)
            return
        valores = self.tree.item(item[0], "values")
        MaterialDialog(self, self.gerenciador, "Editar Material", self.exibir_mensagem, material=valores)

    def remover_material(self):
        item = self.tree.selection()
        if not item:
            self.exibir_mensagem("Selecione um material para remover.", erro=True)
            return
        valores = self.tree.item(item[0], "values")
        resposta = messagebox.askyesno("Confirmação", f"Remover material '{valores[1]}'?")
        if resposta:
            self.gerenciador.excluir_material(valores[0])
            self.atualizar_lista()
            self.exibir_mensagem("Material removido com sucesso.", erro=False)

    def exibir_mensagem(self, texto, erro=False):
        self.msg_var.set(texto)
        if erro:
            self.msg_label.config(fg=BTN_REMOVE)
        else:
            self.msg_label.config(fg="#28A745")  # Verde sucesso mais padrão

    def limpar_mensagem(self):
        self.msg_var.set("")
