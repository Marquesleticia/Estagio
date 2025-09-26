import customtkinter as ctk
from tkinter import ttk, messagebox
from bll.gerenciador_estoque import GerenciadorDeEstoque
from ui.dialogs import MaterialDialog # Manter import para o diálogo
from PIL import Image, ImageTk 


CATEGORIAS_FIXAS = [
    "Copa e Consumo",
    "Papelaria / Escritório",
    "Higiene e Limpeza"

]
# Cores ajustadas para customtkinter, que gerencia melhor o tema
# CTkButton usa fg_color, hover_color, text_color
BG_COLOR = "#F0F2F5"          # Fundo cinza muito claro (quase branco)
BTN_PRIMARY = "#1E70E0"       # Azul mais vibrante
BTN_PRIMARY_HOVER = "#1A5BBF" # Tom mais escuro para hover
BTN_REMOVE = "#DC3545"        # Vermelho mais padrão
BTN_REMOVE_HOVER = "#C82333"  # Tom mais escuro para hover
BTN_SECONDARY = "#6C757D"     # Cinza mais escuro
BTN_SECONDARY_HOVER = "#5A6268" # Tom mais escuro para hover
HEADER_BG = "#0056B3"         # Azul escuro para cabeçalho
HEADER_FG = "white"
ROW_ALT_BG = "#E9ECEF"        # Cinza claro para linhas alternadas
FONT_FAMILY = "Segoe UI"      
TEXT_COLOR = "#343A40"        # Cor de texto principal

