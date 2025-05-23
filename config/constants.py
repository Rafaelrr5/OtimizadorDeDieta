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

# Configurações de limite de porções
PORTION_LIMITS = {
    'daily': {
        'enabled': True,
        'default_max': 10.0,  # máximo padrão de porções por dia
        'default_min': 0.0    # mínimo padrão de porções por dia
    },
    'weekly': {
        'enabled': False,
        'default_max': 70.0,  # máximo padrão de porções por semana
        'default_min': 0.0    # mínimo padrão de porções por semana
    }
}

# Limites específicos por categoria de alimento
CATEGORY_PORTION_LIMITS = {
    'Óleos e Gorduras': {'max_daily': 3.0, 'min_daily': 0.0},
    'Proteínas': {'max_daily': 5.0, 'min_daily': 1.0},
    'Frutas': {'max_daily': 4.0, 'min_daily': 2.0},
    'Vegetais': {'max_daily': 8.0, 'min_daily': 3.0},
    'Cereais e Grãos': {'max_daily': 6.0, 'min_daily': 2.0},
    'Laticínios': {'max_daily': 3.0, 'min_daily': 1.0}
}

# Labels dos campos de entrada atualizados
FIELD_LABELS = [
    ("Calorias mínimas (kcal):", "cal_entry", "Ex: 2000"),
    ("Proteína mínima (g):", "prot_entry", "Ex: 50"),
    ("Gordura máxima (g):", "fat_entry", "Ex: 65"),
    ("Orçamento máximo (R$):", "budget_entry", "Ex: 50.00"),
    ("Usar limites de porção:", "portion_limits_var", "checkbox")
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
