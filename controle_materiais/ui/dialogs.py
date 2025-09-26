import tkinter as tk
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
BTN_SECONDARY = "#6C757D"

class MaterialDialog(tk.Toplevel):
    def __init__(self, parent, gerenciador, titulo, feedback_callback=None, material=None):
        super().__init__(parent)
        self.gerenciador = gerenciador
        self.material = material
        self.feedback_callback = feedback_callback
        self.title(titulo)
        
        
        self.geometry("600x550")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)
        self.create_widgets()
        if material:
            self.preencher_campos()
        self.transient(parent)
        self.grab_set()
        self.focus()
        self.wait_window(self)

    def create_widgets(self):
        frame = tk.Frame(self, bg=BG_COLOR)
        frame.pack(padx=25, pady=25, fill=tk.BOTH, expand=True)

        label_opts = {"bg": BG_COLOR, "anchor": "w", "font": (FONT_FAMILY, 11), "fg": TEXT_COLOR}
        entry_opts = {"font": (FONT_FAMILY, 11), "relief": "flat", "bd": 2, "highlightbackground": BTN_SECONDARY, "highlightthickness": 1}

        tk.Label(frame, text="Nome:", **label_opts).grid(row=0, column=0, sticky="w", pady=10, padx=5)
        self.entry_nome = tk.Entry(frame, **entry_opts)
        self.entry_nome.grid(row=0, column=1, sticky="ew", pady=10, padx=5)

        tk.Label(frame, text="Categoria:", **label_opts).grid(row=1, column=0, sticky="w", pady=10, padx=5)
        self.combo_categoria = ttk.Combobox(frame, values=CATEGORIAS_FIXAS, state="readonly", font=(FONT_FAMILY, 11), style="TCombobox")
        self.combo_categoria.grid(row=1, column=1, sticky="ew", pady=10, padx=5)
        self.combo_categoria.current(0)

        tk.Label(frame, text="Quantidade:", **label_opts).grid(row=2, column=0, sticky="w", pady=10, padx=5)
        self.entry_quantidade = tk.Entry(frame, **entry_opts)
        self.entry_quantidade.grid(row=2, column=1, sticky="ew", pady=10, padx=5)

        tk.Label(frame, text="Descrição:", **label_opts).grid(row=3, column=0, sticky="nw", pady=10, padx=5)
        
        self.entry_descricao = tk.Text(frame, height=10, font=(FONT_FAMILY, 11), relief="flat", bd=2, highlightbackground=BTN_SECONDARY, highlightthickness=1)
        self.entry_descricao.grid(row=3, column=1, sticky="ew", pady=10, padx=5)

        frame.columnconfigure(1, weight=1)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
       
        btn_frame.pack(pady=(10, 20)) 

        btn_salvar = tk.Button(btn_frame, text="Salvar", command=self.salvar,
                               bg=BTN_PRIMARY, fg="white", font=(FONT_FAMILY, 12, "bold"),
                               activebackground="#1A5BBF", activeforeground="white", # Corrigido activebackground para ser um tom mais escuro de BTN_PRIMARY
                               relief="flat", padx=25, pady=12, cursor="hand2", borderwidth=0)
        btn_salvar.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

        btn_cancelar = tk.Button(btn_frame, text="Cancelar", command=self.destroy,
                                 bg=BTN_SECONDARY, fg="white", font=(FONT_FAMILY, 12, "bold"),
                                 activebackground="#5A6268", activeforeground="white", # Corrigido activebackground para ser um tom mais escuro de BTN_SECONDARY
                                 relief="flat", padx=25, pady=12, cursor="hand2", borderwidth=0)
        btn_cancelar.pack(side=tk.LEFT, padx=15, ipadx=10, ipady=5)

    def preencher_campos(self):
        self.entry_nome.insert(0, self.material[1])
        self.combo_categoria.set(self.material[2])
        self.entry_quantidade.insert(0, self.material[3])
        self.entry_descricao.insert("1.0", self.material[4])

    def salvar(self):
        nome = self.entry_nome.get().strip()
        categoria = self.combo_categoria.get().strip()
        quantidade_str = self.entry_quantidade.get().strip()
        descricao = self.entry_descricao.get("1.0", tk.END).strip()

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
