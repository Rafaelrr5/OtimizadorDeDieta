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
    - preco: custo em R$ por porção
    - max_portions_daily: máximo de porções por dia
    - min_portions_daily: mínimo de porções por dia
    
    Returns:
        list: Lista de dicionários com dados dos alimentos
    """
    base_foods = [
        # Cereais e grãos
        {"nome": "Arroz", "calorias": 2600, "proteina": 48.0, "gordura": 4.0, "preco": 7.00, "categoria": "Cereais e Grãos", "porcao": "1kg", "carboidratos": 280.0},
        {"nome": "Feijao", "calorias": 2533.33, "proteina": 156.67, "gordura": 16.67, "preco": 8.00, "categoria": "Cereais e Grãos", "porcao": "1kg", "carboidratos": 230.0},
        {"nome": "Macarrao", "calorias": 987.5, "proteina": 36.25, "gordura": 5.625, "preco": 4.00, "categoria": "Cereais e Grãos", "porcao": "500g", "carboidratos": 375.0},
        {"nome": "Aveia", "calorias": 370.0, "proteina": 12.5, "gordura": 6.25, "preco": 1.50, "categoria": "Cereais e Grãos", "porcao": "100g", "carboidratos": 60.0},
        {"nome": "Pao Integral", "calorias": 130, "proteina": 5.0, "gordura": 2.5, "preco": 0.70, "categoria": "Cereais e Grãos", "porcao": "50g", "carboidratos": 24.0},
        
        # Proteínas
        {"nome": "Frango", "calorias": 1650, "proteina": 310.0, "gordura": 36.0, "preco": 15.00, "categoria": "Proteínas", "porcao": "1kg", "carboidratos": 0.0},
        {"nome": "Carne Bovina", "calorias": 217, "proteina": 26.0, "gordura": 12.0, "preco": 4.00, "categoria": "Proteínas", "porcao": "100g", "carboidratos": 0.0},
        {"nome": "Peixe", "calorias": 129, "proteina": 26.0, "gordura": 2.7, "preco": 3.00, "categoria": "Proteínas", "porcao": "100g", "carboidratos": 0.0},
        {"nome": "Ovos", "calorias": 1360, "proteina": 120.0, "gordura": 100.0, "preco": 17.00, "categoria": "Proteínas", "porcao": "20 unidades", "carboidratos": 7.0},
        {"nome": "Queijo", "calorias": 3333.33, "proteina": 233.33, "gordura": 266.67, "preco": 30.00, "categoria": "Proteínas", "porcao": "1kg", "carboidratos": 20.0},
        
        # Laticínios
        {"nome": "Leite", "calorias": 650, "proteina": 33.0, "gordura": 37.0, "preco": 5.00, "categoria": "Laticínios", "porcao": "1L", "carboidratos": 50.0},
        {"nome": "Iogurte", "calorias": 500, "proteina": 25.0, "gordura": 17.5, "preco": 12.79, "categoria": "Laticínios", "porcao": "1kg", "carboidratos": 47.0},
        
        # Vegetais
        {"nome": "Brócolis", "calorias": 35, "proteina": 2.4, "gordura": 0.4, "preco": 1.50, "categoria": "Vegetais", "porcao": "80g", "carboidratos": 5.6},
        {"nome": "Cenoura", "calorias": 41, "proteina": 0.9, "gordura": 0.2, "preco": 0.80, "categoria": "Vegetais", "porcao": "50g", "carboidratos": 5.0},
        {"nome": "Tomate", "calorias": 18, "proteina": 0.9, "gordura": 0.2, "preco": 1.20, "categoria": "Vegetais", "porcao": "100g", "carboidratos": 4.0},
        {"nome": "Alface", "calorias": 15, "proteina": 1.4, "gordura": 0.2, "preco": 0.50, "categoria": "Vegetais", "porcao": "50g", "carboidratos": 1.0},
        
        # Frutas
        {"nome": "Banana", "calorias": 89, "proteina": 1.1, "gordura": 0.3, "preco": 3.00, "categoria": "Frutas", "porcao": "1 unidade (120g)", "carboidratos": 27.6},
        {"nome": "Maçã", "calorias": 52, "proteina": 0.3, "gordura": 0.2, "preco": 14.00, "categoria": "Frutas", "porcao": "1 unidade (150g)", "carboidratos": 20.7},
        {"nome": "Laranja", "calorias": 47, "proteina": 0.9, "gordura": 0.1, "preco": 0.80, "categoria": "Frutas", "porcao": "1 unidade (150g)", "carboidratos": 17.7},
        
        # Óleos e gorduras
        {"nome": "Azeite", "calorias": 8800, "proteina": 0.0, "gordura": 1000.0, "preco": 50.00, "categoria": "Óleos e Gorduras", "porcao": "1L", "carboidratos": 0.0},
        {"nome": "Manteiga", "calorias": 102, "proteina": 0.1, "gordura": 11.5, "preco": 0.42, "categoria": "Óleos e Gorduras", "porcao": "10g", "carboidratos": 0.1},
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
    
    return base_foods

def get_food_categories():
    """Retorna as categorias de alimentos disponíveis
    
    Returns:
        dict: Dicionário com categorias e seus alimentos
    """
    alimentos = get_food_data()
    
    categorias = {
        'Cereais e Grãos': ['Arroz', 'Feijao', 'Macarrao', 'Aveia', 'Pao Integral'],
        'Proteínas': ['Frango', 'Carne Bovina', 'Peixe', 'Ovos', 'Queijo'],
        'Laticínios': ['Leite', 'Iogurte'],
        'Vegetais': ['Brócolis', 'Cenoura', 'Tomate', 'Alface'],
        'Frutas': ['Banana', 'Maçã', 'Laranja'],
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
