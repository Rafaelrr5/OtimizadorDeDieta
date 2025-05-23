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
        {"nome": "Arroz", "calorias": 130, "proteina": 2.7, "gordura": 0.3, "preco": 1.20, "categoria": "Cereais e Grãos"},
        {"nome": "Feijao", "calorias": 95, "proteina": 6.0, "gordura": 0.5, "preco": 2.50, "categoria": "Cereais e Grãos"},
        {"nome": "Macarrao", "calorias": 220, "proteina": 8.0, "gordura": 1.1, "preco": 1.80, "categoria": "Cereais e Grãos"},
        {"nome": "Aveia", "calorias": 68, "proteina": 2.4, "gordura": 1.4, "preco": 1.50, "categoria": "Cereais e Grãos"},
        {"nome": "Pao Integral", "calorias": 80, "proteina": 4.0, "gordura": 1.0, "preco": 1.00, "categoria": "Cereais e Grãos"},
        
        # Proteínas
        {"nome": "Frango", "calorias": 165, "proteina": 31.0, "gordura": 3.6, "preco": 8.50, "categoria": "Proteínas"},
        {"nome": "Carne Bovina", "calorias": 250, "proteina": 26.0, "gordura": 15.0, "preco": 15.00, "categoria": "Proteínas"},
        {"nome": "Peixe", "calorias": 206, "proteina": 22.0, "gordura": 12.0, "preco": 12.00, "categoria": "Proteínas"},
        {"nome": "Ovos", "calorias": 155, "proteina": 13.0, "gordura": 11.0, "preco": 4.50, "categoria": "Proteínas"},
        {"nome": "Queijo", "calorias": 113, "proteina": 7.0, "gordura": 9.0, "preco": 5.50, "categoria": "Proteínas"},
        
        # Laticínios
        {"nome": "Leite", "calorias": 60, "proteina": 3.2, "gordura": 3.2, "preco": 2.80, "categoria": "Laticínios"},
        {"nome": "Iogurte", "calorias": 59, "proteina": 3.5, "gordura": 3.3, "preco": 4.20, "categoria": "Laticínios"},
        
        # Vegetais
        {"nome": "Brócolis", "calorias": 25, "proteina": 3.0, "gordura": 0.3, "preco": 3.50, "categoria": "Vegetais"},
        {"nome": "Cenoura", "calorias": 25, "proteina": 0.6, "gordura": 0.1, "preco": 2.00, "categoria": "Vegetais"},
        {"nome": "Tomate", "calorias": 18, "proteina": 0.9, "gordura": 0.2, "preco": 2.50, "categoria": "Vegetais"},
        {"nome": "Alface", "calorias": 5, "proteina": 0.5, "gordura": 0.1, "preco": 1.80, "categoria": "Vegetais"},
        
        # Frutas
        {"nome": "Banana", "calorias": 89, "proteina": 1.1, "gordura": 0.3, "preco": 2.20, "categoria": "Frutas"},
        {"nome": "Maçã", "calorias": 52, "proteina": 0.3, "gordura": 0.2, "preco": 3.00, "categoria": "Frutas"},
        {"nome": "Laranja", "calorias": 47, "proteina": 0.9, "gordura": 0.1, "preco": 2.80, "categoria": "Frutas"},
        
        # Óleos e gorduras
        {"nome": "Azeite", "calorias": 884, "proteina": 0.0, "gordura": 100.0, "preco": 0.80, "categoria": "Óleos e Gorduras"},
        {"nome": "Manteiga", "calorias": 717, "proteina": 0.9, "gordura": 81.0, "preco": 1.20, "categoria": "Óleos e Gorduras"},
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
