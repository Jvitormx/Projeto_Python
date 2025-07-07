import tkinter as tk
from tkinter import messagebox

class MenuGestor(tk.Frame):
    def __init__(self, master, gestor, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.gestor = gestor
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Bem-vindo, {self.gestor.nome}", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text=f"Departamento: {self.gestor.departamento}", font=("Arial", 12)).pack(pady=2)
        tk.Label(self, text="Menu do Gestor", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Button(self, text="Cadastrar Funcionário", width=30, command=self.cadastrar_funcionario).pack(pady=4)
        tk.Button(self, text="Listar/Editar Funcionários", width=30, command=self.listar_funcionarios).pack(pady=4)
        tk.Button(self, text="Aprovar/Rejeitar Solicitações de Viagem", width=30, command=self.aprovar_viagens).pack(pady=4)
        tk.Button(self, text="Configurar Políticas de Despesas", width=30, command=self.configurar_politicas).pack(pady=4)
        tk.Button(self, text="Relatórios de Viagem", width=30, command=self.relatorio_viagem).pack(pady=4)
        tk.Button(self, text="Relatórios de Auditoria", width=30, command=self.relatorio_auditoria).pack(pady=4)
        tk.Button(self, text="Sair", width=30, command=self.sair).pack(pady=10)

    def cadastrar_funcionario(self):
        messagebox.showinfo("Funcionalidade", "Abrir tela de cadastro de funcionário.")

    def listar_funcionarios(self):
        messagebox.showinfo("Funcionalidade", "Abrir tela de listagem/edição de funcionários.")

    def aprovar_viagens(self):
        messagebox.showinfo("Funcionalidade", "Abrir tela de aprovação/rejeição de viagens.")

    def configurar_politicas(self):
        messagebox.showinfo("Funcionalidade", "Abrir tela de configuração de políticas de despesas.")

    def relatorio_viagem(self):
        messagebox.showinfo("Funcionalidade", "Abrir tela de relatórios de viagem.")

    def relatorio_auditoria(self):
        messagebox.showinfo("Funcionalidade", "Abrir tela de relatórios de auditoria.")

    def sair(self):
        self.master.destroy()
