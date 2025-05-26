"""
Base de dados de alimentos com informações nutricionais e preços
"""

from config.constants import CATEGORY_PORTION_LIMITS

def get_food_data():
    """Retorna lista de alimentos com informações nutricionais e preço por porção.
    
    Cada alimento possui:
    - nome: identificação do alimento
    - calorias: kcal por porção
    - proteina: gramas de proteína por porção
    - gordura: gramas de gordura por porção
    - carboidrato: gramas de carboidrato por porção
    - preco: custo em R$ por porção
    - max_portions_daily: máximo de porções por dia
    - min_portions_daily: mínimo de porções por dia
    
    Returns:
        list: Lista de dicionários com dados dos alimentos
    """
    base_foods = [
        # Cereais e grãos
        {"nome": "Arroz branco cozido", "calorias": 100, "proteina": 2.0, "gordura": 0.3, "carboidrato": 22.0, "preco": 0.70, "categoria": "Cereais e Grãos", "porcao": "4 colheres (80g)"},
        {"nome": "Feijão cozido", "calorias": 90, "proteina": 6.0, "gordura": 0.5, "carboidrato": 15.0, "preco": 1.00, "categoria": "Cereais e Grãos", "porcao": "1 concha (80g)"},
        {"nome": "Macarrão cozido", "calorias": 300, "proteina": 10.0, "gordura": 1.0, "carboidrato": 62.0, "preco": 1.50, "categoria": "Cereais e Grãos", "porcao": "80g (cru)"},
        {"nome": "Aveia", "calorias": 140, "proteina": 5.0, "gordura": 3.0, "carboidrato": 25.0, "preco": 1.20, "categoria": "Cereais e Grãos", "porcao": "40g (4 colheres)"},
        {"nome": "Pão francês", "calorias": 135, "proteina": 4.0, "gordura": 1.0, "carboidrato": 27.0, "preco": 0.50, "categoria": "Cereais e Grãos", "porcao": "1 unidade (50g)"},
        {"nome": "Farinha Láctea", "calorias": 110, "proteina": 3.0, "gordura": 0.5, "carboidrato": 23.0, "preco": 1.80, "categoria": "Cereais e Grãos", "porcao": "2 colheres (30g)"},
        {"nome": "Batata inglesa", "calorias": 78, "proteina": 2.0, "gordura": 0.0, "carboidrato": 18.0, "preco": 0.60, "categoria": "Cereais e Grãos", "porcao": "150g (1 unidade)"},
        {"nome": "Batata-doce", "calorias": 77, "proteina": 0.6, "gordura": 0.1, "carboidrato": 18.4, "preco": 0.80, "categoria": "Cereais e Grãos", "porcao": "100g"},
        
        # Proteínas
        {"nome": "Frango grelhado", "calorias": 159, "proteina": 32.0, "gordura": 2.5, "carboidrato": 0.0, "preco": 3.50, "categoria": "Proteínas", "porcao": "100g"},
        {"nome": "Carne moída magra", "calorias": 170, "proteina": 26.0, "gordura": 8.0, "carboidrato": 0.0, "preco": 4.00, "categoria": "Proteínas", "porcao": "100g"},
        {"nome": "Atum em água", "calorias": 130, "proteina": 30.0, "gordura": 1.0, "carboidrato": 0.0, "preco": 6.50, "categoria": "Proteínas", "porcao": "1 lata (170g)"},
        {"nome": "Ovo cozido", "calorias": 73, "proteina": 6.6, "gordura": 4.7, "carboidrato": 0.3, "preco": 0.80, "categoria": "Proteínas", "porcao": "1 unidade (50g)"},
        {"nome": "Queijo mussarela", "calorias": 99, "proteina": 6.8, "gordura": 7.6, "carboidrato": 0.9, "preco": 2.50, "categoria": "Proteínas", "porcao": "1 fatia (30g)"},
        {"nome": "Pasta de Amendoim", "calorias": 88, "proteina": 4.0, "gordura": 7.5, "carboidrato": 3.0, "preco": 1.30, "categoria": "Proteínas", "porcao": "1 colher (15g)"},
        
        # Laticínios
        {"nome": "Leite integral", "calorias": 128, "proteina": 8.0, "gordura": 5.0, "carboidrato": 12.0, "preco": 1.50, "categoria": "Laticínios", "porcao": "1 copo (250ml)"},
        {"nome": "Iogurte natural", "calorias": 62, "proteina": 5.7, "gordura": 0.45, "carboidrato": 8.7, "preco": 2.00, "categoria": "Laticínios", "porcao": "1 pote (150g)"},
        
        # Vegetais
        {"nome": "Brócolis", "calorias": 35, "proteina": 2.4, "gordura": 0.4, "carboidrato": 7.0, "preco": 1.50, "categoria": "Vegetais", "porcao": "80g"},
        {"nome": "Cenoura", "calorias": 41, "proteina": 0.9, "gordura": 0.2, "carboidrato": 9.5, "preco": 0.80, "categoria": "Vegetais", "porcao": "50g"},
        {"nome": "Tomate", "calorias": 18, "proteina": 0.9, "gordura": 0.2, "carboidrato": 3.9, "preco": 1.20, "categoria": "Vegetais", "porcao": "100g"},
        {"nome": "Alface", "calorias": 15, "proteina": 1.4, "gordura": 0.2, "carboidrato": 2.9, "preco": 0.50, "categoria": "Vegetais", "porcao": "50g"},
        
        # Frutas
        {"nome": "Banana nanica", "calorias": 98, "proteina": 1.3, "gordura": 0.1, "carboidrato": 26.0, "preco": 0.50, "categoria": "Frutas", "porcao": "1 unidade (100g)"},
        {"nome": "Maçã", "calorias": 84, "proteina": 0.5, "gordura": 0.0, "carboidrato": 22.0, "preco": 1.20, "categoria": "Frutas", "porcao": "1 unidade (150g)"},
        {"nome": "Laranja", "calorias": 47, "proteina": 0.9, "gordura": 0.1, "carboidrato": 11.8, "preco": 0.80, "categoria": "Frutas", "porcao": "1 unidade (150g)"},
        
        # Óleos e gorduras
        {"nome": "Azeite", "calorias": 72, "proteina": 0.0, "gordura": 8.0, "carboidrato": 0.0, "preco": 1.00, "categoria": "Óleos e Gorduras", "porcao": "1 colher (10g)"},
        {"nome": "Manteiga", "calorias": 102, "proteina": 0.1, "gordura": 11.5, "carboidrato": 0.0, "preco": 0.42, "categoria": "Óleos e Gorduras", "porcao": "10g"},
    ]
    
    # Adicionar limites de porção baseados na categoria
    for food in base_foods:
        categoria = food['categoria']
        if categoria in CATEGORY_PORTION_LIMITS:
            food['max_portions_daily'] = CATEGORY_PORTION_LIMITS[categoria]['max_daily']
            food['min_portions_daily'] = CATEGORY_PORTION_LIMITS[categoria]['min_daily']
        else:
            food['max_portions_daily'] = 10.0  # padrão
            food['min_portions_daily'] = 0.0   # padrão
    
    # Adicionar observações para tabela nutricional
    food_observations = [
        "Valores podem variar conforme método de preparo e marca do produto.",
        "Dados baseados em tabelas nutricionais médias (TBCA, TACO).",
        "Porções referem-se a medidas caseiras comuns."
    ]
    
    return base_foods

