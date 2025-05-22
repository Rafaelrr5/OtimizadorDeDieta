"""
Constantes de configuração para o otimizador de dieta
"""

# Configurações da interface
WINDOW_TITLE = "Otimizador de Dieta - Programação Linear"
WINDOW_SIZE = "700x600"
WINDOW_THEME = 'clam'

# Valores padrão para exemplos
DEFAULT_VALUES = {
    'calorias': "2000",
    'proteina': "50", 
    'gordura': "65",
    'orcamento': "50.00"
}

# Labels dos campos de entrada
FIELD_LABELS = [
    ("Calorias mínimas (kcal):", "cal_entry", "Ex: 2000"),
    ("Proteína mínima (g):", "prot_entry", "Ex: 50"),
    ("Gordura máxima (g):", "fat_entry", "Ex: 65"),
    ("Orçamento máximo (R$):", "budget_entry", "Ex: 50.00")
]

# Configurações de validação
VALIDATION_NAMES = ["Calorias", "Proteína", "Gordura", "Orçamento"]

# Configurações de exibição
RESULT_DISPLAY = {
    'height': 15,
    'width': 70,
    'font': ('Consolas', 10),
    'wrap': 'word'
}

# Tolerância para valores numéricos
NUMERICAL_TOLERANCE = 1e-6
