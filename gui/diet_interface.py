"""
Interface gráfica para o otimizador de dieta
"""

import tkinter as tk
from tkinter import ttk, messagebox
from optimization.diet_optimizer import optimize_diet
from config.constants import *

class DietApp:
    """Classe principal da interface gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.setup_style()
        self.create_widgets()
    
    def setup_style(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        style.theme_use(WINDOW_THEME)
    
    def create_widgets(self):
        """Cria e posiciona os elementos da interface"""
        # Configuração do layout principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Otimizador de Dieta", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, columnspan=2, pady=(0, 20))
        
        # Criação dos campos de entrada
        self.create_input_fields(main_frame)
        
        # Frame para botões
        self.create_button_frame(main_frame)
        
        # Área de resultados
        self.create_result_display(main_frame)
    
    def create_input_fields(self, parent):
        """Cria os campos de entrada de dados"""
        input_frame = ttk.LabelFrame(parent, text="Parâmetros da Dieta", padding=10)
        input_frame.grid(row=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        for row, (label, entry_var, placeholder) in enumerate(FIELD_LABELS):
            ttk.Label(input_frame, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=row, column=1, pady=5, padx=10, sticky=(tk.W, tk.E))
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e, ph=placeholder: self.clear_placeholder(e, ph))
            setattr(self, entry_var, entry)
    
    def create_button_frame(self, parent):
        """Cria o frame com botões de ação"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, columnspan=2, pady=15)
        
        buttons = [
            ("Otimizar Dieta", self.run_optimization),
            ("Limpar", self.clear_fields),
            ("Exemplo", self.load_example)
        ]
        
        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)
    
    def clear_placeholder(self, event, placeholder):
        """Remove placeholder quando o campo recebe foco"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
    
    def create_result_display(self, parent):
        """Cria a área de exibição de resultados"""
        result_frame = ttk.LabelFrame(parent, text="Resultados", padding=10)
        result_frame.grid(row=6, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        text_frame = ttk.Frame(result_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(text_frame, 
                                 height=RESULT_DISPLAY['height'], 
                                 width=RESULT_DISPLAY['width'], 
                                 state=tk.DISABLED,
                                 wrap=RESULT_DISPLAY['wrap'],
                                 font=RESULT_DISPLAY['font'])
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text.configure(yscrollcommand=scrollbar.set)
    
    def load_example(self):
        """Carrega valores de exemplo"""
        entries = [self.cal_entry, self.prot_entry, self.fat_entry, self.budget_entry]
        values = [DEFAULT_VALUES['calorias'], DEFAULT_VALUES['proteina'], 
                 DEFAULT_VALUES['gordura'], DEFAULT_VALUES['orcamento']]
        
        for entry, value in zip(entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)
    
    def clear_fields(self):
        """Limpa todos os campos"""
        for entry in [self.cal_entry, self.prot_entry, self.fat_entry, self.budget_entry]:
            entry.delete(0, tk.END)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def run_optimization(self):
        """Executa a otimização e exibe os resultados"""
        try:
            inputs = self.validate_inputs()
            if not inputs:
                return
            
            self.show_processing_message()
            self.root.update()
            
            resultado = optimize_diet(*inputs)
            self.show_results(resultado)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante a otimização:\n{str(e)}")
    
    def show_processing_message(self):
        """Mostra mensagem de processamento"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Processando otimização...\n")
        self.result_text.config(state=tk.DISABLED)
    
    def validate_inputs(self):
        """Valida e converte os valores de entrada"""
        try:
            values = []
            entries = [self.cal_entry, self.prot_entry, self.fat_entry, self.budget_entry]
            
            for entry, name in zip(entries, VALIDATION_NAMES):
                value_str = entry.get().replace("Ex: ", "").strip()
                if not value_str:
                    messagebox.showerror("Erro", f"Campo {name} está vazio!")
                    return None
                
                value = float(value_str)
                if value <= 0:
                    messagebox.showerror("Erro", f"{name} deve ser maior que zero!")
                    return None
                values.append(value)
            
            return tuple(values)
            
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos! Use apenas números.")
            return None
    
    def show_results(self, resultado):
        """Atualiza a área de resultados com os dados da otimização"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if resultado['status'] == 'Optimal':
            self.display_success_results(resultado)
        else:
            self.display_error_message(resultado['status'])
        
        self.result_text.config(state=tk.DISABLED)
    
    def display_success_results(self, resultado):
        """Exibe os resultados de uma solução bem-sucedida"""
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        self.result_text.insert(tk.END, "           DIETA OTIMIZADA\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Lista de alimentos recomendados
        self.result_text.insert(tk.END, "ALIMENTOS RECOMENDADOS:\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
        
        alimentos_utilizados = []
        for alimento, qtd in resultado['quantidades'].items():
            if qtd > NUMERICAL_TOLERANCE:
                alimentos_utilizados.append((alimento, qtd))
        
        if alimentos_utilizados:
            for alimento, qtd in sorted(alimentos_utilizados, key=lambda x: x[1], reverse=True):
                self.result_text.insert(tk.END, f"• {alimento:<20}: {qtd:>6.2f} porções\n")
        else:
            self.result_text.insert(tk.END, "Nenhum alimento necessário.\n")
        
        # Resumo nutricional
        self.result_text.insert(tk.END, f"\n{'RESUMO NUTRICIONAL:'}\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
        self.result_text.insert(tk.END, f"Calorias totais: {resultado['detalhes']['calorias_total']:>10.1f} kcal\n")
        self.result_text.insert(tk.END, f"Proteína total:  {resultado['detalhes']['proteina_total']:>10.1f} g\n")
        self.result_text.insert(tk.END, f"Gordura total:   {resultado['detalhes']['gordura_total']:>10.1f} g\n")
        
        # Custo total
        self.result_text.insert(tk.END, f"\n{'CUSTO:'}\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
        self.result_text.insert(tk.END, f"Custo total:     R$ {resultado['custo_total']:>10.2f}\n")
        
        self.result_text.insert(tk.END, "\n" + "=" * 50 + "\n")
    
    def display_error_message(self, status):
        """Exibe mensagem para casos sem solução"""
        self.result_text.insert(tk.END, "=" * 50 + "\n")
        self.result_text.insert(tk.END, "        PROBLEMA SEM SOLUÇÃO\n")
        self.result_text.insert(tk.END, "=" * 50 + "\n\n")
        
        self.result_text.insert(tk.END, f"Status: {status}\n\n")
        self.result_text.insert(tk.END, "Não foi possível encontrar uma solução viável\n")
        self.result_text.insert(tk.END, "com as restrições especificadas.\n\n")
        
        self.result_text.insert(tk.END, "SUGESTÕES:\n")
        self.result_text.insert(tk.END, "-" * 20 + "\n")
        self.result_text.insert(tk.END, "• Aumente o orçamento disponível\n")
        self.result_text.insert(tk.END, "• Reduza as exigências de calorias ou proteína\n")
        self.result_text.insert(tk.END, "• Aumente o limite de gordura\n")
        self.result_text.insert(tk.END, "• Verifique se os valores estão realistas\n")
