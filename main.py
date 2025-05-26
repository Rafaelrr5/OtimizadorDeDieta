"""
Otimizador de Dieta - Aplicação Principal
Executa a interface gráfica do otimizador de dieta usando programação linear.

Para executar: python main.py
"""

import tkinter as tk
from gui.diet_interface import DietApp

def main():
    """Função principal da aplicação"""
    # Inicializar e executar aplicação
    app = DietApp()
    app.run()

if __name__ == "__main__":
    main()
