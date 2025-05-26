"""
Interface gráfica moderna para o otimizador de dieta usando Tkinter nativo com visual melhorado
"""

import tkinter as tk
from tkinter import ttk, messagebox
from optimization.diet_optimizer import optimize_diet
from config.constants import *
from data.food_database import get_food_data, get_food_categories

class DietApp:
    """Classe principal da interface gráfica moderna"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🥗 Otimizador de Dieta - Inteligência Artificial")
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
        
        # Configurar grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
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
        """Cria e posiciona os elementos da interface"""
        # Frame principal com scroll
        main_canvas = tk.Canvas(self.root, bg=self.colors['bg_primary'], highlightthickness=0)
        main_canvas.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame scrollável
        self.main_frame = ttk.Frame(main_canvas, style='Modern.TFrame', padding=20)
        canvas_frame = main_canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configurar scroll
        def configure_scroll(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
            
        def configure_canvas(event):
            main_canvas.itemconfig(canvas_frame, width=event.width-20)
            
        self.main_frame.bind("<Configure>", configure_scroll)
        main_canvas.bind("<Configure>", configure_canvas)
        
        # Bind scroll com mouse
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind("<MouseWheel>", on_mousewheel)
        
        # Configurar grid do frame principal
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Título principal
        title_label = ttk.Label(
            self.main_frame, 
            text="🥗 Otimizador de Dieta com IA",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 30), sticky="ew")
        
        # Criar seções
        self.create_input_section()
        self.create_food_exclusion_section()
        self.create_action_buttons()
        self.create_results_section()
    
    def create_input_section(self):
        """Cria a seção de entrada de parâmetros"""
        # Frame para parâmetros
        params_frame = ttk.LabelFrame(
            self.main_frame, 
            text="📊 Parâmetros Nutricionais",
            style='Card.TFrame',
            padding=20
        )
        params_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        params_frame.grid_columnconfigure((0, 1), weight=1)
        
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
    
    def create_food_exclusion_section(self):
        """Cria a seção de exclusão de alimentos"""
        # Frame para exclusão
        exclusion_frame = ttk.LabelFrame(
            self.main_frame,
            text="🚫 Exclusão de Alimentos",
            style='Card.TFrame',
            padding=20
        )
        exclusion_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
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
    
    def create_action_buttons(self):
        """Cria os botões de ação"""
        # Frame para botões
        button_frame = ttk.Frame(self.main_frame, style='Modern.TFrame')
        button_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
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
    
    def create_results_section(self):
        """Cria a seção de resultados"""
        # Frame para resultados
        results_frame = ttk.LabelFrame(
            self.main_frame,
            text="📋 Resultados da Otimização",
            style='Card.TFrame',
            padding=20
        )
        results_frame.grid(row=4, column=0, sticky="nsew", pady=(0, 20))
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Área de resultados com scroll
        text_frame = ttk.Frame(results_frame, style='Modern.TFrame')
        text_frame.grid(row=0, column=0, sticky="nsew")
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
        messagebox.showinfo("Em Desenvolvimento", "Funcionalidade de seleção de alimentos será implementada em breve!")
    
    def load_example(self):
        """Carrega valores de exemplo"""
        # Limpar e inserir valores
        for entry_name, value in [
            ('cal_entry', str(DEFAULT_VALUES['calorias'])),
            ('prot_entry', str(DEFAULT_VALUES['proteina'])),
            ('fat_entry', str(DEFAULT_VALUES['gordura'])),
            ('budget_entry', str(DEFAULT_VALUES['orcamento']))
        ]:
            entry = self.entries[entry_name]
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.configure(foreground=self.colors['text_primary'])
            # Mark as not placeholder since these are real example values
            if hasattr(self, 'placeholder_status'):
                self.placeholder_status[entry_name] = False
        
        messagebox.showinfo("✅ Sucesso", "📝 Exemplo carregado com sucesso!")
    
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
            
            # Adicionar lista de alimentos excluídos e uso de limites
            values.append(self.excluded_foods if self.excluded_foods else None)
            values.append(self.use_portion_limits.get())
            
            return tuple(values)
            
        except Exception as e:
            messagebox.showerror("❌ Erro Inesperado", f"Erro na validação: {str(e)}")
            return None
    
    def run_optimization(self):
        """Executa a otimização e exibe os resultados"""
        try:
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
            resultado = optimize_diet(*inputs)
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
          # Lista básica de alimentos
        text += "🥘 ALIMENTOS SELECIONADOS:\n\n"
        for alimento in resultado['alimentos']:
            emoji = self.get_food_emoji(alimento['nome'])
            text += f"{emoji} {alimento['nome']}\n"
            text += f"   📏 {alimento['quantidade']:.1f}g | "
            text += f"🔥 {alimento['calorias']:.1f}kcal | "
            text += f"💪 {alimento['proteina']:.1f}g | "
            text += f"💰 R$ {alimento['custo']:.2f}\n\n"
        
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
