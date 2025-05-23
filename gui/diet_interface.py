"""
Interface gráfica para o otimizador de dieta
"""

import tkinter as tk
from tkinter import ttk, messagebox
from optimization.diet_optimizer import optimize_diet
from config.constants import *
from data.food_database import get_food_data, get_food_categories

class DietApp:
    """Classe principal da interface gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(500, 400)  # Define um tamanho mínimo para a janela
        self.setup_style()
        
        # Lista de alimentos a serem excluídos
        self.excluded_foods = []
        
        # Lista completa de alimentos
        self.all_foods = get_food_data()
        
        self.create_widgets()
    
    def setup_style(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        style.theme_use(WINDOW_THEME)

    def create_widgets(self):
        """Cria e posiciona os elementos da interface"""
        # Configurar redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Criar canvas principal para scroll
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Adicionar barras de rolagem
        v_scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.main_canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        h_scrollbar = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.main_canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar canvas com scrollbars
        self.main_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Frame principal dentro do canvas
        main_frame = ttk.Frame(self.main_canvas, padding=20)
        self.canvas_frame_id = self.main_canvas.create_window((0, 0), window=main_frame, anchor=tk.NW)
        
        # Configurar redimensionamento do frame principal
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        
        # Configurar redimensionamento de todas as linhas importantes
        for i in range(7):
            main_frame.rowconfigure(i, weight=1 if i == 6 else 0)  # Dá peso à linha de resultados
        
        # Bind eventos para atualizar scroll region
        main_frame.bind("<Configure>", self.on_frame_configure)
        self.main_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind mousewheel para scroll
        self.bind_mousewheel()
        
        # Título
        title_label = ttk.Label(main_frame, text="Otimizador de Dieta", 
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, columnspan=2, pady=(0, 20))
        
        # Criação dos campos de entrada
        self.create_input_fields(main_frame)
        
        # Criação da área de exclusão de alimentos
        self.create_food_selection(main_frame)
        
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

    def create_food_selection(self, parent):
        """Cria a área para seleção de alimentos a excluir"""
        food_frame = ttk.LabelFrame(parent, text="Excluir Alimentos", padding=10)
        food_frame.grid(row=2, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        food_frame.columnconfigure(0, weight=1)
        
        # Exibição dos alimentos selecionados para exclusão
        excluded_label = ttk.Label(food_frame, text="Alimentos excluídos:")
        excluded_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Frame para conter o texto e barra de rolagem
        excluded_frame = ttk.Frame(food_frame)
        excluded_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        excluded_frame.columnconfigure(0, weight=1)
        excluded_frame.rowconfigure(0, weight=1)
        
        self.excluded_display = tk.Text(excluded_frame, height=2, width=40, wrap=tk.WORD)
        self.excluded_display.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.excluded_display.insert(tk.END, "Nenhum alimento excluído")
        self.excluded_display.config(state=tk.DISABLED)
        
        # Adiciona barra de rolagem horizontal para a área de alimentos excluídos
        hsb = ttk.Scrollbar(excluded_frame, orient=tk.HORIZONTAL, command=self.excluded_display.xview)
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.excluded_display.configure(xscrollcommand=hsb.set)
        
        # Botão para selecionar alimentos a excluir
        select_button = ttk.Button(food_frame, text="Selecionar Alimentos", command=self.open_food_selector)
        select_button.grid(row=2, column=0, pady=(0, 5))
    def open_food_selector(self):
        """Abre uma janela para seleção de alimentos a excluir"""
        self.selector_window = tk.Toplevel(self.root)
        self.selector_window.title("Selecionar Alimentos a Excluir")
        self.selector_window.geometry("500x400")
        self.selector_window.minsize(400, 300)  # Define o tamanho mínimo da janela de seleção
        self.selector_window.transient(self.root)
        self.selector_window.grab_set()
        
        # Configurar redimensionamento
        self.selector_window.columnconfigure(0, weight=1)
        self.selector_window.rowconfigure(0, weight=1)
        
        # Frame para a lista de alimentos
        selector_frame = ttk.Frame(self.selector_window, padding=10)
        selector_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        selector_frame.columnconfigure(0, weight=1)
        selector_frame.rowconfigure(0, weight=1)
        selector_frame.rowconfigure(1, weight=0)
        
        # Dicionário para armazenar as variáveis de cada checkbox
        self.food_vars = {}
          # Notebook para categorias
        categories_notebook = ttk.Notebook(selector_frame)
        categories_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Obter categorias de alimentos
        categories = get_food_categories()
        
        # Criar uma aba para cada categoria
        for category, foods in categories.items():
            # Frame com scroll para cada categoria
            cat_container = ttk.Frame(categories_notebook)
            categories_notebook.add(cat_container, text=category)
            
            cat_container.columnconfigure(0, weight=1)
            cat_container.rowconfigure(0, weight=1)
            
            # Canvas para permitir rolagem
            canvas = tk.Canvas(cat_container)
            canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Scrollbar para o canvas
            vsb = ttk.Scrollbar(cat_container, orient=tk.VERTICAL, command=canvas.yview)
            vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
            canvas.configure(yscrollcommand=vsb.set)
            
            # Frame dentro do canvas para os checkboxes
            category_frame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=category_frame, anchor=tk.NW, tags="category_frame")
            
            # Adicionar checkboxes para cada alimento na categoria
            for i, food_name in enumerate(sorted(foods)):
                var = tk.BooleanVar(value=food_name in self.excluded_foods)
                self.food_vars[food_name] = var
                
                checkbox = ttk.Checkbutton(category_frame, text=food_name, variable=var)
                checkbox.grid(row=i, column=0, sticky=tk.W, pady=2)
            
            # Atualizar o scrollregion sempre que o tamanho do frame mudar
            category_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
        
        # Botões Aplicar/Cancelar
        button_frame = ttk.Frame(selector_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.E), pady=10)
        
        apply_button = ttk.Button(button_frame, text="Aplicar", command=self.apply_food_selection)
        apply_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Cancelar", command=self.selector_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def apply_food_selection(self):
        """Aplica a seleção de alimentos excluídos"""
        self.excluded_foods = [food for food, var in self.food_vars.items() if var.get()]
        self.update_excluded_display()
        self.selector_window.destroy()
    
    def update_excluded_display(self):
        """Atualiza o display de alimentos excluídos"""
        self.excluded_display.config(state=tk.NORMAL)
        self.excluded_display.delete(1.0, tk.END)
        
        if self.excluded_foods:
            self.excluded_display.insert(tk.END, ", ".join(self.excluded_foods))
        else:
            self.excluded_display.insert(tk.END, "Nenhum alimento excluído")
        
        self.excluded_display.config(state=tk.DISABLED)
    
    def find_food_info(self, nome_alimento):
        """Busca informações detalhadas de um alimento pelo nome
        
        Args:
            nome_alimento (str): Nome do alimento
            
        Returns:
            dict or None: Dicionário com informações do alimento ou None se não encontrado
        """
        for food in self.all_foods:
            if food['nome'] == nome_alimento:
                return food
        return None
    
    def get_food_category(self, nome_alimento):
        """Obtém a categoria de um alimento pelo nome
        
        Args:
            nome_alimento (str): Nome do alimento
            
        Returns:
            str: Nome da categoria ou "Outros" se não encontrado
        """
        categorias = get_food_categories()
        for categoria, alimentos in categorias.items():
            if nome_alimento in alimentos:
                return categoria
        return "Outros"
    
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
          # Configura a área de texto para expandir com o redimensionamento da janela
        self.result_text = tk.Text(text_frame, 
                                 height=RESULT_DISPLAY['height'], 
                                 width=RESULT_DISPLAY['width'], 
                                 state=tk.DISABLED,
                                 wrap=None,  # Muda para None para permitir rolagem horizontal
                                 font=RESULT_DISPLAY['font'])
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Adiciona barras de rolagem vertical e horizontal
        vsb = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        hsb = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.result_text.xview)
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        text_frame.rowconfigure(1, weight=0)  # A linha da barra de rolagem horizontal não expande
        self.result_text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
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
            
        # Limpar alimentos excluídos
        self.excluded_foods = []
        self.update_excluded_display()
        
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
            
            # Adicionar a lista de alimentos excluídos
            values.append(self.excluded_foods if self.excluded_foods else None)
            
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
        self.result_text.insert(tk.END, "-" * 60 + "\n")
        
        # Cabeçalho da tabela
        self.result_text.insert(tk.END, f"{'Nome':<20} {'Qtd':>6} {'R$/porção':>10} {'R$ Total':>10}\n")
        self.result_text.insert(tk.END, "-" * 60 + "\n")
        
        alimentos_utilizados = []
        for alimento, qtd in resultado['quantidades'].items():
            if qtd > NUMERICAL_TOLERANCE:
                # Buscar informações do alimento na base de dados
                food_info = self.find_food_info(alimento)
                alimentos_utilizados.append((alimento, qtd, food_info['preco'] if food_info else 0))
        
        if alimentos_utilizados:
            for alimento, qtd, preco in sorted(alimentos_utilizados, key=lambda x: x[1], reverse=True):
                custo_total = qtd * preco
                self.result_text.insert(tk.END, f"• {alimento:<18} {qtd:>6.2f} {preco:>10.2f} {custo_total:>10.2f}\n")
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
        
        # Informações sobre porções
        self.result_text.insert(tk.END, f"\n{'INFORMAÇÕES SOBRE PORÇÕES:'}\n")
        self.result_text.insert(tk.END, "-" * 40 + "\n")
        self.result_text.insert(tk.END, "Uma porção de cada alimento contém:\n\n")
        
        # Buscar alimentos utilizados e mostrar detalhes de cada porção
        categorias = {}
        for alimento, qtd in resultado['quantidades'].items():
            if qtd > NUMERICAL_TOLERANCE:
                food_info = self.find_food_info(alimento)
                if food_info:
                    categoria = self.get_food_category(alimento)
                    if categoria not in categorias:
                        categorias[categoria] = []
                    categorias[categoria].append((alimento, food_info))
        
        # Mostrar por categoria
        for categoria, alimentos in sorted(categorias.items()):
            self.result_text.insert(tk.END, f"{categoria}:\n")
            for alimento, info in alimentos:
                self.result_text.insert(tk.END, f"• {alimento:<15}: {info['calorias']:>5} kcal, " + 
                                            f"{info['proteina']:>4}g prot, " + 
                                            f"{info['gordura']:>4}g gord, " + 
                                            f"R${info['preco']:>5.2f}\n")
            self.result_text.insert(tk.END, "\n")
        
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
    
    def on_frame_configure(self, event):
        """Atualiza a região de scroll quando o frame muda de tamanho"""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Ajusta o tamanho do frame quando o canvas é redimensionado"""
        canvas_width = event.width
        canvas_height = event.height
        
        # Obter o frame dentro do canvas
        frame = self.main_canvas.nametowidget(self.main_canvas.itemcget(self.canvas_frame_id, "window"))
        
        # Definir largura mínima e altura mínima para o frame
        min_width = 600  # Largura mínima desejada
        min_height = 700  # Altura mínima desejada
        
        # Usar o maior valor entre o tamanho do canvas e o tamanho mínimo
        frame_width = max(canvas_width - 20, min_width)  # -20 para padding
        frame_height = max(canvas_height - 20, min_height)  # -20 para padding
        
        # Configurar o tamanho do frame
        self.main_canvas.itemconfig(self.canvas_frame_id, width=frame_width, height=frame_height)
    
    def bind_mousewheel(self):
        """Configura o scroll com a roda do mouse"""
        def on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def on_shift_mousewheel(event):
            self.main_canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind para Windows
        self.main_canvas.bind("<MouseWheel>", on_mousewheel)
        self.main_canvas.bind("<Shift-MouseWheel>", on_shift_mousewheel)
        
        # Bind para Linux
        self.main_canvas.bind("<Button-4>", lambda e: self.main_canvas.yview_scroll(-1, "units"))
        self.main_canvas.bind("<Button-5>", lambda e: self.main_canvas.yview_scroll(1, "units"))
        self.main_canvas.bind("<Shift-Button-4>", lambda e: self.main_canvas.xview_scroll(-1, "units"))
        self.main_canvas.bind("<Shift-Button-5>", lambda e: self.main_canvas.xview_scroll(1, "units"))
        
        # Dar foco ao canvas para permitir scroll
        self.main_canvas.focus_set()
