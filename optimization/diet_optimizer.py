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
    
    def optimize_diet(self, metac, metap, metag, orcamento, excluded_foods=None, use_portion_limits=False, metacarb=None):
        """Resolve o problema de otimização de dieta com restrições nutricionais e orçamentárias.
        
        Args:
            metac (float): Mínimo de calorias diárias
            metap (float): Mínimo de proteína diária (em gramas)
            metag (float): Máximo de gordura diária (em gramas)
            orcamento (float): Orçamento máximo diário (em R$)
            excluded_foods (list): Lista de nomes de alimentos a serem excluídos da otimização
            use_portion_limits (bool): Se deve aplicar limites de porção por dia
            metacarb (float, optional): Máximo de carboidratos diários (em gramas)
        
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
        self._add_nutritional_constraints(metac, metap, metag, metacarb)
        self._add_budget_constraint(orcamento)
        
        # Adicionar limites de porção se habilitado
        if use_portion_limits:
            self._add_portion_constraints()
        
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
    
    def _add_nutritional_constraints(self, metac, metap, metag, metacarb=None):
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
        
        # Carboidrato máximo (opcional)
        if metacarb is not None:
            self.problem += pulp.lpSum([
                self.food_vars[food['nome']] * food.get('carboidrato', 0) 
                for food in self.alimentos
            ]) <= metacarb
    
    def _add_budget_constraint(self, orcamento):
        """Adiciona restrição de orçamento"""
        self.problem += pulp.lpSum([
            self.food_vars[food['nome']] * food['preco'] 
            for food in self.alimentos
        ]) <= orcamento
    
    def _add_portion_constraints(self):
        """Adiciona restrições de limite de porções diárias"""
        for food in self.alimentos:
            nome = food['nome']
            
            # Limite mínimo de porções
            if food.get('min_portions_daily', 0) > 0:
                self.problem += self.food_vars[nome] >= food['min_portions_daily']
            
            # Limite máximo de porções
            if food.get('max_portions_daily'):
                self.problem += self.food_vars[nome] <= food['max_portions_daily']
    
    def _prepare_result(self):
        """Prepara o resultado da otimização"""
        resultado = {
            'status': pulp.LpStatus[self.problem.status],
            'quantidades': {},
            'custo_total': 0,
            'detalhes': {
                'calorias_total': 0,
                'proteina_total': 0,
                'gordura_total': 0,
                'carboidrato_total': 0
            }
        }
        
        if self.problem.status == pulp.LpStatusOptimal:
            self._extract_optimal_quantities(resultado)
        
        return resultado
    
    def _extract_optimal_quantities(self, resultado):
        """Extrai as quantidades ótimas da solução"""
        # Lista formatada para interface gráfica
        resultado['alimentos'] = []
        
        for food in self.alimentos:
            qtd = self.food_vars[food['nome']].varValue or 0
            resultado['quantidades'][food['nome']] = qtd
            
            # Calcular totais
            resultado['custo_total'] += qtd * food['preco']
            resultado['detalhes']['calorias_total'] += qtd * food['calorias']
            resultado['detalhes']['proteina_total'] += qtd * food['proteina']
            resultado['detalhes']['gordura_total'] += qtd * food['gordura']
            resultado['detalhes']['carboidrato_total'] += qtd * food.get('carboidrato', 0)
            
            # Adicionar formato esperado pela interface
            if qtd > 0.01:  # Apenas alimentos com quantidade significativa
                resultado['alimentos'].append({
                    'nome': food['nome'],
                    'quantidade': qtd,
                    'calorias': qtd * food['calorias'],
                    'proteina': qtd * food['proteina'],
                    'gordura': qtd * food['gordura'],
                    'carboidrato': qtd * food.get('carboidrato', 0),
                    'custo': qtd * food['preco']
                })

def optimize_diet(metac, metap, metag, orcamento, excluded_foods=None, use_portion_limits=False):
    """Função de conveniência para otimização de dieta
    
    Args:
        metac (float): Mínimo de calorias diárias
        metap (float): Mínimo de proteína diária (em gramas)
        metag (float): Máximo de gordura diária (em gramas)
        orcamento (float): Orçamento máximo diário (em R$)
        excluded_foods (list): Lista de alimentos a serem excluídos da otimização
        use_portion_limits (bool): Se deve aplicar limites de porção por dia
    
    Returns:
        dict: Resultado da otimização
    """
    optimizer = DietOptimizer()
    return optimizer.optimize_diet(metac, metap, metag, orcamento, excluded_foods, use_portion_limits)


def exemplo_otimizacao_dieta():
    """Exemplo de uso da otimização de dieta com valores realistas.
    
    Esta função demonstra como usar o otimizador de dieta com valores
    nutricionais personalizados: 384g carboidratos, 120g proteínas, 140g gorduras e meta de 3100 kcal.
    
    Valores utilizados:
    - Carboidratos: 384g (meta diária)
    - Calorias: 3100 kcal (meta diária)
    - Proteínas: 120g (meta diária)
    - Gorduras: 140g (limite diário)
    - Orçamento: R$ 50,00 (valor diário realista)
    
    Returns:
        dict: Resultado da otimização com alimentos, quantidades e valores nutricionais
    """
    # Valores nutricionais personalizados
    calorias_min = 3100    # kcal mínimas diárias
    proteina_min = 120     # gramas mínimas diárias
    gordura_max = 140      # gramas máximas diárias
    orcamento_max = 50.0   # orçamento diário em R$
    carboidratos_target = 384  # gramas de carboidratos meta diária
    
    # Alimentos que desejamos excluir (opcional)
    # Verificar que estes alimentos existem na base de dados
    alimentos_excluidos = ["Bacon", "Refrigerante"]
    
    # Executar otimização
    resultado = optimize_diet(
        metac=calorias_min,
        metap=proteina_min, 
        metag=gordura_max,
        orcamento=orcamento_max,
        excluded_foods=alimentos_excluidos,
        use_portion_limits=True  # Aplicar limites de porção recomendados
    )
    
    # Exibir resultados
    print(f"Status da otimização: {resultado['status']}")
    
    if resultado['status'] == 'Optimal':
        print("\nAlimentos recomendados (porções):")
        for alimento in resultado['alimentos']:
            print(f"- {alimento['nome']}: {alimento['quantidade']:.2f}")
        
        print(f"\nCusto total: R$ {resultado['custo_total']:.2f}")
        print("\nNutrientes totais:")
        print(f"- Calorias: {resultado['detalhes']['calorias_total']:.2f} kcal")
        print(f"- Carboidratos (meta): {carboidratos_target}g")
        print(f"- Proteínas: {resultado['detalhes']['proteina_total']:.2f}g")
        print(f"- Gorduras: {resultado['detalhes']['gordura_total']:.2f}g")
    else:
        print("Não foi possível encontrar uma solução ótima com os parâmetros informados.")
    
    return resultado


# Para executar o exemplo diretamente quando o script é rodado
if __name__ == "__main__":
    exemplo_otimizacao_dieta()
