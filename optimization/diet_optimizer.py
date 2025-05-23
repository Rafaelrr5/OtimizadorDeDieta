"""
Módulo de otimização de dieta usando programação linear
"""

import pulp
from data.food_database import get_food_data

class DietOptimizer:
    """Classe responsável pela otimização da dieta"""
    
    def __init__(self):
        self.alimentos = get_food_data()
        self.problem = None
        self.food_vars = {}
    
    def optimize_diet(self, metac, metap, metag, orcamento, excluded_foods=None):
        """Resolve o problema de otimização de dieta com restrições nutricionais e orçamentárias.
        
        Args:
            metac (float): Mínimo de calorias diárias
            metap (float): Mínimo de proteína diária (em gramas)
            metag (float): Máximo de gordura diária (em gramas)
            orcamento (float): Orçamento máximo diário (em R$)
            excluded_foods (list): Lista de nomes de alimentos a serem excluídos da otimização
        
        Returns:
            dict: Resultado da otimização com status, quantidades e custo total
        """
        # Filtrar alimentos excluídos
        if excluded_foods:
            self.alimentos = [food for food in self.alimentos if food['nome'] not in excluded_foods]
        
        # Criar o problema de minimização
        self.problem = pulp.LpProblem("Otimizacao_Dieta", pulp.LpMinimize)
        
        # Criar variáveis de decisão
        self._create_decision_variables()
        
        # Definir função objetivo
        self._set_objective_function()
        
        # Adicionar restrições
        self._add_nutritional_constraints(metac, metap, metag)
        self._add_budget_constraint(orcamento)
        
        # Resolver o problema
        self.problem.solve(pulp.PULP_CBC_CMD(msg=0))
        
        # Retornar resultado
        return self._prepare_result()
    
    def _create_decision_variables(self):
        """Cria as variáveis de decisão (quantidade de cada alimento)"""
        self.food_vars = {}
        for i, food in enumerate(self.alimentos):
            self.food_vars[food['nome']] = pulp.LpVariable(
                f"x_{i}_{food['nome']}", 
                lowBound=0, 
                cat='Continuous'
            )
    
    def _set_objective_function(self):
        """Define a função objetivo: minimizar custo total"""
        self.problem += pulp.lpSum([
            self.food_vars[food['nome']] * food['preco'] 
            for food in self.alimentos
        ])
    
    def _add_nutritional_constraints(self, metac, metap, metag):
        """Adiciona restrições nutricionais"""
        # Calorias mínimas
        self.problem += pulp.lpSum([
            self.food_vars[food['nome']] * food['calorias'] 
            for food in self.alimentos
        ]) >= metac
        
        # Proteína mínima
        self.problem += pulp.lpSum([
            self.food_vars[food['nome']] * food['proteina'] 
            for food in self.alimentos
        ]) >= metap
        
        # Gordura máxima
        self.problem += pulp.lpSum([
            self.food_vars[food['nome']] * food['gordura'] 
            for food in self.alimentos
        ]) <= metag
    
    def _add_budget_constraint(self, orcamento):
        """Adiciona restrição de orçamento"""
        self.problem += pulp.lpSum([
            self.food_vars[food['nome']] * food['preco'] 
            for food in self.alimentos
        ]) <= orcamento
    
    def _prepare_result(self):
        """Prepara o resultado da otimização"""
        resultado = {
            'status': pulp.LpStatus[self.problem.status],
            'quantidades': {},
            'custo_total': 0,
            'detalhes': {
                'calorias_total': 0,
                'proteina_total': 0,
                'gordura_total': 0
            }
        }
        
        if self.problem.status == pulp.LpStatusOptimal:
            self._extract_optimal_quantities(resultado)
        
        return resultado
    
    def _extract_optimal_quantities(self, resultado):
        """Extrai as quantidades ótimas da solução"""
        for food in self.alimentos:
            qtd = self.food_vars[food['nome']].varValue or 0
            resultado['quantidades'][food['nome']] = qtd
            
            # Calcular totais
            resultado['custo_total'] += qtd * food['preco']
            resultado['detalhes']['calorias_total'] += qtd * food['calorias']
            resultado['detalhes']['proteina_total'] += qtd * food['proteina']
            resultado['detalhes']['gordura_total'] += qtd * food['gordura']

def optimize_diet(metac, metap, metag, orcamento, excluded_foods=None):
    """Função de conveniência para otimização de dieta
    
    Args:
        metac (float): Mínimo de calorias diárias
        metap (float): Mínimo de proteína diária (em gramas)
        metag (float): Máximo de gordura diária (em gramas)
        orcamento (float): Orçamento máximo diário (em R$)
        excluded_foods (list): Lista de alimentos a serem excluídos da otimização
    
    Returns:
        dict: Resultado da otimização
    """
    optimizer = DietOptimizer()
    return optimizer.optimize_diet(metac, metap, metag, orcamento, excluded_foods)
