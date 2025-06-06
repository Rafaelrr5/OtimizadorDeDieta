"""
Otimizador de Dieta - Aplicação Principal

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
