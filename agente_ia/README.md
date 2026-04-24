# 🤖 Agente IA — Pipeline Multi-Agente

Pipeline multi-agente usando **Anthropic Claude** diretamente.  
Compatível com **Python 3.10, 3.11, 3.12, 3.13 e 3.14**.

> ⚡ **Por que não CrewAI?**  
> O CrewAI exige Python < 3.14. Este projeto usa o SDK oficial da Anthropic,
> que funciona em todas as versões modernas e dá controle total sobre o pipeline.

---

## 🏗️ Arquitetura

```
agente_ia/
├── main.py              # CLI com Rich
├── crew.py              # Orquestração do pipeline
├── config.py            # Variáveis de ambiente
├── requirements.txt
├── .env.example
├── agents/
│   ├── base_agent.py    # Motor agentico (loop tool-use)
│   └── agentes.py       # 4 agentes especializados
├── tools/
│   └── custom_tools.py  # 4 ferramentas customizadas
└── output/              # Relatórios gerados aqui
```

## 👥 Agentes

| Agente         | Papel                        | Ferramentas                  |
|----------------|------------------------------|------------------------------|
| 🔍 Pesquisador | Coleta dados na internet     | busca_web, data_hora         |
| 📊 Analista    | Analisa e extrai insights    | analisar_texto, data_hora    |
| ✍️ Redator     | Produz relatório executivo   | salvar_arquivo, data_hora    |
| 🎯 Gerente     | Revisão e aprovação final    | salvar_arquivo, data_hora    |

## 🔧 Ferramentas

- **busca_web** — DuckDuckGo (sem API key necessária)
- **analisar_texto** — Métricas: palavras, sentenças, top termos
- **salvar_arquivo** — Persiste resultados em `output/`
- **data_hora_atual** — Timestamp atual

## 🚀 Instalação

```bash
# 1. Entre na pasta
cd agente_ia

# 2. Crie um ambiente virtual (qualquer Python 3.10+)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a chave
cp .env.example .env
# Edite o .env: coloque sua ANTHROPIC_API_KEY
```

## ▶️ Uso

```bash
# Modo interativo
python main.py

# Passando o tema
python main.py --tema "mercado de SaaS para barbearias no Nordeste"
python main.py -t "inteligência artificial na saúde"

# Listar agentes
python main.py --listar
```

## 📄 Output

Os relatórios são salvos em `output/`:
- `relatorio_final.md` — Produzido pelo Redator
- `relatorio_revisado.md` — Revisado e aprovado pelo Gerente

## ⚙️ .env

```env
ANTHROPIC_API_KEY=sk-ant-...      # obrigatório
CLAUDE_MODEL=claude-opus-4-5      # ou claude-sonnet-4-5 (mais barato)
VERBOSE=true
```

## 🔄 Fluxo

```
Usuário fornece tema
        ↓
  🔍 Pesquisador  →  3+ buscas DuckDuckGo  →  documento de pesquisa
        ↓ (contexto passado adiante)
  📊 Analista     →  análise de métricas   →  5 insights + oportunidades/riscos
        ↓ (contexto acumulado)
  ✍️  Redator     →  8 seções estruturadas →  salva relatorio_final.md
        ↓ (contexto acumulado)
  🎯 Gerente      →  checklist de qualidade →  salva relatorio_revisado.md
```

## 💡 Exemplos de Temas

```bash
python main.py -t "mercado de fintechs no Nordeste"
python main.py -t "sistema de agendamento online para pequenas empresas"
python main.py -t "WhatsApp como canal de vendas B2C"
python main.py -t "SaaS para barbearias e salões de beleza"
```