class App(ctk.CTk): # Mudar para ctk.CTk
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Estoque")
        self.geometry("1050x800") 

        # ctk.CTk não usa iconbitmap diretamente, mas você pode definir um ícone da janela
        # self.iconbitmap("controle_materiais/ui/logo.ico") 
        # Para ícone, pode ser necessário usar self.wm_iconbitmap() ou um método específico do OS
        # ou deixar sem ícone por enquanto para focar nos botões.

        self.configure(fg_color=BG_COLOR) # Usar fg_color para background em CTk
        self.gerenciador = GerenciadorDeEstoque()
        self.create_styles()
        self.create_widgets()
        self.atualizar_lista()

    def create_styles(self):
        # Manter estilos para Treeview e Combobox, pois são ttk widgets
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure("Treeview",
                        background=BG_COLOR,
                        foreground=TEXT_COLOR,
                        rowheight=30,
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

        # Não precisamos mais dos estilos ttk.Button para os botões CTkButton

    def create_widgets(self):
      
        header_frame = ctk.CTkFrame(self, fg_color=BG_COLOR) # Usar CTkFrame
        header_frame.pack(pady=15, fill=ctk.X)

        
        self.logo_image = None
        try:
            original_image = Image.open('controle_materiais/ui/logo.png')
            resized_image = original_image.resize((85, 85), Image.LANCZOS) 
            self.logo_image = ctk.CTkImage(light_image=resized_image, dark_image=resized_image, size=(85, 85)) # Usar CTkImage
            logo_label = ctk.CTkLabel(header_frame, image=self.logo_image, text="", fg_color=BG_COLOR) # Usar CTkLabel
            logo_label.pack(side=ctk.LEFT, padx=(20, 10))
        except FileNotFoundError:
            print("Logo file 'logo.png' not found. Skipping logo display.")
            

        # Título
        titulo = ctk.CTkLabel(header_frame, text="Gerenciamento de Estoque Detran", # Usar CTkLabel
                          font=ctk.CTkFont(family=FONT_FAMILY, size=25, weight="bold"), # Usar CTkFont
                          fg_color=BG_COLOR, text_color=TEXT_COLOR)
        titulo.pack(side=ctk.LEFT, anchor=ctk.W)


        
        filtro_frame = ctk.CTkFrame(self, fg_color=BG_COLOR) 
        filtro_frame.pack(pady=15, fill=ctk.X, padx=20) 

        # Nome filtro
        ctk.CTkLabel(filtro_frame, text="Filtro por Nome:", fg_color=BG_COLOR, text_color=TEXT_COLOR, font=ctk.CTkFont(family=FONT_FAMILY, size=15)).pack(side=ctk.LEFT)
        self.filtro_nome = ctk.CTkEntry(filtro_frame, width=200, font=ctk.CTkFont(family=FONT_FAMILY, size=13),
                                        fg_color="white", text_color=TEXT_COLOR, border_color=BTN_SECONDARY, border_width=1) # Usar CTkEntry
        self.filtro_nome.pack(side=ctk.LEFT, padx=10) 

        # Categoria filtro
        ctk.CTkLabel(filtro_frame, text="Filtro por Categoria:", fg_color=BG_COLOR, text_color=TEXT_COLOR, font=ctk.CTkFont(family=FONT_FAMILY, size=15)).pack(side=ctk.LEFT, padx=(25,0))
        self.filtro_categoria = ttk.Combobox(filtro_frame, values=[""] + CATEGORIAS_FIXAS,
                                             state="readonly", width=28, font=(FONT_FAMILY, 14), style="TCombobox")
        self.filtro_categoria.pack(side=ctk.LEFT, padx=10)
        self.filtro_categoria.current(0)

        # Botões filtrar e limpar
        btn_filtrar = ctk.CTkButton(filtro_frame, text="Consultar", command=self.atualizar_lista,
                               fg_color=BTN_PRIMARY, hover_color=BTN_PRIMARY_HOVER,
                               font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                               text_color="white", corner_radius=8) # Botão CTk
        btn_filtrar.pack(side=ctk.LEFT, padx=15)

        btn_limpar = ctk.CTkButton(filtro_frame, text="Limpar", command=self.limpar_filtros,
                              fg_color=BTN_SECONDARY, hover_color=BTN_SECONDARY_HOVER,
                              font=ctk.CTkFont(family=FONT_FAMILY, size=13, weight="bold"),
                              text_color="white", corner_radius=8) # Botão CTk
        btn_limpar.pack(side=ctk.LEFT)

        # Treeview para lista de materiais (mantido como ttk.Treeview)
        columns = ("ID", "Nome", "Categoria", "Quantidade", "Descrição")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse",
                                 style="Treeview")
        self.tree.pack(fill=ctk.BOTH, expand=True, padx=20, pady=15)

        # Configurar colunas e cabeçalho
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=60, anchor=ctk.CENTER)
        self.tree.heading("Nome", text="Nome")
        self.tree.column("Nome", width=220)
        self.tree.heading("Categoria", text="Categoria")
        self.tree.column("Categoria", width=190)
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.column("Quantidade", width=120, anchor=ctk.CENTER)
        self.tree.heading("Descrição", text="Descrição")
        self.tree.column("Descrição", width=300)

        # Frame inferior para botões
        btn_frame = ctk.CTkFrame(self, fg_color=BG_COLOR) # Usar CTkFrame
        btn_frame.pack(pady=20)

        # Botões com ícones e estilos
        btn_add = ctk.CTkButton(btn_frame, text="➕ Cadastrar", command=self.cadastrar_material,
                            fg_color=BTN_PRIMARY, hover_color=BTN_PRIMARY_HOVER,
                            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
                            text_color="white", corner_radius=8, width=200, height=60) # Botão CTk
        btn_add.pack(side=ctk.LEFT, padx=20)

        btn_edit = ctk.CTkButton(btn_frame, text="✏️ Atualizar", command=self.editar_material,
                             fg_color=BTN_SECONDARY, hover_color=BTN_SECONDARY_HOVER,
                             font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
                             text_color="white", corner_radius=8, width=200, height=50) # Botão CTk
        btn_edit.pack(side=ctk.LEFT, padx=20)

        btn_del = ctk.CTkButton(btn_frame, text="🗑️ Remover", command=self.remover_material,
                            fg_color=BTN_REMOVE, hover_color=BTN_REMOVE_HOVER,
                            font=ctk.CTkFont(family=FONT_FAMILY, size=15, weight="bold"),
                            text_color="white", corner_radius=8, width=200, height=60) # Botão CTk
        btn_del.pack(side=ctk.LEFT, padx=20)

        # Barra de status inferior
        self.status_var = ctk.StringVar() 
        self.status_var.set("Total de materiais: 0")
        status_bar = ctk.CTkLabel(self, textvariable=self.status_var, fg_color=BG_COLOR, 
                              text_color=TEXT_COLOR, font=ctk.CTkFont(family=FONT_FAMILY, size=11), anchor="w")
        status_bar.pack(side=ctk.BOTTOM, fill=ctk.X, padx=20, pady=10)

        
        self.msg_var = ctk.StringVar() 
        self.msg_label = ctk.CTkLabel(self, textvariable=self.msg_var, fg_color=BG_COLOR, 
                                  font=ctk.CTkFont(family=FONT_FAMILY, size=11, weight="bold"))
        self.msg_label.pack(side=ctk.BOTTOM, fill=ctk.X, padx=20, pady=(0,10))

    def limpar_filtros(self):
        self.filtro_nome.delete(0, ctk.END) # Usar ctk.END
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
            self.tree.insert("", ctk.END, values=mat, tags=(tag,)) # Usar ctk.END
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
            self.msg_label.configure(text_color=BTN_REMOVE) 
        else:
            self.msg_label.configure(text_color="#28A745")  # Verde sucesso mais padrão

    def limpar_mensagem(self):
        self.msg_var.set("")