def get_food_categories():
    """Retorna as categorias de alimentos disponíveis
    
    Returns:
        dict: Dicionário com categorias e seus alimentos
    """
    alimentos = get_food_data()
    
    categorias = {
        'Cereais e Grãos': ['Arroz branco cozido', 'Feijão cozido', 'Macarrão cozido', 'Aveia', 'Pão francês', 'Farinha Láctea', 'Batata inglesa', 'Batata-doce'],
        'Proteínas': ['Frango grelhado', 'Carne moída magra', 'Atum em água', 'Ovo cozido', 'Queijo mussarela', 'Pasta de Amendoim'],
        'Laticínios': ['Leite integral', 'Iogurte natural'],
        'Vegetais': ['Brócolis', 'Cenoura', 'Tomate', 'Alface'],
        'Frutas': ['Banana nanica', 'Maçã', 'Laranja'],
        'Óleos e Gorduras': ['Azeite', 'Manteiga']
    }
    
    return categorias

def get_food_by_name(nome):
    """Busca um alimento específico pelo nome
    
    Args:
        nome (str): Nome do alimento
        
    Returns:
        dict or None: Dados do alimento se encontrado, None caso contrário
    """
    alimentos = get_food_data()
    
    for alimento in alimentos:
        if alimento['nome'].lower() == nome.lower():
            return alimento
    
    return None

def get_food_observations():
    """Retorna observações sobre os dados nutricionais
    
    Returns:
        list: Lista de strings com observações sobre os dados
    """
    return [
        "Valores podem variar conforme método de preparo e marca do produto.",
        "Dados baseados em tabelas nutricionais médias (TBCA, TACO).",
        "Porções referem-se a medidas caseiras comuns."
    ]
