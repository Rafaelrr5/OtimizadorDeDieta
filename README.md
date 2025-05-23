# Otimizador de Dieta - Programação Linear

## Descrição
Aplicação para otimização de dieta usando programação linear com interface gráfica em Python. O sistema encontra a combinação de alimentos de menor custo que satisfaça requisitos nutricionais específicos.

## Estrutura do Projeto
```
PO/
├── main.py                          # Arquivo principal de execução
├── config/
│   ├── __init__.py
│   └── constants.py                 # Constantes de configuração
├── data/
│   ├── __init__.py
│   └── food_database.py            # Base de dados de alimentos
├── optimization/
│   ├── __init__.py
│   └── diet_optimizer.py           # Lógica de otimização
├── gui/
│   ├── __init__.py
│   └── diet_interface.py           # Interface gráfica
└── README.md                       # Este arquivo
```

## Dependências
- Python 3.7+
- pulp
- tkinter (incluído no Python)

## Instalação
1. Instale o PuLP:
```bash
pip install pulp
```

## Como Executar
1. Navegue até o diretório do projeto:
```bash
cd c:\Users\faelr\Downloads\reps\PO
```

2. Execute o arquivo principal:
```bash
python main.py
```

## Como Usar
1. Execute a aplicação
2. Preencha os parâmetros da dieta:
   - Calorias mínimas diárias
   - Proteína mínima diária (gramas)
   - Gordura máxima diária (gramas)
   - Orçamento máximo diário (R$)
   - **Usar limites de porção**: Ativa/desativa limites diários de porções por categoria
3. Selecione alimentos a excluir (opcional)
4. Clique em "Otimizar Dieta"
5. Visualize os resultados na área de resultados

## Funcionalidades
- **Otimização Linear**: Usa programação linear para encontrar a solução ótima
- **Limites de Porção**: Sistema configurável de limites mínimos e máximos de porções por categoria de alimento
- **Interface Intuitiva**: GUI amigável com validação de entrada
- **Interface Totalmente Responsiva**: 
  - Janela redimensionável com tamanho mínimo definido
  - Elementos que se adaptam automaticamente ao tamanho da janela
  - Barras de rolagem horizontais e verticais para melhor visualização
  - Seletor de alimentos com categorias e rolagem interna
- **Base de Dados**: 21 alimentos com informações nutricionais, preços e limites de porção
- **Resultados Detalhados**: Mostra quantidades, limites, custos e resumo nutricional
- **Validação**: Verifica entradas e fornece sugestões para problemas inviáveis

## Algoritmo
O sistema resolve um problema de programação linear onde:
- **Objetivo**: Minimizar custo total
- **Restrições**: 
  - Calorias ≥ mínimo especificado
  - Proteína ≥ mínimo especificado
  - Gordura ≤ máximo especificado
  - Custo ≤ orçamento especificado
  - **Porções por alimento** ≥ mínimo e ≤ máximo por categoria (quando habilitado)

## Limites de Porção por Categoria
- **Cereais e Grãos**: 2-6 porções/dia
- **Proteínas**: 1-5 porções/dia
- **Laticínios**: 1-3 porções/dia
- **Vegetais**: 3-8 porções/dia
- **Frutas**: 2-4 porções/dia
- **Óleos e Gorduras**: 0-3 porções/dia

## Arquivos Principais
- `main.py`: Ponto de entrada da aplicação
- `diet_optimizer.py`: Implementa a lógica de otimização usando PuLP
- `diet_interface.py`: Interface gráfica com Tkinter
- `food_database.py`: Base de dados de alimentos
- `constants.py`: Configurações e constantes da aplicação
