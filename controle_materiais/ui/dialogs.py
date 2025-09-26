import customtkinter as ctk
from tkinter import messagebox, ttk

CATEGORIAS_FIXAS = [
    "Copa e Consumo",
    "Papelaria / Escritório",
    "Higiene e Limpeza"
]

# Usar as mesmas cores e fontes do app principal para consistência
BG_COLOR = "#F0F2F5"
FONT_FAMILY = "Segoe UI"
TEXT_COLOR = "#343A40"
BTN_PRIMARY = "#1E70E0"
BTN_PRIMARY_HOVER = "#1A5BBF"
BTN_SECONDARY = "#6C757D"
BTN_SECONDARY_HOVER = "#5A6268"

class MaterialDialog(ctk.CTkToplevel): # Mudar para ctk.CTkToplevel
    def __init__(self, parent, gerenciador, titulo, feedback_callback=None, material=None):
        super().__init__(parent)
        self.gerenciador = gerenciador
        self.material = material
        self.feedback_callback = feedback_callback
        self.title(titulo)
        
        
        self.geometry("500x370")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR) # Usar fg_color
        self.create_styles() # Manter para o Combobox
        self.create_widgets()
        if material:
            self.preencher_campos()
        self.transient(parent)
        self.grab_set()
        self.focus()
        self.wait_window(self)

    def create_styles(self):
        # Estilo para o Combobox (ttk)
        style = ttk.Style(self)
        style.configure("TCombobox",
                        fieldbackground="white",
                        background=BG_COLOR,
                        font=(FONT_FAMILY, 11))
        style.map('TCombobox', fieldbackground=[('readonly', 'white')])
      

    def create_widgets(self):
        frame = ctk.CTkFrame(self, fg_color=BG_COLOR) # Usar CTkFrame
        frame.pack(padx=25, pady=25, fill=ctk.BOTH, expand=True)

        label_opts = {"fg_color": BG_COLOR, "anchor": "w", "font": ctk.CTkFont(family=FONT_FAMILY, size=11), "text_color": TEXT_COLOR}
        entry_opts = {"font": ctk.CTkFont(family=FONT_FAMILY, size=11), "fg_color": "white", "text_color": TEXT_COLOR, "border_color": BTN_SECONDARY, "border_width": 1, "corner_radius": 5} # Adicionar corner_radius

        ctk.CTkLabel(frame, text="Nome:", **label_opts).grid(row=0, column=0, sticky="w", pady=10, padx=5)
        self.entry_nome = ctk.CTkEntry(frame, **entry_opts) # Usar CTkEntry
        self.entry_nome.grid(row=0, column=1, sticky="ew", pady=10, padx=5)

        ctk.CTkLabel(frame, text="Categoria:", **label_opts).grid(row=1, column=0, sticky="w", pady=10, padx=5)
        self.combo_categoria = ttk.Combobox(frame, values=CATEGORIAS_FIXAS, state="readonly", font=(FONT_FAMILY, 11), style="TCombobox")
        self.combo_categoria.grid(row=1, column=1, sticky="ew", pady=10, padx=5)
        self.combo_categoria.current(0)

        ctk.CTkLabel(frame, text="Quantidade:", **label_opts).grid(row=2, column=0, sticky="w", pady=10, padx=5)
        self.entry_quantidade = ctk.CTkEntry(frame, **entry_opts) # Usar CTkEntry
        self.entry_quantidade.grid(row=2, column=1, sticky="ew", pady=10, padx=5)

        ctk.CTkLabel(frame, text="Descrição:", **label_opts).grid(row=3, column=0, sticky="nw", pady=10, padx=5)
        
        self.entry_descricao = ctk.CTkTextbox(frame, height=10, font=ctk.CTkFont(family=FONT_FAMILY, size=11), # Usar CTkTextbox
                                              fg_color="white", text_color=TEXT_COLOR, border_color=BTN_SECONDARY, border_width=1, corner_radius=5)
        self.entry_descricao.grid(row=3, column=1, sticky="ew", pady=10, padx=5)

        frame.columnconfigure(1, weight=1)

        btn_frame = ctk.CTkFrame(self, fg_color=BG_COLOR) # Usar CTkFrame
       
        btn_frame.pack(pady=(10, 20)) 

        btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", command=self.salvar,
                               fg_color=BTN_PRIMARY, hover_color=BTN_PRIMARY_HOVER,
                               font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
                               text_color="white", corner_radius=8, width=120, height=40) # Botão CTk
        btn_salvar.pack(side=ctk.LEFT, padx=15)

        btn_cancelar = ctk.CTkButton(btn_frame, text="Cancelar", command=self.destroy,
                                 fg_color=BTN_SECONDARY, hover_color=BTN_SECONDARY_HOVER,
                                 font=ctk.CTkFont(family=FONT_FAMILY, size=12, weight="bold"),
                                 text_color="white", corner_radius=8, width=120, height=40) # Botão CTk
        btn_cancelar.pack(side=ctk.LEFT, padx=15)

    def preencher_campos(self):
        self.entry_nome.insert(0, self.material[1])
        self.combo_categoria.set(self.material[2])
        self.entry_quantidade.insert(0, self.material[3])
        self.entry_descricao.insert("0.0", self.material[4]) # CTkTextbox usa "0.0" para o início

    def salvar(self):
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get().strip()
        quantidade_str = self.entry_quantidade.get().strip()
        descricao = self.entry_descricao.get("0.0", ctk.END).strip() # CTkTextbox usa "0.0" e ctk.END

        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório.")
            return
        if categoria not in CATEGORIAS_FIXAS:
            messagebox.showerror("Erro", "Selecione uma categoria válida.")
            return
        if not quantidade_str.isdigit():
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro não negativo.")
            return

        quantidade = int(quantidade_str)
        if quantidade < 0:
            messagebox.showerror("Erro", "Quantidade não pode ser negativa.")
            return

        try:
            if self.material:
                self.gerenciador.editar_material(self.material[0], nome, categoria, quantidade, descricao)
                if self.feedback_callback:
                    self.feedback_callback("Material atualizado com sucesso.", erro=False)
            else:
                self.gerenciador.cadastrar_material(nome, categoria, quantidade, descricao)
                if self.feedback_callback:
                    self.feedback_callback("Material cadastrado com sucesso.", erro=False)
            self.master.atualizar_lista()
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
