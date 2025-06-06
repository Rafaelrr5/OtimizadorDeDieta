import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from optimization.diet_optimizer import optimize_diet
from config.constants import *
from data.food_database import get_food_data, get_food_categories, get_food_by_name
from tkinter.ttk import Notebook

class DietApp:
    """Classe principal da interface gráfica moderna"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🥗 Otimizador de Dieta com Programação Linear")
        self.root.geometry("1200x800")
        self.root.minsize(900, 600)
        
        # Configurar cores modernas (tema escuro)
        self.colors = {
            'bg_primary': '#1e1e2e',      # Fundo principal
            'bg_secondary': '#313244',    # Fundo secundário
            'bg_tertiary': '#45475a',     # Fundo terciário
            'accent': '#89b4fa',          # Cor de destaque (azul)
            'accent_hover': '#74c7ec',    # Cor de destaque hover
            'success': '#a6e3a1',         # Verde para sucesso
            'warning': '#f9e2af',         # Amarelo para avisos
            'error': '#f38ba8',           # Rosa para erros
            'text_primary': '#cdd6f4',    # Texto principal
            'text_secondary': '#bac2de'   # Texto secundário
        }
        
        # Configurar tema escuro
        self.setup_dark_theme()
          # Dados da aplicação
        self.excluded_foods = []
        self.all_foods = get_food_data()
        self.use_portion_limits = tk.BooleanVar(value=True)
        self.placeholder_status = {}  # Initialize placeholder tracking
        self.auto_entries = {}  # Store widgets for automatic calculation inputs
        
        # Configurar grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Criar widgets
        self.create_widgets()
    
    def setup_dark_theme(self):
        """Configura tema escuro moderno"""
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configurar estilo ttk
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores para widgets ttk
        style.configure('Title.TLabel', 
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 20, 'bold'))
        
        style.configure('Heading.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 14, 'bold'))
        
        style.configure('Modern.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10))
        
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['bg_tertiary'],
                       bordercolor=self.colors['accent'],
                       foreground=self.colors['text_primary'],
                       insertcolor=self.colors['text_primary'])
        
        style.configure('Modern.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='raised',
                       borderwidth=2)
        
        style.configure('Modern.TCheckbutton',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       focuscolor='none')
    
    def create_widgets(self):
        """Cria e posiciona os elementos da interface usando abas"""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        # Criar Notebook
        notebook = Notebook(self.root)
        notebook.grid(row=0, column=0, sticky="nsew")
        # Abas
        auto_tab = ttk.Frame(notebook, style='Modern.TFrame', padding=20)
        params_tab = ttk.Frame(notebook, style='Modern.TFrame', padding=20)
        exclusion_tab = ttk.Frame(notebook, style='Modern.TFrame', padding=20)
        results_tab = ttk.Frame(notebook, style='Modern.TFrame', padding=20)
        notebook.add(auto_tab, text="🧮 Auto Cálculo")
        notebook.add(params_tab, text="📊 Parâmetros")
        notebook.add(exclusion_tab, text="🚫 Exclusões")
        notebook.add(results_tab, text="📋 Resultados")
        # Construir seções em cada aba
        self.create_auto_calc_section(auto_tab)
        # Parâmetros
        title_label = ttk.Label(params_tab, text="🥗 Otimizador de Dieta com Programação Linear", style='Title.TLabel')
        title_label.pack(pady=(0,20))
        self.create_input_section(params_tab)
        self.create_action_buttons(params_tab)
        # Exclusões
        self.create_food_exclusion_section(exclusion_tab)
        # Resultados
        self.create_results_section(results_tab)
    
    def create_input_section(self, parent):
        """Cria a seção de entrada de parâmetros"""
        # Frame para parâmetros
        params_frame = ttk.LabelFrame(parent, text="📊 Parâmetros Nutricionais", style='Card.TFrame', padding=20)
        params_frame.pack(fill='x', pady=(0,20))
        params_frame.grid_columnconfigure((0,1), weight=1)
        
        # Grid para organizar entradas
        entries_data = [
            ("🔥 Calorias mínimas (kcal):", "cal_entry", str(DEFAULT_VALUES['calorias'])),
            ("💪 Proteína mínima (g):", "prot_entry", str(DEFAULT_VALUES['proteina'])),
            ("🧈 Gordura máxima (g):", "fat_entry", str(DEFAULT_VALUES['gordura'])),
            ("💰 Orçamento máximo (R$):", "budget_entry", str(DEFAULT_VALUES['orcamento']))
        ]
        
        self.entries = {}
        
        for i, (label_text, entry_name, placeholder) in enumerate(entries_data):
            # Label
            label = ttk.Label(params_frame, text=label_text, style='Modern.TLabel')
            label.grid(row=i, column=0, sticky="w", padx=(0, 20), pady=10)
            
            # Entry
            entry = ttk.Entry(params_frame, style='Modern.TEntry', font=('Segoe UI', 11))
            entry.grid(row=i, column=1, sticky="ew", pady=10)
            entry.insert(0, placeholder)
            
            # Mark as placeholder - store in dict for validation
            self.placeholder_status[entry_name] = True
            
            # Efeito placeholder
            entry.bind('<FocusIn>', lambda e, ph=placeholder, name=entry_name: self.clear_placeholder(e, ph, name))
            entry.bind('<FocusOut>', lambda e, ph=placeholder, name=entry_name: self.restore_placeholder(e, ph, name))
            
            self.entries[entry_name] = entry
            setattr(self, entry_name, entry)
        
        # Checkbox para limites de porção
        checkbox_frame = ttk.Frame(params_frame, style='Modern.TFrame')
        checkbox_frame.grid(row=len(entries_data), column=0, columnspan=2, pady=20)
        
        self.portion_checkbox = ttk.Checkbutton(
            checkbox_frame,
            text="⚖️ Usar limites de porção por categoria",
            variable=self.use_portion_limits,
            style='Modern.TCheckbutton'
        )
        self.portion_checkbox.pack()
    
    def create_food_exclusion_section(self, parent):
        """Cria a seção de exclusão de alimentos"""
        # Frame para exclusão
        exclusion_frame = ttk.LabelFrame(parent,
             text="🚫 Exclusão de Alimentos",
             style='Card.TFrame',
             padding=20
         )
        exclusion_frame.pack(fill='x', pady=(0,20))
        exclusion_frame.grid_columnconfigure(0, weight=1)
        
        # Área de exibição
        display_frame = ttk.Frame(exclusion_frame, style='Modern.TFrame')
        display_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        display_frame.grid_columnconfigure(0, weight=1)
        
        self.excluded_display = tk.Text(
            display_frame,
            height=3,
            wrap=tk.WORD,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            font=('Segoe UI', 10),
            relief='flat',
            padx=10,
            pady=5
        )
        self.excluded_display.grid(row=0, column=0, sticky="ew")
        self.excluded_display.insert("1.0", "Nenhum alimento excluído")
        self.excluded_display.configure(state=tk.DISABLED)
        
        # Scrollbar para texto
        text_scroll = ttk.Scrollbar(display_frame, orient="vertical", command=self.excluded_display.yview)
        text_scroll.grid(row=0, column=1, sticky="ns")
        self.excluded_display.configure(yscrollcommand=text_scroll.set)
        
        # Botão de seleção
        select_button = self.create_modern_button(
            exclusion_frame,
            "🥘 Selecionar Alimentos para Excluir",
            self.open_food_selector,
            self.colors['accent']
        )
        select_button.grid(row=1, column=0, pady=(0, 10))
    
    def create_action_buttons(self, parent):
        """Cria os botões de ação"""
        # Frame para botões
        button_frame = ttk.Frame(parent, style='Modern.TFrame')
        button_frame.pack(fill='x', pady=(0,20))
        button_frame.grid_columnconfigure((0,1,2), weight=1)
        # Botão principal de otimização
        optimize_button = self.create_modern_button(
            button_frame,
            "🚀 Otimizar Dieta",
            self.run_optimization,
            self.colors['success'],
            height=50
        )
        optimize_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        # Botão de exemplo
        example_button = self.create_modern_button(
            button_frame,
            "📝 Carregar Exemplo",
            self.load_example,
            self.colors['warning']
        )
        example_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Botão de limpar
        clear_button = self.create_modern_button(
            button_frame,
            "🗑️ Limpar Tudo",
            self.clear_fields,
            self.colors['error']
        )
        clear_button.grid(row=0, column=2, padx=5, sticky="ew")
    
    def create_auto_calc_section(self, parent):
        """Cria a seção de cálculo automático de parâmetros baseados em dados pessoais"""
        frame = ttk.LabelFrame(parent, text="🔢 Cálculo Automático", style='Card.TFrame', padding=20)
        frame.pack(fill='x', pady=(0,20))
        frame.grid_columnconfigure((0,1), weight=1)
        fields = [("Peso (kg):","weight"),("Altura (cm):","height"),("Idade (anos):","age"),("Sexo (Masculino/Feminino):","gender"),("Nível de Atividade:","activity")]
        activity_options = ['Sedentário','Leve','Moderado','Ativo','Muito Ativo']
        for i,(label_text,key) in enumerate(fields):
            label = ttk.Label(frame, text=label_text, style='Modern.TLabel')
            label.grid(row=i, column=0, sticky='w', padx=(0,20), pady=10)
            if key=='gender':
                combo = ttk.Combobox(frame, values=['Masculino','Feminino'], state='readonly', style='Modern.TEntry')
                combo.grid(row=i, column=1, sticky='ew', pady=10)
                self.auto_entries[key] = combo
            elif key=='activity':
                combo = ttk.Combobox(frame, values=activity_options, state='readonly', style='Modern.TEntry')
                combo.grid(row=i, column=1, sticky='ew', pady=10)
                self.auto_entries[key] = combo
            else:
                entry = ttk.Entry(frame, style='Modern.TEntry', font=('Segoe UI',11))
                entry.grid(row=i, column=1, sticky='ew', pady=10)
                self.auto_entries[key] = entry
        # Botão de cálculo
        calc_btn = self.create_modern_button(frame, "🔢 Calcular", self.calculate_parameters, self.colors['accent'])
        calc_btn.grid(row=len(fields), column=0, columnspan=2, pady=10, sticky='ew')
    
    def calculate_parameters(self):
        """Calcula calorias, proteína e gordura automaticamente via dados pessoais"""
        try:
            # Coletar valores do formulário automático
            weight = float(self.auto_entries['weight'].get())
            height = float(self.auto_entries['height'].get())
            age = int(self.auto_entries['age'].get())
            sex = self.auto_entries['gender'].get()
            activity = self.auto_entries['activity'].get()
            # Validar preenchimento
            if not all([weight, height, age, sex, activity]):
                messagebox.showerror("Campos Incompletos","Preencha todos os campos de cálculo automático.")
                return
            # Níveis de atividade
            activity_levels = {'Sedentário':1.2,'Leve':1.375,'Moderado':1.55,'Ativo':1.725,'Muito Ativo':1.9}
            if sex not in ('Masculino','Feminino') or activity not in activity_levels:
                messagebox.showerror("Erro de Validação","Sexo ou nível de atividade inválido.")
                return
            factor = activity_levels[activity]
            # Cálculo BMR e TDEE
            bmr = (10*weight + 6.25*height -5*age +5) if sex=='Masculino' else (10*weight + 6.25*height -5*age -161)
            tdee = bmr * factor
            calories = round(tdee)
            protein = round(1.6 * weight)
            fat = round((0.25 * calories) / 9)
            # Preencher campos de parâmetros
            self.entries['cal_entry'].delete(0, tk.END)
            self.entries['cal_entry'].insert(0, str(calories))
            self.entries['prot_entry'].delete(0, tk.END)
            self.entries['prot_entry'].insert(0, str(protein))
            self.entries['fat_entry'].delete(0, tk.END)
            self.entries['fat_entry'].insert(0, str(fat))
            messagebox.showinfo("Valores Calculados", f"Calorias: {calories} kcal\nProteína: {protein} g\nGordura: {fat} g")
        except Exception as e:
            messagebox.showerror("Erro no Cálculo", f"Falha ao calcular parâmetros: {e}")
    
    def create_modern_button(self, parent, text, command, bg_color, height=40):
        """Cria um botão moderno personalizado"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg=self.colors['bg_primary'],
            font=('Segoe UI', 11, 'bold'),
            relief='flat',
            borderwidth=0,
            height=2 if height == 40 else 3,
            cursor='hand2'
        )
        
        # Efeitos hover
        def on_enter(e):
            button.configure(bg=self.lighten_color(bg_color))
            
        def on_leave(e):
            button.configure(bg=bg_color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
    
    def lighten_color(self, color):
        """Clareia uma cor hexadecimal"""
        # Conversão simples para clarear cores
        color_map = {
            self.colors['success']: '#b8f2b8',
            self.colors['warning']: '#ffeaa7',
            self.colors['error']: '#ff7675',
            self.colors['accent']: '#a2c4ff'
        }
        return color_map.get(color, color)
    
    def create_results_section(self, parent):
        """Cria a seção de resultados da otimização"""
        # Frame para resultados
        results_frame = ttk.LabelFrame(parent,
             text="📋 Resultados da Otimização",
             style='Card.TFrame',
             padding=20
         )
        results_frame.pack(fill='both', expand=True, pady=(0,20))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Área de resultados com scroll
        text_frame = ttk.Frame(results_frame, style='Modern.TFrame')
        text_frame.pack(fill='both', expand=True)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        self.result_display = tk.Text(
            text_frame,
            wrap=tk.WORD,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            font=('Consolas', 11),
            relief='flat',
            padx=15,
            pady=10,
            state=tk.DISABLED
        )
        self.result_display.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_display.yview)
        v_scroll.grid(row=0, column=1, sticky="ns")
        
        h_scroll = ttk.Scrollbar(text_frame, orient="horizontal", command=self.result_display.xview)
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        self.result_display.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Texto inicial
        self.result_display.configure(state=tk.NORMAL)
        self.result_display.insert("1.0", "🔍 Resultados aparecerão aqui após a otimização...\n\n💡 Dica: Use o botão 'Carregar Exemplo' para testar rapidamente!")
        self.result_display.configure(state=tk.DISABLED)
        
        # Configurar peso para expansão        self.main_frame.grid_rowconfigure(4, weight=1)
    
    def clear_placeholder(self, event, placeholder, entry_name):
        """Remove placeholder quando o campo recebe foco"""
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            # Mark as not placeholder since user is about to enter real data
            if hasattr(self, 'placeholder_status'):
                self.placeholder_status[entry_name] = False
    
    def restore_placeholder(self, event, placeholder, entry_name):
        """Restaura placeholder se o campo estiver vazio"""
        if not event.widget.get():
            event.widget.insert(0, placeholder)            # Mark as placeholder since we're showing placeholder text
            if not hasattr(self, 'placeholder_status'):
                self.placeholder_status = {}
            self.placeholder_status[entry_name] = True
    
    def open_food_selector(self):
        """Abre janela moderna para seleção de alimentos"""
        # Criar janela de seleção de alimentos para exclusão
        top = tk.Toplevel(self.root)
        top.title("Selecionar Alimentos para Excluir")
        top.geometry("400x500")
        # Container de lista
        frame = ttk.Frame(top, style='Modern.TFrame', padding=10)
        frame.pack(fill='both', expand=True)
        listbox = tk.Listbox(
            frame,
            selectmode='multiple',
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            selectbackground=self.colors['accent'],
            activestyle='none'
        )
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=listbox.yview)
        scrollbar.pack(side='right', fill='y')
        listbox.configure(yscrollcommand=scrollbar.set)
        # Preencher lista com alimentos
        for idx, food in enumerate(self.all_foods):
            listbox.insert('end', food['nome'])
            if food['nome'] in self.excluded_foods:
                listbox.selection_set(idx)
        # Função de confirmação
        def confirm():
            selected = [listbox.get(i) for i in listbox.curselection()]
            self.excluded_foods = selected
            # Atualizar display de exclusões
            self.excluded_display.configure(state=tk.NORMAL)
            self.excluded_display.delete('1.0', tk.END)
            if selected:
                self.excluded_display.insert('1.0', "\n".join(selected))
            else:
                self.excluded_display.insert('1.0', 'Nenhum alimento excluído')
            self.excluded_display.configure(state=tk.DISABLED)
            top.destroy()
        # Botões de ação
        btn_frame = ttk.Frame(top, style='Modern.TFrame', padding=10)
        btn_frame.pack(fill='x')
        confirm_btn = self.create_modern_button(btn_frame, 'Confirmar', confirm, self.colors['accent'])
        confirm_btn.pack(side='left', expand=True, padx=5)
        cancel_btn = self.create_modern_button(btn_frame, 'Cancelar', top.destroy, self.colors['error'])
        cancel_btn.pack(side='right', expand=True, padx=5)
    
    def load_example(self):
        """Carrega valores de exemplo"""
        # Carregar exemplo de parâmetros a partir de DEFAULT_VALUES
        # Limpar exclusões
        self.excluded_foods = []
        self.excluded_display.configure(state='normal')
        self.excluded_display.delete('1.0', 'end')
        self.excluded_display.insert('1.0', 'Nenhum alimento excluído')
        self.excluded_display.configure(state='disabled')
        # Preencher campos
        for key, entry_name in [('calorias', 'cal_entry'), ('proteina', 'prot_entry'), ('gordura', 'fat_entry'), ('orcamento', 'budget_entry')]:
            entry = self.entries[entry_name]
            entry.delete(0, 'end')
            entry.insert(0, DEFAULT_VALUES[key])
        messagebox.showinfo(
            'Exemplo Carregado',
            f"Exemplo carregado: {DEFAULT_VALUES['calorias']} kcal, {DEFAULT_VALUES['proteina']}g proteína, {DEFAULT_VALUES['gordura']}g gordura, R$ {DEFAULT_VALUES['orcamento']}"
        )
    
    def clear_fields(self):
        """Limpa todos os campos"""
        # Limpar entradas
        placeholders = [
            str(DEFAULT_VALUES['calorias']),
            str(DEFAULT_VALUES['proteina']),
            str(DEFAULT_VALUES['gordura']),
            str(DEFAULT_VALUES['orcamento'])
        ]
        
        for entry_name, placeholder in zip(self.entries.keys(), placeholders):
            entry = self.entries[entry_name]
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.configure(foreground=self.colors['text_secondary'])
        
        # Limpar alimentos excluídos
        self.excluded_foods = []
        
        # Limpar resultados
        self.result_display.configure(state=tk.NORMAL)
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert("1.0", "🔍 Resultados aparecerão aqui após a otimização...\n\n💡 Dica: Use o botão 'Carregar Exemplo' para testar rapidamente!")
        self.result_display.configure(state=tk.DISABLED)
        
        messagebox.showinfo("✅ Sucesso", "🗑️ Todos os campos foram limpos!")
    
    def validate_inputs(self):
        """Valida e converte os valores de entrada usando detecção por cor"""
        try:
            values = []
            entries = [self.entries['cal_entry'], self.entries['prot_entry'], 
                      self.entries['fat_entry'], self.entries['budget_entry']]
            names = VALIDATION_NAMES
            defaults = [str(DEFAULT_VALUES['calorias']), str(DEFAULT_VALUES['proteina']), 
                       str(DEFAULT_VALUES['gordura']), str(DEFAULT_VALUES['orcamento'])]
            
            for entry, name, default in zip(entries, names, defaults):
                value_str = entry.get().strip()
                entry_color = str(entry.cget('foreground'))  # Convert Tcl_Obj to string
                
                # Verificação simplificada: 
                # 1. Campo vazio é sempre inválido
                # 2. Valor igual ao default COM cor secundária = placeholder (inválido)
                # 3. Valor igual ao default COM cor primária = válido (load_example ou input manual)
                # 4. Qualquer outro valor com cor primária = válido
                
                if not value_str:
                    messagebox.showerror("❌ Campo Vazio", 
                                       f"O campo {name} está vazio!\n\n"
                                       f"💡 Dica: Clique no campo e insira um valor válido ou use 'Carregar Exemplo'.")
                    entry.focus()
                    return None
                
                # Se o valor é igual ao default mas a cor é secundária, é placeholder
                if value_str == default and entry_color == self.colors['text_secondary']:
                    messagebox.showerror("❌ Valor Placeholder", 
                                       f"O campo {name} contém texto placeholder!\n\n"
                                       f"💡 Dica: Clique no campo e insira um valor válido ou use 'Carregar Exemplo'.")
                    entry.focus()
                    return None
                
                # Validar se é um número válido
                try:
                    value = float(value_str)
                    if value <= 0:
                        messagebox.showerror("❌ Valor Inválido", 
                                           f"O campo {name} deve conter um valor positivo!\n\n"
                                           f"💡 Valor inserido: {value_str}\n"
                                           f"💡 Dica: Insira um número maior que zero.")
                        entry.focus()
                        return None
                    values.append(value)
                    
                except ValueError:
                    messagebox.showerror("❌ Formato Inválido", 
                                       f"O campo {name} deve conter um número válido!\n\n"
                                       f"💡 Valor inserido: '{value_str}'\n"
                                       f"💡 Dica: Use apenas números (ex: 2000, 50.5)")
                    entry.focus()
                    return None
            
            # Retornar apenas valores numéricos para serem combinados com argumentos nomeados
            return tuple(values)
            
        except Exception as e:
            messagebox.showerror("❌ Erro Inesperado", f"Erro na validação: {str(e)}")
            return None
    
    def run_optimization(self):
        """Executa a otimização e exibe os resultados"""
        try:
            # Validar e obter entradas
            inputs = self.validate_inputs()
            if not inputs:
                return
            
            # Mostrar mensagem de processamento
            self.result_display.configure(state=tk.NORMAL)
            self.result_display.delete("1.0", tk.END)
            
            loading_text = """🚀 INICIANDO OTIMIZAÇÃO...

🔄 Processando parâmetros nutricionais...
🧮 Executando algoritmo de programação linear...
📊 Analisando combinações de alimentos...
⚖️ Aplicando restrições de porção...
💰 Calculando custo mínimo...

⏳ Por favor, aguarde alguns segundos..."""
            
            self.result_display.insert("1.0", loading_text)
            self.result_display.configure(state=tk.DISABLED)
            self.root.update()
            
            # Executar otimização
            resultado = optimize_diet(*inputs, excluded_foods=self.excluded_foods, use_portion_limits=self.use_portion_limits.get())
            self.show_results(resultado)
            
        except Exception as e:
            messagebox.showerror("❌ Erro na Otimização", 
                               f"Ocorreu um erro durante a otimização:\n\n{str(e)}\n\n"
                               f"💡 Verifique se todos os valores estão corretos e tente novamente.")
    
    def show_results(self, resultado):
        """Exibe os resultados da otimização"""
        self.result_display.configure(state=tk.NORMAL)
        self.result_display.delete("1.0", tk.END)
        
        if resultado['status'] == 'Optimal':
            self.display_success_results(resultado)
        else:
            self.display_error_results(resultado)
        
        self.result_display.configure(state=tk.DISABLED)
    
    def display_success_results(self, resultado):
        """Exibe os resultados de uma solução bem-sucedida"""
        text = ""
        text += "🎉 " + "═" * 80 + "\n"
        text += "                    ✅ DIETA OTIMIZADA COM SUCESSO!\n"
        text += "🎉 " + "═" * 80 + "\n\n"
        
        # Resumo nutricional destacado com caixas
        text += "┌─ 📊 RESUMO NUTRICIONAL ─────────────────────────────────────────┐\n"
        text += f"│ 🔥 Calorias totais: {resultado['detalhes']['calorias_total']:>15.1f} kcal          │\n"
        text += f"│ 💪 Proteína total:  {resultado['detalhes']['proteina_total']:>15.1f} g             │\n"
        text += f"│ 🧈 Gordura total:   {resultado['detalhes']['gordura_total']:>15.1f} g             │\n"
        text += f"│ 💰 Custo total:     R$ {resultado['custo_total']:>12.2f}                 │\n"
        text += "└─────────────────────────────────────────────────────────────────┘\n\n"
          # Lista de alimentos com preço e porção
        text += "🥘 ALIMENTOS SELECIONADOS:\n\n"
        for alimento in resultado['alimentos']:
            emoji = self.get_food_emoji(alimento['nome'])
            # Exibir preço de mercado e porção de mercado, e informar porção nutricional
            food_data = get_food_by_name(alimento['nome'])
            text += f"{emoji} {alimento['nome']} | 💰 R$ {food_data['market_price']:.2f} por {food_data['market_portion']} | 🍽️ Porção nutr.: {food_data['porcao']}\n"
            text += f"   🔢 Quantidade otim.: {alimento['quantidade']:.1f} porções | 🔥 {alimento['calorias']:.1f} kcal | 💪 {alimento['proteina']:.1f} g | 🧈 {alimento['gordura']:.1f} g | 🥖 {alimento.get('carboidrato', 0):.1f} g\n\n"
        
        self.result_display.insert("1.0", text)
    
    def display_error_results(self, resultado):
        """Exibe resultados quando não há solução viável"""
        text = ""
        text += "❌ " + "═" * 70 + "\n"
        text += "                 ⚠️ NENHUMA SOLUÇÃO ENCONTRADA\n"
        text += "❌ " + "═" * 70 + "\n\n"
        
        text += f"🔍 Status: {resultado['status']}\n"
        text += f"📝 Detalhes: Não foi possível encontrar uma combinação de alimentos que atenda a todos os critérios.\n\n"
        
        text += "💡 SUGESTÕES:\n"
        text += "• 📈 Aumente o orçamento máximo\n"
        text += "• 📉 Reduza os valores mínimos de calorias ou proteína\n"
        text += "• 📊 Aumente o limite máximo de gordura\n"
        text += "• 🔄 Tente diferentes combinações de parâmetros\n"
        
        self.result_display.insert("1.0", text)
    
    def get_food_emoji(self, food_name):
        """Retorna emoji apropriado para o alimento"""
        food_name_lower = food_name.lower()
        
        if any(word in food_name_lower for word in ['frango', 'carne', 'boi', 'porco', 'peixe', 'salmão', 'atum']):
            return '🥩'
        elif any(word in food_name_lower for word in ['ovo', 'clara']):
            return '🥚'
        elif any(word in food_name_lower for word in ['leite', 'iogurte', 'queijo']):
            return '🥛'
        elif any(word in food_name_lower for word in ['banana', 'maçã', 'laranja', 'fruta']):
            return '🍎'
        elif any(word in food_name_lower for word in ['arroz', 'feijão', 'aveia', 'pão']):
            return '🌾'
        elif any(word in food_name_lower for word in ['azeite', 'óleo', 'manteiga']):
            return '🫒'
        elif any(word in food_name_lower for word in ['alface', 'tomate', 'cenoura', 'vegetal']):
            return '🥬'
        else:
            return '🥘'
    
    def run(self):
        """Inicia o loop principal da aplicação"""
        self.root.mainloop()


def main():
    """Função principal para executar a aplicação"""
    app = DietApp()
    app.run()


if __name__ == "__main__":
    main()
