"""
Base de dados de alimentos com informações nutricionais e preços
"""

def get_food_data():
    """Retorna lista de alimentos com informações nutricionais e preço por porção.
    
    Cada alimento possui:
    - nome: identificação do alimento
    - calorias: kcal por porção
    - proteina: gramas de proteína por porção
    - gordura: gramas de gordura por porção
    - preco: custo em R$ por porção
    
    Returns:
        list: Lista de dicionários com dados dos alimentos
    """
    return [
        # Cereais e grãos
        {"nome": "Arroz", "calorias": 130, "proteina": 2.7, "gordura": 0.3, "preco": 1.20},
        {"nome": "Feijao", "calorias": 95, "proteina": 6.0, "gordura": 0.5, "preco": 2.50},
        {"nome": "Macarrao", "calorias": 220, "proteina": 8.0, "gordura": 1.1, "preco": 1.80},
        {"nome": "Aveia", "calorias": 68, "proteina": 2.4, "gordura": 1.4, "preco": 1.50},
        {"nome": "Pao Integral", "calorias": 80, "proteina": 4.0, "gordura": 1.0, "preco": 1.00},
        
        # Proteínas
        {"nome": "Frango", "calorias": 165, "proteina": 31.0, "gordura": 3.6, "preco": 8.50},
        {"nome": "Carne Bovina", "calorias": 250, "proteina": 26.0, "gordura": 15.0, "preco": 15.00},
        {"nome": "Peixe", "calorias": 206, "proteina": 22.0, "gordura": 12.0, "preco": 12.00},
        {"nome": "Ovos", "calorias": 155, "proteina": 13.0, "gordura": 11.0, "preco": 4.50},
        {"nome": "Queijo", "calorias": 113, "proteina": 7.0, "gordura": 9.0, "preco": 5.50},
        
        # Laticínios
        {"nome": "Leite", "calorias": 60, "proteina": 3.2, "gordura": 3.2, "preco": 2.80},
        {"nome": "Iogurte", "calorias": 59, "proteina": 3.5, "gordura": 3.3, "preco": 4.20},
        
        # Vegetais
        {"nome": "Brócolis", "calorias": 25, "proteina": 3.0, "gordura": 0.3, "preco": 3.50},
        {"nome": "Cenoura", "calorias": 25, "proteina": 0.6, "gordura": 0.1, "preco": 2.00},
        {"nome": "Tomate", "calorias": 18, "proteina": 0.9, "gordura": 0.2, "preco": 2.50},
        {"nome": "Alface", "calorias": 5, "proteina": 0.5, "gordura": 0.1, "preco": 1.80},
        
        # Frutas
        {"nome": "Banana", "calorias": 89, "proteina": 1.1, "gordura": 0.3, "preco": 2.20},
        {"nome": "Maçã", "calorias": 52, "proteina": 0.3, "gordura": 0.2, "preco": 3.00},
        {"nome": "Laranja", "calorias": 47, "proteina": 0.9, "gordura": 0.1, "preco": 2.80},
        
        # Óleos e gorduras
        {"nome": "Azeite", "calorias": 884, "proteina": 0.0, "gordura": 100.0, "preco": 0.80},
        {"nome": "Manteiga", "calorias": 717, "proteina": 0.9, "gordura": 81.0, "preco": 1.20},
    ]

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
