import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Destino Corporativo - Menu Principal")
        self.geometry("400x400")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Destino Corporativo", font=("Arial", 18, "bold")).pack(pady=20)

        btn_gestor = tk.Button(self, text="Gestores", width=25, command=self.abrir_gestor)
        btn_gestor.pack(pady=5)

        btn_funcionario = tk.Button(self, text="Funcionários", width=25, command=self.abrir_funcionario)
        btn_funcionario.pack(pady=5)

        btn_viagem = tk.Button(self, text="Viagens", width=25, command=self.abrir_viagem)
        btn_viagem.pack(pady=5)

        btn_despesa = tk.Button(self, text="Despesas", width=25, command=self.abrir_despesa)
        btn_despesa.pack(pady=5)

        btn_relatorio = tk.Button(self, text="Relatórios", width=25, command=self.abrir_relatorio)
        btn_relatorio.pack(pady=5)

        btn_sair = tk.Button(self, text="Sair", width=25, command=self.quit)
        btn_sair.pack(pady=20)

    def abrir_gestor(self):
        messagebox.showinfo("Gestores", "Abrir tela de Gestores (implementar)")

    def abrir_funcionario(self):
        messagebox.showinfo("Funcionários", "Abrir tela de Funcionários (implementar)")

    def abrir_viagem(self):
        messagebox.showinfo("Viagens", "Abrir tela de Viagens (implementar)")

    def abrir_despesa(self):
        messagebox.showinfo("Despesas", "Abrir tela de Despesas (implementar)")

    def abrir_relatorio(self):
        messagebox.showinfo("Relatórios", "Abrir tela de Relatórios (implementar)")


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
