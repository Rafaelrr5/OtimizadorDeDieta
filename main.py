"""
Otimizador de Dieta - Aplicação Principal
Executa a interface gráfica do otimizador de dieta usando programação linear.

Para executar: python main.py
"""

import tkinter as tk
from gui.diet_interface import DietApp

def main():
    """Função principal da aplicação"""
    # Criar janela principal
    root = tk.Tk()
    
    # Inicializar aplicação
    app = DietApp(root)
    
    # Executar loop principal
    root.mainloop()

if __name__ == "__main__":
    main()
