
import sys
import os
import tkinter as tk
from tkinter import messagebox

# Garante que o diretório raiz está no sys.path para imports absolutos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.gestor_controller import buscar_gestor

class TestGestorDB(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Teste de Conexão com o Banco - Gestor", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self, text="Digite o nome do gestor cadastrado:").pack()
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=5)
        tk.Button(self, text="Buscar", command=self.buscar_gestor).pack(pady=10)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(pady=10)

    def buscar_gestor(self):
        nome = self.entry_nome.get().strip()
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        if not nome:
            messagebox.showerror("Erro", "Informe o nome do gestor.")
            return
        resultado = buscar_gestor(nome)
        gestor = None
        if resultado and hasattr(resultado, 'nome'):
            gestor = resultado
        elif isinstance(resultado, tuple) and resultado[0]:
            gestor = resultado[1]
        if gestor:
            tk.Label(self.result_frame, text="Dados do Gestor:", font=("Arial", 12, "bold")).pack(anchor="w")
            for attr, value in gestor.__dict__.items():
                tk.Label(self.result_frame, text=f"{attr}: {value}", font=("Arial", 11)).pack(anchor="w", padx=20)
        else:
            tk.Label(self.result_frame, text="Gestor não encontrado.", fg="red").pack()

def main():
    root = tk.Tk()
    root.title("Teste Gestor - Banco de Dados")
    TestGestorDB(root)
    root.mainloop()

if __name__ == "__main__":
    main()
