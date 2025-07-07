import sys
import os
import tkinter as tk
from tkinter import messagebox

# Garante que o diretório raiz está no sys.path para imports absolutos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.gestor_controller import buscar_gestor
from controllers.funcionario_controller import buscar_funcionario

class LoginScreen(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Destino Corporativo", font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(self, text="Login pelo nome cadastrado no sistema:").pack()
        tk.Label(self, text="Nome completo:").pack()
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=2)
        tk.Label(self, text="Perfil:").pack()
        self.perfil_var = tk.StringVar(value="funcionario")
        tk.Radiobutton(self, text="Funcionário", variable=self.perfil_var, value="funcionario").pack(anchor="w")
        tk.Radiobutton(self, text="Gestor", variable=self.perfil_var, value="gestor").pack(anchor="w")
        tk.Label(self, text="(Use o nome exatamente como cadastrado pelo gestor/administrador)", font=("Arial", 8, "italic"), fg="gray").pack(pady=2)
        tk.Button(self, text="Entrar", command=self.login).pack(pady=10)

    def login(self):
        nome = self.entry_nome.get().strip()
        perfil = self.perfil_var.get()
        if not nome:
            messagebox.showerror("Erro", "Informe o nome para login.")
            return
        if perfil == "gestor":
            ok, result = buscar_gestor_por_nome(nome)
        else:
            ok, result = buscar_funcionario_por_nome(nome)
        if ok:
            self.destroy()
            if perfil == "gestor":
                from menu_gestor import MenuGestor
                MenuGestor(self.master, result)
            else:
                # Aqui você pode importar e chamar o menu do funcionário
                # from menu_funcionario import MenuFuncionario
                # MenuFuncionario(self.master, result)
                messagebox.showinfo("Sucesso", f"Bem-vindo, {result.nome}! (Menu do funcionário em construção)")
        else:
            messagebox.showerror("Erro", result)

# Funções auxiliares para buscar por nome (ajuste conforme controllers)
def buscar_gestor_por_nome(nome):
    gestor = None
    try:
        gestor = buscar_gestor(nome) if callable(buscar_gestor) else None
    except Exception:
        pass
    if gestor and hasattr(gestor, 'nome'):
        return True, gestor
    # Se controller retorna (bool, obj/msg):
    if isinstance(gestor, tuple) and gestor[0]:
        return True, gestor[1]
    return False, "Gestor não encontrado."

def buscar_funcionario_por_nome(nome):
    funcionario = None
    try:
        funcionario = buscar_funcionario(nome) if callable(buscar_funcionario) else None
    except Exception:
        pass
    if funcionario and hasattr(funcionario, 'nome'):
        return True, funcionario
    if isinstance(funcionario, tuple) and funcionario[0]:
        return True, funcionario[1]
    return False, "Funcionário não encontrado."

def main():
    root = tk.Tk()
    root.title("Destino Corporativo - Login")
    LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
