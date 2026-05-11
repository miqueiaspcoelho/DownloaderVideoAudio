# Constituição Técnica do Projeto — Python 3.14

## 1. Fundamentos do Projeto

Esta constituição define os princípios, padrões e regras inegociáveis para todo o ciclo de vida do projeto.
Seu objetivo é garantir:

* Alta qualidade de código
* Escalabilidade
* Modularidade
* Legibilidade
* Facilidade de manutenção
* Evolução sustentável do sistema
* Padronização entre desenvolvedores e agentes de IA

---

# 2. Princípios Inegociáveis

## 2.1 Modularidade Obrigatória

O projeto DEVE ser dividido em módulos independentes e desacoplados.

### Regras:

* Cada módulo deve possuir responsabilidade única.
* Nenhum arquivo deve concentrar múltiplas responsabilidades.
* Evitar arquivos “god objects” ou “utils.py” genéricos.
* Toda funcionalidade deve ser reutilizável.
* Dependências entre módulos devem ser explícitas e mínimas.

---

## 2.2 Arquitetura Orientada a Objetos

O projeto DEVE utilizar:

* Classes
* Objetos
* Encapsulamento
* Composição
* Abstrações claras

### Regras:

* Classes devem representar entidades ou comportamentos reais.
* Herança só deve ser utilizada quando houver relação legítima.
* Preferir composição ao invés de herança.
* Objetos devem possuir estado e comportamento coerentes.
* Métodos privados devem utilizar prefixo `_`.

---

## 2.3 Funções Pequenas e Coesas

Toda função DEVE:

* Fazer apenas uma coisa
* Possuir nome autoexplicativo
* Ter baixa complexidade cognitiva

### Regras:

* Funções longas devem ser refatoradas.
* Evitar múltiplos níveis de aninhamento.
* Evitar efeitos colaterais ocultos.
* Preferir retorno explícito.
* Toda função deve ser previsível e testável.

---

## 2.4 Código Autoexplicativo

O código deve ser entendido sem necessidade excessiva de comentários.

### Regras:

* Nomes devem expressar intenção.
* Comentários devem explicar “por quê”, nunca “o quê”.
* Evitar abreviações ambíguas.
* Evitar números mágicos.
* Utilizar constantes nomeadas.

---

# 3. Convenções de Nomenclatura

## 3.1 Variáveis

Todas as variáveis DEVEM seguir:

```python
snake_case
```

### Exemplos:

```python
user_name
total_price
database_connection
```

---

## 3.2 Funções

Todas as funções DEVEM:

* Utilizar camelCase
* Começar obrigatoriamente com letra minúscula

### Exemplos:

```python
calculateTotal()
fetchUserData()
validatePassword()
```

---

## 3.3 Classes e Objetos

Classes DEVEM utilizar:

```python
PascalCase
```

### Exemplos:

```python
UserService
PaymentProcessor
DatabaseManager
```

Objetos/instâncias devem seguir:

```python
camelCase
```

### Exemplos:

```python
userService
paymentProcessor
```

---

## 3.4 Constantes

Constantes DEVEM utilizar:

```python
UPPER_SNAKE_CASE
```

### Exemplos:

```python
MAX_RETRIES
DEFAULT_TIMEOUT
API_VERSION
```

---

# 4. Estrutura do Projeto

A estrutura mínima obrigatória:

```text
project_root/
│
├── src/
│   ├── modules/
│   ├── services/
│   ├── domain/
│   ├── infrastructure/
│   ├── interfaces/
│   └── shared/
│
├── tests/
├── docs/
├── scripts/
├── .venv/
├── requirements/
├── pyproject.toml
├── README.md
└── .gitignore
```

---

# 5. Ambiente Virtual Obrigatório

## Regra Absoluta

Toda instalação de dependências DEVE ocorrer dentro de um ambiente virtual (`venv`).

### Proibido:

* Instalações globais
* Dependências fora do ambiente virtual

### Obrigatório:

```bash
python -m venv .venv
```

Ativação:

### Linux/Mac

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Instalação:

```bash
pip install -r requirements/dev.txt
```

---

# 6. Controle de Dependências

## Regras:

* Toda dependência deve possuir justificativa.
* Dependências não utilizadas devem ser removidas.
* Versões devem ser fixadas.
* Utilizar `pyproject.toml` como fonte principal.
* Dependências separadas entre:

  * produção
  * desenvolvimento
  * testes

---

# 7. Git Workflow Obrigatório

## 7.1 Toda nova funcionalidade deve ser criada em nova branch

### Obrigatório:

```text
feature/nome-da-feature
```

### Correções:

```text
fix/nome-do-fix
```

### Hotfix:

```text
hotfix/nome-do-hotfix
```

---

## 7.2 Proibições

### É proibido:

* Commit direto na `main`
* Push sem revisão
* Merge sem testes
* Código quebrado na branch principal

---

## 7.3 Commits

Commits DEVEM ser semânticos.

### Exemplos:

```text
feat: adiciona autenticação JWT
fix: corrige vazamento de memória
refactor: simplifica camada de serviço
test: adiciona testes de integração
docs: atualiza documentação da API
```

---

# 8. Testes Obrigatórios

Todo código novo DEVE possuir testes.

## Tipos obrigatórios:

* Unitários
* Integração
* Contrato (quando aplicável)

---

## Cobertura mínima

```text
>= 85%
```

---

## Ferramentas recomendadas

* pytest
* pytest-cov
* factory-boy
* faker

---

# 9. Qualidade de Código

## Ferramentas obrigatórias

### Lint

* ruff

### Formatação

* black

### Type checking

* mypy

### Segurança

* bandit

---

## Regras

O pipeline deve falhar caso:

* lint falhe
* testes falhem
* type checking falhe
* cobertura mínima não seja atingida

---

# 10. Tipagem Estática Obrigatória

Todo código novo DEVE utilizar type hints.

### Exemplo:

```python
def calculateTotal(price: float, quantity: int) -> float:
    return price * quantity
```

---

# 11. Tratamento de Erros

## Regras:

* Nunca utilizar `except:` genérico.
* Exceções devem ser específicas.
* Logs devem ser claros.
* Erros não devem ser silenciosos.

### Obrigatório:

```python
try:
    processPayment()
except PaymentError as error:
    logger.error(str(error))
```

---

# 12. Logging Obrigatório

## Regras:

* Nunca utilizar `print()` para debug.
* Utilizar módulo `logging`.
* Logs devem possuir contexto suficiente.

### Níveis:

* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL

---

# 13. Documentação

## Obrigatório:

* README atualizado
* Docstrings em módulos públicos
* Exemplos de uso
* Guia de setup
* Guia de arquitetura

---

# 14. Segurança

## Regras inegociáveis:

* Nunca commitar secrets
* Utilizar `.env`
* Validar entradas externas
* Sanitizar dados
* Nunca confiar em input do usuário

---

# 15. Performance e Escalabilidade

## Regras:

* Evitar processamento desnecessário
* Evitar queries redundantes
* Aplicar lazy loading quando necessário
* Medir antes de otimizar
* Toda otimização deve ser justificável

---

# 16. Clean Code

O projeto deve seguir:

* SOLID
* DRY
* KISS
* YAGNI

---

# 17. Revisão de Código

Todo PR DEVE:

* Ser revisado
* Possuir descrição clara
* Explicar impacto
* Explicar riscos
* Explicar estratégia de teste

---

# 18. CI/CD Obrigatório

O pipeline deve executar automaticamente:

* lint
* testes
* cobertura
* análise estática
* análise de segurança

---

# 19. Compatibilidade

## Obrigatório:

* Compatível com Python 3.14+
* Evitar bibliotecas obsoletas
* Priorizar bibliotecas ativamente mantidas

---

# 20. Proibições Gerais

É proibido:

* Código duplicado
* Funções gigantes
* Dependências circulares
* Código morto
* Comentários inúteis
* Hardcode de configurações
* Misturar regra de negócio com infraestrutura

---

# 21. Regra Suprema

Toda decisão técnica deve priorizar:

1. Clareza
2. Manutenibilidade
3. Testabilidade
4. Escalabilidade
5. Simplicidade
6. Segurança
7. Consistência

Se uma implementação violar estes princípios, ela deve ser refatorada antes do merge.
